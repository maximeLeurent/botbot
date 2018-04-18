#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import sqlalchemy
from sqlalchemy import Table,Column, Integer, String, Date,Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from PriceToStr import priceToStr

import datetime
base = declarative_base()

class Categorie(base):
    __tablename__ = "categorie"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(20))
    HDVs = relationship("HDV", back_populates= "categorie")
    ingredients = relationship("Ingredient", back_populates= "categorie")

    def __str__(self):
        return self.nom

class HDV(base):
    __tablename__ = "hdv"
    id_ = Column(Integer, primary_key=True)
    xPos = Column(Integer)
    yPos = Column(Integer)
    ville = Column(String(20))
    categorie_id = Column(Integer, ForeignKey("categorie.id_"))
    categorie = relationship("Categorie", back_populates= "HDVs")

    def __str__(self):
        return "%i;%i"%(self.xPos, self.yPos)


bonusBaseEquipement = Table('bonusBaseEquipement', base.metadata,
    Column('equipement_id', Integer, ForeignKey('equipement.id_')),
    Column('bonus_id', Integer, ForeignKey('bonusBase.id_'))
)

class Ingredient(base):
    __tablename__ = "ingredient"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))
    categorie_id = Column(Integer, ForeignKey("categorie.id_"))
    categorie = relationship("Categorie", back_populates= "ingredients")
    lvl = Column(Integer)
    craftable = Column(Boolean)

    ing_id_1 = Column(Integer,ForeignKey("ingredient.id_"))
    ing_1 = relationship("Ingredient", foreign_keys = [ing_id_1], remote_side= id_ )
    quant_1 = Column(Integer)

    ing_id_2 = Column(Integer, ForeignKey("ingredient.id_"))
    ing_2 = relationship("Ingredient", foreign_keys = [ing_id_2], remote_side= id_  )
    quant_2 = Column(Integer)

    ing_id_3 = Column(Integer,ForeignKey("ingredient.id_"))
    ing_3 = relationship("Ingredient", foreign_keys = [ing_id_3], remote_side= id_  )
    quant_3 = Column(Integer)

    ing_id_4 = Column(Integer,ForeignKey("ingredient.id_"))
    ing_4 = relationship("Ingredient", foreign_keys = [ing_id_4], remote_side= id_  )
    quant_4 = Column(Integer)

    ing_id_5 = Column(Integer,ForeignKey("ingredient.id_"))
    ing_5 = relationship("Ingredient", foreign_keys = [ing_id_5], remote_side= id_  )
    quant_5 = Column(Integer)

    ing_id_6 = Column(Integer,ForeignKey("ingredient.id_"))
    ing_6 = relationship("Ingredient", foreign_keys = [ing_id_6], remote_side= id_  )
    quant_6 = Column(Integer)

    ing_id_7 = Column(Integer,ForeignKey("ingredient.id_"))
    ing_7 = relationship("Ingredient", foreign_keys = [ing_id_7], remote_side= id_  )
    quant_7 = Column(Integer)

    ing_id_8 = Column(Integer,ForeignKey("ingredient.id_"))
    ing_8 = relationship("Ingredient", foreign_keys = [ing_id_8], remote_side= id_  )
    quant_8 = Column(Integer)
    metier_id = Column(Integer,ForeignKey("metier.id_"))
    metier = relationship("Metier",back_populates="ingredients")
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity':'ingredient',
        'polymorphic_on':type
    }
    def __str__(self):
        return self.nom

    def getListReceipt(self):
        """
        yield tuples of the receipt (ing,quant)
        """
        for n in range(1,9):
            if getattr(self , "ing_id_%i"%n) is None:
                break
            else:
                yield (getattr(self , "ing_%i"%n),getattr(self , "quant_%i"%n))

class Ressource(Ingredient):
    __tablename__ = "ressource"
    id_ = Column(Integer, ForeignKey("ingredient.id_"),primary_key=True)
    prixs = relationship("PrixRessource", back_populates= "ressources")
    __mapper_args__ = {
        'polymorphic_identity':'ingredient',
    }

class Equipement(Ingredient):
    #categorie d'objet
    __tablename__ = "equipement"
    id_ = Column(Integer, ForeignKey("ingredient.id_"),primary_key=True)
    boni = relationship("BonusBase",secondary=bonusBaseEquipement, back_populates= "equipements")
    panoplie_id = Column(Integer,ForeignKey("panoplie.id_"))
    panoplie = relationship("Panoplie", back_populates="equipements")
    objets = relationship("Objet", back_populates = "equipement")
    __mapper_args__ = {
        'polymorphic_identity':'ingredient',
    }

class Panoplie(base):
    __tablename__ = "panoplie"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))
    equipements = relationship("Equipement", back_populates= "panoplie")

    def __str__(self):
        return self.nom

class Metier(base):
    __tablename__ = "metier"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))
    ingredients = relationship("Ingredient", back_populates= "metier")

    def __str__(self):
        return self.nom

class BonusBase(base):
    __tablename__ = "bonusBase"
    id_ = Column(Integer, primary_key=True)
    val_min = Column(Integer)
    val_max = Column(Integer)
    element_id = Column(Integer, ForeignKey("element.id_"))
    element = relationship("Element")
    equipements = relationship(
        "Equipement",
        secondary=bonusBaseEquipement,
        back_populates="boni")

    def __str__(self):
        if self.val_min  <0:
            color = "red"
        else:
            color = "black"
        if (self.val_min == self.val_max):
            return "<font color=%s>%i en %s</font>" %(color,self.val_min,self.element.nom)
        return "<font color=%s>%i à %i en %s</font>" %(color,self.val_min,self.val_max,self.element.nom)


class Element(base):
    __tablename__ = "element"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))

    def __str__(self):
        return self.nom

class Carac(base):
    __tablename__ = "carac"
    id_ = Column(Integer, primary_key=True)
    val = Column(Integer)
    element_id = Column(Integer, ForeignKey("element.id_"))
    element = relationship("Element")
    objet_id = Column(Integer, ForeignKey('objet.id_'))
    objet = relationship("Objet",  back_populates="caracs")

    def __str__(self):
        if self.val  <0:
            color = "red"
        else:
            color = "black"
        return "<font color=%s>%i en %s</font>" %(color,self.val,self.element.nom)

class Prix(base):
    __tablename__ = "prix"
    id_ = Column(Integer, primary_key=True)
    val = Column(Integer)
    premiere_vue = Column(Date)
    derniere_vue = Column(Date)
    en_cours = Column(Boolean)
    quantite = Column(Integer)
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity':'prix',
        'polymorphic_on':type
    }

    def __str__(self):
        return priceToStr(self.val)

class PrixObjet(Prix):
    __tablename__ = "prixObjet"
    id_ = Column(Integer, ForeignKey("prix.id_"),primary_key=True)
    objet_id = Column(Integer, ForeignKey('objet.id_'))
    objet = relationship("Objet",  back_populates="prixs")
    __mapper_args__ = {
        'polymorphic_identity':'prixObjet',
    }

class PrixRessource(Prix):
    __tablename__ = "prixRessource"
    id_ = Column(Integer, ForeignKey("prix.id_"), primary_key=True)
    ressource_id = Column(Integer, ForeignKey('ressource.id_'))
    ressources = relationship("Ressource",  back_populates="prixs")
    __mapper_args__ = {
        'polymorphic_identity':'prixRessource',
    }

class Objet(base):
    #vrai objet du jeu
    __tablename__ = "objet"
    id_ = Column(Integer, primary_key=True)
    equipement_id =  Column(Integer, ForeignKey('equipement.id_'))
    equipement = relationship("Equipement", back_populates = "objets")
    caracs = relationship("Carac", back_populates= "objet")
    prixs = relationship("PrixObjet", back_populates= "objet")
    a_moi = Column(Boolean)

    def __str__(self):
        return self.equipement.nom

def createFakePrice(session):
    """
    add price for item anneau de sagesse
    """
    pr = PrixRessource( val = 111,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 1,
            ressource_id = 2603)
    session.add(pr)
    pr1 = PrixRessource( val = 10,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 10,
            ressource_id = 2603)
    session.add(pr1)
    pr3 = PrixRessource( val = 10023,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 100,
            ressource_id = 2603)
    session.add(pr3)

    pr4 = PrixRessource( val = 1,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 1,
            ressource_id = 2600)
    session.add(pr4)
    pr5 = PrixRessource( val = 10,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 10,
            ressource_id = 2600)
    session.add(pr5)
    pr6 = PrixRessource( val = 100,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 100,
            ressource_id = 2600)
    session.add(pr6)
    session.commit()

def createFakeVente(session):
    car = Carac(val = 5, element_id = 7)
    ob = Objet(equipement_id = 3111,caracs = [car], a_moi = False)
    po = PrixObjet(val = 100,
            premiere_vue = datetime.datetime(2018,4,16),
            derniere_vue = datetime.datetime.now(),
            en_cours = True,
            quantite = 1,
            objet = ob)

    car1 = Carac(val = 4, element_id = 7)
    ob1 = Objet(equipement_id = 3111,caracs = [car1], a_moi = False)
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

def create():
    # Creating my base and my session
    engine = sqlalchemy.create_engine("sqlite:///my_db.db")#, echo='debug'
    base.metadata.create_all(engine)

    DBsession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBsession()
    #createFakeVente(session)
    return engine, session
