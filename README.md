# Report for Assignment 1

## Project chosen

Name: pybrain

URL: https://github.com/pybrain/pybrain

Number of lines of code and the tool used to count it: 27148 (lizard)

Programming language: Python

## Coverage measurement

### Existing tool

We used Coverage.py as the existing tool to check the coverage of our forked project.
It was executed by the command `coverage run -m unittest discover `
![Coverage results](sources/old_coverage.png)

### Your own coverage tool
#### Yaïr Jacob
_forwardImplementation from pybrain/structure/modules/gaussianlayer.py and whichNeuron from pybrain/structure/modules/lstm.py
[Relevant commit](https://github.com/24x6fhy/SEP_pybrain/commit/a476662013e86b5b76812ad3ac5328d21afb08ed)
Code output: \

![Yaïr Jacob](sources/yair_coverage.png)

#### Celal Turkmen
semilinear(x) and explnPrime(x) from pybrain/tools/functions.py \
[Relevant commit](https://github.com/24x6fhy/SEP_pybrain/commit/4f6d168feb45c2e99709aa0c82eaede21168f136) \
Code output: \
![Celal Coverage](sources/celal_coverage.png)

#### Enis Kerem Cakmak
addData(self, id0, x, y) and setLineStyle(self, id=None, **kwargs) from pybrain\tools\plotting\multiline.py \
[Relevant commit](https://github.com/24x6fhy/SEP_pybrain/commit/8638ffb2020cae48d70d25936c0262559df276e0) \
Code output: \
![Enis Coverage](sources/enis_coverage.PNG)
## Coverage improvement

### Individual tests

#### Yaïr Jacob
[Relevant commit](https://github.com/24x6fhy/SEP_pybrain/commit/cdc522f50547317da2c2edbbc75285e68ca8e7bc)

Old coverage : \ 
![Old Coverage File](sources/yair_before_cov.png)
![Old Covered Statements](sources/coverage_before_yair.png)
New coverage: \
![New Coverage](sources/yair_after_cov.png)
![Old Covered Statements](sources/overall_before_coverage.png)

#### Celal Turkmen

Note: Test 1 & 2 are both in the same file, so I did not make it separately.
[Relevant commit](https://github.com/24x6fhy/SEP_pybrain/commit/7a086fb7b8edb133ca4311066f875acf8ada334f) \

Old coverage: \
![Old Coverage](sources/old_coverage.png)
New coverage: \
![New Coverage](sources/celal_improvement.png)

Covered statements are increased from 10753 to 10797. This is because test_celal.py file under test/unittest folder includes some test cases covering the statements in tools/functions.py.

#### Enis Kerem Cakmak

Note: Test 1 & 2 are both in the same file, that is, multiline.py.
[Relevant commit](https://github.com/24x6fhy/SEP_pybrain/commit/8638ffb2020cae48d70d25936c0262559df276e0) \

Old coverage: \
![Old Coverage](sources/old_coverage.png)
New coverage: \
![New Coverage](sources/enis_improvement.png)

As it is seen from the screenshots, the coverage is improved from 10753 to 10822 as a result of the new test cases added under pybrain\tests\unittests\tools\test_enis.py covering the selected function statements in pybrain\tools\plotting\multiline.py.

### Overall
Old Coverage:
![Old Coverage](sources/overall_before_coverage.png)

Final Coverage:
![Final Coverage](sources/overall_after_coverage.png)

## Statement of individual contributions

### Celal Turkmen
- Found the project and checked if it meets the requirements.
- Instrumented the aforementioned functions.
- Showed the improvement of the coverage thanks to the instrumented functions in the report.
- Completed my own part in the report.

### Enis Kerem Cakmak
- Selected the individual functions to be tested.
- Instrumented the functions with custom coverage tool.
- Improved existing coverage with the new testcases and instrumented functions added.
- Finished the necessary report part.

### Yair Jacob
- Sought for projects that fit the requirements
- Selected individual functions to be tested.
- Improved existing coverage with new testcases
- Report finalization
