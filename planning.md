## Research Question
Do explicit, model-conditioned plans reduce unintended foreshadowing (premature disclosure of future events) in LLM-generated narratives compared to prompt-only generation?

## Background and Motivation
LLMs often leak upcoming plot information while generating fiction, likely because planning and prose generation are entangled. Prior work separates planning from realization (plan-and-write, outline conditioning, event graphs), but few studies directly quantify “spoiler” leakage. This study measures whether conditioning on an explicit plan lets a model set up future events without hinting at them early.

## Hypothesis Decomposition
1. **H1 (Primary):** Plan-conditioned generation reduces premature revelation of future events compared to prompt-only generation.
2. **H2 (Secondary):** Plan-conditioned generation maintains or improves narrative coherence relative to prompt-only generation.
3. **H3 (Ablation):** Stronger plan structure (outline with ordered events) reduces leakage more than minimal plans.

Independent variables:
- Generation strategy: prompt-only vs plan-conditioned vs plan-conditioned with structured outline.
- Model: GPT-4.1 (primary), optional GPT-5 for robustness.
- Temperature: low (0.3) vs moderate (0.7) to check robustness.

Dependent variables:
- **Leakage score:** degree of premature hinting of later plan events in early story segments.
- **Plan adherence:** overlap between planned events and realized events in appropriate order.
- **Coherence:** automated coherence proxy + human/LLM-judge ratings.

Success criteria:
- Statistically significant reduction in leakage for plan-conditioned vs prompt-only (p < 0.05) with non-trivial effect size.

Alternative explanations:
- Lower leakage may stem from shorter outputs or reduced creativity rather than improved planning.
- Prompt conditioning may change style/length and indirectly affect leakage.

## Proposed Methodology

### Approach
Create a controlled narrative benchmark from ROCStories and WritingPrompts. For each prompt, generate an explicit plan (outline events). Then generate stories under different conditions and measure leakage by comparing early segments against later planned events. Use LLM-based evaluation for leakage and coherence, with consistent rubrics and multiple runs for variance.

### Experimental Steps
1. **Resource review and dataset selection**: Use ROCStories (short narrative) and WritingPrompts sample (longer) for diversity.
2. **Plan generation**: Use a dedicated prompt to generate 4–6 ordered events for each prompt.
3. **Story generation**:
   - Baseline: prompt-only generation.
   - Plan-conditioned: include full plan in context.
   - Structured plan-conditioned: include plan plus explicit “no foreshadowing” instruction.
4. **Leakage evaluation**:
   - Split each story into early vs late halves.
   - Ask a judge LLM to identify whether early text reveals later plan events.
   - Score leakage on 0–3 ordinal scale per story.
5. **Plan adherence**: LLM judge matches realized events to plan and checks order.
6. **Coherence evaluation**: LLM judge scores coherence on 1–5.
7. **Statistical analysis**: Compare leakage scores across conditions using paired tests.

### Baselines
- Prompt-only generation (no plan).
- Plan-conditioned generation (outline provided).
- Structured plan-conditioned with anti-foreshadowing instruction.

### Evaluation Metrics
- **Leakage score (0–3)**: 0 = no early hinting; 3 = explicit spoiler.
- **Plan adherence (% events realized in order)**.
- **Coherence score (1–5)**.

### Statistical Analysis Plan
- Paired Wilcoxon signed-rank tests for ordinal leakage scores.
- Cohen’s d for effect size on coherence and adherence.
- 95% confidence intervals via bootstrap.
- Multiple comparison correction with Benjamini–Hochberg FDR.

## Expected Outcomes
- Support for H1: Plan-conditioned conditions show lower leakage without large coherence loss.
- Refutation: No significant leakage reduction or coherence collapse.

## Timeline and Milestones
- Phase 1 (Planning): 1–2 hours.
- Phase 2 (Setup + data prep): 1 hour.
- Phase 3 (Implementation): 2–3 hours.
- Phase 4 (Experiments): 2–3 hours.
- Phase 5 (Analysis): 1–2 hours.
- Phase 6 (Documentation): 1–2 hours.

## Potential Challenges
- LLM judge bias: mitigate with fixed rubric and blinded condition labels.
- API costs: limit sample size (e.g., 100 prompts per dataset).
- Prompt leakage: ensure plan generation and evaluation prompts are distinct.
- Variance: use multiple seeds and temperatures.

## Success Criteria
- Significant reduction in leakage score in plan-conditioned conditions with stable coherence.
- Clear documentation of prompts, model versions, and results in REPORT.md.
