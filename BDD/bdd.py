#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import sqlalchemy
from sqlalchemy import Table,Column, Integer, String, Date,Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()

class Categorie(base):
    __tablename__ = "categorie"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(20))
    HDVs = relationship("HDV", back_populates= "categorie")
    ingredients = relationship("Ingredient", back_populates= "categorie")

class HDV(base):
    __tablename__ = "hdv"
    id_ = Column(Integer, primary_key=True)
    xPos = Column(Integer)
    yPos = Column(Integer)
    ville = Column(String(20))
    categorie_id = Column(Integer, ForeignKey("categorie.id_"))
    categorie = relationship("Categorie", back_populates= "HDVs")


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
    quant_1 = Column(Integer)
    ing_id_2 = Column(Integer, ForeignKey("ingredient.id_"))
    quant_2 = Column(Integer)
    ing_id_3 = Column(Integer,ForeignKey("ingredient.id_"))
    quant_3 = Column(Integer)
    ing_id_4 = Column(Integer,ForeignKey("ingredient.id_"))
    quant_4 = Column(Integer)
    ing_id_5 = Column(Integer,ForeignKey("ingredient.id_"))
    quant_5 = Column(Integer)
    ing_id_6 = Column(Integer,ForeignKey("ingredient.id_"))
    quant_6 = Column(Integer)
    ing_id_7 = Column(Integer,ForeignKey("ingredient.id_"))
    quant_7 = Column(Integer)
    ing_id_8 = Column(Integer,ForeignKey("ingredient.id_"))
    quant_8 = Column(Integer)
    metier_id = Column(Integer,ForeignKey("metier.id_"))
    metier = relationship("Metier",back_populates="ingredients")
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity':'ingredient',
        'polymorphic_on':type
    }


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
    __mapper_args__ = {
        'polymorphic_identity':'ingredient',
    }

class Panoplie(base):
    __tablename__ = "panoplie"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))
    equipements = relationship("Equipement", back_populates= "panoplie")

class Metier(base):
    __tablename__ = "metier"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))
    ingredients = relationship("Ingredient", back_populates= "metier")

class BonusBase(base):
    __tablename__ = "bonusBase"
    id_ = Column(Integer, primary_key=True)
    val_min = Column(Integer)
    val_max = Column(Integer)
    element_id = Column(Integer, ForeignKey("element.id_"))
    equipements = relationship(
        "Equipement",
        secondary=bonusBaseEquipement,
        back_populates="boni")

class Element(base):
    __tablename__ = "element"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))

class Carac(base):
    __tablename__ = "carac"
    id_ = Column(Integer, primary_key=True)
    val = Column(Integer)
    element_id = Column(Integer, ForeignKey("element.id_"))
    element = relationship("Element")
    objet_id = Column(Integer, ForeignKey('objet.id_'))
    objet = relationship("Objet",  back_populates="caracs")

class Prix(base):
    __tablename__ = "prix"
    id_ = Column(Integer, primary_key=True)
    val = Column(Integer)
    premiere_vue = Column(Date)
    derniere_vue = Column(Date)
    en_cours = Column(Boolean)
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity':'prix',
        'polymorphic_on':type
    }

class PrixObjet(Prix):
    __tablename__ = "prixObjet"
    id_ = Column(Integer, ForeignKey("prix.id_"),primary_key=True)
    objet_id = Column(Integer, ForeignKey('objet.id_'))
    objet = relationship("Objet",  back_populates="prixs")
    __mapper_args__ = {
        'polymorphic_identity':'prix',
    }

class PrixRessource(Prix):
    __tablename__ = "prixRessource"
    id_ = Column(Integer, ForeignKey("prix.id_"), primary_key=True)
    quantite = Column(Integer)
    ressource_id = Column(Integer, ForeignKey('ressource.id_'))
    ressources = relationship("Ressource",  back_populates="prixs")
    __mapper_args__ = {
        'polymorphic_identity':'prix',
    }

class Objet(base):
    #vrai objet du jeu
    __tablename__ = "objet"
    id_ = Column(Integer, primary_key=True)
    equipement_id =  Column(Integer, ForeignKey('equipement.id_'))
    caracs = relationship("Carac", back_populates= "objet")
    prixs = relationship("PrixObjet", back_populates= "objet")
    a_moi = Column(Boolean)





# Creating my base and my session
engine = sqlalchemy.create_engine("sqlite:///my_db.db")#, echo='debug'
base.metadata.create_all(engine)

DBsession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBsession()
