<<<<<<< HEAD
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

# ROCmify AI

AI-powered copilot for migrating CUDA/PyTorch workloads to AMD ROCm.

## Features

- Upload Python, CUDA, or requirements files
- Detect NVIDIA-specific dependencies
- Severity-based compatibility findings
- Human-readable explanations
- Actionable migration recommendations
- ROCm Readiness Score
- Migration verdict
- JSON report export
=======
---
title: ROCmify AI
emoji: 🚀
colorFrom: blue
colorTo: red
sdk: docker
python_version: "3.10.12"
pinned: false
---

# ROCmify AI

AI-powered copilot for migrating CUDA/PyTorch workloads to AMD ROCm.

## Features

- Upload Python, CUDA, or requirements files
- Detect NVIDIA-specific dependencies
- Severity-based compatibility findings
- Human-readable explanations
- Actionable migration recommendations
- ROCm Readiness Score
- Migration verdict
- JSON report export

## Tech Stack

- Python
- Streamlit
- FastAPI
- Hugging Face (planned)
- AMD Developer Cloud (planned)

## Run Locally

```bash
source venv/bin/activate
streamlit run frontend/streamlit_app.py
>>>>>>> 9b043d3 (Update README.md)
