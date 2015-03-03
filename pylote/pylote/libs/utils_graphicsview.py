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
    La zone d'affichage (GraphicsView).
    Affiche l'image de fond et les items.
"""

# importation des modules utiles :
from __future__ import division, print_function

import utils, utils_dialogs, utils_instruments

if utils.PYSIDE:
    from PySide import QtCore, QtGui, QtSvg
else:
    from PyQt4 import QtCore, QtGui, QtSvg








"""
###########################################################
###########################################################

                LE GRAPHICSVIEW : ZONE D'AFFICHAGE

###########################################################
###########################################################
"""

class GraphicsView(QtGui.QGraphicsView):
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        
        # on récupère main (fenêtre principale)
        self.main = parent
        # pas d'ascenseurs
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        scene = QtGui.QGraphicsScene(self)
        scene.setSceneRect(0, 0, 1, 1)
        # je n'ai pas compris pourquoi mais il faut créer puis supprimer 
        # un premier item pour que mouseMoveEvent fonctionne dès le début
        # (nécessaire si on utilise le faux curseur) :
        item = QtGui.QGraphicsTextItem()
        scene.addItem(item)
        scene.removeItem(item)
        del item
        self.setScene(scene)

        # les éléments de dessin utiles :
        self.pens = []
        for i in range(5):
            newPen = QtGui.QPen(
                QtCore.Qt.black, 1,
                QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                QtCore.Qt.RoundJoin)
            self.pens.append(newPen)
        self.drawPen = self.pens[0]
        self.path = QtGui.QPainterPath()
        self.font = QtGui.QFont()
        self.drawId = -1

        # les différents curseurs affichés sur les objets :
        self.CURSORS = {
            0: 'ARROW',
            1: 'MOVE',
            2: 'ROTATE',
            3: 'SCALE',
            4: 'TRACE',
            'NOTHING': QtCore.Qt.BlankCursor,
            'ARROW': QtCore.Qt.ArrowCursor,
            'CROSS': QtCore.Qt.CrossCursor,
            'MOVE': QtGui.QCursor(QtGui.QPixmap('./images/transform-move.png')),
            'ROTATE': QtGui.QCursor(QtGui.QPixmap('./images/transform-rotate.png')),
            'SCALE': QtGui.QCursor(QtGui.QPixmap('./images/transform-scale.png')),
            'TRACE': QtGui.QCursor(QtGui.QPixmap('./images/transform-trace.png')),
            }
        # état de la sélection (pour gérer les actions à effectuer) :
        self.state = {
            'mouseEvent': '',
            'mouseAction': '',
            'mouseButton': QtCore.Qt.NoButton,
            'mousePos': None,
            'selected': None,
            'cursorIndex': 0,
            'transform': '',
            'instrumentName': '',
            'locked': False,
            'attachInstrument': None,
            'lastPoint': QtCore.QPointF(),
            }
        self.changeCursor()

    def changeCursor(self, newCursor='ARROW'):
        if utils_instruments.WITH_FALSE_CURSOR:
            newCursor = 'NOTHING'
        self.setCursor(self.CURSORS[newCursor])
        self.viewport().setCursor(self.CURSORS[newCursor])

    def mousePressEvent(self, event):
        """
        On veut distinguer le clic du double-clic et du tracé (mouseMove).
        Ici, on met les variables mouseRelease et doubleClick à False,
            et on retarde la gestion du simple clic à la fonction doMouseClick.
        Entre temps, si c'est un double-clic, la variable doubleClick sera devenue True
            et si un événement mouseRelease a eu lieu, mouseRelease sera devenue True.
        Enfin firstMouseMove sert à initialiser un événement mouseMove.
        """
        super(GraphicsView, self).mousePressEvent(event)
        self.state['mouseEvent'] = 'mousePress'
        self.state['mouseAction'] = ''
        self.state['mouseButton'] = event.button()
        self.state['mousePos'] = self.mapToScene(event.pos())
        self.state['transform'] = ''
        self.state['instrumentName'] = ''
        try:
            self.state['selected'].setCursor(self.CURSORS['MOVE'])
            self.state['selected'].unsetCursor()
        except:
            pass

        if len(self.scene().selectedItems()) > 0:
            selected = self.scene().selectedItems()[0]
            isInstrument = isinstance(selected, utils_instruments.Instrument)
            mustDo = False
            if self.main.drawingMode[0] == 'SELECT':
                mustDo = True
            elif isInstrument:
                mustDo = True
            if mustDo:
                self.state['mouseAction'] = 'editing'
                if selected != self.state['selected']:
                    if self.state['selected'] != None:
                        self.state['selected'].unsetCursor()
                    self.state['selected'] = selected
                    selected.setCursor(self.CURSORS['MOVE'])
                    isMovable = True
                    if isInstrument:
                        self.state['instrumentName'] = selected.objectName()
                        selected.updateZValue()
                        if self.state['locked']:
                            isMovable = False
                    if isMovable:
                        selected.setFlags(
                            QtGui.QGraphicsItem.ItemIsSelectable|QtGui.QGraphicsItem.ItemIsMovable)
                    else:
                        selected.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
                    self.state['cursorIndex'] = 0
                elif isInstrument:
                    self.state['instrumentName'] = selected.objectName()
                    if self.state['locked']:
                        selected.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
                    else:
                        selected.setFlags(
                            QtGui.QGraphicsItem.ItemIsSelectable|QtGui.QGraphicsItem.ItemIsMovable)
                if self.state['mouseButton'] == QtCore.Qt.RightButton:
                    self.state['transform'] = 'ROTATE'
                    if (self.state['instrumentName'] == 'Compass') \
                        and (utils_instruments.IS_TRACING_ENABLED):
                            selected.setCursor(self.CURSORS['TRACE'])
                    else:
                        selected.setCursor(self.CURSORS['ROTATE'])
                    self.state['cursorIndex'] = 2
                elif self.state['mouseButton'] == QtCore.Qt.MiddleButton:
                    self.state['transform'] = 'SCALE'
                    selected.setCursor(self.CURSORS['SCALE'])
                    self.state['cursorIndex'] = 3
        elif self.main.drawingMode[0] == 'SELECT':
            if self.state['selected'] != None:
                self.state['selected'].unsetCursor()
                self.state['selected'] = None
        elif self.main.drawingMode[0] != 'NO':
            self.state['mouseAction'] = 'drawing'
        # en dessous de 300, ça foire :
        QtCore.QTimer.singleShot(300, self.doMouseClick)

    def mouseDoubleClickEvent(self, event):
        """
        On met la variable doubleClick à True, pour ne pas executer 
            la procédure liée au simple clic.
        Si le double-clic est fait sur un texte ou le label d'un point,
            il permet de l'éditer.
        Sinon, il permet de cacher/afficher la barre d'outils.
        """
        super(GraphicsView, self).mouseDoubleClickEvent(event)
        self.state['mouseEvent'] = 'mouseDoubleClick'
        if self.state['instrumentName'] == 'Compass':
            utils_instruments.changeTracingEnabled()
        elif self.main.editText() == False:
            if not(self.main.toolsWindow.toolsKidMode):
                if self.main.toolsWindow.isVisible():
                    self.main.doMinimizeToolsWindow()
                else:
                    self.main.doRestoreToolsWindow()

    def doMouseClick(self):
        """
         On vérifie d'abord que c'est bien un simple clic
            (variables doubleClick et mouseRelease).
         Gestion des différents cas possibles 
            (ajout d'un texte, début d'un tracé, ...)
        """
        if self.state['mouseEvent'] == 'mouseDoubleClick':
            return
        elif self.state['mouseEvent'] != 'mouseRelease':
            self.state['mouseEvent'] = 'firstMouseMove'
            return
        self.state['mouseEvent'] = 'mouseClick'

        if self.state['mouseAction'] == 'editing':
            selected = self.state['selected']
            self.state['cursorIndex'] += 1
            if self.state['cursorIndex'] == 4:
                self.state['cursorIndex'] = 1
            if (self.state['cursorIndex'] == 2) \
                and (self.state['instrumentName'] == 'Compass') \
                and (utils_instruments.IS_TRACING_ENABLED):
                    self.state['selected'].setCursor(self.CURSORS['TRACE'])
            else:
                self.state['selected'].setCursor(
                    self.CURSORS[self.CURSORS[self.state['cursorIndex']]])
            isMovable = (self.state['cursorIndex'] == 1)
            if (self.state['instrumentName'] != '') and self.state['locked']:
                isMovable = False
            if isMovable:
                self.state['selected'].setFlags(
                    QtGui.QGraphicsItem.ItemIsSelectable|QtGui.QGraphicsItem.ItemIsMovable)
            else:
                self.state['selected'].setFlags(
                    QtGui.QGraphicsItem.ItemIsSelectable)
        elif self.state['mouseAction'] == 'drawing':
            point = self.state['mousePos']
            self.doDrawing(point)

    def mouseMoveEvent(self, event):
        """
        D'une part, si on trace une courbe, on met à jour.
        D'autre part, on vérifie quel curseur est affiché (y compris le faux)
        """
        super(GraphicsView, self).mouseMoveEvent(event)

        if utils_instruments.WITH_FALSE_CURSOR:
            point = self.mapToScene(event.pos())
            self.main.myCursor.setPos(point.x(), point.y())

        if self.state['mouseEvent'] == 'firstMouseMove':
            # pour ne calculer qu'une seule fois :
            if self.state['mouseAction'] == 'editing':
                self.state['transform'] = self.CURSORS[self.state['cursorIndex']]
                if self.state['selected'] != None:
                    point = self.state['selected'].mapFromScene(self.state['mousePos'])
                    self.doTransform(point)
            elif self.state['mouseAction'] == 'drawing':
                point = self.state['mousePos']
                self.doDrawing(point)
            else:
                self.state['transform'] = ''
            self.state['mouseEvent'] = 'mouseMove'
        elif self.state['mouseEvent'] == 'mouseMove':
            if self.state['mouseAction'] == 'editing':
                if self.state['selected'] != None:
                    point = self.state['selected'].mapFromScene(self.mapToScene(event.pos()))
                    self.doTransform(point)
            elif self.state['mouseAction'] == 'scribbling':
                point = self.mapToScene(event.pos())
                self.doDrawing(point)

    def mouseReleaseEvent(self, event):
        """
        On termine l'éventuel tracé
        """
        super(GraphicsView, self).mouseReleaseEvent(event)
        if self.state['mouseEvent'] == 'mouseDoubleClick':
            return
        self.state['mouseEvent'] = 'mouseRelease'
        if self.state['mouseAction'] == 'editing':
            self.doTransform()
        elif self.state['mouseAction'] == 'scribbling':
            point = self.mapToScene(event.pos())
            self.doDrawing(point)

    def doTransform(self, point=None):
        mouseEvent = self.state['mouseEvent']
        if mouseEvent == 'firstMouseMove':
            center = self.state['selected'].transformOriginPoint()
            rayon = QtCore.QLineF(center, point)
            self.initialLength = rayon.length()
            if self.initialLength < 1:
                self.initialLength = 1
            self.initialAngle = rayon.angle()
            # cas du tracé au compas :
            if (self.state['cursorIndex'] == 2) \
                and (self.state['instrumentName'] == 'Compass') \
                and (utils_instruments.IS_TRACING_ENABLED):
                    self.last = None
                    center = self.state['selected'].mapToScene(center)
                    point = self.state['selected'].mapToScene(self.state['selected'].tracePoint)
                    self.initArc(center, point)
                    self.state['selected'].isTracing = True
        elif mouseEvent == 'mouseMove':
            if (self.state['instrumentName'] != '') and self.state['locked']:
                return
            center = self.state['selected'].transformOriginPoint()
            rayon = QtCore.QLineF(center, point)
            length = rayon.length()
            if length < 1:
                length = 1
            angle = rayon.angle()
            if self.state['transform'] == 'ROTATE':
                self.state['selected'].setRotation(
                    self.state['selected'].rotation() + self.initialAngle - angle)
                # cas du tracé au compas :
                if (self.state['instrumentName'] == 'Compass'):
                    if self.state['selected'].isTracing:
                        self.last = None
                        center = self.state['selected'].mapToScene(center)
                        point = self.state['selected'].mapToScene(self.state['selected'].tracePoint)
                        self.drawArcTo(center, point)
                        if not utils_instruments.IS_TRACING_ENABLED:
                            self.state['selected'].isTracing = False
                    elif utils_instruments.IS_TRACING_ENABLED:
                        self.last = None
                        center = self.state['selected'].mapToScene(center)
                        point = self.state['selected'].mapToScene(self.state['selected'].tracePoint)
                        self.initArc(center, point)
                        self.state['selected'].isTracing = True
            elif self.state['transform'] == 'SCALE':
                mustDo = True
                if self.state['instrumentName'] != '':
                    if self.state['selected'].units \
                        and self.main.toolsWindow.actionUnitsLock.isChecked():
                            mustDo = False
                if mustDo:
                    coeff = length / self.initialLength
                    self.state['selected'].setScale(self.state['selected'].scale() * coeff)
        elif mouseEvent == 'mouseRelease':
            self.state['transform'] = ''
            # cas du tracé au compas :
            if (self.state['cursorIndex'] == 2) \
                and (self.state['instrumentName'] == 'Compass') \
                and (utils_instruments.IS_TRACING_ENABLED):
                    self.last = None
                    center = self.state['selected'].mapToScene(
                        self.state['selected'].transformOriginPoint())
                    point = self.state['selected'].mapToScene(
                        self.state['selected'].tracePoint)
                    item = self.drawArcTo(center, point)
                    self.state['selected'].isTracing = False
                    self.drawId += 1
                    item.setData(QtCore.Qt.UserRole, self.drawId)
            # si on avait transformé l'objet avec le bouton droit ou la molette,
            # on remet l'état en "move" :
            if self.state['mouseButton'] in (QtCore.Qt.RightButton, QtCore.Qt.MiddleButton):
                if self.state['selected'] != None:
                    self.state['selected'].setCursor(self.CURSORS['MOVE'])
                    self.state['cursorIndex'] = 1
            self.main.saveTempFile()

    def doDrawing(self, point):
        mouseEvent = self.state['mouseEvent']
        if mouseEvent == 'mouseClick':
            self.state['attachInstrument'] = None
            if self.main.drawingMode[0] in ('POINT',):
                for instrument in self.main.listeInstruments[:3]:
                    if (self.state['attachInstrument'] == None) and instrument.isVisible():
                        A = instrument.mapToScene(instrument.A)
                        B = instrument.mapToScene(instrument.B)
                        d = utils.distanceSegment(point, A, B)
                        if d < self.main.attachDistance:
                            self.state['attachInstrument'] = instrument
                            point = utils.projectionOrthogonale(point, A, B)
            ok = False
            toolsWindowHided = False
            try:
                if self.main.drawingMode[0] == 'TEXT':
                    toolsWindowHided = True
                    self.main.toolsWindow.hide()
                    item = QtGui.QGraphicsTextItem()
                    item.setFont(self.font)
                    item.setDefaultTextColor(self.drawPen.color())
                    dialog = utils_dialogs.TextItemDlg(parent=self, graphicsTextItem=item)
                    if dialog.exec_() == QtGui.QDialog.Accepted:
                        ok = True
                elif self.main.drawingMode[0] == 'POINT':
                    toolsWindowHided = True
                    self.main.toolsWindow.hide()
                    brush = QtGui.QBrush(self.drawPen.color())
                    exStyle = self.drawPen.style()
                    self.drawPen.setStyle(QtCore.Qt.SolidLine)
                    item = utils_instruments.PointItem(self.main, self.drawPen, brush, self.font)
                    self.drawPen.setStyle(exStyle)
                    ok = item.chooseText(self.drawPen, brush, self.font)
                elif self.main.drawingMode[0] == 'PIXMAP':
                    toolsWindowHided = True
                    self.main.toolsWindow.hide()
                    fileName = QtGui.QFileDialog.getOpenFileName(
                        self.main, 
                        QtCore.QCoreApplication.translate('MainWindow', 'Open Image'),
                        self.main.pixmapDir, 
                        QtCore.QCoreApplication.translate(
                            'MainWindow', 'Image Files (*.png *.jpg *.jpeg *.xpm)'))
                    # pour PySide :
                    if isinstance(fileName, tuple):
                        fileName = fileName[0]
                    if fileName != '':
                        self.main.pixmapDir = QtCore.QFileInfo(fileName).absolutePath()
                        image = QtGui.QImage(fileName)
                        pixmap = QtGui.QPixmap.fromImage(image)
                        item = QtGui.QGraphicsPixmapItem(pixmap)
                        ok = True
                elif self.main.drawingMode[0] == 'PASTE':
                    # récupération du presse-papier :
                    clipboard = QtGui.QApplication.clipboard()
                    mimeData = clipboard.mimeData()
                    if mimeData.hasImage():
                        pixmap = clipboard.pixmap()
                        item = QtGui.QGraphicsPixmapItem(pixmap)
                        ok = True
                    elif mimeData.hasText():
                        item = QtGui.QGraphicsTextItem()
                        item.setFont(self.font)
                        item.setDefaultTextColor(self.drawPen.color())
                        item.setPlainText(clipboard.text())
                        ok = True
            finally:
                if ok:
                    self.scene().addItem(item)
                    item.setPos(point)
                    self.drawId += 1
                    item.setData(QtCore.Qt.UserRole, self.drawId)
                    item.setTransformOriginPoint(item.boundingRect().center())
                    self.main.saveTempFile()
                if toolsWindowHided:
                    self.main.toolsWindow.show()
        elif mouseEvent == 'firstMouseMove':
            self.state['attachInstrument'] = None
            if self.main.drawingMode[0] in ('LINE',):
                for instrument in self.main.listeInstruments[:3]:
                    if (self.state['attachInstrument'] == None) and instrument.isVisible():
                        A = instrument.mapToScene(instrument.A)
                        B = instrument.mapToScene(instrument.B)
                        d = utils.distanceSegment(point, A, B)
                        if d < self.main.attachDistance:
                            self.state['attachInstrument'] = instrument
                            point = utils.projectionOrthogonale(point, A, B)
            self.state['mouseAction'] = 'scribbling'
            self.last = None
            if self.main.drawingMode[0] == 'LINE':
                self.initLine(point)
            else: 
                self.initCurve(point)
        elif mouseEvent == 'mouseMove':
            if self.main.drawingMode[0] == 'LINE':
                if self.state['attachInstrument'] != None:
                    A = self.state['attachInstrument'].mapToScene(self.state['attachInstrument'].A)
                    B = self.state['attachInstrument'].mapToScene(self.state['attachInstrument'].B)
                    H = utils.projectionOrthogonale(point, A, B)
                    self.drawLineTo(H)
                else:
                    self.drawLineTo(point)
            else:
                self.drawCurveTo(point)
        elif mouseEvent == 'mouseRelease':
            if self.main.drawingMode[0] == 'LINE':
                if self.state['attachInstrument'] != None:
                    A = self.state['attachInstrument'].mapToScene(self.state['attachInstrument'].A)
                    B = self.state['attachInstrument'].mapToScene(self.state['attachInstrument'].B)
                    H = utils.projectionOrthogonale(point, A, B)
                    item = self.drawLineTo(H)
                else:
                    item = self.drawLineTo(point)
            else:
                item = self.drawCurveTo(point, endLine=True)
            self.drawId += 1
            item.setData(QtCore.Qt.UserRole, self.drawId)
            item.setTransformOriginPoint(item.boundingRect().center())
            self.state['mouseAction'] = ''
            self.state['attachInstrument'] = None
            self.state['lastPoint'] = QtCore.QPointF()
            self.main.saveTempFile()

    def keyPressEvent(self, event):
        """
        Gestion des touches Control et Delete
        """
        if event.key() == QtCore.Qt.Key_Control:
            utils_instruments.changeTracingEnabled(True)
        elif event.key() == QtCore.Qt.Key_Delete:
            self.main.removeSelected()
        else:
            self.main.keyPressEvent(event)
            
    def keyReleaseEvent(self, event):
        """
        Gestion de la touche Control
        """
        if event.key() == QtCore.Qt.Key_Control:
            utils_instruments.changeTracingEnabled(False)

    def initLine(self, startPoint):
        """
        Début d'une ligne (un segment).
        On initialise le path et le pathItem
        """
        self.state['lastPoint'] = startPoint
        self.path = QtGui.QPainterPath()
        self.path.moveTo(startPoint)
        pen = self.drawPen
        brush = QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.NoBrush)
        self.pathItem = self.scene().addPath(self.path, pen, brush)
        self.pathItem.setFlags(QtGui.QGraphicsItem.ItemIgnoresTransformations)

    def drawLineTo(self, endPoint):
        """
        On supprime systématiquement la ligne précédente
            avant d'ajouter la nouvelle
        """
        self.path.lineTo(endPoint)
        if self.last != None:
            self.scene().removeItem(self.last)
        self.last = self.scene().addLine(
            self.state['lastPoint'].x(), self.state['lastPoint'].y(), 
            endPoint.x(), endPoint.y(), 
            self.drawPen)
        return self.last

    def initCurve(self, startPoint):
        """
        Début d'une courbe.
        On initialise le path et le pathItem. En cours de tracé, on affichera 
            une suite de segments (polyligne).
        Le path sera recalculé à la fin du tracé, pour tracer une courbe.
        On récupèrera donc les points de passage dans une liste (listPoints).
        """
        self.state['lastPoint'] = startPoint
        self.path = QtGui.QPainterPath()
        self.path.moveTo(startPoint)
        if self.main.drawingMode[0] == 'HIGHLIGHTER':
            pen = QtGui.QPen(
                self.main.drawingMode[1], 20,
                QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        else:
            pen = self.drawPen
        brush = QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.NoBrush)
        self.pathItem = self.scene().addPath(self.path, pen, brush)
        self.pathItem.setFlags(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        # pour faire la courbe finale :
        self.listPoints = []
        self.listPoints.append(startPoint)

    def drawCurveTo(self, endPoint, endLine=False):
        """
        En cours de tracé, c'est path qui est affiché.
            On récupère le point dans listPoints.
        À la fin (appel avec la variable endLine à True), 
            on calcule la courbe, et on l'affiche.
        """
        self.path.lineTo(endPoint)
        self.state['lastPoint'] = endPoint
        self.pathItem.setPath(self.path)
        self.listPoints.append(endPoint)
        if endLine:
            """
            # tentative d'interpolation (désactivé car moche)
            self.state['lastPoint'] = endPoint
            self.path = QtGui.QPainterPath()
            self.path.moveTo(self.listPoints[0])
            for i in range(len(self.listPoints) // 2):
                self.path.quadTo(self.listPoints[2*i], self.listPoints[2*i + 1])
            self.pathItem.setPath(self.path)
            """
            return self.pathItem

    def initArc(self, center, startPoint):
        """
        Début d'un arc de compas.
        On initialise les différentes valeurs d'angles utiles.
        On calcule le rectangle d'affichage (carré contenant le cercle complet).
        """
        self.state['lastPoint'] = startPoint
        self.path = QtGui.QPainterPath()
        self.path.moveTo(startPoint)
        pen = self.drawPen
        brush = QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.NoBrush)
        self.pathItem = self.scene().addPath(self.path, pen, brush)
        self.startPoint = startPoint
        rayon = QtCore.QLineF(center, startPoint)
        self.startAngle = rayon.angle()
        self.minAngle = self.startAngle
        self.maxAngle = self.startAngle
        self.lastAngle = self.startAngle
        length = rayon.length()
        self.rectangle = QtCore.QRectF(
            center.x() - length, center.y() - length, 2 * length, 2 * length)

    def drawArcTo(self, center, endPoint):
        """
        En cours de tracé, on recalcule les différents angles utiles.
            Pas mal de cas à gérer, et la complication du passage brutal de 0 à 360.
        Ensuite on trace l'arc.
        """
        self.state['lastPoint'] = QtCore.QPointF(endPoint)
        rayon = QtCore.QLineF(center, endPoint)
        self.path = QtGui.QPainterPath()
        angle = rayon.angle()
        if angle - self.lastAngle > 300:
            self.minAngle = self.minAngle + 360.0
            self.maxAngle = self.maxAngle + 360.0
        if angle - self.lastAngle < -300:
            self.minAngle = self.minAngle - 360.0
            self.maxAngle = self.maxAngle - 360.0
        if angle < self.minAngle:
            self.minAngle = angle
            self.startPoint = self.state['lastPoint']
        if angle > self.maxAngle:
            self.maxAngle = angle
        endAngle = self.maxAngle - self.minAngle
        self.path.moveTo(self.startPoint)
        self.path.arcTo(self.rectangle, self.minAngle, endAngle)
        self.pathItem.setPath(self.path)
        self.lastAngle = angle
        return self.pathItem

    def penColor(self):
        """
        Dialog de sélection de couleur
        """
        try:
            self.main.toolsWindow.hide()
            color = self.drawPen.color()
            newColor = QtGui.QColorDialog.getColor(
                color, 
                self, 
                QtCore.QCoreApplication.translate('GraphicsView', 'Select color'), 
                QtGui.QColorDialog.ShowAlphaChannel)
            if newColor.isValid():
                self.drawPen.setColor(newColor)
                #print(newColor, newColor.red(), newColor.green(), newColor.blue(), newColor.alpha())
        finally:
            self.main.toolsWindow.show()

    def penWidth(self):
        """
        Dialog de sélection d'épaisseur du crayon
        """
        try:
            self.main.toolsWindow.hide()
            newWidth, ok = QtGui.QInputDialog.getInteger(
                self, utils.PROGLABEL,
                QtCore.QCoreApplication.translate('GraphicsView', 'Select pen width:'),
                self.drawPen.width(),
                1, 50, 1)
            if ok:
                self.drawPen.setWidth(newWidth)
        finally:
            self.main.toolsWindow.show()

    def penStyle(self):
        """
        Dialog de sélection de style du crayon
        """
        try:
            self.main.toolsWindow.hide()
            solid = QtCore.QCoreApplication.translate('GraphicsView', 'Solid')
            dash = QtCore.QCoreApplication.translate('GraphicsView', 'Dash')
            dot = QtCore.QCoreApplication.translate('GraphicsView', 'Dot')
            dashDot = QtCore.QCoreApplication.translate('GraphicsView', 'Dash Dot')
            dashDotDot = QtCore.QCoreApplication.translate('GraphicsView', 'Dash Dot Dot')
            items = {
                solid: QtCore.Qt.SolidLine, 
                dash: QtCore.Qt.DashLine, 
                dot: QtCore.Qt.DotLine,
                dashDot: QtCore.Qt.DashDotLine, 
                dashDotDot: QtCore.Qt.DashDotDotLine}
            response, ok = QtGui.QInputDialog.getItem(
                self, utils.PROGLABEL,
                QtCore.QCoreApplication.translate('GraphicsView', 'Select pen style:'), 
                [solid, dash, dot, dashDot, dashDotDot], 
                0, False)
            if ok and response != '':
                newStyle = items[response]
                self.drawPen.setStyle(newStyle)
        finally:
            self.main.toolsWindow.show()

    def comboBoxPensChanged(self):
        """
        On change de stylo
        """
        indexPen = self.main.toolsWindow.comboBoxPens.currentIndex()
        self.drawPen = self.pens[indexPen]

    def customColor(self):
        if self.main.toolsWindow.actionEditCustomColors.isChecked():
            try:
                self.main.toolsWindow.hide()
                color = self.sender().data()
                newColor = QtGui.QColorDialog.getColor(
                    color, 
                    self, 
                    QtCore.QCoreApplication.translate('GraphicsView', 'Select color'), 
                    QtGui.QColorDialog.ShowAlphaChannel)
                if newColor.isValid():
                    self.drawPen.setColor(newColor)
                    pixmap = QtGui.QPixmap(128, 128)
                    pixmap.fill(newColor)
                    icon = QtGui.QIcon(pixmap)
                    self.sender().setIcon(icon)
                    self.sender().setData(newColor)
            finally:
                self.main.toolsWindow.show()
        else:
            color = self.sender().data()
            self.drawPen.setColor(color)

    def customSize(self):
        if self.main.toolsWindow.actionEditCustomSizes.isChecked():
            try:
                self.main.toolsWindow.hide()
                width = self.sender().data()
                newWidth, ok = QtGui.QInputDialog.getInteger(
                    self, utils.PROGLABEL,
                    QtCore.QCoreApplication.translate('GraphicsView', 'Select pen width:'),
                    width,
                    1, 50, 1)
                if ok:
                    self.drawPen.setWidth(newWidth)
                    self.sender().setData(newWidth)
                    self.sender().setToolTip('{0}'.format(newWidth))
                    # on réorganise pour garder l'ordre croissant :
                    sizes = []
                    for action in self.main.toolsWindow.actionCustomSizes:
                        sizes.append(action.data())
                    sizes = sorted(sizes)
                    for i in range(5):
                        action = self.main.toolsWindow.actionCustomSizes[i]
                        size = sizes[i]
                        action.setData(size)
                        action.setToolTip('{0}'.format(size))
            finally:
                self.main.toolsWindow.show()
        else:
            penWidth = self.sender().data()
            self.drawPen.setWidth(penWidth)










