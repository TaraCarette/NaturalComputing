from random import shuffle, randint, uniform
import math

# constants
FILENAME = "file-tsp.txt"
MATRIX_SIZE = (50, 2)
POP_SIZE = 20
TERM_LOOPS = 50
MUTATION = 0.1



# extract the data from the file and put it into a matrix
def readFile(fileN, mSize):
    with open("file-tsp.txt", "r") as f:
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
            travel = math.sqrt((firstC[0] + secondC[0]) ** 2 + (firstC[1] + secondC[1]) ** 2)

            distance[p] += travel


    # convert distance to fitness: 1 / total distance
    fitness = [1 / d for d in distance]

    return distance, fitness


def tournamentSelection(population, fitness):
    selected = []
    # need to fully replace generation and so tournament will select same number
    nextGenSize = len(population)

    # select enough candidates for reproduction
    for i in range(0, nextGenSize):
        # pick 2 random candiates for tournament
        firstIndex = randint(0, nextGenSize - 1)
        secondIndex = randint(0, nextGenSize - 1)

        # choose the candidate with higher fitness
        if fitness[firstIndex] > fitness[secondIndex]:
            selected.append(population[firstIndex])
        else:
            selected.append(population[secondIndex])

    return selected


def crossover(population):
    mutatedPop = []
    popSize = len(population)
    candidateSize = len(population[0])

    # do it enough to completely replace old generation
    for i in range(0, popSize):
        # choose 2 random parents to apply crossover
        firstParentInd = randint(0, popSize - 1)
        secondParentInd = randint(0, popSize - 1)

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
        offspring1[firstIndex:secondIndex] = population[firstParentInd][firstIndex:secondIndex]

        # fill in the rest of the numbers in order of other parent
        counter = 0
        for i in range(0, len(offspring1)):
            if offspring1[i] == -1:
                while population[secondParentInd][counter] in offspring1:
                    counter += 1
                offspring1[i] = population[secondParentInd][counter]
                counter += 1


        # create second offspring
        # default all -1
        offspring2 = [-1 for x in range(0, candidateSize)]
        # fill in crossover part
        offspring2[firstIndex:secondIndex] = population[secondParentInd][firstIndex:secondIndex]

        # fill in the rest of the numbers in order of other parent
        counter = 0
        for i in range(0, len(offspring2)):
            if offspring2[i] == -1:
                while population[firstParentInd][counter] in offspring2:
                    counter += 1
                offspring2[i] = population[firstParentInd][counter]
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


def main():
    # get the location of the cities
    cities = readFile(FILENAME, MATRIX_SIZE)
    
    # initialize the population
    population = initPopulation(POP_SIZE, len(cities))

    # evaluate the fitness of the population
    distance, fitness = fitnessEval(population, cities)

    # loop until reach termination condition
    counter = 0
    while counter < TERM_LOOPS:
        counter += 1
        print(sum(fitness) / len(fitness))
        print(sum(distance) / len(distance))
        print("*********")

        # select candidates for reproduction
        # using binary tournament selection
        selectedCandidates = tournamentSelection(population, fitness)

        # crossover
        crossedCandidates = crossover(selectedCandidates)

        # mutation
        mutatedCandidates = mutation(crossedCandidates, MUTATION)

        # update fitness
        distance, fitness = fitnessEval(mutatedCandidates, cities)

        # select new generation
        # simply fully replace
        population = selectedCandidates

    


if __name__ == '__main__':
    main()