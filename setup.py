from setuptools import setup, find_packages
import pkg_resources
import pathlib
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

with pathlib.Path('requirements.txt').open() as requirements_txt:
    reqs = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

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
