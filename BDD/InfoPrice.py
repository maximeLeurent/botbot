
class InfoPrice():
    def __init__(self, ing, quant):
        self.ing = ing
        self.quant = quant
        self.quant_hol = 0
        self.price_1 = None
        self.lastRefresh_1 = None
        self.price_10 = None
        self.lastRefresh_10 = None
        self.price_100 = None
        self.lastRefresh_100 = None
        self.smartQuantite = [0,0,0]
        self.smartPrice = 0

    def setQuantInvent(self, quant):
        self.quant_hol = quant

    def setSmartQuant(self,typeQuant, newQuant):
        #typeQuant = 0 -> quant_1 ,1->quant_10, 2 -> quant_100
        #newQuant -> the new smartQuantite
        self.smartQuantite[typeQuant] = newQuant
        self.__calculateSmartPrice()


    def __calculateSmartPrice(self):
        self.smartPrice = self.smartQuantite[0]* self.price_1 + self.smartQuantite[1] * self.price_10 + self.smartQuantite[2]*self.price_100

    def calculateSmartPrice(self, nbCraft):
        need_quant = self.quant*nbCraft - self.quant_hol
        quant_100 = int(need_quant/100)
        rest = need_quant-100*quant_100
        quant_10 = int(rest/10)
        quant_1 = rest - quant_10*10
        #pas de prix pour 1 et 10
        if(self.price_1 is None )and (self.price_10 is None):
            quant_1 = 0
            quant_10 = 0
            if(self.price_100 is None):
                #pas de prix pour 100 aussi on peut rien faire
                quant_100 = 0
                self.smartPrice = None
            else:
                #on achete que du 100
                quant_100 +=1
                self.smartPrice = quant_100*self.price_100
            self.smartQuantite = [quant_1,quant_10,quant_100]
            return

        if (self.price_1 is None) and self.price_10 is not None :
            #pas de prix 1, on se repli sur du 10
            quant_1 = 0
            quant_10 +=1

        if (self.price_10 is None and self.prive_100 is not None) :
            #pas de prix 10, on se repli sur du 100, du coup on achete pas de 1
            quant_0 = 0
            quant_10 = 0
            quant_100 +=1

        if (self.price_1 is not None) and (self.price_10 is not None) and (quant_1 * self.price_1 >= self.price_10) :
            #meilleur prix si on achete des 10 que des 1
            quant_1 = 0
            quant_10 +=1

        if (self.price_10 is not None) and (self.price_100 is not None) and (quant_10 * self.price_10 >= self.price_100) :
            #meilleur prix si on achete des 100 que des 10, du coup on achete pas de 1
            quant_1 = 0
            quant_10 = 0
            quant_100 +=1

        self.smartQuantite = [quant_1,quant_10,quant_100]
        self.__calculateSmartPrice()
