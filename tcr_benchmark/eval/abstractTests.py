import os
import abc
import warnings
import pandas as pd
import numpy as np

import tcr_benchmark.utils.config as config
from tcr_benchmark.pp.datasets import get_dataset


class AbstractTest(abc.ABC):
    def __init__(self, name, path_out):
        """
        Abstract test class for automatic testing.
        :param name: str, name of the test
        :param path_out: str, folder where results will be stored
        """
        self.ds_name = name

        self.df_base_data = get_dataset(self.ds_name)

        self.path_out = f'{config.path_results}' if path_out is None else path_out
        os.makedirs(self.path_out, exist_ok=True)

        self.test_settings = {}

    def run_tests(self, predictor, name=None, config_predictor=None):
        """

        :return:
        """
        prediction = self.run_prediction(predictor, config_predictor)
        prediction.to_csv(f'{self.path_out}/predictions_{name}_{self.ds_name}.csv')
        mask_nans = prediction["Score"].isna()
        if mask_nans.sum() > 0:
            warnings.warn(f"Filtering {np.sum(mask_nans)} elements for {name} due to NaN prediction.", stacklevel=-1)
            prediction = prediction[~mask_nans]

        results = {
            name: test_func(prediction) for name, test_func in self.test_settings.items()
        }
        results = {(self.ds_name, test_name, metric_name): metric_value
                   for test_name, test_values in results.items()
                   for metric_name, metric_value in test_values.items()}
        columns = pd.MultiIndex.from_tuples(results.keys())
        results = pd.DataFrame(data=results.values(), index=columns,
                               columns=[name if name is not None else 'predictor'])
        results = results.transpose()
        results.to_csv(f'{self.path_out}/results_{name}_{self.ds_name}.csv')
        return results

    @abc.abstractmethod
    def run_prediction(self, prediction_func, config_predictor):
        """
        To reduce computational load, predictions are conducted once in this function covering all test settings.
        :param config_predictor:
        :param prediction_func: function, that receives a pd.DataFrame, and returns the dataframe with a binding score
        :return: pd.DataFrame, containing TCR-epitope pairs, binding label, and prediction score
        """
        raise NotImplementedError

    def save_results(self, results):
        """
        Stores the results to disk.
        :param results: dict {name, results as pd.DataFrame} containin the results of the individual tests
        :return: writes results to '{path_results}/{dataset_name}_{test_name}.csv'
        """
        for test_name, result in results.items():
            path_res = f'{self.path_out}/{self.ds_name}_{test_name}.csv'
            result.to_csv(path_res)
