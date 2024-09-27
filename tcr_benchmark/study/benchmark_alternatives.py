import pandas as pd
import argparse
from tqdm import tqdm

from tcr_benchmark.pp.datasets import download_datasets
from tcr_benchmark.study.ePytopeWrapper import wrapp_predictor
from tcr_benchmark.eval.allTests import NAME_2_TEST
from tcr_benchmark.utils.config import read_config_yaml


DATASETS = ["minervina", "francis", "dorigatti"]


def select_predictors(predictor_selection, config):
    if predictor_selection == "all":
        return list(config.keys())
    else:
        return predictor_selection.split(",")


def select_datasets(dataset_selection):
    if dataset_selection == "all":
        return DATASETS
    else:
        return dataset_selection.split(",")


def evaluate_predictor_on_dataset(prediction_func, predictor_name, dataset_name, config):
    test = NAME_2_TEST[dataset_name.lower()](None)
    results_dataset = test.run_tests(prediction_func, predictor_name, config)
    return results_dataset


def form_options(config, base_name):
    base_config = config.copy()
    if "options" not in base_config:
        return {base_name: base_config}

    options = base_config.pop("options")

    all_configs = {base_name: base_config}
    for opt_name, opt_dict in options.items():
        all_configs_new = {}
        for old_name, old_config in all_configs.items():
            for add_name, add_value in opt_dict.items():
                add_config = {opt_name: add_value}
                all_configs_new[f"{old_name}_{add_name}"] = {**old_config, **add_config}
        all_configs = all_configs_new
    return all_configs


def evaluate_predictor_options(prediction_func, predictor_name, datasets, config):
    results_predictor = []
    for dataset in tqdm(datasets, leave=False):
        configs_options = form_options(config[predictor_name], predictor_name)
        results_options = []
        for option_name, config in configs_options.items():
            result_dataset = evaluate_predictor_on_dataset(prediction_func, option_name, dataset, config)
            results_options.append(result_dataset)
        results_predictor.append(pd.concat(results_options))
    results_predictor = pd.concat(results_predictor, axis=1)
    return results_predictor


def evaluate_all(args, datasets, config):
    results_total = []
    for predictor_name in tqdm(select_predictors(args.predictor_selection, config)):
        prediction_func = wrapp_predictor(predictor_name)
        results_predictor = evaluate_predictor_options(prediction_func, predictor_name, datasets, config)
        results_total.append(results_predictor)

    results_total = pd.concat(results_total)
    results_total.to_csv(args.path_out)
    return results_total


def run_full_benchmark():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_selection", type=str, default="all")
    parser.add_argument("--predictor_selection", type=str, default="all")
    parser.add_argument("--path_option_yaml", type=str, default=None)
    parser.add_argument("--path_out", type=str, default="results/full_test_alternatives.csv")
    args = parser.parse_args()

    print("- Load config")
    config = read_config_yaml(args.path_option_yaml)

    print("- Setup all datasets")
    datasets = select_datasets(args.dataset_selection)
    download_datasets(datasets)

    print("- Evaluate all predictors")
    evaluate_all(args, datasets, config)


if __name__ == "__main__":
    run_full_benchmark()

# python -m tcr_benchmark.study.benchmark_alternatives --dataset_selection dorigatti --predictor_selection imrex --path_option_yaml config/sample_config_options.yaml
