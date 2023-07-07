import os
import abc

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

    def run_tests(self):
        """

        :return:
        """
        results = {
            name: test_func() for name, test_func in self.test_settings.items()
        }
        self.save_results(results)

    def save_results(self, results):
        """
        Stores the results to disk.
        :param results: dict {name, results as pd.DataFrame} containin the results of the individual tests
        :return: writes results to '{path_results}/{dataset_name}_{test_name}.csv'
        """
        for test_name, result in results.items():
            path_res = f'{self.path_out}/{self.ds_name}_{test_name}.csv'
            result.to_csv(path_res)
