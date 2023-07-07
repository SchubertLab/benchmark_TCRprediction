from tcr_benchmark.pp.datasets import download_all_datasets
from tcr_benchmark.study.ePytopeWrapper import wrapp_predictor


DATASETS = ['minervina', 'francis']
PREDICTORS = ['ERGO-II']


def evaluate_predictor_on_dataset(prediction_func, dataset_name):
    raise NotImplementedError


def evaluate_predictor(prediction_func):
    for dataset in DATASETS:
        evaluate_predictor_on_dataset(prediction_func, dataset)


def evaluate_all():
    for predictor in PREDICTORS:
        prediction_func = wrapp_predictor(predictor)
        evaluate_predictor(prediction_func)

    raise NotImplementedError


def run_full_benchmark():
    print('- Setup all datasets')
    download_all_datasets()

    print('- Evaluate all predictors')
    evaluate_all()
