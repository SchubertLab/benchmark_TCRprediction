import pandas as pd
import os
import requests

import tcr_benchmark.utils.config as config
from tcr_benchmark.pp.abstractDownloader import AbstractDownloader


class MinervinaDownloader(AbstractDownloader):
    def __init__(self):
        super().__init__('minervina')

        self.url = 'https://static-content.springer.com/esm/art%3A10.1038%2Fs41590-022-01184-4/' \
                   'MediaObjects/41590_2022_1184_MOESM6_ESM.xlsx'
        self.rename_columns = {
            'cdr3a': config.col_cdr3a,
            'va': config.col_va,
            'ja': config.col_ja,
            'cdr3b': config.col_cdr3b,
            'vb': config.col_vb,
            'jb': config.col_jb,
        }

    def download_data(self):
        r = requests.get(self.url, allow_redirects=True)
        open(f'{self.path_tmp}.xlsx ', 'wb').write(r.content)

    def extract_data(self):
        df_data = pd.read_excel(f'{self.path_data}/tmp_minervina.xlsx', sheet_name='cd8_final')

        epitope_2_mhc = {
            'A01_TTD': 'HLA-A*01:01',
            'A01_LTD': 'HLA-A*01:01',
            'A01_PTD': 'HLA-A*01:01',
            'A01_FTS': 'HLA-A*01:01',
            'A01_NTN': 'HLA-A*01:01',
            'A01_DTD': 'HLA-A*01:01',
            'A02_YLQ': 'HLA-A*02:01',
            'A02_ALS': 'HLA-A*02:01',
            'A02_LLY': 'HLA-A*02:01',
            'A24_VYI': 'HLA-A*24:02',
            'A24_QYI': 'HLA-A*24:02',
            'A24_VYF': 'HLA-A*24:02',
            'A24_NYN': 'HLA-A*24:02',
            'B15_NQK': 'HLA-B*15:01',
            'B15_RVA': 'HLA-B*15:01',
            'B44_AEV': 'HLA-B*44:0',
            'B44_VEN': 'HLA-B*44:0',
            'B44_QEL': 'HLA-B*44:0',
        }

        abr_epitopes = {
            'A01_TTD': 'TTDPSFLGRY',
            'A01_LTD': 'LTDEMIAQY',
            'A01_PTD': 'PTDNYITTY',
            'A01_FTS': 'FTSDYYQLY',
            'A01_NTN': 'NTNSSPDDQIGYY',
            'A01_DTD': 'DTDFVNEFY',
            'A02_YLQ': 'YLQPRTFLL',
            'A02_ALS': 'ALSKGVHFV',
            'A02_LLY': 'LLYDANYFL',
            'A24_VYI': 'VYIGDPAQL',
            'A24_QYI': 'QYIKWPWYI',
            'A24_VYF': 'VYFLQSINF',
            'A24_NYN': 'NYNYLYRLF',
            'B15_NQK': 'NQKLIANQF',
            'B15_RVA': 'RVAGDSGFAAY',
            'B44_AEV': 'AEVQIDRLI',
            'B44_VEN': 'VENPHLMGWD',
            'B44_QEL': 'QELIRQGTDY',
        }

        df_data[config.col_mhc] = df_data['epitope'].map(epitope_2_mhc)
        df_data[config.col_epitope] = df_data['epitope'].map(abr_epitopes)
        return df_data

    def clean_up(self):
        os.remove(f'{self.path_data}/tmp_minervina.xlsx')
