from copy import deepcopy
from random import randint

from numpy.random import random

from Point import Point


class Individual:
    def __init__(self, words, words_str):
        """
        representation
        @param words: a list of Words
        """
        self.words = words
        self.words_str = words_str
        # add a random word from words_str in a space that fits in words
        pickedWord = words_str[randint(0, len(words_str)-1)]
        pickedSize = len(pickedWord)

        fitting_spaces = []
        for word in words:
            if word.size == pickedSize:
                fitting_spaces.append(word)
        # no need to check other constraints beside size because there are no other words strings populated in words
        # pick a random space to be used with the word
        # fitting_spaces[randint(0, len(fitting_spaces) - 1)].setWordStr(pickedWord)
        self.addWord(pickedWord)
        self.fitness()

    def addWord(self, word_str):
        """
        :param word_str: word to be added without breaking any constraints
        :return: True if the operation succeeded, False otherwise
        """
        fitting_spaces = []
        for word in self.words:
            if word.size == len(word_str):
                fitting_spaces.append(word)

        # remove the spaces in which adding the word will break constraints
        for space in fitting_spaces:
            if not self.__fits(word_str, space):
                fitting_spaces.remove(space)

        if len(fitting_spaces) == 0:
            # the word doesn't fit anywhere
            return False

        # pick a random space to be used with the word
        pickedSpace = fitting_spaces[randint(0, len(fitting_spaces) - 1)]
        pickedSpace.setWordStr(word_str)
        pickedSpace.filledIn = True

        self.__updateConstraints(pickedSpace)
        return True

    def __fits(self, word_str, space):
        """

        :param word_str: word string to check
        :param space: space (Word) to check
        :return: True if word_str can be inserted into space without breaking constraints, False otherwise
        """
        for cond in space.restrictions:
            if word_str[cond[1]] == cond[0]:
                continue
            else:
                return False

        return True


    def __updateConstraints(self, word):
        """
        Update the constraints of each space which has a tile intersecting word
        :param word: Word
        :return: none
        """
        # iterate through each cell and check what other Words intersect it
        # if intersecting, set (append to the restrictions) the intersection cell's restrictions in the other Word to
        # be the letter of the intersecting cell from this word
        intersects = self.__wordsIntersecting(word)

        for (intersected, word_idx, intersected_idx, point) in intersects:
            char = word.word[word_idx]
            # check that the constraint hasn't been added already
            if (char, word_idx, intersected_idx, point) not in intersected.restrictions:
                intersected.addRestriction(char, intersected_idx, point.getX(), point.getY())
                # intersected.restrictions.append((char, intersected_idx, point))

    def __wordsIntersecting(self, word):
        """
        Return a list representing the words which intersect the given word
        :param word:
        :return: list
        """
        intersects = []

        # 2 cases, either X is const or Y is const
        if word.point_start.getX() - word.point_end.getX() == 0:
            # X const, Y varies
            Y_interval = range(word.point_start.getY(), word.point_end.getY()+1)
            for w in self.words:
                # look for words with const Y and with Y in the interval in which Y from the word varies
                if w.point_start.getY() - w.point_end.getY() == 0 and w.point_start.getY() in Y_interval:
                    # intersection! Get the intersection indexes in both word and w
                    word_idx_y = list(filter(lambda e: e == w.point_start.getY(), Y_interval))
                    word_idx = word_idx_y[0] - word.point_start.getY()

                    w_idx_x = list(filter(lambda e: e == word.point_start.getX(), range(w.point_start.getX(),
                                                                                        w.point_end.getX()+1)))
                    w_idx = w_idx_x[0] - w.point_start.getX()

                    intersects.append((w, word_idx, w_idx, Point(word.point_start.getX(), word_idx_y)))
        else:
            # Y const, X varies
            X_interval = (word.point_start.getX(), word.point_end.getX())
            for w in self.words:
                # look for words with const X and with X in the interval in which X from the word varies
                if w.point_start.getX() - w.point_end.getX() == 0 and w.point_start.getX() in X_interval:
                    # intersection!

                    word_idx_x = list(filter(lambda e: e == w.point_start.getX(), X_interval))
                    word_idx = word_idx_x[0] - word.point_start.getX()

                    w_idx_y = list(filter(lambda e: e == word.point_start.getY(), range(w.point_start.getY(),
                                                                                        w.point_end.getY() + 1)))
                    w_idx = w_idx_y[0] - w.point_start.getY()

                    intersects.append((w, word_idx, w_idx, Point(word_idx_x, word.point_start.getY())))
        return intersects
    """
    @:returns float
    """
    def fitness(self):
        """
        The fitness of an individual represents the number of word placed that intersect (hence, the most
        words placed while constraints hold)
        :param problem:
        :return: int
        """
        fitness = 0
        for w in self.words:
            for i in self.__wordsIntersecting(w):
                if i[0].filledIn:
                    fitness += 1

        return fitness/2

    """
    """
    def mutate(self, probability):
        """
        Mutate the individual by picking a random free space and finding a word that fits in without breaking
        constraints
        :param probability:
        :return: none
        """

        if random() > probability:
            return
        succeeded = False
        max_tries = 10
        trials = 0
        while not succeeded and trials < max_tries:
            trials += 1
            # try to find a random space and a random word which fits the space
            space_idx = randint(0, len(self.words)-1)
            word_idx = randint(0, len(self.words_str)-1)
            word_str = self.words_str[word_idx]

            if word_str in [x.word for x in self.words]:
                # word used, try again
                continue

            if self.words[space_idx].size != len(word_str):
                # wrong size, try again
                continue

            # word not used and the size fits as size. Check the constraints
            if self.__fits(word_str, self.words[space_idx]):
                # constraints hold, perform the mutation
                self.words[space_idx].word = word_str
                self.__updateConstraints(self.words[space_idx])
                succeeded = True

    def crossover(self, other_ind, probability):
        """
        The child results from adding in the fittest individual a random word that fits somewhere, from the
        other individual
        If they have the same fitness, pick a random one as the destination (receiver). The crossover doesn't
        alter the genotype of the parents, by destination I mean the state of the child before adding genes
        If the parents are incompatible (there are no words that can be added from one into another without
        breaking the constraints), either:

        -- the child is a copy of either ind1 or ind2 (random) and it replaces the less fit parent or a
            random parent if they have the same fitness

        -- or nothing happends

        :param other_ind: other individual to combine data with
        :param probability: the probability of the crossover occuring
        :return: the resulted individual
        """

        if random() > probability:
            return self

        if self.fitness() > other_ind.fitness():
            # this ind. is better, use it as template for building the child
            child = deepcopy(self)
            source = other_ind
        elif self.fitness() < other_ind.fitness():
            # the other ind. is better
            child = deepcopy(other_ind)
            source = self
        else:
            # both are as fit, pick a random one as source
            if random() > 0.5:
                child = deepcopy(self)
                source = other_ind
            else:
                child = deepcopy(other_ind)
                source = self

        if self.__transferWordToChild(source, child):
            # parents are compatible and the crossover has succeeded
            return child
        else:
            # parents are incompatible, where are no words to be passed from one of them to the template (child)
            # without breaking the constraints
            # nothing happend, crossover fails and the child is the same as one of the parents
            return source



    def __transferWordToChild(self, source, child):
        """
        Find a word to copy from the source ind. to put into the child's 'genome'

        :param source: the Individual that serves as a data source
        :param child: the receiving Individual
        :return: the modified child
        """
        for w in [w for w in source.words if w.filledIn]:
            for space in [s for s in child.words if not s.filledIn]:
                if self.__fits(w.word, space) and w.word not in [w.word for w in child.words]:
                    space.word = w.word
                    space.restrictions = deepcopy(w.restrictions)
                    space.filledIn = True
                    return True
        return False

    def __str__(self):
        output = ""

        for w in self.words:
            output += str(w) + '\n'

        return output
