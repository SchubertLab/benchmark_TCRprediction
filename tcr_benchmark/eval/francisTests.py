from tcr_benchmark.eval.abstractTests import AbstractTest


class FrancisTest(AbstractTest):
    def __init__(self, path_out):
        """

        :param path_out:
        """
        super().__init__('minervina', path_out)
        self.test_settings = {
            'TTP': self.run_tcr_peptide_pairing_test,
        }

    def run_prediction(self, predictor):
        """

        :param predictor:
        :return:
        """
        raise NotImplementedError

    def run_tcr_peptide_pairing_test(self, prediction):
        raise NotImplementedError
