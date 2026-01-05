# REPORT: LLMs Are Bad at Keeping Obvious Secrets

## 1. Executive Summary
We tested whether explicit plan-conditioning reduces early spoilers in LLM-generated narratives. Across 40 prompts (20 ROCStories + 20 WritingPrompts), plan-conditioned generation did **not** reduce leakage scores relative to prompt-only generation (Wilcoxon p > 0.78). Plan-conditioned outputs showed higher plan adherence and slightly higher coherence, but leakage remained effectively unchanged.

## 2. Goal
**Hypothesis**: Providing an explicit plan allows an LLM to avoid foreshadowing future events because planning and prose are disentangled.

**Importance**: If true, plan-conditioned generation could mitigate “spoiler leakage” and improve narrative suspense and controllability.

**Problem solved**: Quantify whether plan-conditioning actually reduces premature reveals in narrative text.

## 3. Data Construction

### Dataset Description
- **ROCStories** (mintujupally/ROCStories): 78,528 training short stories. We used the first sentence as a prompt.
- **WritingPrompts sample** (euclaise/writingprompts): 2,726 prompt/story pairs (sample subset).

### Example Samples

ROCStories (prompt from first sentence):
```
The boy went to a video arcade.
```

WritingPrompts:
```
[ WP ] The moon is actually a giant egg, and it has just started to hatch.
```

### Data Quality
- Missing values: 0% for both datasets.
- Duplicates: not assessed (not required for this pilot).

### Preprocessing Steps
1. ROCStories: extracted the first sentence as the prompt.
2. WritingPrompts: used the provided prompt field directly.
3. No tokenization or normalization; raw text preserved for prompt fidelity.

### Train/Val/Test Splits
Not applicable (generation/evaluation study). We sample 20 prompts from each dataset with a fixed seed for reproducibility.

## 4. Experiment Description

### Methodology

#### High-Level Approach
1. Generate an ordered plan (4–6 events) per prompt.
2. Generate stories under three conditions:
   - Prompt-only
   - Plan-conditioned (plan included)
   - Plan-conditioned + anti-foreshadowing instruction
3. Use an LLM judge to score spoiler leakage, coherence, and plan adherence.

#### Why This Method?
The hypothesis targets an interaction between explicit planning and prose generation. Using an LLM judge with a fixed rubric is a scalable way to quantify leakage across multiple conditions.

### Implementation Details

#### Tools and Libraries
- openai 2.14.0
- datasets 4.4.2
- numpy 2.4.0
- pandas 2.3.3
- scipy 1.16.3
- statsmodels 0.14.6
- matplotlib 3.10.8
- seaborn 0.13.2

#### Algorithms/Models
- **Generation model**: `gpt-4.1`
- **Judge model**: `gpt-4.1`

#### Hyperparameters
| Parameter | Value | Selection Method |
|-----------|-------|------------------|
| temperature | 0.7 | fixed |
| max_output_tokens | 700 | fixed |
| sample_size_per_dataset | 20 | cost/latency constraint |

#### Analysis Pipeline
1. Generate plans and stories (JSONL outputs).
2. Evaluate with judge rubric (JSONL outputs).
3. Aggregate metrics and run paired Wilcoxon tests.

### Experimental Protocol

#### Reproducibility Information
- Runs: 1 per condition (temperature 0.7)
- Seeds: 42
- Hardware: CPU
- Execution time: ~12–15 minutes for 120 judge calls

#### Evaluation Metrics
- **Leakage score (0–3)**: 0 = no hinting, 3 = explicit spoiler.
- **Plan adherence (0–1)**: fraction of plan events realized in order.
- **Coherence (1–5)**: holistic narrative coherence rating.

### Raw Results

#### Tables
| Condition | Leakage (mean ± std) | Coherence (mean ± std) | Plan Adherence (mean ± std) |
|-----------|-----------------------|-------------------------|------------------------------|
| prompt_only | 1.10 ± 0.84 | 4.90 ± 0.30 | 0.59 ± 0.33 |
| plan_conditioned | 1.13 ± 0.88 | 5.00 ± 0.00 | 1.00 ± 0.00 |
| plan_structured | 1.10 ± 0.81 | 5.00 ± 0.00 | 1.00 ± 0.00 |

#### Visualizations
- `results/plots/leakage_by_condition.png`
- `results/plots/coherence_by_condition.png`
- `results/plots/adherence_by_condition.png`

#### Output Locations
- Results JSON: `results/evaluations/summary.json`
- Statistical tests: `results/evaluations/stat_tests.json`
- Plots: `results/plots/`
- Model outputs: `results/model_outputs/`

## 5. Result Analysis

### Key Findings
1. **No leakage reduction**: Plan-conditioning did not reduce spoiler leakage vs prompt-only (Wilcoxon p > 0.78; effect sizes near 0).
2. **Plan adherence improved**: As expected, plan-conditioned outputs matched the plan closely (mean adherence 1.0).
3. **Coherence ceiling**: Judge assigned near-perfect coherence scores for plan-conditioned stories, suggesting possible evaluation ceiling effects.

### Hypothesis Testing Results
- H₀: No difference in leakage between prompt-only and plan-conditioned generation.
- H₁: Plan-conditioned generation reduces leakage.
- **Result**: Fail to reject H₀. Leakage scores are statistically indistinguishable.

### Comparison to Baselines
- Leakage: prompt-only vs plan-conditioned shows no meaningful change.
- Coherence: slight increase but likely inflated by judging bias.

### Visualizations
See the plots in `results/plots/` for leakage and coherence comparisons.

### Surprises and Insights
- The judge scored plan adherence and coherence as perfect for plan-conditioned stories, which may indicate a bias toward plan inclusion rather than actual narrative quality.

### Error Analysis
- Leakage often came from early thematic hints (score 1–2) rather than explicit spoilers.
- Some prompt-only stories still avoided spoilers, indicating that leakage is not inevitable.

### Limitations
- Small sample size (40 prompts total).
- Single model family used for both generation and judging.
- Judge may be biased by seeing the plan and may overestimate coherence/adherence.
- Leakage scoring relies on subjective LLM interpretation rather than human annotations.

## 6. Conclusions
Explicit plan-conditioning did **not** reduce early spoilers in this pilot study. Plans improved adherence but did not meaningfully separate planning from prose generation in a way that reduced leakage. The hypothesis is not supported under these conditions.

### Implications
- Plan-conditioning alone may be insufficient to prevent subtle foreshadowing.
- More explicit control mechanisms or revised prompting strategies may be required.

### Confidence in Findings
Moderate. Results are consistent across the sample but limited by judge bias and sample size.

## 7. Next Steps

### Immediate Follow-ups
1. Use a second judge model (e.g., GPT-5) to reduce evaluator bias.
2. Add human annotation for leakage on a smaller subset.

### Alternative Approaches
- Enforce narrative constraints via editing/revision steps or event masking.

### Broader Extensions
- Test on longer narratives where foreshadowing is more likely.

### Open Questions
- Can iterative planning with explicit “no spoilers” constraints reduce leakage when coupled with revision?

## References
- papers/2402.17119_creating_suspenseful_stories_iterative_planning_llms.pdf
- papers/2004.14967_plotmachines_outline_conditioned_generation.pdf
- papers/1904.02357_plan_write_and_revise_story_generation.pdf
