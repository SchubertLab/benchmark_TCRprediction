from tcr_benchmark.eval.minervinaTests import MinervinaTests
from tcr_benchmark.eval.francisTests import FrancisTest
from tcr_benchmark.eval.dorigattiTests import DorigattiTests


NAME_2_TEST = {
    "minervina": MinervinaTests,
    "francis": FrancisTest,
    "dorigatti": DorigattiTests,
}