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

        self.path_out = f"{config.path_results}" if path_out is None else path_out
        os.makedirs(self.path_out, exist_ok=True)

        self.test_settings = {}

    def run_tests(self, predictor, name=None, config_predictor=None):
        """

        :return:
        """
        prediction = self.run_prediction(predictor, config_predictor)
        prediction.to_csv(f"{self.path_out}/predictions_{name}_{self.ds_name}.csv")
        mask_nans = prediction["Score"].isna()
        if mask_nans.sum() > 0:
            warnings.warn(f"Filtering {np.sum(mask_nans)} elements for {name} due to NaN prediction.", stacklevel=-1)
            prediction = prediction[~mask_nans]

        results = []
        for metric_type, test_func in self.test_settings.items():
            df_tmp = test_func(prediction)
            df_tmp["Metric_Type"] = metric_type
            results.append(df_tmp)
        results = pd.concat(results)

        groups = []
        supports = []
        metrics = []
        values = []
        datasets = []
        types = []
        for i, row in results[["Metric", "Metric_Type"]].drop_duplicates().iterrows():
            m = row["Metric"]
            c = row["Metric_Type"]
            df_tmp = results[(results["Metric"] == m) & (results["Group"] != "full_data")]
            average = df_tmp["Value"].mean()
            weighted = (df_tmp["Value"] * df_tmp["Support"] / df_tmp["Support"].sum()).sum()
            groups += ["Average", "WeightedAverage"]
            supports += [len(df_tmp)] * 2
            metrics += [m] * 2
            values += [average, weighted]
            datasets += ["All"] * 2
            types += [c] * 2
        results_avg = pd.DataFrame({
            "Group": groups,
            "Support": supports,
            "Metric": metrics,
            "Value": values,
            "Dataset": datasets,
            "Metric_Type": types,
        })
        results = pd.concat([results, results_avg])

        results = results.reset_index(drop=True)
        results["Method"] = name
        results = results[["Method", "Dataset", "Group", "Support", "Metric_Type", "Metric", "Value"]]
        results.to_csv(f"{self.path_out}/results_{name}_{self.ds_name}.csv")
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
        :return: writes results to "{path_results}/{dataset_name}_{test_name}.csv"
        """
        for test_name, result in results.items():
            path_res = f"{self.path_out}/{self.ds_name}_{test_name}.csv"
            result.to_csv(path_res)
