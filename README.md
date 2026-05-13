---
title: ROCmify AI
emoji: 🚀
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860
python_version: "3.10"
pinned: false
---

# 🚀 ROCmify AI

> AI-powered copilot for migrating CUDA/PyTorch projects to AMD ROCm.

ROCmify AI analyzes source code, requirements files, and entire repositories to identify NVIDIA-specific dependencies and generate actionable migration guidance for AMD GPU compatibility.

---

## 🌐 Live Demo

**Hugging Face Space:** [https://huggingface.co/spaces/k-tushar/rocmify-ai](https://huggingface.co/spaces/k-tushar/rocmify-ai)

**GitHub Repository:** [https://github.com/108-TusharBK/rocmify-ai](https://github.com/108-TusharBK/rocmify-ai)

---

## 📌 Problem Statement

Organizations with CUDA-based codebases often face significant effort when migrating to AMD GPUs and the ROCm ecosystem.

Common challenges include:

* Detecting NVIDIA-specific libraries and APIs.
* Estimating migration effort.
* Identifying ROCm-compatible alternatives.
* Prioritizing engineering work.
* Communicating migration risk to stakeholders.

ROCmify AI automates this analysis and produces structured, executive-ready reports.

---

## ✨ Features

### 🔍 Static Compatibility Analysis

Detects usage of:

* `cuda`
* `torch.cuda`
* `cudnn`
* `nccl`
* `tensorrt`
* `cupy`
* `torch.distributed`
* `tensorflow-gpu`
* `nvidia`

### 📊 ROCm Readiness Score

Generates a score from **0–100** based on issue severity.

### ⏱️ Migration Effort Estimation

Estimates engineering effort such as:

* 1–2 hours
* 0.5–2 days
* 2–5 days
* 1–2 weeks

### 🧠 AI-Powered Executive Summary

Uses the Hugging Face Inference API to generate natural-language migration summaries.
Falls back to deterministic summaries if the model is unavailable.

### 🔁 Suggested ROCm Replacements

Maps NVIDIA dependencies to AMD alternatives.

### 🗺️ Migration Plan Generator

Produces a step-by-step migration plan.

### 📁 ZIP Repository Analysis

Upload entire repositories as `.zip` files.

### 📥 Export Reports

Download:

* JSON report
* Markdown report

---

## 🏗️ System Architecture

```text
User Upload (.py/.txt/.zip)
           │
           ▼
   Static Analyzer Engine
           │
           ├── Dependency Detection
           ├── Severity Classification
           ├── ROCm Readiness Score
           ├── Migration Effort Estimation
           └── Replacement Mapping
           │
           ▼
     LLM Executive Summary
   (Hugging Face Inference API)
           │
           ▼
       Streamlit UI
           │
           ├── Dashboard Metrics
           ├── Migration Plan
           ├── Downloadable Reports
           └── Visual Findings
```

---

## 📂 Project Structure

```text
rocmify-ai/
├── backend/
│   ├── analyzer.py
│   ├── llm_advisor.py
│   └── lim_explainer.py
├── frontend/
│   └── streamlit_app.py
├── .streamlit/
│   └── config.toml
├── sample_inputs/
├── Dockerfile
├── requirements.txt
├── README.md
├── .gitignore
└── .dockerignore
```

---

## 🧮 Scoring Logic

Each finding reduces the score from 100.

| Severity | Penalty |
| -------: | ------: |
|     High |      25 |
|   Medium |      15 |
|  Warning |      10 |

Final score is clamped to a minimum of 0.

---

## 🔁 Example Replacement Table

| NVIDIA Component | ROCm Alternative     |
| ---------------- | -------------------- |
| cuda             | HIP / ROCm           |
| torch.cuda       | ROCm-enabled PyTorch |
| cudnn            | MIOpen               |
| nccl             | RCCL                 |
| tensorrt         | ONNX Runtime or vLLM |
| tensorflow-gpu   | tensorflow-rocm      |

---

## 📸 Example Output

### ROCm Readiness Score

* **25/100**

### Estimated Migration Effort

* **1–2 weeks**

### Executive Summary

> This project has a ROCm readiness score of 25/100, indicating high migration risk. Major blockers include cuDNN, CuPy, and TensorRT dependencies. Migration should prioritize replacing these libraries with ROCm-compatible alternatives such as MIOpen and ONNX Runtime.

---

## 🛠️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/108-TusharBK/rocmify-ai.git
cd rocmify-ai
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run frontend/streamlit_app.py
```

---

## 🤖 Hugging Face Secret

To enable LLM summaries, add the following secret in your Hugging Face Space:

```text
HF_TOKEN=your_huggingface_access_token
```

---

## 🐳 Docker Deployment

The application is containerized and deployed on Hugging Face Spaces using Docker.

Run locally with Docker:

```bash
docker build -t rocmify-ai .
docker run -p 7860:7860 rocmify-ai
```

---

## 📊 Supported File Types

* `.py`
* `.txt`
* `requirements.txt`
* `Dockerfile`
* `.zip`

---

## 🧪 Sample Test Cases

Recommended examples:

* `easy_case.txt`
* `medium_case.txt`
* `hard_case.txt`
* `sample_repo.zip`

---

## 🏆 Hackathon Value Proposition

ROCmify AI reduces manual compatibility audits from hours to seconds by:

* Automatically detecting NVIDIA-specific dependencies.
* Quantifying migration readiness.
* Generating executive summaries.
* Providing concrete ROCm replacements.
* Exporting reports for engineering and management.

---

## 🔮 Future Enhancements

* AST-based analysis.
* Automated code translation suggestions.
* ROCm package installation recommendations.
* CI/CD integration.
* Multi-language support.
* Model fine-tuning on migration datasets.

---

## 👨‍💻 Author

**Tushar Kale**

* GitHub: [https://github.com/108-TusharBK](https://github.com/108-TusharBK)
* Hugging Face: [https://huggingface.co/k-tushar](https://huggingface.co/k-tushar)

---


## ⭐ Support

If you found this project useful, consider starring the GitHub repository.

