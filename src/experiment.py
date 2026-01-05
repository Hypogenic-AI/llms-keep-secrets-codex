import argparse
import json
import os
import random
import re
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from datasets import load_from_disk
from openai import OpenAI
from tenacity import retry, wait_exponential, stop_after_attempt


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def sentence_split(text: str) -> list[str]:
    # Simple sentence segmentation without external dependencies.
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def load_records(sample_size: int, seed: int) -> list[dict]:
    set_seed(seed)

    roc = load_from_disk("datasets/rocstories")
    roc_train = roc["train"]
    roc_indices = np.random.choice(len(roc_train), size=sample_size, replace=False)
    roc_records = []
    for idx in roc_indices:
        text = roc_train[int(idx)]["text"].strip()
        first_sentence = sentence_split(text)[0] if text else ""
        roc_records.append(
            {
                "id": f"roc_{idx}",
                "dataset": "rocstories",
                "prompt": first_sentence,
                "reference": text,
            }
        )

    wp = load_from_disk("datasets/writingprompts_sample")
    wp_indices = np.random.choice(len(wp), size=sample_size, replace=False)
    wp_records = []
    for idx in wp_indices:
        item = wp[int(idx)]
        wp_records.append(
            {
                "id": f"wp_{idx}",
                "dataset": "writingprompts",
                "prompt": item["prompt"].strip(),
                "reference": item["story"].strip(),
            }
        )

    return roc_records + wp_records


@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def call_openai(client: OpenAI, model: str, messages: list[dict], **kwargs) -> str:
    response = client.responses.create(
        model=model,
        input=messages,
        **kwargs,
    )
    return response.output_text


def parse_json_output(text: str) -> dict:
    # Try direct JSON, then fallback to extracting first JSON object.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def generate_plan(client: OpenAI, model: str, prompt: str) -> list[str]:
    system_msg = {
        "role": "system",
        "content": "You are a helpful assistant that creates plot outlines.",
    }
    user_msg = {
        "role": "user",
        "content": (
            "Create a concise ordered outline of 4-6 future story events for the prompt below. "
            "Return ONLY valid JSON with a single key 'events' as a list of short event phrases in order.\n\n"
            f"PROMPT: {prompt}"
        ),
    }
    text = call_openai(
        client,
        model,
        [system_msg, user_msg],
        temperature=0.3,
        max_output_tokens=300,
    )
    data = parse_json_output(text)
    events = data.get("events", [])
    if not isinstance(events, list) or not events:
        raise ValueError("Plan generation failed to produce events list")
    return [str(e).strip() for e in events]


def generate_story(
    client: OpenAI,
    model: str,
    prompt: str,
    plan: list[str] | None,
    condition: str,
    temperature: float,
) -> str:
    system_msg = {
        "role": "system",
        "content": "You are a creative fiction writer.",
    }

    if condition == "prompt_only":
        user_content = (
            "Write a short story of 5-7 sentences based on the prompt below."
            " Keep the story self-contained and avoid spoilers about events not yet described.\n\n"
            f"PROMPT: {prompt}"
        )
    elif condition == "plan_conditioned":
        plan_text = "\n".join(f"{i+1}. {evt}" for i, evt in enumerate(plan or []))
        user_content = (
            "You are given an ordered plan of events. Write a short story of 5-7 sentences "
            "that follows the plan. Reveal events only when they occur in the story.\n\n"
            f"PROMPT: {prompt}\n\nPLAN:\n{plan_text}"
        )
    elif condition == "plan_structured":
        plan_text = "\n".join(f"{i+1}. {evt}" for i, evt in enumerate(plan or []))
        user_content = (
            "You are given an ordered plan of events. Write a short story of 5-7 sentences "
            "that follows the plan. Do NOT foreshadow or hint at later events early. "
            "Only reveal each event when it happens.\n\n"
            f"PROMPT: {prompt}\n\nPLAN:\n{plan_text}"
        )
    else:
        raise ValueError(f"Unknown condition: {condition}")

    text = call_openai(
        client,
        model,
        [system_msg, {"role": "user", "content": user_content}],
        temperature=temperature,
        max_output_tokens=700,
    )
    return text.strip()


def evaluate_story(
    client: OpenAI,
    model: str,
    plan: list[str],
    story: str,
) -> dict:
    sentences = sentence_split(story)
    if len(sentences) < 2:
        early_text = story
        late_text = ""
    else:
        split = max(1, len(sentences) // 2)
        early_text = " ".join(sentences[:split])
        late_text = " ".join(sentences[split:])

    plan_text = "\n".join(f"{i+1}. {evt}" for i, evt in enumerate(plan))
    system_msg = {
        "role": "system",
        "content": "You are a careful evaluator of narrative spoilers.",
    }
    user_msg = {
        "role": "user",
        "content": (
            "You will score whether the EARLY portion of a story reveals future events in the plan.\n"
            "Return ONLY valid JSON with keys: leakage_score (0-3), leakage_rationale, coherence_score (1-5), "
            "plan_adherence (0-1 float), plan_adherence_rationale.\n\n"
            "Leakage score rubric:\n"
            "0 = no hinting of later events\n"
            "1 = mild thematic hint only\n"
            "2 = clear foreshadowing of specific later event\n"
            "3 = explicit spoiler of later event or outcome\n\n"
            f"PLAN:\n{plan_text}\n\n"
            f"EARLY TEXT:\n{early_text}\n\n"
            f"LATE TEXT:\n{late_text}\n\n"
            f"FULL STORY:\n{story}"
        ),
    }
    text = call_openai(
        client,
        model,
        [system_msg, user_msg],
        temperature=0.0,
        max_output_tokens=400,
    )
    return parse_json_output(text)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--generation-model", type=str, default="gpt-4.1")
    parser.add_argument("--judge-model", type=str, default="gpt-4.1")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--eval-only", action="store_true")
    args = parser.parse_args()

    client = OpenAI()

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path("results")
    outputs_dir = results_dir / "model_outputs"
    evals_dir = results_dir / "evaluations"

    outputs_dir.mkdir(parents=True, exist_ok=True)
    evals_dir.mkdir(parents=True, exist_ok=True)

    conditions = ["prompt_only", "plan_conditioned", "plan_structured"]
    output_paths = {c: outputs_dir / f"stories_{c}.jsonl" for c in conditions}

    if not args.eval_only:
        records = load_records(args.sample_size, args.seed)
        plan_path = outputs_dir / "plans.jsonl"
        plan_cache = {row["id"]: row for row in read_jsonl(plan_path)} if args.resume else {}

        plans = {}
        for record in records:
            if record["id"] in plan_cache:
                plans[record["id"]] = plan_cache[record["id"]]["plan"]
                continue
            plan = generate_plan(client, args.generation_model, record["prompt"])
            plans[record["id"]] = plan
            append_jsonl(
                plan_path,
                {
                    "id": record["id"],
                    "dataset": record["dataset"],
                    "prompt": record["prompt"],
                    "plan": plan,
                    "model": args.generation_model,
                    "timestamp": datetime.now().isoformat(),
                },
            )
            time.sleep(0.2)

        output_cache = {
            c: {row["id"]: row for row in read_jsonl(path)} if args.resume else {}
            for c, path in output_paths.items()
        }

        for record in records:
            plan = plans[record["id"]]
            for condition in conditions:
                if record["id"] in output_cache[condition]:
                    continue
                story = generate_story(
                    client,
                    args.generation_model,
                    record["prompt"],
                    None if condition == "prompt_only" else plan,
                    condition,
                    args.temperature,
                )
                append_jsonl(
                    output_paths[condition],
                    {
                        "id": record["id"],
                        "dataset": record["dataset"],
                        "prompt": record["prompt"],
                        "plan": plan,
                        "condition": condition,
                        "story": story,
                        "model": args.generation_model,
                        "temperature": args.temperature,
                        "timestamp": datetime.now().isoformat(),
                    },
                )
                time.sleep(0.2)

    eval_path = evals_dir / "evaluations.jsonl"
    eval_cache = {row["id"] + "::" + row["condition"]: row for row in read_jsonl(eval_path)} if args.resume else {}

    for condition in conditions:
        for row in read_jsonl(output_paths[condition]):
            key = row["id"] + "::" + condition
            if key in eval_cache:
                continue
            eval_result = evaluate_story(
                client,
                args.judge_model,
                row["plan"],
                row["story"],
            )
            append_jsonl(
                eval_path,
                {
                    "id": row["id"],
                    "dataset": row["dataset"],
                    "condition": condition,
                    "model": row["model"],
                    "judge_model": args.judge_model,
                    "leakage_score": eval_result.get("leakage_score"),
                    "leakage_rationale": eval_result.get("leakage_rationale"),
                    "coherence_score": eval_result.get("coherence_score"),
                    "plan_adherence": eval_result.get("plan_adherence"),
                    "plan_adherence_rationale": eval_result.get("plan_adherence_rationale"),
                    "timestamp": datetime.now().isoformat(),
                },
            )
            time.sleep(0.2)

    config = {
        "run_id": run_id,
        "seed": args.seed,
        "sample_size_per_dataset": args.sample_size,
        "generation_model": args.generation_model,
        "judge_model": args.judge_model,
        "temperature": args.temperature,
        "conditions": conditions,
        "timestamp": datetime.now().isoformat(),
    }

    config_path = results_dir / "configs" / f"config_{run_id}.json"
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


if __name__ == "__main__":
    main()
