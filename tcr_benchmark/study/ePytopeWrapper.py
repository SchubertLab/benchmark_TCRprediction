import pandas as pd
import tcr_benchmark.utils.config as config


def wrapp_predictor(name):
    from epytope.IO.IRDatasetAdapter import IRDataset
    from epytope.Core.TCREpitope import TCREpitope
    from epytope.TCRSpecificityPrediction import TCRSpecificityPredictorFactory

    def prediction_function(df_data, **kwargs):
        df_epytope = df_data.copy()
        df_epytope["organism"] = "Homo Sapiens"
        df_epytope["celltype"] = "T cell"
        df_epytope["VJ_chain_type"] = "TRA"
        df_epytope["VDJ_chain_type"] = "TRB"
        rename_dict = {
            config.col_cdr3a: "VJ_cdr3",
            config.col_ja: "VJ_j_gene",
            config.col_va: "VJ_v_gene",
            config.col_cdr3b: "VDJ_cdr3",
            config.col_jb: "VDJ_j_gene",
            config.col_vb: "VDJ_v_gene",
            config.col_epitope: "Peptide",
            config.col_mhc: "MHC",
        }
        df_epytope = df_epytope.rename(columns=rename_dict)
        tcrs = IRDataset()
        tcrs.from_dataframe(df_epytope)
        epitopes = [TCREpitope(row["Epitope"], row["MHC"]) for _, row in df_data.iterrows()]
        predictor = TCRSpecificityPredictorFactory(name)
        prediction = predictor.predict(tcrs, epitopes, pairwise=False, **kwargs)
        prediction = prediction.droplevel(0, axis=1)
        prediction = prediction.drop(columns=["celltype", "organism", "VDJ_chain_type", "VJ_chain_type"])
        prediction = prediction.rename(columns={k: v for v, k in rename_dict.items()})
        prediction = prediction.drop_duplicates(list(rename_dict.keys()))

        df_data = pd.merge(df_data, prediction, "left", list(rename_dict.keys()))
        df_data.columns = list(df_data.columns[:-1]) + ["Score"]
        return df_data
    return prediction_function
