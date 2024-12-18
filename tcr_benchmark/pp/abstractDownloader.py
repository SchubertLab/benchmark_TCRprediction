import os
import abc

import tcr_benchmark.utils.config as config


class AbstractDownloader(abc.ABC):
    def __init__(self, name):
        """
        Abstract downloader class for automatic dataset download.
        :param name: str, name of the dataset
        """
        self.name = name
        self.rename_columns = {}

        self.path_data = config.path_data
        self.path_tmp = f"{self.path_data}/tmp_{name}"
        self.path_out = f"{self.path_data}/{name}.csv"
        os.makedirs(self.path_data, exist_ok=True)

    def get_data(self):
        """
        Downloads, processes, and saves the dataset.
        :return: dataset under ../data/{name}.csv
        """
        if not os.path.exists(self.path_out):
            self.download_data()
            df_data = self.extract_data()
            df_data = self.standardize_data(df_data)
            df_data.to_csv(self.path_out)
            self.clean_up()

    @abc.abstractmethod
    def download_data(self):
        """
        Download and unpacks the data from specified location.
        :return: unprocessed datasets under ../data/tmp_{name}
        """
        raise NotImplementedError

    @abc.abstractmethod
    def extract_data(self):
        """
        Processes the data into a standardized format.
        :return: pd.DataFrame containing the dataset
        """
        raise NotImplementedError

    def standardize_data(self, df_data):
        """
        Standardize data to same columns, naming conventions, and missing values.
        :param df_data: pd.DataFrame, with missing CDR3b and wrong column names
        :return: pd.DataFrame, containing the filtered, correctly named dataset
        """
        df_data = df_data.rename(columns=self.rename_columns)
        df_data = df_data[~df_data[config.col_cdr3b].isna()]
        df_data = df_data.reset_index(drop=True)
        df_data = df_data[config.required_cols]
        df_data = df_data.drop_duplicates()
        return df_data

    @abc.abstractmethod
    def clean_up(self):
        """
        Removes tmp data.
        """
        raise NotImplementedError

# TODO filter epitope length 13 in minervina