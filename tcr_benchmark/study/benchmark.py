import pandas as pd
import argparse
from tqdm import tqdm

from tcr_benchmark.pp.datasets import download_datasets
from tcr_benchmark.study.ePytopeWrapper import wrapp_predictor
from tcr_benchmark.eval.allTests import NAME_2_TEST
from tcr_benchmark.utils.config import read_config_yaml


DATASETS = ["mutation"]


def select_predictors(predictor_selection):
    if predictor_selection == "all":
        from epytope.TCRSpecificityPrediction import TCRSpecificityPredictorFactory
        return TCRSpecificityPredictorFactory.available_methods().keys()
    else:
        return predictor_selection.split(",")


def select_datasets(dataset_selection):
    if dataset_selection == "all":
        return DATASETS
    else:
        return dataset_selection.split(",")


def evaluate_predictor_on_dataset(prediction_func, predictor_name, dataset_name, config):
    test = NAME_2_TEST[dataset_name.lower()](None)
    config = {} if config is None or predictor_name not in config else config[predictor_name]
    results_dataset = test.run_tests(prediction_func, predictor_name, config)
    return results_dataset


def evaluate_predictor(prediction_func, predictor_name, datasets, config):
    results_predictor = []
    for dataset in tqdm(datasets, leave=False):
        result_dataset = evaluate_predictor_on_dataset(prediction_func, predictor_name, dataset, config)
        results_predictor.append(result_dataset)
    results_predictor = pd.concat(results_predictor, axis=1)
    return results_predictor


def evaluate_all(args, datasets, config):
    results_total = []
    for predictor_name in tqdm(select_predictors(args.predictor_selection)):
        prediction_func = wrapp_predictor(predictor_name)
        results_predictor = evaluate_predictor(prediction_func, predictor_name, datasets, config)
        results_total.append(results_predictor)

    results_total = pd.concat(results_total)
    results_total.to_csv(args.path_out)
    return results_total


def run_full_benchmark():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_selection", type=str, default="all")
    parser.add_argument("--predictor_selection", type=str, default="all")
    parser.add_argument("--path_config_yaml", type=str, default=None)
    parser.add_argument("--path_out", type=str, default="results/full_test.csv")
    args = parser.parse_args()

    print("- Load config")
    config = None
    if args.path_config_yaml is not None:
        config = read_config_yaml(args.path_config_yaml)

    print("- Setup all datasets")
    datasets = select_datasets(args.dataset_selection)
    download_datasets(datasets)

    print("- Evaluate all predictors")
    evaluate_all(args, datasets, config)


if __name__ == "__main__":
    run_full_benchmark()

# python -m tcr_benchmark.study.benchmark --dataset_selection minervina,minervina --predictor_selection ergo-ii,imrex
# python -m tcr_benchmark.study.benchmark --dataset_selection minervina --predictor_selection imrex --path_config_yaml config/sample_config.yaml
#  python -m tcr_benchmark.study.benchmark --dataset_selection dorigatti --predictor_selection ergo-ii --path_config_yaml ./config/cluster_config.yaml --path_out results/base_experiment_dorigatti.csv
#  python -m tcr_benchmark.study.benchmark --dataset_selection mutation --path_config_yaml ./config/config_docker.yaml
