from tcr_benchmark.eval.abstractTests import AbstractTest


class MinervinaTests(AbstractTest):
    def __init__(self, path_out):
        """

        :param path_out:
        """
        super(MinervinaTests, self).__init__('minervina', path_out)
        self.test_settings = {
            'MPS': self.run_multiple_peptide_selection_test,
            'TTP': self.run_tcr_peptide_pairing_test,
        }

    def run_prediction(self, predictor):
        """

        :param predictor:
        :return:
        """
        raise NotImplementedError

    def run_multiple_peptide_selection_test(self, prediction):
        raise NotImplementedError

    def run_tcr_peptide_pairing_test(self, prediction):
        raise NotImplementedError
