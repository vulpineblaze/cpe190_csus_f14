# -*- coding: utf8 -*-

#-----------------------------------------------------------------
# This is a part of Pylote project.
# Author:       Pascal Peter
# Copyright:    (C) 2009-2014 Pascal Peter
# Licence:      GNU General Public Licence version 3
# Website:      http://pascal.peter.free.fr
# Email:        pascal.peter at free.fr
#-----------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------


"""
DESCRIPTION :
    Ce module contient les variables et fonctions utiles au programme.
    Certaines parties spécialisées sont dans les fichiers utils_aaa.py
"""

# importation des modules utiles :
import sys
import os

import utils

if utils.PYSIDE:
    from PySide import QtCore, QtGui, QtSvg
else:
    from PyQt4 import QtCore, QtGui, QtSvg



###########################################################"
###########################################################"
#   VARIABLES GLOBALES
###########################################################"
###########################################################"

# MAX_ZVALUE pour placer l'instrument sélectionné au premier plan
MAX_ZVALUE = 1
# IS_TRACING_ENABLED pour tracer avec le compas
IS_TRACING_ENABLED = False
# WITH_FALSE_CURSOR pour savoir si le "faux" curseur est actif
WITH_FALSE_CURSOR = False

# POINT_NAMES est la liste des noms disponibles pour les points
# elle est construite à partir de LETTERS
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
POINT_NAMES = []
for letter in LETTERS:
    POINT_NAMES.append(letter)


def changeTracingEnabled(newValue=None):
    global IS_TRACING_ENABLED
    if newValue == None:
        IS_TRACING_ENABLED = not(IS_TRACING_ENABLED)
    else:
        IS_TRACING_ENABLED = newValue

def changeFalseCursor(newValue):
    global WITH_FALSE_CURSOR
    WITH_FALSE_CURSOR = newValue

def changePointNames(value):
    # pour retirer une lettre de la liste POINT_NAMES
    global POINT_NAMES
    if value in POINT_NAMES:
        POINT_NAMES.pop(POINT_NAMES.index(value))






###########################################################"
###########################################################"
#                LES INSTRUMENTS DE GÉOMÉTRIE
###########################################################"
###########################################################"

class Instrument(QtSvg.QGraphicsSvgItem):
    """
    La classe de base pour un instrument de géométrie
    Les vrais instruments en dérivent
    """
    def __init__(self, parent, imageFile):
        QtSvg.QGraphicsSvgItem.__init__(self, imageFile)
        self.main = parent
        """
        MAX_ZVALUE sert à faire passer l'instrument au premier plan à la sélection
        imageFile passé en paramètre est l'image de l'instrument à afficher
        transformOriginPoint() est le centre pour les rotations (redéfinit pour chaque instrument)
        tracePoint est le point pour les trace (voir le compas)
        units si l'instrument a des graduations (règle et équerre)
        """
        self.setFlags(
            QtGui.QGraphicsItem.ItemIsSelectable|QtGui.QGraphicsItem.ItemIsMovable)
        self.updateZValue()
        self.tracePoint = QtCore.QPointF(0, 0)
        self.units = False
        self.A = None
        self.B = None

    def updateZValue(self):
        global MAX_ZVALUE
        MAX_ZVALUE += 1
        self.setZValue(MAX_ZVALUE)



class Protractor(Instrument):
    """
    Le Rapporteur. L'image doit être décalée pour que le centre du rapporteur soit en (0;0)
    transformOriginPoint() est donc redéfini ainsi
    """
    def __init__(self, parent):
        Instrument.__init__(self, parent, './images/instruments/rapporteur.svg')
        self.setObjectName('Protractor')
        x, y = self.boundingRect().width() // 2, self.boundingRect().height()
        self.setTransformOriginPoint(x, y)
        self.moveBy(- x, - y)
        self.setScale(0.75)

class Ruler(Instrument):
    """
    La règle. La graduation 0 doit être l'origine des rotations.
    transformOriginPoint() est donc redéfini ainsi
    """
    def __init__(self, parent):
        Instrument.__init__(self, parent, './images/instruments/regle.svg')
        self.setObjectName('Ruler')
        x = 20.4
        self.setTransformOriginPoint(x, 0)
        self.moveBy(- x, 0)
        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        scale = float(settings.value('instrumentsScale', 1))
        self.setScale(scale)
        self.units = True
        self.A = QtCore.QPointF(x, 0)
        self.B = QtCore.QPointF(730, 0)

class Square(Instrument):
    """
    L'équerre graduée.
    """
    def __init__(self, parent):
        Instrument.__init__(self, parent, './images/instruments/equerre.svg')
        self.setObjectName('Square')
        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        scale = float(settings.value('instrumentsScale', 1))
        self.setScale(scale)
        self.units = True
        self.A = QtCore.QPointF(10, 0)
        self.B = QtCore.QPointF(470, 0)

class SquareNotGraduated(Instrument):
    """
    L'équerre graduée.
    """
    def __init__(self, parent):
        Instrument.__init__(self, parent, './images/instruments/equerre_non_graduee.svg')
        self.setObjectName('SquareNotGraduated')
        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        self.A = QtCore.QPointF(10, 0)
        self.B = QtCore.QPointF(470, 0)

class Compass(Instrument):
    """
    Le compas doit pouvoir tracer des arcs si la variable globale IS_TRACING_ENABLED est à True.
    En fait on a besoin de 2 variables :
    
    IS_TRACING_ENABLED (variable globale) est à True quand la trace du compas est sélectionnée
        (outil sélectionné ou touche control maintenue)
    isTracing est à True quand le compas est en train de tracer
    
    On redéfinit donc les évènements souris
    transformOriginPoint() est redéfini sur la pointe du compas
    tracePoint est sur la mine
    """
    def __init__(self, parent):
        Instrument.__init__(self, parent, './images/instruments/compas.svg')
        self.setObjectName('Compass')
        x, y = self.boundingRect().width(), self.boundingRect().height()
        self.setTransformOriginPoint(0, y)
        self.moveBy(0, - y)
        self.tracePoint = QtCore.QPointF(x, y)
        self.isTracing = False





###########################################################"
###########################################################"

#                LE FAUX CURSEUR

###########################################################"
###########################################################"

class MyCursor(QtGui.QGraphicsPixmapItem):
    """
    Le "faux" curseur qui suit la souris (utile pour certains TBI ?).
    """
    def __init__(self, parent):
        QtGui.QGraphicsPixmapItem.__init__(self)
        self.main = parent

        newimage = QtGui.QImage('./images/cursor.png')
        self.setPixmap(QtGui.QPixmap.fromImage(newimage))
        
        centralPoint = QtCore.QPointF(-8, -8)
        self.setOffset(centralPoint)

        self.units = False
        self.setZValue(1000)










###########################################################"
###########################################################"

#                LES POINTS CRÉÉS PAR L'UTILISATEUR

###########################################################"
###########################################################"

class PointItem(QtGui.QGraphicsPathItem):
    """
    Un point et son label.
    C'est un QGraphicsPathItem qui contient le dessin du point (path)
        et un label (QGraphicsTextItem)
    """
    def __init__(self, parent, pen, brush, font, text=''):
        QtGui.QGraphicsPathItem.__init__(self)
        self.main = parent
        self.setFlags(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        self.setPen(pen)
        self.setBrush(brush)
        self.font = font
        self.text = text
        self.path = QtGui.QPainterPath()
        self.path.moveTo(QtCore.QPointF(-8, -8))
        self.path.lineTo(QtCore.QPointF(8, 8))
        self.path.moveTo(QtCore.QPointF(-8, 8))
        self.path.lineTo(QtCore.QPointF(8, -8))
        self.setPath(self.path)
        self.textItem = QtGui.QGraphicsTextItem(text, self)
        self.textItem.setFont(font)
        self.textItem.setDefaultTextColor(pen.color())
        self.textItem.setPos(QtCore.QPointF(8, -32))  
        self.textItem.setTransformOriginPoint(
            self.textItem.boundingRect().center())

    def chooseText(self, pen, brush, font):
        """
        pour choisir le texte à la création du point.
        """
        try:
            proposedText = POINT_NAMES[0]
        except:
            proposedText = ''
        text, ok = QtGui.QInputDialog.getText(
            self.main,
            utils.PROGLABEL,
            QtGui.QApplication.translate('main', 'Point Name:'),
            QtGui.QLineEdit.Normal,
            proposedText)
        if ok:
            self.text = text
            changePointNames(text)
            self.textItem = QtGui.QGraphicsTextItem(text, self)
            self.textItem.setFont(font)
            self.textItem.setDefaultTextColor(pen.color())
            self.textItem.setPos(QtCore.QPointF(8, -32))
            self.textItem.setTransformOriginPoint(
                self.textItem.boundingRect().center())
        return ok



