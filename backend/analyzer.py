import re

PATTERNS = {
    "torch.cuda": {
        "severity": "high",

        "issue":
        "TensorRT dependency detected",

        "recommendation":
        "Use ONNX Runtime or vLLM on ROCm.",

        "pattern": r"\btensorrt\b"
    },


    "cuda": {
        "severity": "warning",
        "issue": "Generic CUDA usage detected.",
        "recommendation": "Review CUDA-specific code and port it using HIP/ROCm where needed.",
        "pattern": r"\bcuda\b",
    },

    "cudnn": {
        "severity": "high",
        "issue": "cuDNN dependency detected.",
        "recommendation": "Use MIOpen, AMD's deep learning library.",
        "pattern": r"\bcudnn\b",
    },

    "nccl": {
        "severity": "medium",
        "issue": "NCCL dependency detected.",
        "recommendation": "Use RCCL for distributed communication on AMD GPUs.",
        "pattern": r"\bnccl\b",
    },

    "tensorrt": {
        "severity": "high",
        "issue": "TensorRT dependency detected.",
        "recommendation": "Use ONNX Runtime or vLLM on ROCm.",
        "pattern": r"\btensorrt\b",
    },

    "cupy": {
        "severity": "high",
        "issue": "CuPy dependency detected.",
        "recommendation": "Verify ROCm support or replace with ROCm-compatible alternatives.",
        "pattern": r"\bcupy\b",
    },

    "torch.distributed": {
        "severity": "medium",
        "issue": "Distributed PyTorch usage detected.",
        "recommendation": "Configure PyTorch distributed with RCCL backend.",
        "pattern": r"torch\.distributed",
    },

    "tensorflow-gpu": {
        "severity": "high",
        "issue": "tensorflow-gpu dependency detected.",
        "recommendation": "Use tensorflow-rocm instead.",
        "pattern": r"tensorflow-gpu",
    },

    "nvidia": {
        "severity": "medium",
        "issue": "NVIDIA-specific dependency detected.",
        "recommendation": "Look for ROCm-compatible alternatives.",
        "pattern": r"\bnvidia\b",
    },
}

def analyze_code(content):
    content_lower = content.lower()
    findings = []
    seen = set()
    skip_cuda = "torch.cuda" in content_lower

    for keyword, data in PATTERNS.items():
        if keyword == "cuda" and skip_cuda:
            continue

        if keyword in seen:
            continue

        if re.search(data["pattern"], content_lower):
            findings.append({
                "keyword": keyword,
                "severity": data["severity"],
                "issue": data["issue"],
                "recommendation": data["recommendation"],
            })
            seen.add(keyword)

    return findings