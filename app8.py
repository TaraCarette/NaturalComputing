import numpy as np
import matplotlib.pyplot as plt
from ypstruct import structure
import ga8

# Sphere Test Function
def sphere(x):
    # Find a function of one independent
    # variable, in symbolic form, that fits a
    # given sample of 21 (xi, yi) data points -> insert datapoints
    # we have y and we need x
    
    return sum(x**2)
    #answer = sum(x**4 + x**3 + x**2 + x)
    
# The sum, taken over the 21 fitness cases,
# of the absolute value of difference
# between value of the dependent variable
# produced by the individual program and
# the target value yi of the dependent variable
    

# Problem Definition
problem = structure()
problem.costfunc = sphere
problem.nvar = 21
problem.varmin = -1
problem.varmax = 1

#funciton set : +, -, *, %, SIN, COS, EXP,RLOG


# GA Parameters
params = structure()
params.maxit = 50
params.npop = 50 # change later to 500

params.beta = 1
params.pc = 1
params.gamma = 0.1
params.mu = 0.01
params.sigma = 0.1

# Run GA
out = ga8.run(problem, params)

# Results
plt.plot(out.bestcost)
# plt.semilogy(out.bestcost)
plt.xlim(0, params.maxit)
plt.xlabel('Iterations')
plt.ylabel('Best Cost')
plt.title('Genetic Algorithm (GA)')
plt.grid(True)
plt.show()
