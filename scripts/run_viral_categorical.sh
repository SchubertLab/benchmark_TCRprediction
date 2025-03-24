#!/bin/bash
mkdir -p results
python -m tcr_benchmark.study.benchmark_alternatives \
        --dataset_selection viral \
        --predictor_selection mixtcrpred,nettcr,tcrgp \
        --path_option_yaml ./config/config_docker_options_categorical.yaml \
	--path_out ./results/results_viral_categorical_models_option.csv
