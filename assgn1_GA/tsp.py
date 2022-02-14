from random import shuffle, randint, uniform
import math
import matplotlib.pyplot as plt

# constants
# FILENAME = "file-tsp.txt"
# MATRIX_SIZE = (50, 2) 
# FILENAME = "file_drilling.txt"
# MATRIX_SIZE = (280, 2) 
FILENAME = "file_b_cities.txt"
MATRIX_SIZE = (29, 2) 
POP_SIZE = 10 # if odd, 1 will disappear as crossover creates 2 offspring
TERM_LOOPS = 1500
MUTATION = 0.1

# flag to set if want to run 2-opt version
TWO_OPT = True




# extract the data from the file and put it into a matrix
def readFile(fileN, mSize):
    with open(fileN, "r") as f:
        data = f.readlines()

    # initialize matrix in given size
    matrix = [[0 for x in range(mSize[1])] for y in range(mSize[0])]
    
    # fill matrix with data from file
    for d in range(0, len(data)):
        matrix[d] = [float(x) for x in data[d].strip("\n").split()]

    return matrix


def initPopulation(popSize, cityRange):
    population = []
    cityList = list(range(cityRange))

    # create a random order to visit eac city once
    for i in range(0, popSize):
        shuffle(cityList)
        population.append(cityList.copy())

    return population



def fitnessEval(population, cities):
    # initialize list for distances travelled by each solution
    distance = [0 for x in range(0, len(population))]

    # for each population, find distance travelled
    for p in range(0, len(population)):
        # in order of cities for solution, travel and keep track of distance
        for city in range(1, len(population[p])):
            firstC = cities[population[p][city - 1]]
            secondC = cities[population[p][city]]

            # calculate euclidean distance
            travel = math.sqrt((abs(firstC[0] - secondC[0])) ** 2 + (abs(firstC[1] - secondC[1])) ** 2)

            distance[p] += travel


    # convert distance to fitness: 1 / total distance
    fitness = [1 / d for d in distance]

    return distance, fitness


def tournamentSelection(population, fitness, numSelect):
    selected = []

    # select the specified number of candidates
    for i in range(0, numSelect):
        # pick 2 random candiates for tournament
        firstIndex = randint(0, len(population) - 1)
        secondIndex = randint(0, len(population) - 1)

        # choose the candidate with higher fitness
        if fitness[firstIndex] > fitness[secondIndex]:
            selected.append(population[firstIndex])
        else:
            selected.append(population[secondIndex])

    return selected


def crossover(population, fitness):
    mutatedPop = []
    popSize = len(population)
    candidateSize = len(population[0])

    # do it enough to completely replace old generation
    for i in range(0, int(popSize / 2)):
        # choose 2 random parents to apply crossover
        # firstParentInd = randint(0, popSize - 1)
        # secondParentInd = randint(0, popSize - 1)
        firstParent = tournamentSelection(population, fitness, 1)[0]
        secondParent = tournamentSelection(population, fitness, 1)[0]

        # choose 2 random crossover points
        firstIndex = randint(0, candidateSize - 1)
        secondIndex = randint(0, candidateSize - 1)

        # maintain order
        if firstIndex > secondIndex:
            firstIndex, secondIndex = secondIndex, firstIndex


        # create first offspring
        # default all -1
        offspring1 = [-1 for x in range(0, candidateSize)]
        # fill in crossover part
        offspring1[firstIndex:secondIndex] = firstParent[firstIndex:secondIndex]

        # fill in the rest of the numbers in order of other parent
        counter = 0
        for i in range(0, len(offspring1)):
            if offspring1[i] == -1:
                while secondParent[counter] in offspring1:
                    counter += 1
                offspring1[i] = secondParent[counter]
                counter += 1


        # create second offspring
        # default all -1
        offspring2 = [-1 for x in range(0, candidateSize)]
        # fill in crossover part
        offspring2[firstIndex:secondIndex] = secondParent[firstIndex:secondIndex]

        # fill in the rest of the numbers in order of other parent
        counter = 0
        for i in range(0, len(offspring2)):
            if offspring2[i] == -1:
                while firstParent[counter] in offspring2:
                    counter += 1
                offspring2[i] = firstParent[counter]
                counter += 1


        mutatedPop.append(offspring1)
        mutatedPop.append(offspring2)

    return mutatedPop


def mutation(population, mutationRate):
    mutatedPop = []

    # mutate each candidate in population
    for p in range(0, len(population)):
        # chance of each element of solution to mutate
        if uniform(0, 1) < mutationRate:
            # select 2 points to swap
            p1 = randint(0, len(population[p]) - 1)
            p2 = randint(0, len(population[p]) - 1)

            v1 = population[p][p1]
            v2 = population[p][p2]

            # swap
            population[p][p1] = v2
            population[p][p2] = v1

            mutatedPop.append(population[p])
        else:
            mutatedPop.append(population[p])

    return mutatedPop



def twoOptSwap(parent, j, k):
    # make a copy to be offsping
    offspring = parent.copy()

    # reverse the specified section
    temp = parent[j:k + 1].copy()
    temp.reverse()

    # replace relevant part of offspring with reversed section
    offspring[j:k + 1] = temp

    return offspring


def twoOptCalc(parent, distance, cities):
    # keep track of improved root and distance
    bestDistance = distance
    bestRoute = parent

    # loop over all sequences of nodes that can be swapped
    i = 0
    while(i < len(parent)):
        k = i + 1
        while(k < len(parent)):
            newRoute = twoOptSwap(parent, i, k)
            newDistance, _ = fitnessEval([newRoute], cities)
            if newDistance[0] < bestDistance:
                bestDistance = newDistance[0]
                bestRoute = newRoute
            k += 1
        i += 1

    return bestRoute


def twoOpt(population, cities):
    distance, _ = fitnessEval(population, cities)

    optPopulation = []
    # apply 2 opt to each member of the population to improve it
    for p in range(0, len(population)):
        route = twoOptCalc(population[p], distance[p], cities)
        optPopulation.append(route)

    return optPopulation


def main():
    # get the location of the cities
    cities = readFile(FILENAME, MATRIX_SIZE)
    
    # initialize the population
    population = initPopulation(POP_SIZE, len(cities))

    # if relevant do local search to population
    if TWO_OPT:
        population = twoOpt(population, cities)

    # evaluate the fitness of the population
    distance, fitness = fitnessEval(population, cities)

    # track best and average fitness over time
    bestFitness = [max(fitness)]
    averageFitness = [sum(fitness) / len(fitness)]

    # loop until reach termination condition
    counter = 0
    while counter < TERM_LOOPS:
        counter += 1
        print(max(fitness))
        print(min(distance))
        print(counter)
        print("*********")

        # crossover which selects candidates using binary tournament selection
        crossedCandidates = crossover(population, fitness)

        # mutation
        mutatedCandidates = mutation(crossedCandidates, MUTATION)

        # if relevant do local search to population
        if TWO_OPT:
            population = twoOpt(mutatedCandidates, cities)
        else:
            # select new generation
            # simply fully replace
            population = mutatedCandidates

        # update fitness
        distance, fitness = fitnessEval(population, cities)

        # update fitness tracker
        bestFitness.append(max(fitness))
        averageFitness.append(sum(fitness) / len(fitness))

    return bestFitness, averageFitness


if __name__ == '__main__':
    totalBF = []
    totalAF = []
    # run it 10 times
    for i in range(0, 5):
        print("On loop " + str(i))
        bestFitness, averageFitness = main()
        totalBF.append(bestFitness)
        totalAF.append(averageFitness)


    # plot the best fitness
    for i in range(0, len(totalBF)):
        plt.plot(list(range(0, TERM_LOOPS + 1)), totalBF[i])

    plt.xlabel('Iteration')
    plt.ylabel('Best Fitness')
    plt.title('Best Fitness over Time')
    plt.show()

    # plot the average fitness
    for i in range(0, len(totalAF)):
        plt.plot(list(range(0, TERM_LOOPS + 1)), totalAF[i])

    plt.xlabel('Iteration')
    plt.ylabel('Average Fitness')
    plt.title('Average Fitness over Time')
    plt.show()