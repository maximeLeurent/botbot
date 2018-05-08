from Queue import Queue
from threading import Thread

class Player(Thread):
    def __init__(self):
        self.queueOrder = Queue

    def orderAffinity(self, order):
        """
        return a value between 0 and 1.
        0 the players can't do the order.
        1 the players loves the order
        """
        return 1
