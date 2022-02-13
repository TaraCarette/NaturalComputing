# a) generate random sequence x (l=100)
# b) copy x and invert each bit with probability p
# c) if copy is closer to goal -> replace x by copy
# d) repeat step b and c untill goal is reached

import random
from re import A
import matplotlib.pyplot as plt

GOAL = '1' * 100


def main():
    
    for _ in range(10):
        x = initialize(100)
    
        bestx = [sum(int(x)for x in x)]
        iteration = [0]
        
        for i in range(1500):
            xm = copy_mutate(x)
            if sum(int(a)for a in xm) > sum(int(b)for b in x):
                x = xm
            bestx.append(sum(int(x)for x in x))
            iteration.append(i)
        
        plt.plot(iteration, bestx)

    #plt.ylim(0, sum(int(x)for x in GOAL)+1)
    #plt.xlim(0, 1500)
    plt.xlabel('iteration')
    plt.ylabel('best x')
    plt.title('best fitness')
    plt.show()


def initialize(length):
    x = str(random.getrandbits(1))
    for i in range(length -1):
        x+=str(random.getrandbits(1))
    return x

def copy_mutate(x):
    xm = ''
    for bit in x:
        if random.randint(0,100) == 1:
            xm += flip(int(bit))
        else:
            xm += bit
    return xm

        
def flip(bit):
    if bit == 1:
        return '0'
    if bit == 0:
        return '1'

main()