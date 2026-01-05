# LLMs Are Bad at Keeping Obvious Secrets

This project evaluates whether explicit plan-conditioning reduces spoiler leakage in LLM-generated narratives. We compare prompt-only generation to plan-conditioned variants across ROCStories and WritingPrompts samples.

## Key Findings
- Plan-conditioning did **not** reduce leakage scores relative to prompt-only generation.
- Plan adherence improved with explicit plans, but leakage remained unchanged.
- Coherence scores saturated at the ceiling for plan-conditioned stories, indicating possible evaluator bias.

## How to Reproduce
1. Set up environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```
2. Run data prep:
   ```bash
   .venv/bin/python src/data_prep.py
   ```
3. Run experiments (requires API key in environment):
   ```bash
   .venv/bin/python src/experiment.py --sample-size 20 --seed 42 --temperature 0.7
   ```
4. Run analysis:
   ```bash
   .venv/bin/python src/analyze_results.py
   ```

## File Structure
- `src/experiment.py`: plan generation, story generation, and LLM-judge evaluation.
- `src/data_prep.py`: dataset checks and sample export.
- `src/analyze_results.py`: statistics and plots.
- `results/`: JSONL outputs, summaries, and plots.
- `REPORT.md`: full research report with methods and results.

See `REPORT.md` for detailed methodology, analysis, and discussion.
