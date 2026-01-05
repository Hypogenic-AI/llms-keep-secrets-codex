import json
from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def bootstrap_ci(values: np.ndarray, n_boot: int = 2000, alpha: float = 0.05) -> tuple[float, float]:
    rng = np.random.default_rng(42)
    samples = []
    for _ in range(n_boot):
        sample = rng.choice(values, size=len(values), replace=True)
        samples.append(np.mean(sample))
    lower = np.quantile(samples, alpha / 2)
    upper = np.quantile(samples, 1 - alpha / 2)
    return float(lower), float(upper)


def cohens_d_paired(a: np.ndarray, b: np.ndarray) -> float:
    diff = a - b
    return float(np.mean(diff) / (np.std(diff, ddof=1) + 1e-8))


def main() -> None:
    eval_path = Path("results/evaluations/evaluations.jsonl")
    if not eval_path.exists():
        raise FileNotFoundError("Missing evaluations.jsonl. Run experiments first.")

    df = pd.DataFrame(read_jsonl(eval_path))
    df["leakage_score"] = pd.to_numeric(df["leakage_score"], errors="coerce")
    df["coherence_score"] = pd.to_numeric(df["coherence_score"], errors="coerce")
    df["plan_adherence"] = pd.to_numeric(df["plan_adherence"], errors="coerce")

    summary = []
    for condition, group in df.groupby("condition"):
        leakage = group["leakage_score"].dropna().to_numpy()
        coherence = group["coherence_score"].dropna().to_numpy()
        adherence = group["plan_adherence"].dropna().to_numpy()

        summary.append(
            {
                "condition": condition,
                "n": len(group),
                "leakage_mean": float(np.mean(leakage)),
                "leakage_std": float(np.std(leakage, ddof=1)),
                "leakage_ci": bootstrap_ci(leakage),
                "coherence_mean": float(np.mean(coherence)),
                "coherence_std": float(np.std(coherence, ddof=1)),
                "coherence_ci": bootstrap_ci(coherence),
                "adherence_mean": float(np.mean(adherence)),
                "adherence_std": float(np.std(adherence, ddof=1)),
                "adherence_ci": bootstrap_ci(adherence),
            }
        )

    summary_path = Path("results/evaluations/summary.json")
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Paired tests across conditions by id
    pivot = df.pivot_table(
        index=["id"],
        columns="condition",
        values="leakage_score",
        aggfunc="mean",
    )

    tests = []
    conditions = ["prompt_only", "plan_conditioned", "plan_structured"]
    comparisons = [
        ("prompt_only", "plan_conditioned"),
        ("prompt_only", "plan_structured"),
        ("plan_conditioned", "plan_structured"),
    ]

    for a, b in comparisons:
        pair = pivot[[a, b]].dropna()
        if len(pair) < 5:
            continue
        stat, p_value = stats.wilcoxon(pair[a], pair[b])
        tests.append(
            {
                "metric": "leakage_score",
                "condition_a": a,
                "condition_b": b,
                "n": int(len(pair)),
                "stat": float(stat),
                "p_value": float(p_value),
                "cohens_d": cohens_d_paired(pair[a].to_numpy(), pair[b].to_numpy()),
            }
        )

    tests_path = Path("results/evaluations/stat_tests.json")
    tests_path.write_text(json.dumps(tests, indent=2), encoding="utf-8")

    # Plots
    plots_dir = Path("results/plots")
    plots_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x="condition", y="leakage_score", ax=ax, errorbar="se")
    ax.set_title("Leakage Score by Condition (lower is better)")
    ax.set_xlabel("Condition")
    ax.set_ylabel("Leakage score")
    fig.tight_layout()
    fig.savefig(plots_dir / "leakage_by_condition.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x="condition", y="coherence_score", ax=ax, errorbar="se")
    ax.set_title("Coherence Score by Condition")
    ax.set_xlabel("Condition")
    ax.set_ylabel("Coherence score")
    fig.tight_layout()
    fig.savefig(plots_dir / "coherence_by_condition.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=df, x="condition", y="plan_adherence", ax=ax, errorbar="se")
    ax.set_title("Plan Adherence by Condition")
    ax.set_xlabel("Condition")
    ax.set_ylabel("Plan adherence")
    fig.tight_layout()
    fig.savefig(plots_dir / "adherence_by_condition.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
