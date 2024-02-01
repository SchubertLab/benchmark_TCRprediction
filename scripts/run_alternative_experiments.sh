#!/bin/bash
python -m tcr_benchmark.study.benchmark_alternatives \
        --dataset_selection $1 \
        --predictor_selection all \
        --path_option_yaml ${CODE_PATH}/config/config_docker_options.yaml \
	--path_out ${RESULT_PATH}/alternative_experiment_dorigatti.csv

