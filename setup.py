from setuptools import setup, find_packages

with open('requirements1.txt') as f:
    requirements = f.read().splitlines()

# Filter out comments and empty lines
requirements = [req.strip() for req in requirements if req.strip() and not req.strip().startswith('#')]
requirements = [req for req in requirements if '==' in req or '>=' in req or '<=' in req or '>' in req or '<' in req]
for i in range(len(requirements)):
    print("lala")
    print(requirements[i])

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
