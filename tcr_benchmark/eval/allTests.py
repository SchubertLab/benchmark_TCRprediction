from tcr_benchmark.eval.mutationTests import MutationTest
from tcr_benchmark.eval.mutationTestsMouse import MutationMouseTest
from tcr_benchmark.eval.viralTests import ViralTest


NAME_2_TEST = {
    "mutation": MutationTest,
    "mutation-mouse": MutationMouseTest,
    "viral": ViralTest,
}
