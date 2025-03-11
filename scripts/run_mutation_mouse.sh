#!/bin/bash
PREDICTORS="bertrand,titan,atm-tcr,teim,panpep,itcep,tcellmatch,ergo-i,ergo-ii,imrex,teinet,epitcr,attntap,tulip-tcr"

mkdir -p results
python -m tcr_benchmark.study.benchmark_alternatives \
        --dataset_selection mutation-mouse \
        --predictor_selection ${PREDICTORS} \
        --path_option_yaml ./config/config_docker_options_mutation.yaml \
	--path_out ./results/results_mutation_mouse_applicable_models_and_options.csv
