# Benchmarking T cell receptor - Epitope Predictors with ePytope
This repository contains the code to recreate the study "todo" by Drost et al.

## Install
Stand-alone Benchmark-Suite:
```
pip install tcr-benchmark
```

Benchmark-Suite with ePytope:

Note: you will need to install the individual predictors, separately. You may consult the apptainer recipe in `./container/benchmark.def`
```
pip install tcr-benchmark[epytope]
```

Reproducibility:
To reproduce the environment of the paper. To reproduce the specific environment of the predictors, we advise to use the apptainer recipe in `./container/benchmark.def`
```
pip install tcr-benchmark[epytope]
```

## Reproduce Benchmark
To reproduce the benchmark you can
```
git clone https://github.com/SchubertLab/benchmark_TCRprediction.git
TODO: description how to build the apptainer
```

## Test own Method
To test your own method, you can use the programmatic interface:
```
from tcr_benchmark.pp.datasets import download_datasets
from tcr_benchmark.study.benchmark import evaluate_predictor

download_datasets("all")
results = evaluate_predictor(prediction_func, predictor_name, datasets, config)
```
--- todo: interface prediction function

## Components
```
|
|
|
```

## Cite
When you reference the benchmark or use the provided utilities to evaluate your method please cite:
```
todo
```

If you use the datasets, please also cite their original publication:
### Francis-Dataset
```
todo
```

### Minervina-Dataset
```
@article{minervina2022sars,
  title={SARS-CoV-2 antigen exposure history shapes phenotypes and specificity of memory CD8+ T cells},
  author={Minervina, Anastasia A and Pogorelyy, Mikhail V and Kirk, Allison M and Crawford, Jeremy Chase and Allen, E Kaitlynn and Chou, Ching-Heng and Mettelman, Robert C and Allison, Kim J and Lin, Chun-Yang and Brice, David C and others},
  journal={Nature Immunology},
  volume={23},
  number={5},
  pages={781--790},
  year={2022},
  publisher={Nature Publishing Group US New York}
}
```

### Mutation-Dataset (Dorigatti et al.)
```
@article{dorigatti2023predicting,
  title={Predicting T Cell Receptor Functionality against Mutant Epitopes},
  author={Dorigatti, Emilio and Drost, Felix and Straub, Adrian and Hilgendorf, Philipp and Wagner, Karolin Isabel and Bischl, Bernd and Busch, Dirk and Schober, Kilian and Schubert, Benjamin},
  journal={bioRxiv},
  pages={2023--05},
  year={2023},
  publisher={Cold Spring Harbor Laboratory}
}
```
