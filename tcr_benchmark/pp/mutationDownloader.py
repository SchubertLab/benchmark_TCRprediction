import pandas as pd
import requests
import os

import tcr_benchmark.utils.config as config
from tcr_benchmark.pp.abstractDownloader import AbstractDownloader


class MutationDownloader(AbstractDownloader):
    def __init__(self):
        super().__init__("mutation")
        self.rename_columns = [{
            "CDR3α": config.col_cdr3a,
            "CDR3β": config.col_cdr3b,
            "TRAV": config.col_va,
            "TRAJ": config.col_ja,
            "TRBV": config.col_vb,
            "TRBJ": config.col_jb
        },
            {
            "TCR id": "TCR",
            "cdr3_a_aa": config.col_cdr3a,
            "cdr3_b_aa": config.col_cdr3b,
            "TRAV": config.col_va,
            "TRAJ": config.col_ja,
            "TRBV": config.col_vb,
            "TRBJ": config.col_jb,
        }]
        self.url = [
            "https://figshare.com/ndownloader/files/42571186?private_link=2113c5bbaf8c343d5df1",
            "https://figshare.com/ndownloader/files/46457545?private_link=9c6797680490b667884f",
        ]

    def download_data(self):
        r = requests.get(self.url[0], allow_redirects=True)
        open(f"{self.path_tmp}_0.xlsx", "wb").write(r.content)

        r = requests.get(self.url[1], allow_redirects=True)
        open(f"{self.path_tmp}_1.xlsx", "wb").write(r.content)

    def extract_data(self):
        df_tumor = self.extract_data_tumor()
        df_tumor['dataset'] = 'tumor'

        df_cmv = self.extract_data_cmv()
        df_cmv['dataset'] = 'cmv'

        df_data = pd.concat([df_tumor, df_cmv], axis=0)
        return df_data

    def extract_data_cmv(self):
        df_data = pd.read_excel(f"{self.path_tmp}_1.xlsx", sheet_name="Mean", engine="openpyxl")
        receptors = [f"CMV_{el}" for el in df_data.columns if el != "Peptide_ID"]
        df_data = df_data.rename(columns={"Peptide_ID": "Epitope"})
        df_data.columns = ["Epitope"] + receptors
        df_data = pd.melt(df_data, id_vars=["Epitope"], value_vars=receptors, var_name="TCR",
                          value_name="Activation Score")
        df_data["Label"] = df_data["Activation Score"].apply(lambda x: 1 if x > 40.0 else 0)
        df_data["MHC"] = "HLA-A*02:01"

        df_seqs = pd.read_excel(f"{self.path_tmp}_1.xlsx", sheet_name="TCR sequences", engine="openpyxl")
        df_seqs = df_seqs[list(self.rename_columns[1].keys())]
        df_seqs = df_seqs.rename(columns=self.rename_columns[1])
        df_seqs["TCR"] = "CMV_" + df_seqs["TCR"].str.split(" ").str[1].str.replace("-", "_")
        df_seqs = df_seqs[df_seqs["TCR"].isin(receptors)]
        for col in ["V_alpha", "J_alpha", "V_beta", "J_beta"]:
            df_seqs[col] = df_seqs[col].str.strip()
            df_seqs[col] = df_seqs[col].str.split("(").str[0]
            df_seqs[col] = df_seqs[col].str.split(" ").str[0]

        mapping_id_peptides = pd.read_excel(f"{self.path_tmp}_1.xlsx", sheet_name="peptides", engine="openpyxl")
        mapping_id_peptides = dict(zip(mapping_id_peptides["ID"], mapping_id_peptides["Peptide"]))
        df_data["Epitope"] = df_data["Epitope"].map(mapping_id_peptides)

        df_data = df_data.merge(df_seqs, on="TCR", how="left")
        return df_data

    def extract_data_tumor(self):
        df_data = pd.read_excel(f"{self.path_tmp}_0.xlsx", sheet_name="Normalized by PC", engine="openpyxl")
        receptors = ["R21", "R23", "R24", "R25", "R26", "R28"]
        df_data = df_data[["Peptide"] + receptors]
        df_data = df_data.rename(columns={"Peptide": "Epitope"})
        df_data = pd.melt(df_data, id_vars=["Epitope"], value_vars=receptors, var_name="TCR",
                          value_name="Activation Score")
        df_data["Label"] = df_data["Activation Score"].apply(lambda x: 1 if x > 66.09 else 0)
        df_data["MHC"] = "HLA-B*07:02"

        df_seqs = pd.read_excel(f"{self.path_tmp}_0.xlsx", sheet_name="Sequences", engine="openpyxl", skiprows=1)
        df_seqs = df_seqs[["TCR"] + list(self.rename_columns[0].keys())]
        df_seqs = df_seqs.rename(columns=self.rename_columns[0])
        df_seqs = df_seqs[df_seqs["TCR"].isin(receptors)]
        for col in ["V_alpha", "J_alpha", "V_beta", "J_beta"]:
            df_seqs[col] = df_seqs[col].str.split(" ").str[0]

        df_data = df_data.merge(df_seqs, on="TCR", how="left")
        return df_data

    def standardize_data(self, df_data):
        return df_data

    def clean_up(self):
        os.remove(f"{self.path_tmp}_0.xlsx")
        os.remove(f"{self.path_tmp}_1.xlsx")
