import os
import pandas as pd
from tqdm import tqdm

import tcr_benchmark.utils.config as config

from tcr_benchmark.pp.minervinaDownloader import MinervinaDownloader
from tcr_benchmark.pp.francisDownloader import FrancisDownloader
from tcr_benchmark.pp.mutationDownloader import MutationDownloader


dataset_downloader = {
    # "minervina": MinervinaDownloader,
    # "francis": FrancisDownloader,
    "mutation": MutationDownloader,
}


def get_dataset(name):
    """
    Provides a dataset by its name.
    :param name: str, name of the dataset
    :return: pd.DataFrame, containing the dataset
    """
    assert name.lower() in dataset_downloader, f"Name is '{name}' but must be in {dataset_downloader.keys()}."
    path_dataset = f"{config.path_data}/{name}.csv"
    if not os.path.exists(path_dataset):
        downloader = dataset_downloader[name.lower()]
        downloader().get_data()
    df_data = pd.read_csv(path_dataset, index_col=0)
    return df_data


def get_all_datasets():
    """
    Provides all datasets.
    :return: dict, {dataset_name: dataset}
    """
    datasets = {name: get_dataset(name) for name in dataset_downloader.keys()}
    return datasets


def download_datasets(selection):
    """
    Download the datasets from Minervina, Francis, and ...
    :param selection: list(str) or str
    :return: processed datasets, und ../data/{name}.csv
    """
    for name, dataset in tqdm(dataset_downloader.items()):
        if selection == "all" or name in selection:
            dataset().get_data()


if __name__ == "__main__":
    get_all_datasets()
