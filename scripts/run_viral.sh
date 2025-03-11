#!/bin/bash
mkdir -p results
python -m tcr_benchmark.study.benchmark_alternatives \
        --dataset_selection viral \
        --predictor_selection all \
        --path_option_yaml ./config/config_docker_options.yaml \
	--path_out ./results/results_viral_all_models_and_options.csv
