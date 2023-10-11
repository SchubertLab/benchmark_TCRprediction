from tcr_benchmark.eval.abstractTests import AbstractTest
import tcr_benchmark.eval.metrics as metrics


class DorigattiTests(AbstractTest):
    def __init__(self, path_out):
        """

        :param path_out:
        """
        super().__init__("dorigatti", path_out)
        self.test_settings = {
            "Classification": self.run_classification_test,
            "Regression": self.run_regression_test,
        }
        self.test_data = None

    def run_prediction(self, predictor, config_predictor):
        """

        :param config_predictor:
        :param predictor:
        :return:
        """
        prediction = predictor(self.df_base_data, **config_predictor)
        return prediction

    def run_classification_test(self, prediction):
        scores = metrics.calculate_score_metrics(prediction["Label"], prediction["Score"], prediction["TCR"])
        scores_class = metrics.calculate_classification_metrics(prediction["Label"], prediction["Score"],
                                                                prediction["TCR"])
        scores.update(scores_class)
        return scores

    def run_regression_test(self, prediction):
        scores = metrics.calculate_correlation_metrics(prediction["Activation Score"], prediction["Score"],
                                                       prediction["TCR"])
        return scores
