from time import time
from random import randint


class Indicator:
    def __init__(self, xp, message):
        self.xp = xp
        self.message = message
        self.start = int(time())

        self.colour = (randint(200, 255), randint(200, 255), randint(200, 255))
