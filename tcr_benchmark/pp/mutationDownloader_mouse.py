import pandas as pd
import requests
import os

import tcr_benchmark.utils.config as config
from tcr_benchmark.pp.abstractDownloader import AbstractDownloader


class MutationMouseDownloader(AbstractDownloader):
    def __init__(self):
        super().__init__("mutation-mouse")
        self.rename_columns = {
            "CDR3α": config.col_cdr3a,
            "CDR3β": config.col_cdr3b,
            "TRAV": config.col_va,
            "TRAJ": config.col_ja,
            "TRBV": config.col_vb,
            "TRBJ": config.col_jb
        }
        self.url = [
            "https://figshare.com/ndownloader/files/52895705?private_link=75eaae3007894ab9b77a",
            "https://figshare.com/ndownloader/files/52895828?private_link=35ab54d22bfcb94d1faa"
        ]

    def download_data(self):
        r = requests.get(self.url[0], allow_redirects=True)
        open(f"{self.path_tmp}_0.xlsx", "wb").write(r.content)

        r = requests.get(self.url[1], allow_redirects=True)
        open(f"{self.path_tmp}_1.xlsx", "wb").write(r.content)

    def extract_data(self):
        df_educated = self.extract_data_repertoire(0)
        df_naive = self.extract_data_repertoire(1)

        df_data = pd.concat([df_educated, df_naive], axis=0)
        df_data = df_data.reset_index(drop=True)
        df_data['dataset'] = 'SIINFEKL'
        return df_data

    def extract_data_repertoire(self, i):
        df_data = pd.read_excel(f"{self.path_tmp}_{i}.xlsx", sheet_name="Normalized data", engine="openpyxl",
                                skiprows=1)
        df_data = df_data.rename(columns={"APL": "Epitope"})

        df_apls = pd.read_excel(f"{self.path_tmp}_{i}.xlsx", sheet_name="Individual APL screening", engine="openpyxl",
                                skiprows=1)
        apls = df_apls["Sequence"].str.split("-").str[1]
        df_data["Epitope"] = apls

        df_data = pd.melt(df_data, id_vars=["Epitope"], value_vars=df_data.columns[1:], var_name="TCR",
                          value_name="Activation Score")
        df_data["Label"] = df_data["Activation Score"].apply(lambda x: 1 if x > 46.9 else 0)
        df_data["MHC"] = "H2-Kb"

        df_seqs = pd.read_excel(f"{self.path_tmp}_{i}.xlsx", sheet_name="TCR_info", engine="openpyxl", skiprows=1)
        if i == 1:
            df_seqs["TCR"] = "Ed" + df_seqs["TCR"].str[3:]
        df_seqs = df_seqs[["TCR"] + list(self.rename_columns.keys())]
        df_seqs = df_seqs.rename(columns=self.rename_columns)
        df_seqs = df_seqs[df_seqs["TCR"].isin(df_data["TCR"])]
        for col in ["V_alpha", "J_alpha", "V_beta", "J_beta"]:
            df_seqs[col] = df_seqs[col].str.strip()
            df_seqs[col] = df_seqs[col].str.split("(").str[0]
            df_seqs[col] = df_seqs[col].str.split(" ").str[0]
            df_seqs[col] = df_seqs[col].str.replace("*00", "*01", regex=False)
            df_seqs[col] = df_seqs[col].str.replace("-DV", "/DV", regex=False)

        for col in ["CDR3_alpha", "CDR3_beta"]:
            df_seqs[col] = df_seqs[col].str.strip()

        df_data = df_data.merge(df_seqs, on="TCR", how="left")
        df_data = df_data[df_data["Epitope"] != "SIINFEKL"].copy()
        tcrs_bind = df_data.groupby("TCR")["Label"].sum()
        tcrs_bind = tcrs_bind[tcrs_bind > 0].index
        df_data = df_data[df_data["TCR"].isin(tcrs_bind)]
        return df_data

    def standardize_data(self, df_data):
        return df_data

    def clean_up(self):
        os.remove(f"{self.path_tmp}_0.xlsx")
        os.remove(f"{self.path_tmp}_1.xlsx")
