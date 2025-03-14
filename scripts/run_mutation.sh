#!/bin/bash
mkdir -p results
python -m tcr_benchmark.study.benchmark_alternatives \
        --dataset_selection mutation \
        --predictor_selection all \
        --path_option_yaml ./config/config_docker_options.yaml \
	--path_out ./results/results_mutation_all_models_and_options.csv
