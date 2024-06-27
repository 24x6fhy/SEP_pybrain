from pybrain.structure.modules.lstm import LSTMLayer, printBranchCoverage

print("-------------BRANCH COVERAGE FOR whichNeuron-----------------")
# set env
lstm_layer = LSTMLayer(dim=10, peepholes=True)
input_index = 25
output_index = 3

print("Coverage before tests: ")
printBranchCoverage()

#test1
input_neuron = lstm_layer.whichNeuron(inputIndex=input_index)
print("Coverage after test #1: ")
printBranchCoverage()

#test2
output_neuron = lstm_layer.whichNeuron(outputIndex=output_index)
print("Coverage after test #2: ")
printBranchCoverage()
