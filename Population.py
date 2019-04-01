from Individual import Individual
from copy import deepcopy


class Population:
    def __init__(self, count_ind, words, words_str):
        self.__noIndividuals = count_ind
        # list of the individuals
        self.individuals = [Individual(deepcopy(words), deepcopy(words_str)) for _ in range(self.__noIndividuals)]

    def evaluate(self):
        pass

    # arguments : somethings
    def selection(self):
        pass

    def __getitem__(self, key):
        return self.individuals[key]

    def __setitem__(self, key, value):
        self.individuals[key] = value
