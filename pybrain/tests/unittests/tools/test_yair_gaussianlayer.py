from pybrain.structure.modules.gaussianlayer import GaussianLayer, printBranchCoverage

print("-------------BRANCH COVERAGE FOR _forwardImplementation-----------------")
# set env
layer = GaussianLayer(dim=3)
inbuf = [0.0, 0.0, 0.0]
outbuf = [0.0, 0.0, 0.0]

print("Coverage before tests: ")
printBranchCoverage()

#test1
print("Coverage after test #1: ")
layer._forwardImplementation(inbuf, outbuf)
printBranchCoverage()

#test2
print("Coverage after test #2: ")
layer.enabled = False
layer._forwardImplementation(inbuf, outbuf)
printBranchCoverage()
