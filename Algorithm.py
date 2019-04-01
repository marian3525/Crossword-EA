from numpy.random import random, randint

from Population import Population
from Problem import Problem


class Algorithm:
    def __init__(self):
        self.__problem = Problem()
        # + specific data
        self.__mutationProb = 0
        self.__crossoverProb = 0
        self.__populationSize = 0
        self.noIterations = 0
        self.readParameters("param.in")

        self.__population = Population(self.__populationSize, self.__problem.words, self.__problem.words_str)

        print(f"Created population of {self.__populationSize:d} individuals configured with mutation:"
              f"{self.__mutationProb:1.2f}, crossover:{self.__crossoverProb:1.2f}")
        print("Words:", [str(w) for w in self.__problem.words])
        print("Words set:" + str(self.__problem.words_str))

        # print("Individuals:")
        # for i in self.__population.individuals:
        #   print(str(i))

        # self.__population.individuals[0].mutate(1)

        #print("Individuals:")
        #for i in self.__population.individuals:
        #    print(str(i))

    """
    Read params from file
    """
    def readParameters(self, filename):
        f = open(filename, "r")

        self.__mutationProb = float(f.readline().split("=")[1])
        self.__crossoverProb = float(f.readline().split("=")[1])
        self.__populationSize = int(f.readline().split("=")[1])
        self.noIterations = int(f.readline().split("=")[1])

        f.close()

    def iterate(self):
        i1 = randint(0, self.__populationSize-1)
        i2 = randint(0, self.__populationSize-1)

        if i1 == i2:
            return
        ind1 = self.__population[i1]
        ind2 = self.__population[i2]

        c = ind1.crossover(ind2, self.__crossoverProb)
        c.mutate(self.__mutationProb)

        f1 = ind1.fitness()
        f2 = ind2.fitness()
        fc = c.fitness()

        if f1 > f2 and f2 < fc:
            # the offspring replaces the least fit parent
            self.__population[i2] = c
        elif f2 > f1 and f1 < fc:
            self.__population[i1] = c

        return fc

    def run(self):
        fitness = list()

        for _ in range(self.noIterations):
            fitness.append(self.iterate())

        # print the best individual
        graded = sorted([(x, x.fitness()) for x in self.__population.individuals], key=lambda e: e[1], reverse=True)

        result = graded[0]
        optimalFitness = result[1]
        optimalIndividual = result[0]

        print("Result:")
        print(result)
        print("Optimal fitness:")
        print(optimalFitness)
        print("Optimal Individual")
        print(optimalIndividual)

        return (result, fitness)

    def statistics(self):
        pass
