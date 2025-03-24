import pandas as pd

import tcr_benchmark.utils.config as config
from tcr_benchmark.pp.abstractDownloader import AbstractDownloader


# The following TCRs beta chains with matching epitope were found in public databases
OVERLAP_LIST = [
    'CASSSRSSYEQYF',
    'CASSIRSAYEQYF',
    'CASSIRSSYEQYF',
    'CASSVRSSYEQYF',
    'CASSTRSAYEQYF',
    'CASSARSTGELFF',
    'CASSIRSTGELFF',
    'CASSGRSTDTQYF',
    'CASSQRSTDTQYF',
    'CASSPRSTDTQYF',
    'CASSVRSTGELFF',
    'CASSTRSSYEQYF',
    'CASSTRSTDTQYF',
    'CASSTRSTGELFF',
    'CASSIRASYEQYF',
    'CASSVRSTDTQYF',
    'CASSIRSTDTQYF',
    'CASSMRSTDTQYF',
    'CASSIYSGGYNEQFF',
    'CASSIRSGYEQYF',
    'CASSIHSNQPQHF',
    'CASSLQNTGELFF',
    'CASGDENTGELFF',
    'CATQEGNTGELFF',
    'CASSPDIEAFF',
    'CASSEGQGYEQYF',
    'CASSRRSTDTQYF',
    'CASSFRSTGELFF',
    'CASSNRASYEQYF',
    'CASSGRSSDTQYF',
    'CASSLRSTDTQYF',
    'CASSARSTDTQYF',
    'CASNPDRNTGELFF',
    'CASSLDIEAFF',
    'CASSLTNEQFF',
    'CASSPPGGGNTGELFF',
    'CASSPTGGSYGYTF',
    'CASSIRSGWEQFF',
    'CASSPWGGNTEAFF',
    'CASQDLNTGELFF',
    'CASSDLNTGELFF',
    'CASSPDIEQFF',
    'CASQDQNTGELFF',
    'CASSELAGGNTGELFF',
    'CARGQENTGELFF',
    'CASSPPAGGNTGELFF',
    'CASQDANTGELFF',
    'CASSIRSAYEQFF'
]


class ViralDownloader(AbstractDownloader):
    def __init__(self):
        super().__init__("viral")
        self.rename_columns = {
            "IR_VJ_1_junction_aa": config.col_cdr3a,
            "IR_VDJ_1_junction_aa": config.col_cdr3b,
            "IR_VJ_1_v_call": config.col_va,
            "IR_VDJ_1_v_call": config.col_vb,
            "IR_VJ_1_j_call": config.col_ja,
            "IR_VDJ_1_j_call": config.col_jb,
            "epitope": config.col_epitope,
        }

    def download_data(self):
        pass

    def extract_data(self):
        path_base = config.path_data
        data_beam = pd.read_csv(f"{path_base}/../data/01_beam-t_clones.csv", index_col=0)
        data_beam["epitope"] = data_beam["epitope"].str.split("_").str[0]
        data_covid = pd.read_csv(f"{path_base}/../data/02_covid_dextramer_clones.csv", index_col=0)
        df_data = pd.concat([data_beam, data_covid])
        df_data = df_data.drop(columns=["IR_VJ_1_c_call", "IR_VDJ_1_c_call", "IR_VJ_1_d_call", "IR_VDJ_1_d_call"])
        for col in df_data.columns:
            if "_call" in col:
                df_data[col] = df_data[col].astype(str) + "*01"
        return df_data

    def standardize_data(self, df_data):
        df_data = df_data.rename(columns=self.rename_columns)

        mapper_epitope_mhc = {
            "AVFDRKSDAK": "HLA-A*11:01",
            "GILGFVFTL": "HLA-A*02:01",
            "TYGPVFMCL": "HLA-A*24:02",
            "AYAQKIFKI": "HLA-A*24:02",
            "NLVPMVATV": "HLA-A*02:01",
            "YVLDHLIVV": "HLA-A*02:01",
            "TPRVTGGGAM": "HLA-B*07:02",
            "GLCTLVAML": "HLA-A*02:01",
            "KLPDDFTGCV": "HLA-A*02:01",
            "QYIKWPWYI": "HLA-A*24:02",
            "NYNYLYRLF": "HLA-A*24:02",
            "KCYGVSPTK": "HLA-A*03:01",
            "LTDEMIAQY": "HLA-A*01:01",
            "YLQPRTFLL": "HLA-A*02:01",
            "SPRRARSVA": "HLA-B*07:02",
            "CTELKLSDY": "HLA-A*01:01",
            "FPQSAPHGV": "HLA-B*07:02",
            "YTNSFTRGVY": "HLA-A*01:01",
            "RAKFKQLL": "HLA-B*08:01",
            "RLQSLQTYV": "HLA-A*02:01",
            "FLRGRAYGL": "HLA-B*08:01",
            "QPYRVVVL": "HLA-B*08:01",
            "KIADYNYKL": "HLA-A*02:01",
            "VLNDILSRL": "HLA-A*02:01",
        }
        df_data["MHC"] = df_data["Epitope"].map(mapper_epitope_mhc)
        df_data = df_data[df_data["Epitope"].str.len() == 9]
        large_epitopes = df_data["Epitope"].value_counts()
        large_epitopes = large_epitopes[large_epitopes >= 5].index
        df_data = df_data[df_data["Epitope"].isin(large_epitopes)]

        df_data = df_data[df_data[config.col_cdr3a].str.len() <= 19]
        df_data = df_data[df_data[config.col_cdr3b].str.len() <= 19]
        df_data = df_data[df_data[config.col_cdr3b].str[-1] == "F"]

        df_data = df_data[~df_data["CDR3_beta"].isin(OVERLAP_LIST)]

        df_data = df_data.reset_index(drop=True)
        df_data["dataset"] = "viral"
        return df_data

    def clean_up(self):
        pass
