# Yaïr Jacob
# original location: pybrain/structure/modules/lstm.py
# instrumented function:

from scipy import tanh
from pybrain.tools.functions import sigmoid, sigmoidPrime, tanhPrime

branch_coverage = {
    "branch_1": False,
    "branch_2": False,
}

class NeuronLayer:
    def __init__(self, dim):
        self.dim = dim

class Module:
    def __init__(self, indim, outdim, name=None):
        self.indim = indim
        self.outdim = outdim
        self.name = name
        self.offset = 0

class ParameterContainer:
    def __init__(self, size):
        self.params = [0.0] * size
        self.derivs = [0.0] * size

    def setArgs(self, **args):
        for key, value in args.items():
            setattr(self, key, value)

    def _setParameters(self, p, owner=None):
        self.params = p

    def _setDerivatives(self, d, owner=None):
        self.derivs = d

class LSTMLayer(NeuronLayer, ParameterContainer):

    sequential = True
    peepholes = False
    maxoffset = 0

    # Transfer functions and their derivatives
    f = lambda _, x: sigmoid(x)
    fprime = lambda _, x: sigmoidPrime(x)
    g = lambda _, x: tanh(x)
    gprime = lambda _, x: tanhPrime(x)
    h = lambda _, x: tanh(x)
    hprime = lambda _, x: tanhPrime(x)

    def __init__(self, dim, peepholes=False, name=None):
        self.setArgs(dim=dim, peepholes=peepholes)

        # Initialize internal buffers dynamically
        self.bufferlist = [
            ('ingate', dim), ('outgate', dim), ('forgetgate', dim),
            ('ingatex', dim), ('outgatex', dim), ('forgetgatex', dim),
            ('state', dim), ('ingateError', dim), ('outgateError', dim),
            ('forgetgateError', dim), ('stateError', dim),
        ]

        Module.__init__(self, 4 * dim, dim, name)
        if self.peepholes:
            ParameterContainer.__init__(self, dim * 3)
            self._setParameters(self.params)
            self._setDerivatives(self.derivs)

    def _setParameters(self, p, owner=None):
        ParameterContainer._setParameters(self, p, owner)
        dim = self.outdim
        self.ingatePeepWeights = self.params[:dim]
        self.forgetgatePeepWeights = self.params[dim:dim * 2]
        self.outgatePeepWeights = self.params[dim * 2:]

    def _setDerivatives(self, d, owner=None):
        ParameterContainer._setDerivatives(self, d, owner)
        dim = self.outdim
        self.ingatePeepDerivs = self.derivs[:dim]
        self.forgetgatePeepDerivs = self.derivs[dim:dim * 2]
        self.outgatePeepDerivs = self.derivs[dim * 2:]

    def _isLastTimestep(self):
        return self.maxoffset == self.offset

    def _forwardImplementation(self, inbuf, outbuf):
        self.maxoffset = max(self.offset + 1, self.maxoffset)
        dim = self.outdim

        try:
            self.ingatex[self.offset] = inbuf[:dim]
        except IndexError:
            raise IndexError(f"IndexError at timestep {self.offset} with buffer shape {self.ingatex.shape}")

        self.forgetgatex[self.offset] = inbuf[dim:dim * 2]
        cellx = inbuf[dim * 2:dim * 3]
        self.outgatex[self.offset] = inbuf[dim * 3:]

        if self.peepholes and self.offset > 0:
            self.ingatex[self.offset] += self.ingatePeepWeights * self.state[self.offset - 1]
            self.forgetgatex[self.offset] += self.forgetgatePeepWeights * self.state[self.offset - 1]

        self.ingate[self.offset] = self.f(self.ingatex[self.offset])
        self.forgetgate[self.offset] = self.f(self.forgetgatex[self.offset])

        self.state[self.offset] = self.ingate[self.offset] * self.g(cellx)
        if self.offset > 0:
            self.state[self.offset] += self.forgetgate[self.offset] * self.state[self.offset - 1]

        if self.peepholes:
            self.outgatex[self.offset] += self.outgatePeepWeights * self.state[self.offset]

        self.outgate[self.offset] = self.f(self.outgatex[self.offset])
        outbuf[:] = self.outgate[self.offset] * self.h(self.state[self.offset])

    def _backwardImplementation(self, outerr, inerr, outbuf, inbuf):
        dim = self.outdim
        cellx = inbuf[dim * 2:dim * 3]

        self.outgateError[self.offset] = self.fprime(self.outgatex[self.offset]) * outerr * self.h(self.state[self.offset])
        self.stateError[self.offset] = outerr * self.outgate[self.offset] * self.hprime(self.state[self.offset])

        if not self._isLastTimestep():
            self.stateError[self.offset] += self.stateError[self.offset + 1] * self.forgetgate[self.offset + 1]
            if self.peepholes:
                self.stateError[self.offset] += self.ingateError[self.offset + 1] * self.ingatePeepWeights
                self.stateError[self.offset] += self.forgetgateError[self.offset + 1] * self.forgetgatePeepWeights

        if self.peepholes:
            self.stateError[self.offset] += self.outgateError[self.offset] * self.outgatePeepWeights

        cellError = self.ingate[self.offset] * self.gprime(cellx) * self.stateError[self.offset]

        if self.offset > 0:
            self.forgetgateError[self.offset] = self.fprime(self.forgetgatex[self.offset]) * self.stateError[self.offset] * self.state[self.offset - 1]

        self.ingateError[self.offset] = self.fprime(self.ingatex[self.offset]) * self.stateError[self.offset] * self.g(cellx)

        if self.peepholes:
            self.outgatePeepDerivs += self.outgateError[self.offset] * self.state[self.offset]

            if self.offset > 0:
                self.ingatePeepDerivs += self.ingateError[self.offset] * self.state[self.offset - 1]
                self.forgetgatePeepDerivs += self.forgetgateError[self.offset] * self.state[self.offset - 1]

        inerr[:dim] = self.ingateError[self.offset]
        inerr[dim:dim * 2] = self.forgetgateError[self.offset]
        inerr[dim * 2:dim * 3] = cellError
        inerr[dim * 3:] = self.outgateError[self.offset]

    def whichNeuron(self, inputIndex=None, outputIndex=None):
        if inputIndex is not None:
            branch_coverage["branch_1"] = True
            return inputIndex % self.outdim
        if outputIndex is not None:
            branch_coverage["branch_2"] = True
            return outputIndex

def coverage_report():
    for branch, covered in branch_coverage.items():
        print(f"{branch} {'was hit' if covered else 'was not hit'}")
    
    print("Coverage is ", sum(branch_coverage.values()) / len(branch_coverage) * 100, "%\n")      

# Example usage:
if __name__ == "__main__":
    lstm_layer = LSTMLayer(dim=10, peepholes=True)

    # test data
    input_index = 25
    output_index = 3

    print("Coverage before tests")
    coverage_report()

    input_neuron = lstm_layer.whichNeuron(inputIndex=input_index)
    print("coverage after test 1")
    coverage_report()

    output_neuron = lstm_layer.whichNeuron(outputIndex=output_index)
    print("coverage after test 2")
    coverage_report()

