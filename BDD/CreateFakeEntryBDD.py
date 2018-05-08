from .bdd import *

def createFakeIngredient(session):
    cat1 = Categorie(nom = "os")
    res1 = Ressource(nom = "Tete de mort",
                     categorie = cat1,
                     lvl =5,
                     craftable = False )

    cat2 = Categorie(nom = "poudre")
    res2 = Ressource(nom = "poudre de perlinpinpin",
                     categorie = cat2,
                     lvl =50,
                     craftable = False )

    el = Element(nom = "Intelligence")
    bonus = BonusBase(val_min = 1, val_max = 5, element = el)

    cat3 = Categorie(nom = "coiffe")
    res3 = Equipement(nom = "Coiffe super forte",
                     categorie = cat3,
                     lvl =50,
                     craftable = True,
                     ing_1 = res1,
                     quant_1 = 10,
                     ing_2 = res2,
                     quant_2 = 5,
                     boni = [bonus] )

    session.add(res3)

def createFakePrice(session):
    """
    add price for item anneau de sagesse
    """
    pr = PrixRessource( val = 111,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 1,
            ressource_id = 1)
    session.add(pr)
    pr1 = PrixRessource( val = 10,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 10,
            ressource_id = 1)
    session.add(pr1)
    pr3 = PrixRessource( val = 10023,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 100,
            ressource_id = 1)
    session.add(pr3)

    pr4 = PrixRessource( val = 1,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 1,
            ressource_id = 2)
    session.add(pr4)
    pr5 = PrixRessource( val = 10,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 10,
            ressource_id = 2)
    session.add(pr5)
    pr6 = PrixRessource( val = 100,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 100,
            ressource_id = 2)
    session.add(pr6)
    session.commit()

def createFakeVente(session):
    car = Carac(val = 5, element_id = 1)
    ob = Objet(equipement_id = 3,caracs = [car], a_moi = False)
    po = PrixObjet(val = 100,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 1,
            objet = ob)

    car1 = Carac(val = 4, element_id = 1)
    ob1 = Objet(equipement_id = 3,caracs = [car1], a_moi = False)
    po1 = PrixObjet(val = 200,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 1,
            objet = ob1)
    session.add(car)
    session.add(ob)
    session.add(po)
    session.add(car1)
    session.add(ob1)
    session.add(po1)
    session.commit()

def createAllFakeEntry(session):
    createFakeIngredient(session)
    createFakePrice(session)
    createFakeVente(session)
