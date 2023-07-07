import pandas as pd
import numpy as np
import requests
import zipfile
import os
import shutil

import tcr_benchmark.utils.config as config
from tcr_benchmark.pp.abstractDownloader import AbstractDownloader


class FrancisDownloader(AbstractDownloader):
    def __init__(self):
        super(FrancisDownloader, self).__init__('francis')

        self.url = 'TODO'
        self.rename_columns = {
            'alpha1_vgene': config.col_va,
            'alpha1_jgene': config.col_ja,
            'beta1_vgene': config.col_vb,
            'beta1_jgene': config.col_jb,
            'HLA': config.col_mhc,
        }

    def download_data(self):
        raise NotImplementedError

    def extract_data(self):
        with zipfile.ZipFile(f'{self.path_data}/sciimmunol.abk3070_data_files_s1_to_s9.zip', 'r') as zip_ref:
            zip_ref.extractall(f'{self.path_data}/francis_tmp')

        df_data = pd.read_excel(f'{self.path_tmp}/sciimmunol.abk3070_data_file_s3.xlsx',
                                sheet_name='Supp_Table_hits_VDJ')
        df_data[config.col_cdr3a] = df_data['clonotype'].str.split('_').str[0].str.split(';').str[0]
        df_data[config.col_cdr3a] = df_data[config.col_cdr3a].apply(lambda x: x if x != 'No-alpha-detected' else np.nan)
        df_data[config.col_cdr3b] = df_data['clonotype'].str.split('_').str[1].str.split(';').str[0]
        df_data[config.col_cdr3b] = df_data[config.col_cdr3b].apply(lambda x: x if x != 'No-beta-detected' else np.nan)
        return df_data

    def clean_up(self):
        shutil.rmtree(f'{self.path_data}/francis_tmp')
        os.remove(f'{self.path_data}/sciimmunol.abk3070_data_files_s1_to_s9.zip')
