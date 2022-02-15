from gplearn.genetic import SymbolicRegressor
from gplearn.functions import make_function
from gplearn.fitness import make_fitness
import csv
import matplotlib.pyplot as plt
import numpy as np

FILENAME = "q8_data.txt"


# extract the data from the file 
def readFile(fileN):
    with open(fileN, "r") as csvFile:
        csvReaderOutput = csv.reader(csvFile)

        data = [[], []]
        for line in csvReaderOutput:
            data[0].append(float(line[0]))
            data[1].append(float(line[1]))

    return data

# define the exp for the function list to use as it is not default
def expFunc(x):
    return np.exp(x)

# define fitness function
def fitFunc(y, yPred, sampleWeight):
    return - np.sum(np.abs(y - yPred))


# make own fitness function since not a default
fit = make_fitness(function=fitFunc, greater_is_better=True)#name='fit', arity=3)#, greater_is_better=False)

expV = make_function(function=expFunc, name='exp', arity=1)

# the function set to be used to solve the problem
function_set = ['add', 'sub', 'mul', 'div', 'log', 'sin', 'cos', expV]

# get the data and format it so it can be processed
data = readFile(FILENAME)
data = np.array(data)

X = np.transpose([data[0]])
y = data[1]


# no mutation, only crossover is goal
# seems like exp is not allowed
gp = SymbolicRegressor(generations=50, population_size=1000,
                         function_set=function_set,
                         metric=fit,
                         p_crossover=0.7, p_subtree_mutation=0,
                         p_hoist_mutation=0, p_point_mutation=0,
                         max_samples=0.9, verbose=1,
                         random_state=0)

# fit the data using the regressor
equation = gp.fit(X, y)
print(equation)

# plot the progress
plt.plot(list(range(0, 50)), gp.run_details_["best_fitness"])
plt.xlabel('Iteration')
plt.ylabel('Best Fitness')
plt.title('Best Fitness over Time')
plt.show()

plt.plot(list(range(0, 50)), gp.run_details_["best_length"])
plt.xlabel('Iteration')
plt.ylabel('Best Length')
plt.title('Best Length over Time')
plt.show()
