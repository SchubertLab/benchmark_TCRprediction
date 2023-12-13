from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

print(requirements)

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
