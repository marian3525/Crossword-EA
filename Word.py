from Point import Point


class Word:
    def __init__(self, word, size, point_start, point_end):
        self.word = word
        self.point_start = point_start
        self.point_end = point_end
        self.size = size
        # list of (character, char-idx, Point(boardx, boardy)
        self.restrictions = []
        self.filledIn = False

    def addRestriction(self, character, idx, pointx, pointy):
        """
        Add a restriction to a word
        :param character: character to set the restriction on
        :param idx: the idx of the character in the word
        :param pointx: the coords of the character (intersection) on the board
        :param pointy:
        :return: none
        """
        self.restrictions.append((character, idx, Point(pointx, pointy)))

    def setWordStr(self, word_str):
        self.word = word_str
        self.filledIn = True

    def __str__(self):
        output = "word:"+ str(self.word) + " starting at:(" + str(self.point_start.getX()) + ", " + str(self.point_start.getY()) + "), ending at:("+ str(self.point_end.getX()) + ", " + str(self.point_end.getY()) + ")" \
        + ", restrictions:"
        for r in self.restrictions:
            output += ("char:" + str(r[0]) + ", idx:"+str(r[1]) + ", at:" + str(r[2]) + '\n')
        return output
