## Literature Review

### Research Area Overview
The literature on long-form and narrative text generation consistently finds that fluent local text does not guarantee global coherence or controlled plot development. A common response is to separate planning from realization ("plan-and-write"), using outlines, event graphs, or iterative planning steps to guide generation. Recent work with LLMs explores how explicit plans can improve coherence, suspense, and controllability, which directly intersects with the hypothesis that plans can reduce unintended foreshadowing or leakage of future events.

### Key Papers

#### Paper 1: Creating Suspenseful Stories: Iterative Planning with Large Language Models
- **Authors**: Kaige Xie, Mark Riedl
- **Year**: 2024
- **Source**: arXiv
- **Key Contribution**: Introduces iterative planning with LLMs to control suspense in generated stories.
- **Methodology**: LLM-driven plan refinement and story generation with suspense-oriented planning steps.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Reports improved suspense/control over baselines in narrative generation (details in paper).
- **Code Available**: Not mentioned in abstract.
- **Relevance to Our Research**: Directly tests plan-conditioned generation in narratives, closely tied to foreshadowing and information control.

#### Paper 2: Plan, Write, and Revise: an Interactive System for Open-Domain Story Generation
- **Authors**: Seraphina Goldfarb-Tarrant, Haining Feng, Nanyun Peng
- **Year**: 2019
- **Source**: arXiv
- **Key Contribution**: Interactive plan-write-revise system showing value of human intervention at planning and revision stages.
- **Methodology**: Hierarchical planning followed by generation and revision, with different interaction points.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Human collaboration improves quality and engagement across stages (details in paper).
- **Code Available**: Yes (GitHub: seraphinatarrant/plan-write-revise).
- **Relevance to Our Research**: Provides a baseline plan-and-write pipeline and interaction patterns to compare against LLM plan conditioning.

#### Paper 3: Content Planning for Neural Story Generation with Aristotelian Rescoring
- **Authors**: Seraphina Goldfarb-Tarrant, Tuhin Chakrabarty, Ralph Weischedel, Nanyun Peng
- **Year**: 2020
- **Source**: arXiv
- **Key Contribution**: Learns plot structures and uses Aristotelian-inspired rescoring to improve story coherence.
- **Methodology**: Generate candidate plot structures and rescore with a learned model before surface realization.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Improved narrative coherence and structure compared to baseline generation.
- **Code Available**: Not mentioned in abstract.
- **Relevance to Our Research**: Highlights explicit content planning as a remedy to LLMs’ entangled planning/prose behavior.

#### Paper 4: GraphPlan: Story Generation by Planning with Event Graph
- **Authors**: Hong Chen, Raphael Shu, Hiroya Takamura, Hideki Nakayama
- **Year**: 2021
- **Source**: arXiv
- **Key Contribution**: Plans stories using event graphs to enforce causality and logical flow.
- **Methodology**: Build event graphs and plan sequences prior to generation; use planning to guide story output.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Improved logical correctness and causal consistency in story generation.
- **Code Available**: Not mentioned in abstract.
- **Relevance to Our Research**: Event-graph planning explicitly separates high-level plan from text, relevant to leakage control.

#### Paper 5: PlotMachines: Outline-Conditioned Generation with Dynamic Plot State Tracking
- **Authors**: Hannah Rashkin, Asli Celikyilmaz, Yejin Choi, Jianfeng Gao
- **Year**: 2020
- **Source**: arXiv
- **Key Contribution**: Formalizes outline-conditioned story generation and introduces plot-state tracking.
- **Methodology**: Condition generation on outline phrases while tracking which plot elements have been realized.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Improves adherence to outline and coherence compared to baseline models.
- **Code Available**: Yes (GitHub: hrashkin/plotmachines).
- **Relevance to Our Research**: Outline conditioning is a direct test bed for decoupling plan from prose to reduce foreshadowing.

#### Paper 6: Outline to Story: Fine-grained Controllable Story Generation from Cascaded Events
- **Authors**: Le Fang, Tao Zeng, Chaochun Liu, Liefeng Bo, Wen Dong, Changyou Chen
- **Year**: 2021
- **Source**: arXiv
- **Key Contribution**: Cascaded event outlines to enable fine-grained control over generated stories.
- **Methodology**: Generate hierarchical event plans and realize them into story text.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Enhanced controllability without sacrificing fluency.
- **Code Available**: Not mentioned in abstract.
- **Relevance to Our Research**: Supports plan-conditioned generation for fine control, relevant to preventing premature reveals.

#### Paper 7: DOC: Improving Long Story Coherence With Detailed Outline Control
- **Authors**: Kevin Yang, Dan Klein, Nanyun Peng, Yuandong Tian
- **Year**: 2022
- **Source**: arXiv
- **Key Contribution**: Detailed outline control (DOC) improves coherence in very long stories.
- **Methodology**: Hierarchical detailed outlines and controllers that manage long-range plot consistency.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Better coherence and long-range consistency for multi-thousand-word stories.
- **Code Available**: Not mentioned in abstract.
- **Relevance to Our Research**: A strong baseline for explicit outline control to minimize implicit foreshadowing.

#### Paper 8: EIPE-text: Evaluation-Guided Iterative Plan Extraction for Long-Form Narrative Text Generation
- **Authors**: Wang You, Wenshan Wu, Yaobo Liang, Shaoguang Mao, Chenfei Wu, Maosong Cao, Yuzhe Cai, Yiduo Guo, Yan Xia, Furu Wei, Nan Duan
- **Year**: 2023
- **Source**: arXiv
- **Key Contribution**: Iterative plan extraction guided by evaluation signals to improve long-form narratives.
- **Methodology**: Extract plans from candidate generations, score them, and iteratively refine the plan.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Improved narrative quality and plan adherence in long-form generation.
- **Code Available**: Not mentioned in abstract.
- **Relevance to Our Research**: Demonstrates explicit plan refinement as a strategy to control narrative outcomes.

#### Paper 9: PLANET: Dynamic Content Planning in Autoregressive Transformers for Long-form Text Generation
- **Authors**: Zhe Hu, Hou Pong Chan, Jiachen Liu, Xinyan Xiao, Hua Wu, Lifu Huang
- **Year**: 2022
- **Source**: arXiv
- **Key Contribution**: Dynamic content planning integrated into autoregressive transformers.
- **Methodology**: Introduces planning modules inside generation to maintain coherence and content flow.
- **Datasets Used**: Not specified in abstract (verify in paper).
- **Results**: Improvements in long-form coherence over non-planning baselines.
- **Code Available**: Not mentioned in abstract.
- **Relevance to Our Research**: Suggests architectural integration of planning that could reduce implicit future-event leakage.

### Common Methodologies
- Plan-and-write pipelines: Separate a planning step (outline/events) from story realization.
- Outline conditioning: Provide explicit outlines or event sequences to guide generation.
- Iterative planning/refinement: Re-plan or refine outlines based on evaluation signals.
- Structured planning: Event graphs or hierarchical outlines to enforce causal and temporal consistency.

### Standard Baselines
- Unconditional or prompt-only language models (no explicit plan step).
- Hierarchical RNN/Transformer baselines with no explicit outline tracking.
- Simple outline-conditioned generation without dynamic plot tracking.

### Evaluation Metrics
- Automatic text metrics (e.g., BLEU/ROUGE or perplexity) for fluency.
- Plan adherence and outline coverage metrics (model-specific).
- Human evaluation for coherence, plot consistency, and suspense.

### Datasets in the Literature
- WritingPrompts: prompt-to-story generation.
- ROCStories: short 5-sentence stories (often used for narrative coherence tasks).
- Story Cloze variants: predicting correct endings, useful for plot consistency evaluation.

### Gaps and Opportunities
- Limited explicit evaluation of unintended foreshadowing or information leakage in story generation.
- Need for metrics that quantify how early future events are revealed relative to a plan.
- Sparse comparisons between plan-conditioned LLMs and outline-tracking baselines on secret-keeping tasks.

### Recommendations for Our Experiment
- **Recommended datasets**: WritingPrompts (prompt-to-story) and ROCStories (short narratives) to test plan adherence and spoiler control.
- **Recommended baselines**: Prompt-only LLM generation; outline-conditioned generation (PlotMachines); plan-write-revise pipeline.
- **Recommended metrics**: Human evaluation of suspense/foreshadowing; automatic plan adherence/coverage; textual coherence scores.
- **Methodological considerations**: Keep plan explicit and separate from the prose generation prompt; measure how often planned future events are hinted at prematurely.
