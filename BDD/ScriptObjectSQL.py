from listObject import listObject
#from bdd import session
#from sqlalchemy.sql import select


# conn = engine.connect()
# dict_categorie = {}
# def addCategorie(nom):
#     if nom in dict_categorie:
#         return dict_categorie[nom]
#     #on ajoute une ligne et retourne l'id
#     s = select([Categorie]).where(Categorie.nom == nom)
#     for row in conn.execute(s):
#         return row.id_
#     cat = Categorie()
#     cat.nom = nom
#     session.add(cat)
#     session.commit()
#     return cat.id_

# def addListIngredient(liste_ingredient):
#     #1xHuile de Sésame + 5xPince du Crabe
#     #5xPétale Diaphane + 5xOrtie + 5xEau Potable
#
#     #return a list a igredient in form [(quant, id_ingredient)]
#
#
#     return [(1, 'Huile de Sésame'), (5, 'Pince du Crabe')]
#
# dict_metier = {}
# def addMetier(nom):
#     if nom in dict_metier:
#         return dict_metier[nom]
#     s = select([Categorie]).where(Metier.nom == nom)
#     for row in conn.execute(s):
#         return row.id_
#     met = Metier()
#     met.nom = nom
#     session.add(met)
#     session.commit()
#     return met.id_

def parseListBonus(phrase):
    #+21 à 30 Vitalité & +2 à 3 Soins & +16 à 25 Puissance & +1 Invocations
    #+31 à 50 Chance & +31 à 50 Intelligence & +201 à 250 Vitalité & +21 à 30 Sagesse & +6 à 10 Prospection & +6 à 10 Dommages & +6 à 10 Soins & +2 Invocations & +6 à 10% Résistance Neutre & +1 PM'
    #
    # return a list of bonus in format : [(val_min,val_max, element_id),]
    if phrase is None:
        return []

    output = []
    for bonus in phrase.split("&"):
        pourcentage = False
        val = []
        listBonus = bonus.split()
        element = ''

        for part in listBonus:
            if part[-1] == '%' :
                part = part[:-1]
                element += '%'

            try:
                val.append(int(part))
            except:
                if part != 'à':
                    element += ' ' + part
        if len(val) == 0:
            print("\n Val is empty with the bonus \n %s \n in phrase \n %s " % (bonus, phrase))
            return []
        val_min = min(val)
        val_max = max(val)
        if element == "":
            print("\n element is empty with the bonus \n %s \n in phrase \n %s " % (bonus, phrase))
            return []
        output.append((val_min,val_max,element))
    return output
    # except:
    #     print("An error occured during parseListbonus with the phrase %s." % phrase)
    #     return []

def testParseListBonus():
    print(parseListBonus("+21 à 30 Vitalité & +2 à 3 Soins & +16 à 25 Puissance & +1 Invocations"))
    print(parseListBonus("+31 à 50 Chance & +31 à 50 Intelligence & +201 à 250 Vitalité & +21 à 30 Sagesse & +6 à 10 Prospection & +6 à 10 Dommages & +6 à 10 Soins & +2 Invocations & +6 à 10% Résistance Neutre & +1 PM"))


def parsesql():
    listOb = []
    for (id,id_item, id_image, nom, description, lvl, categorie, poids, liste_ingredient, metier, lvl_metier, dans_craft, drop_monstres,effets, critere, panoplie) in listObject :
        parseListBonus(effets)
        # ob = Equipement()
        # listOb.append(ob)
        # ob.nom = nom
        # ob.categorie_id = addCategorie(categorie)
        # ob.lvl = int(lvl)
        # ob.metier_id = addMetier(metier)
        #
        #
        # session.add(ob)
        # if len(listOb)%100 == 0:
        #     session.commit()


    #dans un second temp on ajoute les liste d'ingredient car avant on avait pas tous les id
    # for (id,id_item, id_image, nom, description, lvl, categorie, poids, liste_ingredient, metier, lvl_metier, dans_craft, drop_monstres,effets, critere, panoplie) in listObject[:5] :
    #     for n,(quant,ingredient_id) in addListIngredient(liste_ingredient):
    #         getattr(ob,"")


if __name__ == "__main__":
    #testParseListBonus()
    parsesql()
