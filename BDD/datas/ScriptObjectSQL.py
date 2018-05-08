from listObject import listObject
from listRessource import listRessource
from listConsomable import listConsomable
from listArme import listArmes
from bdd import *
from sqlalchemy.sql import select


conn = engine.connect()
dict_categorie = {}
def addCategorie(nom):
    if nom in dict_categorie:
        return dict_categorie[nom]
    #on ajoute une ligne et retourne l'id

    for row in session.query(Categorie).filter(Categorie.nom == nom).all():
        dict_categorie[nom] = row
        return row
    cat = Categorie()
    cat.nom = nom
    session.add(cat)
    dict_categorie[nom] = cat
    return cat

def addListIngredient(liste_ingredient):
    """1xHuile de Sésame + 5xPince du Crabe
    5xPétale Diaphane + 5xOrtie + 5xEau Potable

    return a list a igredient in form [(quant, nom_ingredient)]
    ex :[(1, 'Huile de Sésame'), (5, 'Pince du Crabe')]
    """
    if(liste_ingredient is None):
        return []
    output = []
    for element in liste_ingredient.split("+"):
        parts = element.split("x")
        try:
            nbIngredient = int(parts[0])
        except:
            print("Element 0 is not a int \n %s \n %s"%(parts[0], element))
            return []
        nom = "x".join(parts[1:])
        if nom == "":
            print("nom is empty \n %s \n %s"%(parts[1:], element))
            return []
        if(nom.endswith(" ")):
            nom = nom[:-1] #pour retirer le " " en trop
        output.append((nbIngredient, nom))
    return output

def testParseListIngredient():
    print(addListIngredient("1xHuile de Sésame + 5xPince du Crabe"))
    print(addListIngredient("5xPétale Diaphane + 5xOrtie + 5xEau Potable"))

dict_metier = {}
def addMetier(nom):
    if nom in dict_metier:
        return dict_metier[nom]
    for row in session.query(Metier).filter(Metier.nom == nom).all():
        dict_metier[nom] = row
        return row
    met = Metier()
    met.nom = nom
    session.add(met)
    dict_metier[nom] = met
    return met

dictBonus = {} #(min_val, max_val, nom_element)-> Bonus
dictElement = {} # nomElement -> Element
def parseListBonus(phrase):
    # return a list of bonus in format : [Bonus]
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
        tupleBonus = (val_min,val_max,element)

        if tupleBonus in dictBonus:
            output.append(dictBonus[tupleBonus])
        else:
            bonus = BonusBase()
            bonus.val_min = val_min
            bonus.val_max = val_max
            if element in dictElement:
                obElement = dictElement[element]
            else:
                obElement = Element()
                obElement.nom = element
                session.add(obElement)
                session.commit()
                dictElement[element] = obElement
            bonus.element_id = obElement.id_
            session.add(bonus)
            output.append(bonus)
    return output

dictPanoplie = {}# nom -> panoplie.id_
def addPanoplie(nom):
    #reutrn panoplie.id_
    if nom in dictPanoplie:
        return dictPanoplie[nom]
    else:
        s = select([Panoplie]).where(Panoplie.nom == nom)
        for row in conn.execute(s):
            dictPanoplie[nom] = row.id_
            return row.id_
        pano = Panoplie()
        pano.nom = nom
        session.add(pano)
        session.commit()
        dictPanoplie[nom] = pano.id_
        return pano.id_

def testParseListBonus():
    print(parseListBonus("+21 à 30 Vitalité & +2 à 3 Soins & +16 à 25 Puissance & +1 Invocations"))
    print(parseListBonus("+31 à 50 Chance & +31 à 50 Intelligence & +201 à 250 Vitalité & +21 à 30 Sagesse & +6 à 10 Prospection & +6 à 10 Dommages & +6 à 10 Soins & +2 Invocations & +6 à 10% Résistance Neutre & +1 PM"))

dict_ingredient = {}
listIngredientToCraft = [] #l'ingredient, [(quant,ingreient)]

def parseIngredient(ing, nom, lvl, categorie, metier, liste_ingredient):
    ing.nom = nom
    ing.lvl = lvl
    ing.categorie = addCategorie(categorie)
    ing.metier = addMetier(metier)
    session.add(ing)
    dict_ingredient[ing.nom] = ing
    if liste_ingredient is not None:
        ing.craftable = True
        listIngredientToCraft.append((ing, addListIngredient(liste_ingredient)))
def parseConsomable():
    p=0
    for (id,id_item, id_image, nom, description, lvl, categorie, poids, liste_ingredient, metier, lvl_metier, dans_craft, drop_monstres) in listConsomable:
        res = Ressource()
        parseIngredient(res, nom, lvl, categorie, metier, liste_ingredient)
        if p%100 == 0:
            session.commit()
        print("%i consomable imported sur %i" %(p, len(listRessource)))
        p+=1
    session.commit()

def parseRessources():
    p = 0
    for (id,id_item, id_image, nom, description, lvl, categorie, poids, liste_ingredient, metier, lvl_metier, dans_craft, drop_monstres) in listRessource:
        res = Ressource()
        parseIngredient(res, nom, lvl, categorie, metier, liste_ingredient)
        if p%100 == 0:
            session.commit()
        print("%i ressource imported sur %i" %(p, len(listRessource)))
        p+=1
    session.commit()

def parseObjet():
    listOb = []
    p = 0
    for (id,id_item, id_image, nom, description, lvl, categorie, poids, liste_ingredient, metier, lvl_metier, dans_craft, drop_monstres,effets, critere, panoplie)  in (listObject + listArmes) :
        ob = Equipement()
        parseIngredient(ob,nom,lvl,categorie,metier, liste_ingredient)
        ob.boni = parseListBonus(effets)

        if panoplie is not None:
            ob.panoplie_id = addPanoplie(panoplie)
        if p%100 == 0:
            session.commit()
        print("%i objet imported sur %i" %(p, len(listObject)+ len(listArmes)))
        p+=1
    session.commit()

def setListIngredient():
    for p,(ingToCraft,listIng) in enumerate(listIngredientToCraft):
        for n ,(quant,ingRecette) in enumerate(listIng):
            if ingRecette in dict_ingredient:
                ing_id = dict_ingredient[ingRecette]
                setattr(ingToCraft, "ing_id_%i"%(n+1), ing_id)
                setattr(ingToCraft, "quant_%i"%(n+1), quant)
            else:
                print("Impossible de trouver l'id de l'ing %s"%ingRecette)
                print(dict_ingredient)
        session.commit()

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def addInSelect(nom, list):
    if nom.endswith(" "):
        nom = nom[:-1]
    list.append(nom)


def modifBDDDListIng(nom,liste_ingredient):
    #on fabrique une liste des ingredients consernes
    listIngToSelect = []
    addInSelect(nom,listIngToSelect)
    for quant, nomIngInCraft in addListIngredient(liste_ingredient):
        addInSelect(nomIngInCraft,listIngToSelect)
    dictIng = {}
    listIngToSelect = list(set(listIngToSelect))

    #on recupere les ingredients dans la base
    for ing in session.query(Ingredient).filter(Ingredient.nom.in_(listIngToSelect)).all():
        dictIng[ing.nom] = ing

    #on set la recette sur l'ingredient a crafter
    ingToCraft = dictIng[nom]
    for n,(quant, nomIngInCraft) in enumerate(addListIngredient(liste_ingredient)):
        ingInCraft = dictIng[nomIngInCraft]
        setattr(ingToCraft, "ing_id_%i"%(n+1), ingInCraft.id_)
        setattr(ingToCraft, "quant_%i"%(n+1), quant)



def setListIngredientParBDD():
    for (id,id_item, id_image, nom, description, lvl, categorie, poids, liste_ingredient, metier, lvl_metier, dans_craft, drop_monstres) in (listRessource + listConsomable):
        if(liste_ingredient):
            modifBDDDListIng(nom,liste_ingredient)

    for (id,id_item, id_image, nom, description, lvl, categorie, poids, liste_ingredient, metier, lvl_metier, dans_craft, drop_monstres,effets, critere, panoplie)  in (listObject + listArmes) :
        if(liste_ingredient):
            modifBDDDListIng(nom,liste_ingredient)








if __name__ == "__main__":
    #testParseListBonus()
    #testParseListIngredient()
    parseRessources()
    print("Parse Ressource Done")
    parseObjet()
    # print("Parse Objet Done")
    parseConsomable()
    setListIngredientParBDD()
    print("SetList Ingredient Done")
    session.commit()
