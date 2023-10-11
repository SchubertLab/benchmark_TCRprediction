import pandas as pd
import requests
import os

import tcr_benchmark.utils.config as config
from tcr_benchmark.pp.abstractDownloader import AbstractDownloader


class DorigattiDownloader(AbstractDownloader):
    def __init__(self):
        super().__init__("dorigatti")
        self.rename_columns = {
            "CDR3α": config.col_cdr3a,
            "CDR3β": config.col_cdr3b,
            "TRAV": config.col_va,
            "TRAJ": config.col_ja,
            "TRBV": config.col_vb,
            "TRBJ": config.col_jb
        }
        self.url = "https://figshare.com/ndownloader/files/42571186?private_link=2113c5bbaf8c343d5df1"

    def download_data(self):
        r = requests.get(self.url, allow_redirects=True)
        open(f"{self.path_tmp}.xlsx", "wb").write(r.content)

    def extract_data(self):
        df_data = pd.read_excel(f"{self.path_tmp}.xlsx", sheet_name="Normalized by PC", engine="openpyxl")
        receptors = ["R21", "R23", "R24", "R25", "R26", "R28"]
        df_data = df_data[["Peptide"] + receptors]
        df_data = df_data.rename(columns={"Peptide": "Epitope"})
        df_data = pd.melt(df_data, id_vars=["Epitope"], value_vars=receptors, var_name="TCR",
                          value_name="Activation Score")
        df_data["Label"] = df_data["Activation Score"].apply(lambda x: 1 if x > 66.09 else 0)
        df_data["MHC"] = "HLA-B*07:02"

        df_seqs = pd.read_excel(f"{self.path_tmp}.xlsx", sheet_name="Sequences", engine="openpyxl", skiprows=1)
        df_seqs = df_seqs[["TCR"] + list(self.rename_columns.keys())]
        df_seqs = df_seqs.rename(columns=self.rename_columns)
        df_seqs = df_seqs[df_seqs["TCR"].isin(receptors)]
        for col in ["V_alpha", "J_alpha", "V_beta", "J_beta"]:
            df_seqs[col] = df_seqs[col].str.split(" ").str[0]

        df_data = df_data.merge(df_seqs, on="TCR", how="left")
        return df_data

    def standardize_data(self, df_data):
        return df_data

    def clean_up(self):
        os.remove(f"{self.path_tmp}.xlsx")
