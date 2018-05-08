from .Order import Order
from .MoveOrder import MoveOrder
from Perso.Position import Position

class BuyOrder(Order):

    def __init__(self, ingredient, quantite, price,ville,  tolerance = 0.1):
        super(BuyOrder, self).__init__()
        self.ingredient = ingredient
        self.quantite = quantite
        self.price = price
        self.tolerance = tolerance
        self.ville = ville


        for hdv in ingredient.categorie.HDVs:
            if hdv.ville == ville:
                self.hdv = hdv
                self.addPreSubOrder(MoveOrder(Position(hdv.xPos, hdv.yPos)))
