# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="alphapack-tokenizer",
    version="1.0.0",
    author="TUSofia Research",
    author_email="research@tusofia.bg",
    description="A fast, lightweight word-based tokenizer for multilingual NLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tusofia/alphapack-tokenizer",
    py_modules=["alphapack_tokenizer"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    extras_require={
        "torch": ["torch>=1.9.0"],
    },
    keywords="tokenizer nlp multilingual turkish english bulgarian word-based",
    project_urls={
        "Bug Reports": "https://github.com/tusofia/alphapack-tokenizer/issues",
        "Source": "https://github.com/tusofia/alphapack-tokenizer",
    },
)
