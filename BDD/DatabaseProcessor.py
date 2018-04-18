from .bdd import *
from .InfoPrice import InfoPrice

from sqlalchemy import and_

class DatabaseProcessor():
    def __init__(self):
        self.engine, self.session = create()

    def getListItemCraftable(self):
        return self.session.query(Equipement).filter(Equipement.craftable == True).all()

    def getCurrentPriceIngReceipt(self, ing):
        """
        Search in databse all the price relative to the receipt of ing
        return a list of InfoPrice containing info on the price of ingredient
        """
        output = []
        for ingReceipt, quant in ing.getListReceipt():
            infoPrice = InfoPrice(ingReceipt, quant)
            for i in [1,10,100]:
                if ingReceipt.type == "equipement":
                    price = self.session.query(PrixObjet).filter(and_(PrixObjet.objet_id == ingReceipt.id_, PrixObjet.en_cours, PrixObjet.quantite == i)).order_by(PrixObjet.val).first()
                    if(price is not None):
                        setattr(infoPrice, "price_%i"%i, price.val)
                        setattr(infoPrice, "lastRefresh_%i"%i, price.derniere_vue)

                else:
                    price = self.session.query(PrixRessource).filter(and_(PrixRessource.ressource_id == ingReceipt.id_, PrixRessource.en_cours, PrixRessource.quantite == i)).order_by(PrixRessource.val).first()
                    if(price is not None):
                        setattr(infoPrice, "price_%i"%i, price.val)
                        setattr(infoPrice, "lastRefresh_%i"%i, price.derniere_vue)
            output.append(infoPrice)
        return output

    def getListVente(self,ing, en_cours):
        for prix in self.session.query(PrixObjet).join(Objet).filter(and_(Objet.equipement_id == ing.id_, PrixObjet.en_cours == en_cours)).order_by(PrixObjet.val).all():
            print(type(prix))
        return self.session.query(PrixObjet).join(Objet).filter(and_(Objet.equipement_id == ing.id_, PrixObjet.en_cours == en_cours)).order_by(PrixObjet.val).all()
