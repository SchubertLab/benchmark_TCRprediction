from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

reqs = [req.strip() for req in requirements]

setup(
    name="tcr_benchmark",
    version="1.0.0",
    packages=find_packages(include=["tcr_benchmark", "tcr_benchmark.*"]),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "scipy",
        "requests",
        "PyYAML",
        "tqdm"
    ],
    extras_require={
        "epytope": [
            "epytope @ git+https://github.com/SchubertLab/epytope"
            ],
        "reproducability": reqs,
    }
)
