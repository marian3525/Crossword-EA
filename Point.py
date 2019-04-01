class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def __str__(self):
        return "x=" + str(self.__x) + ", y=" + str(self.__y)
