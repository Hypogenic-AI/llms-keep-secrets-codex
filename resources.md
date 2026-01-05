## Resources Catalog

### Summary
This document catalogs all resources gathered for the research project, including papers, datasets, and code repositories.

### Papers
Total papers downloaded: 9

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Creating Suspenseful Stories: Iterative Planning with Large Language Models | Xie, Riedl | 2024 | papers/2402.17119_creating_suspenseful_stories_iterative_planning_llms.pdf | Iterative LLM planning for suspense control |
| Plan, Write, and Revise: an Interactive System for Open-Domain Story Generation | Goldfarb-Tarrant et al. | 2019 | papers/1904.02357_plan_write_and_revise_story_generation.pdf | Plan-write-revise pipeline |
| Content Planning for Neural Story Generation with Aristotelian Rescoring | Goldfarb-Tarrant et al. | 2020 | papers/2009.09870_content_planning_aristotelian_rescoring.pdf | Plot structure learning and rescoring |
| GraphPlan: Story Generation by Planning with Event Graph | Chen et al. | 2021 | papers/2102.02977_graphplan_story_generation_event_graph.pdf | Event-graph planning for causal flow |
| PlotMachines: Outline-Conditioned Generation with Dynamic Plot State Tracking | Rashkin et al. | 2020 | papers/2004.14967_plotmachines_outline_conditioned_generation.pdf | Outline conditioning with plot tracking |
| Outline to Story: Fine-grained Controllable Story Generation from Cascaded Events | Fang et al. | 2021 | papers/2101.00822_outline_to_story_cascaded_events.pdf | Cascaded event outlines for control |
| DOC: Improving Long Story Coherence With Detailed Outline Control | Yang et al. | 2022 | papers/2212.10077_doc_detailed_outline_control_long_story.pdf | Detailed outline control for long stories |
| EIPE-text: Evaluation-Guided Iterative Plan Extraction for Long-Form Narrative Text Generation | You et al. | 2023 | papers/2310.08185_eipe_text_iterative_plan_extraction.pdf | Iterative plan extraction with evaluation |
| PLANET: Dynamic Content Planning in Autoregressive Transformers for Long-form Text Generation | Hu et al. | 2022 | papers/2203.09100_planet_dynamic_content_planning.pdf | Integrated planning in transformers |

See papers/README.md for detailed descriptions.

### Datasets
Total datasets downloaded: 2

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| ROCStories (mintujupally/ROCStories) | HuggingFace | train 78,528; test 19,633 | Narrative generation | datasets/rocstories/ | Story-only text field |
| WritingPrompts (euclaise/writingprompts) sample | HuggingFace | 2,726 (train[:1%]) | Prompt-conditioned story generation | datasets/writingprompts_sample/ | Subset only; full dataset in README |

See datasets/README.md for detailed descriptions.

### Code Repositories
Total repositories cloned: 2

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| plotmachines | https://github.com/hrashkin/plotmachines | Outline-conditioned story generation | code/plotmachines/ | PlotMachines implementation |
| plan-write-revise | https://github.com/seraphinatarrant/plan-write-revise | Plan-write-revise baseline | code/plan-write-revise/ | Interactive story generation system |

See code/README.md for detailed descriptions.

### Resource Gathering Notes

#### Search Strategy
Searched arXiv for story generation, outline conditioning, and plan-and-write keywords; cross-checked for recent planning-focused narrative generation papers. Located code via GitHub search. Chose datasets from HuggingFace that are easy to download and align with narrative generation tasks.

#### Selection Criteria
Prioritized papers that explicitly separate planning from generation (outlines, event graphs, iterative planning). Selected datasets that support narrative generation with prompts or short stories.

#### Challenges Encountered
Some datasets on the Hub rely on loading scripts incompatible with the installed datasets version; selected alternative datasets with direct files.

#### Gaps and Workarounds
Not all papers explicitly list datasets in abstracts. Literature review flags these as "verify in paper" for follow-up.

### Research Process Notes (This Run)
- Generated plans and stories for 40 prompts (20 ROCStories + 20 WritingPrompts sample).
- Conditions: prompt-only, plan-conditioned, plan-conditioned with anti-foreshadowing instruction.
- Model: gpt-4.1 for both generation and evaluation.
- Outputs saved under `results/model_outputs/` and `results/evaluations/`.
- Analysis scripts in `src/analyze_results.py` produced summary stats and plots in `results/plots/`.

### Recommendations for Experiment Design

1. **Primary dataset(s)**: WritingPrompts (prompt-to-story) for plan vs prose separation; ROCStories for short narrative tests.
2. **Baseline methods**: Prompt-only LLM; outline-conditioned generation (PlotMachines); plan-write-revise pipeline.
3. **Evaluation metrics**: Human judgments on suspense/foreshadowing; plan adherence/coverage; coherence metrics.
4. **Code to adapt/reuse**: plotmachines for outline conditioning; plan-write-revise for baseline plan-and-write architecture.
