# Benchmarking T cell receptor - Epitope Predictors with ePytope
This repository contains the code to recreate the study "Benchmarking of T-Cell Receptor-Epitope Predictors with ePytope-TCR" by Drost et al.

## Install
Stand-alone Benchmark-Suite:
```
pip install -e .
```

Benchmark-Suite with ePytope:

Note: you will need to install the individual predictors, separately. You may consult the dockerfile in `./docker/Dockerfile`
```
pip install -e .[epytope]
```

Reproducibility:
To reproduce the environment of the paper. To reproduce the specific environment of the predictors, we advise to use the dockerfile in `./docker/Dockerfile`
```
pip install -e .[epytope]
```

## Reproduce Benchmark
To setup the a docker container with all tools:
```
git clone https://github.com/SchubertLab/benchmark_TCRprediction.git
cd benchmark_TCRprediction
sudo docker build -t img_benchmark -f ./docker/Dockerfile ..
sudo docker run --gpus all -d --name ctr_benchmark -p 8001 img_benchmark
sudo docker exec -it ctr_benchmark /bin/bash
```

Within the docker container, you can reproduce the benchmark via
```
conda activate epytope_base
./scripts/run_viral.sh
./scripts/run_mutations.sh
```
The results can be found in `./results/*` and `./tcr_benchmark/results/*`. Please note, that despite best efforts, not all tools are fully reproducible.

## Test own Method
To test your own method, please refer to this notebook:
https://github.com/SchubertLab/benchmark_TCRprediction/blob/master/tutorials/01_new_method.ipynb

## Cite
When you reference the benchmark or use the provided utilities to evaluate your method please cite the benchmarking paper and the corresponding datasets:
```
@article{drost2024benchmarking,
  title={Benchmarking of T-Cell Receptor-Epitope Predictors with ePytope-TCR},
  author={Drost, Felix and Chernysheva, Anna and Albahah, Mahmoud and Kocher, Katharina and Schober, Kilian and Schubert, Benjamin},
  journal={bioRxiv},
  pages={2024--11},
  year={2024},
  publisher={Cold Spring Harbor Laboratory}
}
```

### Viral Dataset
```
@article{kocher2024quality,
  title={Quality of vaccination-induced T cell responses is conveyed by polyclonality and high, but not maximum, antigen receptor avidity},
  author={Kocher, Katharina and Drost, Felix and Tesfaye, Abel Mekonnen and Moosmann, Carolin and Schuelein, Christine and Grotz, Myriam and D'Ippolito, Elvira and Graw, Frederik and Spriewald, Bernd and Busch, Dirk H and others},
  journal={bioRxiv},
  pages={2024--10},
  year={2024},
  publisher={Cold Spring Harbor Laboratory}
}
```


```
@article{adams2023integrated,
  title={An integrated reagent and multimodal analysis workflow to enrich and characterize peptide-specific CD8+ T cells},
  author={Adams, Bruce A and Shahi, Payam and Reyes, Daniel and Maheshwari, Shamoni and Mousavi, Nima and Krishnan, Sreenath and Ramen, Nandhini and Tsai, FuNien and Kumar, Poornasree and Finnegan, Peter and others},
  journal={The Journal of Immunology},
  volume={210},
  number={1\_Supplement},
  pages={249--17},
  year={2023},
  publisher={American Association of Immunologists}
}
```

### Mutation-Dataset
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
