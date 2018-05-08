#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import sqlalchemy
from sqlalchemy import Table,Column, Integer, String, Date,Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from PriceToStr import priceToStr

import datetime
Base = declarative_base()

categorieHDV = Table('categorieHDV', Base.metadata,
    Column('categorie_id', Integer, ForeignKey('categorie.id_')),
    Column('hdv_id', Integer, ForeignKey('hdv.id_'))
)
categorieAtelier = Table('categorieAtelier', Base.metadata,
    Column('categorie_id', Integer, ForeignKey('categorie.id_')),
    Column('atelier_id', Integer, ForeignKey('atelier.id_'))
)

class Categorie(Base):
    __tablename__ = "categorie"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(20))
    HDVs = relationship("HDV", secondary=categorieHDV, back_populates= "categories")
    ateliers = relationship("Atelier", secondary=categorieAtelier, back_populates= "categories")
    ingredients = relationship("Ingredient", back_populates= "categorie")

    def __str__(self):
        return self.nom

class ObjectFixe(Base):
    __tablename__ = "objectFixe"
    id_ = Column(Integer, primary_key=True)
    pos_id = Column(Integer, ForeignKey("position.id_"))
    pos = relationship("Position", back_populates = "objetsFixes")
    zone_id = Column(Integer, ForeignKey("zoneClick.id_"))
    zone = relationship("ZoneClick", foreign_keys = [zone_id],  back_populates = "objet")
    type = Column(String(10))
    __mapper_args__ = {
        'polymorphic_identity':'objectFixe',
        'polymorphic_on':type
    }

class ZoneClick(Base):
    __tablename__ = "zoneClick"
    id_ = Column(Integer, primary_key=True)
    topLeft = Column(Integer)
    buttomRight = Column(Integer)
    objet = relationship("ObjectFixe", back_populates="zone")

class AppareilCraft(ObjectFixe):
    """
    secondaryZone, sometime it is necessary to make a second click to open interface
    """
    __tablename__ = "appareilCraft"
    id_ = Column(Integer, ForeignKey("objectFixe.id_"),primary_key=True)
    job = Column(String(10))
    atelier_id = Column(Integer, ForeignKey("atelier.id_"))
    ateliers = relationship("Atelier", foreign_keys = [atelier_id],back_populates = "appareilsCraft")
    secondaryZone_id = Column(Integer, ForeignKey("zoneClick.id_"))
    secondaryZone = relationship("ZoneClick", foreign_keys = [secondaryZone_id],  back_populates = "objet")
    __mapper_args__ = {
        'polymorphic_identity':'appareilCraft'
    }
class Atelier(ObjectFixe):
    """
    la zone donne par Object Fixe est la porte d'entree
    """
    __tablename__ = "atelier"
    id_ = Column(Integer, ForeignKey("objectFixe.id_"),primary_key=True)
    ville = Column(String(20))
    outZoneClick_id = Column(Integer, ForeignKey("zoneClick.id_"))
    outZoneClick = relationship("ZoneClick", foreign_keys = [outZoneClick_id], back_populates = "objet")
    appareilsCraft = relationship("AppareilCraft",foreign_keys = [AppareilCraft.atelier_id], back_populates = "ateliers")
    categories = relationship("Categorie", secondary=categorieAtelier, back_populates= "ateliers")
    __mapper_args__ = {
        'polymorphic_identity':'atelier'
    }

class Zaap(ObjectFixe):
    __tablename__ = "zaap"
    id_ = Column(Integer, ForeignKey("objectFixe.id_"),primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'zaap'
    }

class HDV(ObjectFixe):
    __tablename__ = "hdv"
    id_ = Column(Integer, ForeignKey("objectFixe.id_"),primary_key=True)
    ville = Column(String(20))
    categories = relationship("Categorie",secondary=categorieHDV, back_populates= "HDVs")
    __mapper_args__ = {
        'polymorphic_identity':'hdv',
    }

    def __str__(self):
        return "%i;%i"%(self.xPos, self.yPos)

class Position(Base):
    __tablename__ = "position"
    id_ = Column(Integer, primary_key=True)
    xPos = Column(Integer)
    yPos = Column(Integer)
    objetsFixes = relationship("ObjectFixe", back_populates = "pos")

bonusBaseEquipement = Table('bonusBaseEquipement', Base.metadata,
    Column('equipement_id', Integer, ForeignKey('equipement.id_')),
    Column('bonus_id', Integer, ForeignKey('bonusBase.id_'))
)

class Ingredient(Base):
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
        'polymorphic_identity':'ressource',
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

class Panoplie(Base):
    __tablename__ = "panoplie"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))
    equipements = relationship("Equipement", back_populates= "panoplie")

    def __str__(self):
        return self.nom

class Metier(Base):
    __tablename__ = "metier"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))
    ingredients = relationship("Ingredient", back_populates= "metier")

    def __str__(self):
        return self.nom

class BonusBase(Base):
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

class Element(Base):
    __tablename__ = "element"
    id_ = Column(Integer, primary_key=True)
    nom = Column(String(50))

    def __str__(self):
        return self.nom

class Carac(Base):
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

class Prix(Base):
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

class Objet(Base):
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


def create():
    # Creating my base and my session
    engine = sqlalchemy.create_engine("sqlite:///my_db.db")#, echo='debug'
    Base.metadata.create_all(engine)

    DBsession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBsession()
    #createFakeVente(session)
    return engine, session
