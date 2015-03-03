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
    Les fenêtres d'outils (toolbars) et autres dialogs utiles.
"""

# importation des modules utiles :
from __future__ import division, print_function
import sys
import os

import utils, utils_instruments

if utils.PYSIDE:
    from PySide import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui







"""
###########################################################
###########################################################

                DIALOG DE CRÉATION D'UN TEXTE

###########################################################
###########################################################
"""

class TextItemDlg(QtGui.QDialog):
    """
    La fenêtre de dialogue de création d'un texte.
    Le texte s'affiche dans la police sélectionnée, dans un QTextEdit.
    """
    def __init__(self, parent=None, graphicsTextItem=None):
        super(TextItemDlg, self).__init__(parent)

        self.graphicsTextItem = graphicsTextItem
        self.parent = parent

        self.editor = QtGui.QTextEdit()
        self.editor.setAcceptRichText(False)
        self.editor.setTabChangesFocus(True)

        # le bouton ChooseFont :
        chooseFontButton = QtGui.QPushButton(QtGui.QIcon('images/fonts.png'), '')
        chooseFontButton.setToolTip(QtGui.QApplication.translate('main', 'ChooseFont'))
        chooseFontButton.clicked.connect(self.chooseFont)
        # le bouton ChooseFont :
        penColorButton = QtGui.QPushButton(QtGui.QIcon('images/colorize.png'),  '')
        penColorButton.setToolTip(QtGui.QApplication.translate('main', 'PenColor'))
        penColorButton.clicked.connect(self.penColor)

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                          QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

        if self.graphicsTextItem is not None:
            self.font = self.graphicsTextItem.font()
            self.color = self.graphicsTextItem.defaultTextColor()
            self.editor.document().setDefaultFont(self.font)
            self.editor.setTextColor(self.color)
            self.editor.setPlainText(self.graphicsTextItem.toPlainText())
        else:
            self.font = self.parent.font
            self.color = self.parent.drawPen.color()

        layout = QtGui.QGridLayout()
        layout.addWidget(self.editor, 1, 0, 1, 6)
        layout.addWidget(chooseFontButton, 2, 0)
        layout.addWidget(penColorButton, 2, 1)
        layout.addWidget(self.buttonBox, 2, 3, 1, 3)
        self.setLayout(layout)

        self.editor.textChanged.connect(self.updateUi)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.setWindowTitle(QtGui.QApplication.translate('main', 'InsertText'))
        self.noUpdateUi = False
        self.updateUi()
        

    def updateUi(self):
        if self.noUpdateUi:
            return
        self.editor.document().setDefaultFont(self.font)
        self.editor.setTextColor(self.color)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(
                self.editor.toPlainText() != '')

    def accept(self):
        self.graphicsTextItem.setPlainText(self.editor.toPlainText())
        self.graphicsTextItem.setFont(self.font)
        self.graphicsTextItem.update()
        QtGui.QDialog.accept(self)

    def chooseFont(self):
        """
        Dialogue pour choisir la police d'écriture
        """
        font, ok = QtGui.QFontDialog.getFont(self.font, self)
        if ok:
            self.font = font
            self.editor.document().setDefaultFont(font)
            self.graphicsTextItem.setFont(font)

    def penColor(self):
        """
        Dialog de sélection de couleur
        """
        self.noUpdateUi = True
        text = self.editor.toPlainText()
        newColor = QtGui.QColorDialog.getColor(
            self.color, 
            self, 
            QtCore.QCoreApplication.translate('TextItemDlg', 'Select color'), 
            QtGui.QColorDialog.ShowAlphaChannel)
        if newColor.isValid():
            self.color = newColor
            self.editor.setPlainText('')
            self.editor.setTextColor(self.color)
            self.editor.setPlainText(text)
            self.graphicsTextItem.setDefaultTextColor(self.color)
        self.noUpdateUi = False






"""
###########################################################
###########################################################

                LA FENÊTRE D'OUTILS

###########################################################
###########################################################
"""

def createActions(self, toolsWindow):
    """
    Création des actions dans une fonction à part car elles sont
    partagées entre les 2 boîtes à outils (normale et kids)
    """

    # Les actions de base (quitter, aide, ...)
    self.actionQuit = QtGui.QAction(QtGui.QApplication.translate('main', 'Quit'), 
        self, icon=QtGui.QIcon('images/application-exit.png'),
        objectName='Quit', 
        shortcut=QtGui.QApplication.translate('main', 'Ctrl+Q'))
    self.actionQuit.triggered.connect(self.main.quit)
    self.actionFileOpen = QtGui.QAction(QtGui.QApplication.translate('main', 'FileOpen'), 
        self, icon=QtGui.QIcon('images/document-open.png'), objectName='FileOpen')
    self.actionFileOpen.triggered.connect(self.main.fileOpen)
    self.actionFileReload = QtGui.QAction(QtGui.QApplication.translate('main', 'FileReload'), 
        self, icon=QtGui.QIcon('images/view-refresh.png'), objectName='FileReload')
    self.actionFileReload.triggered.connect(self.main.fileReload)
    self.actionFileGoPrevious = QtGui.QAction(QtGui.QApplication.translate('main', 'FileGoPrevious'), 
        self, icon=QtGui.QIcon('images/go-previous.png'), objectName='FileGoPrevious')
    self.actionFileGoPrevious.triggered.connect(self.main.fileGoPrevious)
    self.actionFileGoNext = QtGui.QAction(QtGui.QApplication.translate('main', 'FileGoNext'), 
        self, icon=QtGui.QIcon('images/go-next.png'), objectName='FileGoNext')
    self.actionFileGoNext.triggered.connect(self.main.fileGoNext)
    self.actionFileSave = QtGui.QAction(QtGui.QApplication.translate('main', 'FileSave'), 
        self, icon=QtGui.QIcon('images/document-save.png'), objectName='FileSave')
    self.actionFileSave.triggered.connect(self.main.fileSave)
    self.actionFileSaveAs = QtGui.QAction(QtGui.QApplication.translate('main', 'FileSaveAs'), 
        self, icon=QtGui.QIcon('images/document-save-as.png'), objectName='FileSaveAs')
    self.actionFileSaveAs.triggered.connect(self.main.fileSaveAs)
    self.actionPrint = QtGui.QAction(QtGui.QApplication.translate('main', 'Print'), 
        self, icon=QtGui.QIcon('images/document-print.png'), objectName='Print')
    self.actionPrint.triggered.connect(self.main.documentPrint)
    self.actionPrintDirect = QtGui.QAction(QtGui.QApplication.translate('main', 'PrintDirect'), 
        self, icon=QtGui.QIcon('images/document-print-direct.png'), objectName='PrintDirect')
    self.actionPrintDirect.triggered.connect(self.main.documentPrintDirect)
    self.actionExportPdf = QtGui.QAction(QtGui.QApplication.translate('main', 'ExportPdf'), 
        self, icon=QtGui.QIcon('images/application-pdf.png'), objectName='ExportPdf')
    self.actionExportPdf.triggered.connect(self.main.exportPdf)
    self.actionExportSvg = QtGui.QAction(QtGui.QApplication.translate('main', 'ExportSvg'), 
        self, icon=QtGui.QIcon('images/application-svg.png'), objectName='ExportSvg')
    self.actionExportSvg.triggered.connect(self.main.exportSvg)
    self.actionConfigure = QtGui.QAction(QtGui.QApplication.translate('main', 'Configure'), 
        self, icon=QtGui.QIcon('images/configure.png'), objectName='Configure')
    self.actionConfigure.triggered.connect(self.main.configure)
    self.actionMinimize = QtGui.QAction(QtGui.QApplication.translate('main', 'Minimize'), 
        self, icon=QtGui.QIcon('images/minimize.png'), objectName='Minimize')
    self.actionMinimize.triggered.connect(self.main.showMinimized)
    self.actionCreateDesktopFileLinux = QtGui.QAction(
        QtGui.QApplication.translate('main', 'CreateDesktopFileLinux'), 
        self, icon=QtGui.QIcon('images/logo_linux.png'), objectName='CreateDesktopFileLinux')
    self.actionCreateDesktopFileLinux.triggered.connect(self.main.createDesktopFileLinux)
    self.actionHelp = QtGui.QAction(QtGui.QApplication.translate('main', 'Help'), 
        self, icon=QtGui.QIcon('images/help.png'), objectName='Help',
        shortcut=QtGui.QApplication.translate('main', 'F1'))
    self.actionHelp.triggered.connect(self.main.helpPage)
    self.actionAbout = QtGui.QAction(QtGui.QApplication.translate('main', 'About'), 
        self, icon=QtGui.QIcon('images/help-about.png'), objectName='About')
    self.actionAbout.triggered.connect(self.main.about)

    # Les actions des réglages
    self.actionLockInstruments = QtGui.QAction(QtGui.QApplication.translate('main', 'LockInstruments'), 
        self, icon=QtGui.QIcon('images/object-locked.png'), objectName='LockInstruments',
        checkable=True, checked=False)
    self.actionLockInstruments.triggered.connect(toolsWindow.lockInstruments)
    self.actionShowFalseCursor = QtGui.QAction(QtGui.QApplication.translate('main', 'ShowFalseCursor'), 
        self, icon=QtGui.QIcon('images/cursor.png'), objectName='ShowFalseCursor',
        checkable=True, checked=False)
    self.actionShowFalseCursor.triggered.connect(toolsWindow.showFalseCursor)

    # Les actions des screenshots et autres fonds
    self.actionNewScreenshot = QtGui.QAction(QtGui.QApplication.translate('main', 'NewScreenshot'), 
        self, icon=QtGui.QIcon('images/camera.png'), objectName='NewScreenshot')
    self.actionNewScreenshot.triggered.connect(self.main.newScreenshot)
    self.actionWhitePage = QtGui.QAction(QtGui.QApplication.translate('main', 'WhitePage'), 
        self, icon=QtGui.QIcon('images/white.png'), objectName='WhitePage')
    self.actionWhitePage.triggered.connect(self.main.whitePage)
    self.actionPointsPage = QtGui.QAction(QtGui.QApplication.translate('main', 'PointsPage'), 
        self, icon=QtGui.QIcon('images/points.png'), objectName='PointsPage')
    self.actionPointsPage.triggered.connect(self.main.pointsPage)
    self.actionGridPage = QtGui.QAction(QtGui.QApplication.translate('main', 'GridPage'), 
        self, icon=QtGui.QIcon('images/grid.png'), objectName='GridPage')
    self.actionGridPage.triggered.connect(self.main.gridPage)
    self.actionBackGround = QtGui.QAction(QtGui.QApplication.translate('main', 'ChooseBackGround'), 
        self, icon=QtGui.QIcon('images/images.png'), objectName='ChooseBackGround')
    self.actionBackGround.triggered.connect(self.main.chooseBackGround)

    # Les actions des instruments
    self.actionShowRuler = QtGui.QAction(QtGui.QApplication.translate('main', 'ShowRuler'), 
        self, icon=QtGui.QIcon('images/ruler.png'), objectName='ShowRuler',
        checkable=True, checked=False)
    self.actionShowRuler.triggered.connect(toolsWindow.showRuler)
    self.actionShowSquare = QtGui.QAction(QtGui.QApplication.translate('main', 'ShowSquare'), 
        self, icon=QtGui.QIcon('images/square.png'), objectName='ShowSquare',
        checkable=True, checked=False)
    self.actionShowSquare.triggered.connect(toolsWindow.showSquare)
    self.actionShowSquareNotGraduated = QtGui.QAction(QtGui.QApplication.translate('main', 
        'ShowSquareNotGraduated'), 
        self, icon=QtGui.QIcon('images/square-not-graduated.png'), 
        objectName='ShowSquareNotGraduated',
        checkable=True, checked=False)
    self.actionShowSquareNotGraduated.triggered.connect(toolsWindow.showSquareNotGraduated)
    self.actionShowProtractor = QtGui.QAction(QtGui.QApplication.translate('main', 'ShowProtractor'), 
        self, icon=QtGui.QIcon('images/protractor.png'), objectName='ShowProtractor',
        checkable=True, checked=False)
    self.actionShowProtractor.triggered.connect(toolsWindow.showProtractor)
    self.actionShowCompass = QtGui.QAction(QtGui.QApplication.translate('main', 'ShowCompass'), 
        self, icon=QtGui.QIcon('images/compass.png'), objectName='ShowCompass',
        checkable=True, checked=False)
    self.actionShowCompass.triggered.connect(toolsWindow.showCompass)
    self.actionUnitsLock = QtGui.QAction(QtGui.QApplication.translate('main', 'UnitsLock'), 
        self, icon=QtGui.QIcon('images/units-lock.png'), objectName='UnitsLock',
        checkable=True, checked=self.main.unitsLocked)
    self.actionUnitsSave = QtGui.QAction(QtGui.QApplication.translate('main', 'UnitsSave'), 
        self, icon=QtGui.QIcon('images/units-save.png'), objectName='UnitsSave')
    self.actionUnitsSave.triggered.connect(self.main.unitsActions)
    self.actionUnitsRestore = QtGui.QAction(QtGui.QApplication.translate('main', 'UnitsRestore'), 
        self, icon=QtGui.QIcon('images/units-open.png'), objectName='UnitsRestore')
    self.actionUnitsRestore.triggered.connect(self.main.unitsActions)
    self.actionUnitsInit = QtGui.QAction(QtGui.QApplication.translate('main', 'UnitsInit'), 
        self, icon=QtGui.QIcon('images/units-init.png'), objectName='UnitsInit')
    self.actionUnitsInit.triggered.connect(self.main.unitsActions)

    # Les actions des outils de dessin
    self.actionSelect = QtGui.QAction(QtGui.QApplication.translate('main', 'Select'), 
        self, icon=QtGui.QIcon('images/edit-select.png'), objectName='Select',
        checkable=True, checked=False)
    self.actionSelect.triggered.connect(toolsWindow.select)
    self.comboBoxPens = QtGui.QComboBox()
    self.comboBoxPens.setObjectName('comboBoxPens')
    self.comboBoxPens.setToolTip(QtGui.QApplication.translate('main', 'Pens'))
    self.comboBoxPens.setIconSize(self.main.iconSize)
    for i in range(5):
        fileicon = 'images/pen{0}.png'.format(i + 1)
        label = ''
        self.comboBoxPens.addItem(QtGui.QIcon(fileicon), label)
    self.comboBoxPens.activated.connect(self.main.view.comboBoxPensChanged)
    self.actionPens = QtGui.QWidgetAction(self)
    self.actionPens.setDefaultWidget(self.comboBoxPens)
    self.actionDrawLine = QtGui.QAction(QtGui.QApplication.translate('main', 'DrawLine'), 
        self, icon=QtGui.QIcon('images/draw-freehand.png'), objectName='DrawLine',
        checkable=True, checked=False)
    self.actionDrawLine.triggered.connect(toolsWindow.drawLine)
    self.actionDrawCurve = QtGui.QAction(QtGui.QApplication.translate('main', 'DrawCurve'), 
        self, icon=QtGui.QIcon('images/draw-brush.png'), objectName='DrawCurve',
        checkable=True, checked=False)
    self.actionDrawCurve.triggered.connect(toolsWindow.drawCurve)
    self.actionYellowHighlighterPen = QtGui.QAction(
        QtGui.QApplication.translate('main', 'YellowHighlighterPen'), 
        self, icon=QtGui.QIcon('images/surligneur_jaune.png'), 
        objectName='YellowHighlighterPen',
        checkable=True, checked=False)
    self.actionYellowHighlighterPen.setData(('HIGHLIGHTER', QtGui.QColor(252, 252, 0, 155)))
    self.actionYellowHighlighterPen.triggered.connect(toolsWindow.highlighterPen)
    self.actionGreenHighlighterPen = QtGui.QAction(
        QtGui.QApplication.translate('main', 'GreenHighlighterPen'), 
        self, icon=QtGui.QIcon('images/surligneur_vert.png'), 
        objectName='GreenHighlighterPen',
        checkable=True, checked=False)
    self.actionGreenHighlighterPen.setData(('HIGHLIGHTER', QtGui.QColor(0, 252, 0, 155)))
    self.actionGreenHighlighterPen.triggered.connect(toolsWindow.highlighterPen)
    self.actionPinkHighlighterPen = QtGui.QAction(
        QtGui.QApplication.translate('main', 'PinkHighlighterPen'), 
        self, icon=QtGui.QIcon('images/surligneur_rose.png'), 
        objectName='PinkHighlighterPen',
        checkable=True, checked=False)
    self.actionPinkHighlighterPen.setData(('HIGHLIGHTER', QtGui.QColor(255, 49, 62, 155)))
    self.actionPinkHighlighterPen.triggered.connect(toolsWindow.highlighterPen)
    self.actionBlueHighlighterPen = QtGui.QAction(
        QtGui.QApplication.translate('main', 'BlueHighlighterPen'), 
        self, icon=QtGui.QIcon('images/surligneur_bleu.png'), 
        objectName='BlueHighlighterPen',
        checkable=True, checked=False)
    self.actionBlueHighlighterPen.setData(('HIGHLIGHTER', QtGui.QColor(13, 203, 255, 155)))
    self.actionBlueHighlighterPen.triggered.connect(toolsWindow.highlighterPen)
    self.actionAddText = QtGui.QAction(QtGui.QApplication.translate('main', 'AddText'), 
        self, icon=QtGui.QIcon('images/addtext.png'), objectName='AddText',
        checkable=True, checked=False)
    self.actionAddText.triggered.connect(toolsWindow.addText)
    self.actionAddPoint = QtGui.QAction(QtGui.QApplication.translate('main', 'AddPoint'), 
        self, icon=QtGui.QIcon('images/point.png'), objectName='AddPoint',
        checkable=True, checked=False)
    self.actionAddPoint.triggered.connect(toolsWindow.addPoint)
    self.actionAddPixmap = QtGui.QAction(QtGui.QApplication.translate('main', 'AddPixmap'), 
        self, icon=QtGui.QIcon('images/pixmap.png'), objectName='AddPixmap',
        checkable=True, checked=False)
    self.actionAddPixmap.triggered.connect(toolsWindow.addPixmap)
    self.actionPaste = QtGui.QAction(QtGui.QApplication.translate('main', 'Paste'), 
        self, icon=QtGui.QIcon('images/edit-paste.png'), objectName='Paste',
        checkable=True, checked=False)
    self.actionPaste.triggered.connect(toolsWindow.paste)

    # Les actions de réglage des dessins
    self.actionPenColor = QtGui.QAction(QtGui.QApplication.translate('main', 'PenColor'), 
        self, icon=QtGui.QIcon('images/colorize.png'), objectName='PenColor')
    self.actionPenColor.triggered.connect(self.main.view.penColor)
    self.actionPenWidth = QtGui.QAction(QtGui.QApplication.translate('main', 'PenWidth'), 
        self, icon=QtGui.QIcon('images/line-size.png'), objectName='PenWidth')
    self.actionPenWidth.triggered.connect(self.main.view.penWidth)
    self.actionPenStyle = QtGui.QAction(QtGui.QApplication.translate('main', 'PenStyle'), 
        self, icon=QtGui.QIcon('images/line-style.png'), objectName='PenStyle')
    self.actionPenStyle.triggered.connect(self.main.view.penStyle)
    self.actionChooseFont = QtGui.QAction(QtGui.QApplication.translate('main', 'ChooseFont'), 
        self, icon=QtGui.QIcon('images/fonts.png'), objectName='ChooseFont')
    self.actionChooseFont.triggered.connect(toolsWindow.chooseFont)
    self.actionEditText = QtGui.QAction(QtGui.QApplication.translate('main', 'EditText'), 
        self, icon=QtGui.QIcon('images/document-edit.png'), objectName='EditText')
    self.actionEditText.triggered.connect(self.main.editText)
    self.actionUndo = QtGui.QAction(QtGui.QApplication.translate('main', 'Undo'), 
        self, icon=QtGui.QIcon('images/edit-undo.png'), objectName='Undo')
    self.actionUndo.triggered.connect(self.main.undo)
    self.actionRedo = QtGui.QAction(QtGui.QApplication.translate('main', 'Redo'), 
        self, icon=QtGui.QIcon('images/edit-redo.png'), objectName='Redo')
    self.actionRedo.triggered.connect(self.main.redo)
    self.actionRemoveSelected = QtGui.QAction(QtGui.QApplication.translate('main', 'RemoveSelected'), 
        self, icon=QtGui.QIcon('images/draw-eraser.png'), objectName='RemoveSelected')
    self.actionRemoveSelected.triggered.connect(self.main.removeSelected)
    self.actionRemoveLast = QtGui.QAction(QtGui.QApplication.translate('main', 'RemoveLast'), 
        self, icon=QtGui.QIcon('images/undo.png'), objectName='RemoveLast')
    self.actionRemoveLast.triggered.connect(self.main.removeLast)
    self.actionEraseAll = QtGui.QAction(QtGui.QApplication.translate('main', 'EraseAll'), 
        self, icon=QtGui.QIcon('images/edit-trash.png'), objectName='EraseAll')
    self.actionEraseAll.triggered.connect(self.main.eraseAll)

    # Les actions de la barre des couleurs et tailles persos
    settings = QtCore.QSettings(utils.PROGNAME, 'config')
    defaultSettings = QtCore.QSettings('libs/config.conf', QtCore.QSettings.IniFormat)
    self.actionEditCustomColors = QtGui.QAction(QtGui.QApplication.translate('main', 'EditCustomColors'), 
        self, icon=QtGui.QIcon('images/colorize-edit.png'), objectName='EditCustomColors',
        checkable=True, checked=False)
    self.actionCustomColor1 = QtGui.QAction('', self, objectName='CustomColor1')
    self.actionCustomColor2 = QtGui.QAction('', self, objectName='CustomColor2')
    self.actionCustomColor3 = QtGui.QAction('', self, objectName='CustomColor3')
    self.actionCustomColor4 = QtGui.QAction('', self, objectName='CustomColor4')
    self.actionCustomColor5 = QtGui.QAction('', self, objectName='CustomColor5')
    self.actionCustomColor6 = QtGui.QAction('', self, objectName='CustomColor6')
    self.actionCustomColor7 = QtGui.QAction('', self, objectName='CustomColor7')
    self.actionCustomColor8 = QtGui.QAction('', self, objectName='CustomColor8')
    self.actionCustomColor9 = QtGui.QAction('', self, objectName='CustomColor9')
    self.actionCustomColors = (self.actionCustomColor1, 
                                self.actionCustomColor2, 
                                self.actionCustomColor3, 
                                self.actionCustomColor4, 
                                self.actionCustomColor5, 
                                self.actionCustomColor6, 
                                self.actionCustomColor7, 
                                self.actionCustomColor8, 
                                self.actionCustomColor9,)
    for action in self.actionCustomColors: 
        action.triggered.connect(self.main.view.customColor)
        color = settings.value('custom/{0}'.format(action.objectName()),
            defaultSettings.value('custom/{0}'.format(action.objectName())))
        color = QtGui.QColor(color)
        pixmap = QtGui.QPixmap(128, 128)
        pixmap.fill(color)
        action.setIcon(QtGui.QIcon(pixmap))
        action.setData(color)
    self.actionEditCustomSizes = QtGui.QAction(QtGui.QApplication.translate('main', 'EditCustomSizes'), 
        self, icon=QtGui.QIcon('images/size-edit.png'), objectName='EditCustomSizes',
        checkable=True, checked=False)
    self.actionCustomSize1 = QtGui.QAction('', self, objectName='CustomSize1')
    self.actionCustomSize2 = QtGui.QAction('', self, objectName='CustomSize2')
    self.actionCustomSize3 = QtGui.QAction('', self, objectName='CustomSize3')
    self.actionCustomSize4 = QtGui.QAction('', self, objectName='CustomSize4')
    self.actionCustomSize5 = QtGui.QAction('', self, objectName='CustomSize5')
    self.actionCustomSizes = (self.actionCustomSize1, 
                                self.actionCustomSize2,
                                self.actionCustomSize3,
                                self.actionCustomSize4,
                                self.actionCustomSize5,)
    defaultSizes = {0:1, 1:5, 2:10, 3:20, 4:40}
    for i in range(5):
        action = self.actionCustomSizes[i]
        action.triggered.connect(self.main.view.customSize)
        try:
            size = int(settings.value('custom/{0}'.format(action.objectName()), defaultSizes[i]))
        except:
            size = defaultSizes[i]
        action.setIcon(QtGui.QIcon('images/custom-size-{0}.png'.format(i + 1)))
        action.setToolTip('{0}'.format(size))
        action.setData(size)




class ToolsWindow(QtGui.QMainWindow):
    """
    La boîte à outils.
    Elle contient les différentes barres d'outils,
        et les actions associées.
    """
    def __init__(self, parent):
        super(ToolsWindow, self).__init__(parent)
        """
        Mise en place. On crée les actions, les barres d'outils, ...
        """
        self.main = parent
        self.setWindowTitle(QtGui.QApplication.translate('main', 'Tools'))
        self.toolsKidMode = False
        self.defaultFlags = self.windowFlags() | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint
        self.kidFlags = QtCore.Qt.Tool | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint
        self.setWindowFlags(self.defaultFlags)

        self.actionsState = {}
        createActions(self, self)
        self.createToolBars()

    def closeEvent(self, event):
        self.main.quit()

    def keyPressEvent(self, event):
        self.main.keyPressEvent(event)

    def createToolBars(self):
        # la barre de base (quitter, aide, ...)
        self.toolBarBase = QtGui.QToolBar(QtGui.QApplication.translate('main', 'Base Bar'))
        self.toolBarBase.setObjectName('toolBarBase')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarBase)

        # la barre des screenshots et autres fonds
        self.toolBarBackground = QtGui.QToolBar(QtGui.QApplication.translate('main', 'Background Bar'))
        self.toolBarBackground.setObjectName('toolBarBackground')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarBackground)

        # la barre des instruments
        self.toolBarInstruments = QtGui.QToolBar(QtGui.QApplication.translate('main', 'Tools Bar'))
        self.toolBarInstruments.setObjectName('toolBarInstruments')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarInstruments)

        # la barre des outils de dessin (et son comboboxPens)
        self.toolBarDraw = QtGui.QToolBar(QtGui.QApplication.translate('main', 'Draw Bar'))
        self.toolBarDraw.setObjectName('toolBarDraw')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarDraw)

        # la barre de réglage des dessins
        self.toolBarDrawConfig = QtGui.QToolBar(QtGui.QApplication.translate('main', 'Draw Config Bar'))
        self.toolBarDrawConfig.setObjectName('toolBarDrawConfig')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarDrawConfig)

        # la barre des couleurs et tailles persos
        self.toolBarColorsSizes = QtGui.QToolBar(QtGui.QApplication.translate('main', 
            'Custom colors and sizes Bar'))
        self.toolBarColorsSizes.setObjectName('toolBarColorsSizes')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarColorsSizes)

        self.toolBarsList = (
            self.toolBarBase,
            self.toolBarBackground,
            self.toolBarInstruments,
            self.toolBarDraw,
            self.toolBarDrawConfig,
            self.toolBarColorsSizes,)

        self.toolBars = {
            # la barre de base (quitter, aide, ...)
            self.toolBarBase: (
                self.actionQuit,
                'SEPARATOR',
                self.actionFileOpen,
                self.actionFileReload,
                self.actionFileGoPrevious,
                self.actionFileGoNext,
                'SEPARATOR',
                self.actionFileSave,
                self.actionFileSaveAs,
                self.actionPrint,
                self.actionPrintDirect,
                self.actionExportPdf,
                self.actionExportSvg,
                'SEPARATOR',
                self.actionConfigure,
                self.actionMinimize,
                self.actionCreateDesktopFileLinux,
                'SEPARATOR',
                self.actionHelp,
                self.actionAbout,),
            # la barre des screenshots et autres fonds
            self.toolBarBackground: (
                self.actionNewScreenshot,
                self.actionWhitePage,
                self.actionPointsPage,
                self.actionGridPage,
                self.actionBackGround,),
            # la barre des instruments
            self.toolBarInstruments: (
                self.actionShowRuler,
                self.actionShowSquare,
                self.actionShowSquareNotGraduated,
                self.actionShowProtractor,
                self.actionShowCompass,
                'SEPARATOR',
                self.actionUnitsLock,
                self.actionUnitsSave,
                self.actionUnitsRestore,
                self.actionUnitsInit,
                self.actionLockInstruments,
                self.actionShowFalseCursor,),
            # 
            self.toolBarDraw: (
                self.actionSelect,
                'SEPARATOR',
                self.actionPens,
                self.actionDrawLine,
                self.actionDrawCurve,
                self.actionYellowHighlighterPen,
                self.actionGreenHighlighterPen,
                self.actionPinkHighlighterPen,
                self.actionBlueHighlighterPen,
                'SEPARATOR',
                self.actionAddText,
                self.actionAddPoint,
                self.actionAddPixmap,
                self.actionPaste,),
            # la barre de réglage des dessins
            self.toolBarDrawConfig: (
                self.actionPenColor,
                self.actionPenWidth,
                self.actionPenStyle,
                self.actionChooseFont,
                'SEPARATOR',
                self.actionEditText,
                'SEPARATOR',
                self.actionUndo,
                self.actionRedo,
                'SEPARATOR',
                self.actionRemoveSelected,
                self.actionRemoveLast,
                self.actionEraseAll,),
            # la barre des couleurs et tailles persos
            self.toolBarColorsSizes: (
                self.actionEditCustomColors,
                self.actionCustomColor1,
                self.actionCustomColor2,
                self.actionCustomColor3,
                self.actionCustomColor4,
                self.actionCustomColor5,
                self.actionCustomColor6, 
                self.actionCustomColor7, 
                self.actionCustomColor8, 
                self.actionCustomColor9,
                'SEPARATOR',
                self.actionEditCustomSizes,
                self.actionCustomSize1,
                self.actionCustomSize2,
                self.actionCustomSize3,
                self.actionCustomSize4,
                self.actionCustomSize5,)}
        self.allwaysActions = (
            self.actionQuit, 
            self.actionConfigure,
            self.actionHelp, 
            self.actionAbout)

        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        defaultSettings = QtCore.QSettings('libs/config.conf', QtCore.QSettings.IniFormat)
        for toolBar in self.toolBarsList:
            for action in self.toolBars[toolBar]:
                if isinstance(action, QtGui.QWidgetAction):
                    actionName = action.defaultWidget().toolTip()
                    actionText = action.defaultWidget().toolTip()
                elif isinstance(action, QtGui.QAction):
                    actionName = action.objectName()
                    actionText = action.text()
                else:
                    actionName = ''
                if action in self.actionCustomColors:
                    actionText = utils.u('{0} {1}').format(
                        QtGui.QApplication.translate('main', 'CustomColor'), 
                        self.actionCustomColors.index(action) + 1)
                if action in self.actionCustomSizes:
                    actionText = utils.u('{0} {1}').format(
                        QtGui.QApplication.translate('main', 'CustomSize'), 
                        self.actionCustomSizes.index(action) + 1)
                if (action not in self.allwaysActions) and (actionName != ''):
                    visible = settings.value(utils.u('{0}/{1}').format(toolBar.objectName(), actionName), 1)
                    if int(visible) == 0:
                        action.setVisible(False)
                    kidVisible = settings.value(utils.u('toolBarKid/{0}').format(actionName), 
                        defaultSettings.value(utils.u('toolBarKid/{0}').format(actionName)))
                    if kidVisible == None:
                        kidVisible = 0
                    if int(kidVisible) == 0:
                        kidVisible = False
                    else:
                        kidVisible = True
                    self.actionsState[action] = [actionText, action.isVisible(), kidVisible]
        self.reloadToolBars()

    def reloadToolBars(self):
        """
        Si on modifie la taille de icônes, il faut mettre à jour l'affichage
        """
        for toolBar in self.toolBars:
            #self.removeToolBar(toolBar)
            self.mustAdd = False
            toolBar.clear()
            if self.toolsKidMode:
                toolBar.setIconSize(self.main.iconSizeKid)
                toolBar.setFloatable(False)
                lastAction, lastSeparator = None, None
                for action in self.toolBars[toolBar]:
                    if action == 'SEPARATOR':
                        if lastAction != 'SEPARATOR':
                            lastSeparator = toolBar.addSeparator()
                            lastAction = action
                    elif action in self.actionsState:
                        if self.actionsState[action][2]:
                            action.setVisible(True)
                            toolBar.addAction(action)
                            self.mustAdd = True
                            lastAction = action
                        else:
                            action.setVisible(False)
                if lastAction == 'SEPARATOR':
                    toolBar.removeAction(lastSeparator)
            else:
                toolBar.setIconSize(self.main.iconSize)
                toolBar.setFloatable(True)
                lastAction, lastSeparator = None, None
                for action in self.toolBars[toolBar]:
                    if action == 'SEPARATOR':
                        if lastAction != 'SEPARATOR':
                            lastSeparator = toolBar.addSeparator()
                            lastAction = action
                    elif action in self.allwaysActions:
                        toolBar.addAction(action)
                        self.mustAdd = True
                        lastAction = action
                    elif action in self.actionsState:
                        if self.actionsState[action][1]:
                            action.setVisible(True)
                            toolBar.addAction(action)
                            self.mustAdd = True
                            lastAction = action
                        else:
                            action.setVisible(False)
                if lastAction == 'SEPARATOR':
                    toolBar.removeAction(lastSeparator)
            """
            if self.mustAdd:
                self.addToolBar(toolBar)
            """





    def disableAll(self, what=None):
        """
        Met tous les boutons de dessin à False
        Évite de le gérer pour chaque outil
        Il suffit de remettre ensuite celui choisi à True.
        Permet de n'avoir qu'un seul outil de sélectionné.
        """
        if what != None:
            checked = what.isChecked()
        actions = (
            self.actionSelect,
            self.actionDrawLine,
            self.actionDrawCurve,
            self.actionYellowHighlighterPen,
            self.actionGreenHighlighterPen,
            self.actionPinkHighlighterPen,
            self.actionBlueHighlighterPen,
            self.actionAddText,
            self.actionAddPoint,
            self.actionAddPixmap,
            self.actionPaste,)
        for action in actions:
            action.setChecked(False)
            if what != None:
                if action.text() == what.text():
                    action.setChecked(checked)
        # on ne doit plus non plus pouvoir sélectionner les items créés :
        for item in self.main.view.scene().items():
            if not(item in self.main.listeInstruments):
                item.setFlags(QtGui.QGraphicsItem.ItemIgnoresTransformations)
        # on remet le curseur par défaut :
        self.main.view.changeCursor()
        self.main.drawingMode = ('NO', None)
        if what != None:
            return checked

    def showRuler(self):
        """
        affiche ou masque la règle
        """
        WithRuler = self.actionShowRuler.isChecked()
        self.main.ruler.setVisible(WithRuler)

    def showSquare(self):
        WithSquare = self.actionShowSquare.isChecked()
        self.main.square.setVisible(WithSquare)

    def showSquareNotGraduated(self):
        WithSquareNotGraduated = self.actionShowSquareNotGraduated.isChecked()
        self.main.squareNotGraduated.setVisible(WithSquareNotGraduated)

    def showProtractor(self):
        WithProtractor = self.actionShowProtractor.isChecked()
        self.main.protractor.setVisible(WithProtractor)

    def showCompass(self):
        WithCompass = self.actionShowCompass.isChecked()
        self.main.compass.setVisible(WithCompass)

    def lockInstruments(self):
        """
        Bloque ou débloque l'utilisation des instruments
        """
        self.main.view.state['locked'] = self.actionLockInstruments.isChecked()

    def showFalseCursor(self):
        """
        On utilise ou pas le faux curseur.
        """
        utils_instruments.changeFalseCursor(self.actionShowFalseCursor.isChecked())
        self.main.myCursor.setVisible(utils_instruments.WITH_FALSE_CURSOR)
        if utils_instruments.WITH_FALSE_CURSOR:
            self.disableAll()
        else:
            self.main.view.changeCursor()

    def select(self):
        """
        On met tous les autres à False
        On met à jour drawingMode.
        Si à True, les items créés deviennent sélectionnables.
        """
        if self.disableAll(self.sender()):
            self.main.drawingMode = ('SELECT', None)
            for item in self.main.view.scene().items():
                if not(item in self.main.listeInstruments):
                    item.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)

    def drawLine(self):
        if self.disableAll(self.sender()):
            self.main.drawingMode = ('LINE', None)
            self.main.view.changeCursor('CROSS')

    def drawCurve(self):
        if self.disableAll(self.sender()):
            self.main.drawingMode = ('CURVE', None)
            self.main.view.changeCursor('CROSS')

    def highlighterPen(self):
        if self.disableAll(self.sender()):
            self.main.drawingMode = self.sender().data()
            self.main.view.changeCursor('CROSS')

    def chooseFont(self):
        try:
            self.hide()
            font, ok = QtGui.QFontDialog.getFont(self.main.view.font, self)
            if ok:
                self.main.view.font = font
        finally:
            self.show()

    def addText(self):
        if self.disableAll(self.sender()):
            self.main.drawingMode = ('TEXT', None)
            self.main.view.changeCursor('CROSS')

    def addPoint(self):
        if self.disableAll(self.sender()):
            self.main.drawingMode = ('POINT', None)
            self.main.view.changeCursor('CROSS')

    def addPixmap(self):
        if self.disableAll(self.sender()):
            self.main.drawingMode = ('PIXMAP', None)
            self.main.view.changeCursor('CROSS')

    def paste(self):
        if self.disableAll(self.sender()):
            self.main.drawingMode = ('PASTE', None)
            self.main.view.changeCursor('CROSS')



