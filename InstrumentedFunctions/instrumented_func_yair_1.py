# Yaïr Jacob
# original location: pybrain/structure/modules/gaussianlayer.py
# instrumented function:

from scipy import random
from pybrain.structure.modules.neuronlayer import NeuronLayer
from pybrain.tools.functions import expln, explnPrime
from pybrain.structure.parametercontainer import ParameterContainer

branch_coverage = {
    "branch_1": False,
    "branch_2": False,
}

class GaussianLayer(NeuronLayer, ParameterContainer):
    """ A layer implementing a gaussian interpretation of the input. The mean is
    the input, the sigmas are stored in the module parameters."""

    def __init__(self, dim, name=None):
        NeuronLayer.__init__(self, dim, name)
        ParameterContainer.__init__(self, dim, stdParams = 0)
        self.autoalpha = False
        self.enabled = True

    def _forwardImplementation(self, inbuf, outbuf):
        if not self.enabled:
            branch_coverage["branch_1"] = True
            outbuf[:] = inbuf
        else:
            branch_coverage["branch_2"] = True
            outbuf[:] = random.normal(inbuf, expln(self.params))

def coverage_report():
    for branch, covered in branch_coverage.items():
        print(f"{branch} {'was hit' if covered else 'was not hit'}")
    
    print("Coverage is ", sum(branch_coverage.values()) / len(branch_coverage) * 100, "%\n")      

if __name__ == "__main__":
    # init 3 dimension
    layer = GaussianLayer(dim=3)
    
    # data
    inbuf = [0.0, 0.0, 0.0]
    outbuf = [0.0, 0.0, 0.0]

    print("Coverage before tests")
    coverage_report()
    
    print("# test 1 : self.enabled = true")
    layer._forwardImplementation(inbuf, outbuf)
    coverage_report()

    print("# test 2 : self.enabled = false")
    layer.enabled = False
    layer._forwardImplementation(inbuf, outbuf)
    coverage_report()
