from pybrain.tools.plotting.multiline import MultilinePlotter, print_coverage_addData, print_coverage_setLineStyle
plotter = MultilinePlotter(maxLines=3)
print("-------------BRANCH COVERAGE FOR ADD_DATA-----------------")
print("Before any testcases: ")
print_coverage_addData()
plotter.addData(0, 1, 2)
print("After first testcase:")
print_coverage_addData()
print("After second testcase:")
plotter.addData(1, [3, 4], [5, 6])
print_coverage_addData()


print("-------------BRANCH COVERAGE FOR SET_LINE_STYLE-----------------")
print("Before any testcases: ")
print_coverage_setLineStyle()

# Test default id (currentID)
plotter.currentID = 0
plotter.setLineStyle(color="red", linestyle="--")
print("After first testcase:")
print_coverage_setLineStyle()

# Test list of ids
plotter.setLineStyle(id=[0, 1], color="blue", linestyle="-.")
print("After second testcase:")
print_coverage_setLineStyle()

# Test single id
plotter.setLineStyle(id=1, color="green", linestyle=":")
print("After third testcase:")
print_coverage_setLineStyle()

# Test all lines
plotter.setLineStyle(id=-1, color="black", linestyle="-")
print("After fourth testcase:")
print_coverage_setLineStyle()
