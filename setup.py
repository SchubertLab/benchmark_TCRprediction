from setuptools import setup, find_packages

# with open('epytope_requirements.txt') as f:
#    epytope_requirements = f.read().splitlines()

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
        "tqdm",
        "openpyxl"
    ],
    extras_require={
        "epytope": [
            "epytope @ git+https://github.com/SchubertLab/epytope"
            ],
        # "reproducability": epytope_requirements
    }
)
