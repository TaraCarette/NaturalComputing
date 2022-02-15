import numpy as np
import matplotlib.pyplot as plt
from ypstruct import structure
import ga8


    # Find a function of one independent
    # variable, in symbolic form, that fits a
    # given sample of 21 (xi, yi) data points
    # we have y and we need x
    
def symbolic_expression(x):
    # xi : yi
    # targetdata = {
    #     −1.0: 0.0000,
    #     −0.9: −0.1629,
    #     −0.8: −0.2624,
    #     −0.7: −0.3129,
    #     −0.6: −0.3264,
    #     −0.5: −0.3125,
    #     −0.4: −0.2784,
    #     −0.3: −0.2289,
    #     −0.2: −0.1664,
    #     −0.1: −0.0909,
    #     0: 0.0,
    #     0.1: 0.1111,
    #     0.2: 0.2496,
    #     0.3: 0.4251,
    #     0.4: 0.6496,
    #     0.5: 0.9375,
    #     0.6: 1.3056,
    #     0.7: 1.7731,
    #     0.8: 2.3616,
    #     0.9: 3.0951,
    #     1.0: 4.0000,}
    
    #return sum(x**2) # this is from the old code
    return sum(x**4 + x**3 + x**2 + x)
    #return sum(errors)
    
# The sum, taken over the 21 fitness cases,
# of the absolute value of difference
# between value of the dependent variable
# produced by the individual program and
# the target value yi of the dependent variable


# Problem Definition
problem = structure()
problem.costfunc = symbolic_expression # -> TODO: change to correct problem points
problem.nvar = 21
problem.varmin = -1
problem.varmax = 1

#funciton set : +, -, *, %, SIN, COS, EXP,RLOG


# GA Parameters
params = structure()
params.maxit = 50
params.npop = 50 # change later to 1000
params.beta = 1
params.pc = 1 # amount of children every parant has
params.gamma = 0.7  # crossover prob
params.mu = 0.00    # mutation rate
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
