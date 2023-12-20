from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Filter out comments and empty lines
requirements = [req.strip() for req in requirements if req.strip() and not req.strip().startswith('#')]

# Ensure each requirement is a valid specifier
requirements = [req for req in requirements if '==' in req or '>=' in req or '<=' in req or '>' in req or '<' in req]

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
        "reproducability": requirements,
    }
)
