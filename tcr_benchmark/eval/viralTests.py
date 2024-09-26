import warnings
import pandas as pd
import numpy as np
from tcr_benchmark.eval.abstractTests import AbstractTest
import tcr_benchmark.eval.metrics as metrics


class ViralTest(AbstractTest):
    def __init__(self, path_out):
        """

        :param path_out:
        """
        super().__init__("viral", path_out)
        self.test_settings = {
            "MPS": self.run_multiple_peptide_selection_test,
            "TTP": self.run_tcr_peptide_pairing_test,
        }
        self.test_data = None

    def run_prediction(self, predictor, config_predictor):
        """

        :param config_predictor:
        :param predictor:
        :return:
        """
        epitope_mhcs = self.df_base_data[["Epitope", "MHC"]].drop_duplicates().values
        data_full = []
        for epitope, mhc in epitope_mhcs:
            df_tmp = self.df_base_data.copy()
            df_tmp["Epitope"] = epitope
            df_tmp["MHC"] = mhc
            data_full.append(df_tmp)
        data_full = pd.concat(data_full)
        data_full = pd.merge(data_full, self.df_base_data, how="left", indicator="Label")
        data_full["Label"] = np.where(data_full.Label == "both", 1, 0)

        prediction = predictor(data_full, **config_predictor)
        return prediction

    def run_multiple_peptide_selection_test(self, prediction):
        if np.sum(prediction["Score"].notna()) != len(prediction):
            warnings.warn(f"Filter out {np.sum(prediction['Score'].isna())} Predictions due to NaN values. "
                          f"Metrics invalid")
            prediction = prediction[prediction["Score"].isna()]

        prediction["Epitope_MHC"] = prediction["Epitope"] + "_" + prediction["MHC"]
        prediction = prediction.drop(columns=["Epitope", "MHC"])
        labels = prediction.pivot_table(index=["CDR3_alpha", "V_alpha", "J_alpha", "CDR3_beta", "V_beta", "J_beta"],
                                        columns=["Epitope_MHC"], values="Label")
        prediction = prediction.pivot_table(
            index=["CDR3_alpha", "V_alpha", "J_alpha", "CDR3_beta", "V_beta", "J_beta"],
            columns=["Epitope_MHC"], values="Score")

        epitopes = prediction.columns
        labels = labels[epitopes]
        labels = labels.apply(lambda x: "".join([x[el] * el for el in epitopes]), axis=1)

        scores = metrics.calculated_rank_metrics(labels, prediction, labels, [1, 3, 5, 8])
        scores["Dataset"] = "Viral"
        return scores

    def run_tcr_peptide_pairing_test(self, prediction):
        scores = metrics.calculate_score_metrics(prediction["Label"], prediction["Score"], prediction["Epitope"])
        scores_class = metrics.calculate_classification_metrics(prediction["Label"], prediction["Score"],
                                                                prediction["Epitope"])
        scores = pd.concat([scores, scores_class])
        scores["Dataset"] = "Viral"
        return scores
