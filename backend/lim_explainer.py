def explain_finding(keyword):

    explanations = {

        "tensorrt":
        (
            "TensorRT is optimized for NVIDIA GPUs "
            "and does not directly work on ROCm. "
            "ONNX Runtime or vLLM are common "
            "alternatives for AMD GPUs."
        ),
        

        "cudnn":
        (
            "cuDNN is NVIDIA's deep learning library. "
            "ROCm uses MIOpen instead."
        ),

        "nccl":
        (
            "NCCL is NVIDIA's communication backend. "
            "AMD uses RCCL for distributed workloads."
        ),

        "torch.cuda":
        (
            "torch.cuda indicates NVIDIA CUDA usage "
            "inside PyTorch. "
            "ROCm uses PyTorch with AMD GPU support."
        ),

        "cuda":
        (
            "CUDA-specific code may require HIP/ROCm "
            "adaptation for AMD compatibility."
        ),

        "cupy":
        (
            "CuPy is heavily CUDA-oriented and may not "
            "fully support ROCm workflows."
        ),

        "torch.distributed":
        (
            "Distributed PyTorch workloads on AMD GPUs "
            "typically use RCCL instead of NCCL."
        ),

        "tensorflow-gpu":
        (
            "ROCm typically uses tensorflow-rocm "
            "instead of tensorflow-gpu."
        ),

        "nvidia":
        (
            "This dependency appears NVIDIA-specific "
            "and may require ROCm alternatives."
        ),
    }

    return explanations.get(
        keyword,
        "No explanation available."
    )