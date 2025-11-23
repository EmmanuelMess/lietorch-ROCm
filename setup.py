from setuptools import setup
import os
import torch
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

ROOT = os.path.dirname(os.path.abspath(__file__))

sources_backends = [
    "lietorch/src/lietorch.cpp", 
    "lietorch/src/lietorch_gpu.cu",
    "lietorch/src/lietorch_cpu.cpp"
]

sources_extras = [
    "lietorch/extras/altcorr_kernel.cu",
    "lietorch/extras/corr_index_kernel.cu",
    "lietorch/extras/se3_builder.cu",
    "lietorch/extras/se3_inplace_builder.cu",
    "lietorch/extras/se3_solver.cu",
    "lietorch/extras/extras.cpp",
]

if torch.cuda.is_available() and torch.version.cuda:
    print("Run with NVIDIA GPU")
    ext_modules = [
        CUDAExtension("lietorch_backends", 
            include_dirs=[
                os.path.join(ROOT, "lietorch/include"), 
                os.path.join(ROOT, "eigen")],
            sources=sources_backends,
            extra_compile_args={
                "cxx": ["-O2"], 
                "nvcc": ["-O2"],
            }),

        CUDAExtension("lietorch_extras", 
            sources=sources_extras,
            extra_compile_args={
                "cxx": ["-O2"], 
                "nvcc": ["-O2"],
            }),
    ]
elif torch.cuda.is_available() and torch.version.hip:
    print("Run with AMD GPU")
    ext_modules = [
        CUDAExtension("lietorch_backends", 
            include_dirs=[
                os.path.join(ROOT, "lietorch/include"), 
                os.path.join(ROOT, "eigen")],
            sources=sources_backends,
            extra_compile_args={
                "hipcc": ['-O3'],
                "cxx": ['-O3']
            }),

        CUDAExtension("lietorch_extras", 
            sources=sources_extras,
            extra_compile_args={
                "hipcc": ['-O3'],
                "cxx": ['-O3']
            }),
    ]
else:
    print("Run with CPU (unsupported)")


setup(
    name="lietorch",
    version="0.3",
    description="Lie Groups for PyTorch",
    author="Zachary Teed",
    packages=["lietorch"],
    ext_modules=ext_modules,
    cmdclass={ "build_ext": BuildExtension }
)
