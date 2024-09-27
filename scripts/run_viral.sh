#!/bin/bash
mkdir -p results
python -m tcr_benchmark.study.benchmark \
        --dataset_selection viral \
        --predictor_selection all \
        --path_config_yaml ./config/cluster_config.yaml \
	--path_out ./results/results_viral.csv

