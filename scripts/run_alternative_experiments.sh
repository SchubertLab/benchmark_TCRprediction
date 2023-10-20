#!/bin/bash
python -m tcr_benchmark.study.benchmark_alternatives \
        --dataset_selection dorigatti \
        --predictor_selection all \
        --path_option_yaml ${CODE_PATH}/config/cluster_config_options.yaml \
	--path_out ${RESULT_PATH}/alternative_experiment_dorigatti.csv

