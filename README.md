# Benchmarking T cell receptor - Epitope Predictors with ePytope
This repository contains the code to recreate the study "todo" by Drost et al.

## Install
Stand-alone Benchmark-Suite:
```
pip install tcr-benchmark
```

Benchmark-Suite with ePytope:

Note: you will need to install the individual predictors, separately. You may consult the dockerfile in `./docker/Dockerfile`
```
pip install tcr-benchmark[epytope]
```

Reproducibility:
To reproduce the environment of the paper. To reproduce the specific environment of the predictors, we advise to use the dockerfile in `./docker/Dockerfile`
```
pip install tcr-benchmark[epytope]
```

## Reproduce Benchmark
To reproduce the benchmark you can
```
git clone https://github.com/SchubertLab/benchmark_TCRprediction.git
cd benchmark_TCRprediction
sudo docker build -t tcr_benchmark -f ./docker/Dockerfile ..

```

## Test own Method
To test your own method, you can use the programmatic interface:
```
from tcr_benchmark.pp.datasets import download_datasets
from tcr_benchmark.study.benchmark import evaluate_predictor

download_datasets("all")
results = evaluate_predictor(prediction_func, predictor_name, datasets, config)
```
- prediction_func: python function that obeys the following interface
  - input: a pandas data frame of the columns ['', '', ...] #todo
  - output: the input pandas dataframe with the additional columns <predictor_name> containing binding scores with higher scores representing higher binding probabilities
- predictor_name: str, name of your predictor
- datasets:
  - Viral dataset: 'viral'
  - Mutational dataset: 'mutation'
  - Both datasets: 'all'
- configs: kwargs that will forwarded to your prediction function

## Cite
When you reference the benchmark or use the provided utilities to evaluate your method please cite the benchmarking paper and the corresponding datasets:
```
todo
```

### Viral Dataset
```
todo: Kocher, Drost et al.
```


```
todo: 10x Genomics
```

### Mutation-Dataset (Dorigatti et al.)
```
@article{drost2024predicting,
  title={Predicting T cell receptor functionality against mutant epitopes},
  author={Drost, Felix and Dorigatti, Emilio and Straub, Adrian and Hilgendorf, Philipp and Wagner, Karolin I and Heyer, Kersten and Montes, Marta L{\'o}pez and Bischl, Bernd and Busch, Dirk H and Schober, Kilian and Schubert, Benjamin},
  journal={Cell Genomics},
  volume={4},
  number={9},
  year={2024},
  publisher={Elsevier}
}
```
