from gplearn.genetic import SymbolicRegressor
from gplearn.functions import make_function
from gplearn.fitness import make_fitness
import csv
import numpy as np

FILENAME = "q8_data.txt"


# extract the data from the file and put it into a matrix
def readFile(fileN):
    with open(fileN, "r") as csvFile:
        csvReaderOutput = csv.reader(csvFile)

        data = [[], []]
        for line in csvReaderOutput:
            data[0].append(float(line[0]))
            data[1].append(float(line[1]))

    return data

def expFunc(x):
    return x ** 2

# def fitFunc(y, yPred, sampleWeight):
#     total = 0

#     for i in range(0, len(y)):
#         total += abs(y[i] - yPred[i])

#     return total
# fit = make_function(function=fitFunc, name='fit', arity=3)#, greater_is_better=False)

exp = make_function(function=expFunc, name='exp', arity=1)
function_set = ['add', 'sub', 'mul', 'div', 'log', 'sin', 'cos', exp]


data = readFile(FILENAME)
data = np.array(data)

# no mutation, only crossover is goal
# seems like exp is not allowed
gp = SymbolicRegressor(generations=50, population_size=1000,
                         function_set=function_set,
                         metric="mean absolute error",
                         p_crossover=0.7, p_subtree_mutation=0,
                         p_hoist_mutation=0, p_point_mutation=0,
                         max_samples=0.9, verbose=1,
                         random_state=0)

X = np.transpose([data[0]])
y = data[1]

gp.fit(X, y)