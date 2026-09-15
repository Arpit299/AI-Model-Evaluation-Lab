# AI Model Evaluation Lab

AI Model Evaluation Lab is a lightweight Python benchmarking framework for comparing AI or LLM outputs across datasets using accuracy, consistency, latency, cost, format compliance, and custom evaluation metrics.

## Features

* Model-to-model comparison
* Dataset-based evaluation
* Exact-match accuracy
* Keyword overlap scoring
* Output consistency analysis
* Format compliance scoring
* Latency benchmarking
* Estimated cost calculation
* Weighted overall score
* Automatic model leaderboard
* JSON evaluation reports
* Custom dataset support
* Built-in demo mode

## Tech Stack

**Python | Evaluation Metrics | Statistics | JSON | CLI**

## DSA Used

**Dictionary | Counter | Set | List | Sorting | Frequency Analysis**

## Usage

Run the built-in benchmark:

```bash
python ai_model_evaluation_lab.py --demo
```

Generate a JSON report:

```bash
python ai_model_evaluation_lab.py --demo --json evaluation_report.json
```

Run a custom evaluation:

```bash
python ai_model_evaluation_lab.py --dataset dataset.jsonl --outputs model_outputs.json
```

## Architecture

```text
Evaluation Dataset
        ↓
Model Outputs
        ↓
Metric Engine
   ├── Accuracy
   ├── Consistency
   ├── Format Score
   ├── Latency
   └── Cost
        ↓
Weighted Scoring
        ↓
Model Ranking
        ↓
Evaluation Report
```

## Example

```text
Model-A → 98.30%
Model-B → 76.82%
Model-C → 60.07%
```

## Purpose

Designed to evaluate and benchmark AI models systematically, making it easier to compare model quality, performance, consistency, and cost using reproducible evaluation datasets.


