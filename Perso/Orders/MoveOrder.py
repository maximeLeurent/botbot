

class MoveOrder(Order):
    def __init__(self, toDestination):
        super(MoveOrder, self).__init__()
        self.toDestination = toDestination
