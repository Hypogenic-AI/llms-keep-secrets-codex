import json
from pathlib import Path

from datasets import load_from_disk


def main() -> None:
    results_dir = Path("results/evaluations")
    results_dir.mkdir(parents=True, exist_ok=True)

    roc = load_from_disk("datasets/rocstories")
    roc_train = roc["train"]

    roc_texts = [item["text"] for item in roc_train]
    roc_missing = sum(1 for t in roc_texts if not t or not t.strip())

    wp = load_from_disk("datasets/writingprompts_sample")
    wp_prompts = [item["prompt"] for item in wp]
    wp_stories = [item["story"] for item in wp]
    wp_missing = sum(1 for p, s in zip(wp_prompts, wp_stories) if not p.strip() or not s.strip())

    summary = {
        "rocstories": {
            "rows": len(roc_train),
            "missing_text": roc_missing,
        },
        "writingprompts_sample": {
            "rows": len(wp),
            "missing_prompt_or_story": wp_missing,
        },
    }

    sample_examples = {
        "rocstories": roc_train[:3],
        "writingprompts_sample": wp[:3],
    }

    (results_dir / "data_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (results_dir / "sample_examples.json").write_text(json.dumps(sample_examples, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
