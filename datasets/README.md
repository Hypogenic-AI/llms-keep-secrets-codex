# Downloaded Datasets

This directory contains datasets for the research project. Data files are NOT
committed to git due to size. Follow the download instructions below.

## Dataset 1: ROCStories (mintujupally/ROCStories)

### Overview
- **Source**: https://huggingface.co/datasets/mintujupally/ROCStories
- **Size**: train 78,528; test 19,633
- **Format**: HuggingFace Dataset (single `text` field per story)
- **Task**: short narrative generation/understanding
- **Splits**: train, test
- **License**: Not specified in the dataset card (verify on the dataset page)

### Download Instructions

**Using HuggingFace (recommended):**
```python
from datasets import load_dataset

dataset = load_dataset("mintujupally/ROCStories")
dataset.save_to_disk("datasets/rocstories")
```

### Loading the Dataset
```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/rocstories")
```

### Sample Data
Example records from this dataset:
```json
{
  "text": "..."
}
```

### Notes
- This is a story-only version; for Story Cloze-style endings, additional processing may be needed.

## Dataset 2: WritingPrompts (euclaise/writingprompts) - Sample Subset

### Overview
- **Source**: https://huggingface.co/datasets/euclaise/writingprompts
- **Size**: sample subset (train[:1%] = 2,726 rows) saved locally
- **Format**: HuggingFace Dataset (`prompt`, `story`)
- **Task**: prompt-conditioned story generation
- **Splits**: train (subset stored)
- **License**: Not specified in the dataset card (verify on the dataset page)

### Download Instructions

**Full dataset (recommended for experiments):**
```python
from datasets import load_dataset

dataset = load_dataset("euclaise/writingprompts")
dataset.save_to_disk("datasets/writingprompts_full")
```

**Subset used here:**
```python
from datasets import load_dataset

dataset = load_dataset("euclaise/writingprompts", split="train[:1%]")
dataset.save_to_disk("datasets/writingprompts_sample")
```

### Loading the Dataset
```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/writingprompts_sample")
```

### Sample Data
Example records from this dataset:
```json
{
  "prompt": "...",
  "story": "..."
}
```

### Notes
- The local copy is a small subset to keep storage light; expand to full dataset as needed.
