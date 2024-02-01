#!/bin/bash
python -m tcr_benchmark.study.benchmark \
        --dataset_selection $1 \
        --predictor_selection all \
        --path_config_yaml ${CODE_PATH}/config/config_docker.yaml \
	--path_out ${RESULT_PATH}/base_experiment_$1.csv

