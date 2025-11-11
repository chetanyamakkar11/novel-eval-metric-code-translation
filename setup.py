from setuptools import setup, find_packages

setup(
    name="imm-metric",
    version="0.1.0",
    description="IMM: A hybrid evaluation metric for code translation",
    packages=find_packages(exclude=("tests", "examples", "results")),
    python_requires=">=3.9",
    install_requires=["numpy>=1.24"],
)
