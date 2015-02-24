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
    Contient l'interface graphique (fenêtre principale).
"""

# importation des modules utiles :
from __future__ import division, print_function
import sys

import utils, utils_config, utils_dialogs, utils_instruments, utils_graphicsview

if utils.PYSIDE:
    from PySide import QtCore, QtGui, QtSvg
else:
    from PyQt4 import QtCore, QtGui, QtSvg


class MainWindow(QtGui.QMainWindow):
    def __init__(self, lang, translator, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        """
        dd = QtGui.QApplication.desktop()
        print('screenCount : ', dd.screenCount())
        print('primaryScreen : ', dd.primaryScreen())
        print('isVirtualDesktop : ', dd.isVirtualDesktop())
        print('availableGeometry : ', dd.availableGeometry())
        for i in range(dd.screenCount()):
            print(i, 'availableGeometry : ', dd.availableGeometry(i))
        print('screenGeometry : ', dd.screenGeometry())
        for i in range(dd.screenCount()):
            print(i, 'screenGeometry : ', dd.screenGeometry(i))
        print('winId : ', dd.winId())
        """

        # Les chemins et autres trucs
        self.beginDir = QtCore.QDir.currentPath()
        self.filesDir = QtCore.QDir.homePath()
        self.appExt = QtCore.QCoreApplication.translate(
            'MainWindow', 'Pylote Files (*.plt)')
        self.backgroundsDir = self.beginDir + '/images/backgrounds'
        self.pixmapDir = self.beginDir + '/images'
        self.tempPath = utils.createTempAppDir()
        self.tempFileNum = -1

        # Un premier Screenshot avant affichage de la fenêtre
        self.backgroundPixmap = QtGui.QPixmap.grabWindow(
            QtGui.QApplication.desktop().winId())

        # Pour la fenêtre principale, l'i18n et on lit les Settings
        self.defaultFlags = self.windowFlags()
        self.setWindowFlags(self.defaultFlags | QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle(utils.PROGLABEL)
        self.translator = translator
        self.lang = lang

        # Pour l'affichage de l'image (GraphicsView) :
        self.view = utils_graphicsview.GraphicsView(self)
        self.setCentralWidget(self.view)

        # Les instruments, dans une liste (y compris le faux curseur)
        self.ruler = utils_instruments.Ruler(self)
        self.square = utils_instruments.Square(self)
        self.squareNotGraduated = utils_instruments.SquareNotGraduated(self)
        self.protractor = utils_instruments.Protractor(self)
        self.compass = utils_instruments.Compass(self)
        self.myCursor = utils_instruments.MyCursor(self)
        self.listeInstruments = (
            self.ruler, self.square, self.squareNotGraduated,
            self.protractor, self.compass, self.myCursor)
        for instrument in self.listeInstruments:
            self.view.scene().addItem(instrument)
            instrument.setVisible(False)
        self.attachDistance = 20

        self.readSettings()

        # La boîte à outils :
        self.toolsWindow = utils_dialogs.ToolsWindow(self)
        self.toolsWindow.show()
        self.toolsWindow.restoreGeometry(self.toolsWindowGeometry)
        self.toolsWindow.restoreState(self.toolsWindowState)
        self.toolsWindow.move(120, 80)
        self.firstRestore = [True, True]

        # Les actions et la TrayIcon
        self.createActions()
        if utils.WITH_TRAY_ICON:
            self.createTrayIcon()
            self.trayIcon.setIcon(QtGui.QIcon('./images/icon.png'))
            self.trayIcon.show()
            self.trayIcon.activated.connect(self.iconActivated)

        # divers
        self.brush = QtGui.QBrush()
        self.drawingMode = ('NO', None)
        self.IsMinimized = False

        self.fileName = ''
        # recherche d'un éventuel fichier plt passé en argument :
        for arg in sys.argv:
            extension = arg.split('.')[-1]
            if extension == 'plt':
                self.fileName = utils.u(arg)

        QtCore.QTimer.singleShot(1, self.firstScreenShot)
        self.toolsWindow.setFocus()

    def resizeEvent(self, event):
        """
        gestion du décalage de l'image de fond à afficher
        et affichage d'icelle
        """
        self.calculDecalage()
        brushTransform = QtGui.QTransform()
        brushTransform.translate(-self.decalX, -self.decalY)
        self.brush.setTransform(brushTransform)
        self.brush.setTexture(self.backgroundPixmap)
        self.view.scene().setBackgroundBrush(self.brush)
        # la suite a l'air nécessaire sous windows pour enlever les bordures :
        if sys.platform == 'win32':
            maskedRegion = QtGui.QRegion(
                0, 0, self.width(), self.height(), QtGui.QRegion.Rectangle)
            self.setMask(maskedRegion)

    def calculDecalage(self):
        """
        Calcul du décalage pour positionner la fenêtre
            et l'image à afficher
        Encore quelques bugs sur certains postes (windows !!!)
        """
        if utils.SCREEN_MODE == 'TESTS':
            rect = QtGui.QApplication.desktop().availableGeometry(self.screenNumber)
            self.decalX = rect.x() + (rect.width() - self.width()) // 2
            self.decalY = rect.y() + (rect.height() - self.height()) // 2
            self.move(self.decalX, self.decalY)
            self.decalX += self.width() // 2 - self.view.getContentsMargins()[0] // 2
            self.decalY += self.height() // 2 - self.view.getContentsMargins()[1] // 2
        elif utils.SCREEN_MODE == 'FULL_SPACE':
            # Position de la fenêtre en fonction de l'OS
            rect = QtGui.QApplication.desktop().availableGeometry(self.screenNumber)
            if sys.platform == 'win32':
                self.decalX = rect.x()
                self.decalY = rect.y()
                # cas windows géré à part :
                self. moveIfWin()
            else:
                self.decalX = rect.x() + (rect.width() - self.width()) // 2
                self.decalY = rect.y() + (rect.height() - self.height()) // 2                
                self.move(self.decalX, self.decalY)
            self.decalX += self.width() // 2 - self.view.getContentsMargins()[0] // 2
            self.decalY += self.height() // 2 - self.view.getContentsMargins()[1] // 2
        elif utils.SCREEN_MODE == 'FULL_SCREEN':
            self.decalX = self.width() // 2
            self.decalY = self.height() // 2
        #print('calculDecalage', self.decalX, self.decalY)

    def moveIfWin(self):
        """
        En mode FULL_SPACE, je n'arrive pas à placer correctement la fenêtre sous windows.
        Pour ce système, il vaut mieux utiliser le mode FULL_SCREEN.
        Cette procédure est donc à améliorer.
        Sous Linux, ça marche du tonnerre...
        """
        if utils.SCREEN_MODE == 'FULL_SPACE':
            origine = self.mapToGlobal(QtCore.QPoint(0, 0))
            #print(origine)
            rect = QtGui.QApplication.desktop().availableGeometry(self.screenNumber)
            """
            #print(self.view.getContentsMargins()[0])
            marge = (3 * self.view.getContentsMargins()[0],
                     3 * self.view.getContentsMargins()[1])
            #print(marge)
            self.move(rect.x() - origine.x() - marge[0],
                      rect.y() - origine.y() - marge[1])
            """
            # pourquoi 4 ?  Ça ne marche forcément pas tout le temps.
            a = 4
            self.move(
                rect.x() - origine.x() - a,
                rect.y() - origine.y() - a)

    def doMinimize(self):
        """
        Minimise toute l'interface.
        """
        self.doMinimizeToolsWindow()
        self.hide()
        self.IsMinimized = True

    def doMinimizeToolsWindow(self):
        """
        Minimise la ToolsWindow.
        Séparé de la procédure précédente car peut être appelé 
            indépendamment (double-clic par exemple).
        """
        self.toolsWindow.hide()

    def doRestore(self):
        """
        Restaure toute l'interface.
        Gestion du cas windows.
        """
        self.show()
        self.doRestoreToolsWindow()
        self.IsMinimized = False
        if sys.platform == 'win32':
            self.moveIfWin()

    def doRestoreToolsWindow(self):
        """
        Restaure la ToolsWindow.
        """
        if self.toolsWindow.toolsKidMode:
            if self.firstRestore[1]:
                self.firstRestore[1] = False
        else:
            if self.firstRestore[0]:
                self.firstRestore[0] = False
                geometry = self.toolsWindow.geometry()
                frameGeometry = self.toolsWindow.frameGeometry()
                deltaX = frameGeometry.x() - geometry.x()
                deltaY = frameGeometry.y() - geometry.y()
                self.toolsWindow.move(geometry.x() + deltaX, geometry.y() + deltaY)
        self.toolsWindow.show()

    def keyPressEvent(self, event):
        """
        La touche K bascule entre les modes "Kid" et normal.
        """
        if event.key() == QtCore.Qt.Key_K:
            self.switchKidMode()

    def switchKidMode(self):
        """
        Bascule entre les modes "Kid" et normal.
        """
        self.toolsWindow.toolsKidMode = not self.toolsWindow.toolsKidMode
        self.toolsWindow.hide()
        if self.toolsWindow.toolsKidMode:
            self.toolsWindowGeometry = self.toolsWindow.saveGeometry()
            self.toolsWindowState = self.toolsWindow.saveState()
            self.toolsWindow.setWindowFlags(self.toolsWindow.kidFlags)
            QtCore.QCoreApplication.processEvents()
            self.toolsWindow.reloadToolBars()
            self.toolsWindow.restoreGeometry(self.toolsKidWindowGeometry)
            self.toolsWindow.restoreState(self.toolsKidWindowState)
            self.toolsWindow.setMaximumWidth(self.toolsKidWindowWidth)
            self.toolsWindow.setMaximumHeight(self.toolsKidWindowHeight)
            self.toolsWindow.move(self.toolsKidWindowX, self.toolsKidWindowY)
        else:
            self.toolsKidWindowWidth = self.toolsWindow.width()
            self.toolsKidWindowHeight = self.toolsWindow.height()
            self.toolsKidWindowX = self.toolsWindow.x()
            self.toolsKidWindowY = self.toolsWindow.y()
            self.toolsKidWindowGeometry = self.toolsWindow.saveGeometry()
            self.toolsKidWindowState = self.toolsWindow.saveState()
            self.toolsWindow.setWindowFlags(self.toolsWindow.defaultFlags)
            QtCore.QCoreApplication.processEvents()
            self.toolsWindow.reloadToolBars()
            self.toolsWindow.restoreGeometry(self.toolsWindowGeometry)
            self.toolsWindow.restoreState(self.toolsWindowState)
        self.doRestoreToolsWindow()
        self.toolsWindow.repaint()
        self.toolsWindow.setMaximumWidth(16777215)
        self.toolsWindow.setMaximumHeight(16777215)

    def newScreenshot(self):
        """
        On cache l'interface, puis on lance le ScreenShot.
        """
        self.doMinimize()
        QtCore.QTimer.singleShot(self.screenShotDelay, self.shootScreen)

    def shootScreen(self):
        """
        On fait le ScreenShot
        Puis on place l'image et on réaffiche
        """
        self.backgroundPixmap = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
        brushTransform = QtGui.QTransform()
        brushTransform.translate(-self.decalX, -self.decalY)
        self.brush.setTransform(brushTransform)
        self.brush.setTexture(self.backgroundPixmap)
        self.view.scene().setBackgroundBrush(self.brush)
        self.doRestore()
        self.saveTempFile()

    def firstScreenShot(self):
        """
        On place l'image du premier ScreenShot
        """
        brushTransform = QtGui.QTransform()
        brushTransform.translate(-self.decalX, -self.decalY)
        self.brush.setTransform(brushTransform)
        self.brush.setTexture(self.backgroundPixmap)
        self.view.scene().setBackgroundBrush(self.brush)
        if self.fileName != '':
            self.fileReload()
        self.saveTempFile()

    def quit(self):
        """
        On vide le dossier temporaire.
        """
        utils.emptyDir(QtCore.QDir.tempPath() + "/" + utils.PROGNAME)
        self.close()

    def closeEvent(self, event):
        """
        On sauvegarde les Settings en quittant.
        """
        self.writeSettings()

    def readSettings(self):
        """
        Récupération des réglages.
        On ouvre aussi le fichier interne (defaultSettings) en cas de nouvelle variable
        lors d'une mise à jour du logiciel.
        """
        defaultSettings = QtCore.QSettings('libs/config.conf', QtCore.QSettings.IniFormat)
        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        version = float(settings.value('PROGVERSION', 0.0))
        if version < utils.PROGVERSION:
            settings = defaultSettings
        # variables générales :
        if utils.SCREEN_MODE == 'TESTS':
            size = settings.value('size', QtCore.QSize(600, 400))
            self.resize(size)
        self.screenNumber = int(settings.value('SCREEN_NUMBER', 0))
        utils.changeScreenNumber(self.screenNumber)
        if not(self.screenNumber < QtGui.QApplication.desktop().screenCount()):
            self.screenNumber = 0
        self.screenShotDelay = int(settings.value(
            'ScreenShotDelay', defaultSettings.value('ScreenShotDelay')))
        filesDir = settings.value('filesDir', '')
        if filesDir != '' and QtCore.QDir(filesDir).exists():
            self.filesDir = filesDir
        self.printMode = settings.value('PrintMode', 'FullPage')
        self.printOrientation = settings.value('PrintOrientation', 'Landscape')
        self.attachDistance = int(settings.value('attachDistance', 20))
        # position et état des barres d'outils :
        self.iconSize = settings.value('iconSize', defaultSettings.value('iconSize'))
        self.toolsWindowGeometry = settings.value(
            'toolsWindowGeometry', defaultSettings.value('toolsWindowGeometry'))
        self.toolsWindowState = settings.value(
            'toolsWindowState', defaultSettings.value('toolsWindowState'))
        # ToolsKidWindow :
        self.iconSizeKid = settings.value(
            'iconSizeKid', defaultSettings.value('iconSizeKid'))
        self.toolsKidWindowGeometry = settings.value(
            'toolsKidWindowGeometry', defaultSettings.value('toolsKidWindowGeometry'))
        self.toolsKidWindowState = settings.value(
            'toolsKidWindowState', defaultSettings.value('toolsKidWindowState'))
        self.toolsKidWindowWidth = int(settings.value('toolsKidWindowWidth', 250))
        self.toolsKidWindowHeight = int(settings.value('toolsKidWindowHeight', 100))
        self.toolsKidWindowX = int(settings.value('toolsKidWindowX', 100))
        self.toolsKidWindowY = int(settings.value('toolsKidWindowY', 100))
        # blocage des unités (règle et équerre) :
        unitsLocked = int(settings.value('unitsLocked', 0))
        self.unitsLocked = (unitsLocked == 1)
        self.instrumentsScale = float(settings.value('instrumentsScale', 1))
        # les pinceaux personnalisés :
        for i in range(5):
            a = 'pen{0}/'.format(i + 1)
            penWidth = int(settings.value(a + 'Width', 1))
            self.view.pens[i].setWidth(penWidth)
            try:
                penColor = QtGui.QColor(settings.value(a + 'Color'))
                self.view.pens[i].setColor(penColor)
            except:
                self.view.pens[i].setColor(QtGui.QColor())
            penStyle = int(settings.value(a + 'Style', 1))
            if penStyle == 1:
                penStyle = QtCore.Qt.SolidLine
            elif penStyle == 2:
                penStyle = QtCore.Qt.DashLine
            elif penStyle == 3:
                penStyle = QtCore.Qt.DotLine
            elif penStyle == 4:
                penStyle = QtCore.Qt.DashDotLine
            elif penStyle == 5:
                penStyle = QtCore.Qt.DashDotDotLine
            else:
                penStyle = QtCore.Qt.SolidLine
            self.view.pens[i].setStyle(penStyle)
        self.view.drawPen = self.view.pens[0]
        # police :
        font = QtGui.QFont(settings.value('font'))
        fontPointSize = int(settings.value('fontPointSize', 14))
        font.setPointSize(fontPointSize)
        self.view.font = font

    def writeSettings(self):
        """
        On sauvegarde les variables SCREEN_MODE, SCREEN_NUMBER etc...
        """
        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        settings.setValue('PROGVERSION', utils.PROGVERSION)
        # variables générales :
        if utils.SCREEN_MODE != 'TESTS':
            settings.setValue('SCREEN_MODE', utils.SCREEN_MODE)
        settings.setValue('SCREEN_NUMBER', utils.SCREEN_NUMBER)
        settings.setValue('iconSize', self.iconSize)
        settings.setValue('ScreenShotDelay', self.screenShotDelay)
        settings.setValue('filesDir', self.filesDir)
        settings.setValue('PrintMode', self.printMode)
        settings.setValue('PrintOrientation', self.printOrientation)
        settings.setValue('attachDistance', self.attachDistance)
        # position et état des barres d'outils :
        settings.setValue('toolsWindowGeometry', self.toolsWindow.saveGeometry())
        settings.setValue('toolsWindowState', self.toolsWindow.saveState())
        # ToolsKidWindow :
        settings.setValue('iconSizeKid', self.iconSizeKid)
        settings.setValue('toolsKidWindowGeometry', self.toolsKidWindowGeometry)
        settings.setValue('toolsKidWindowState', self.toolsKidWindowState)
        settings.setValue('toolsKidWindowWidth', self.toolsKidWindowWidth)
        settings.setValue('toolsKidWindowHeight', self.toolsKidWindowHeight)
        settings.setValue('toolsKidWindowX', self.toolsKidWindowX)
        settings.setValue('toolsKidWindowY', self.toolsKidWindowY)
        # visibilité des actions :
        for toolBar in self.toolsWindow.toolBarsList:
            for action in self.toolsWindow.toolBars[toolBar]:
                if action in self.toolsWindow.actionsState:
                    if isinstance(action, QtGui.QWidgetAction):
                        actionName = action.defaultWidget().toolTip()
                    elif isinstance(action, QtGui.QAction):
                        actionName = action.objectName()
                    if self.toolsWindow.actionsState[action][1]:
                        settings.setValue(
                            utils.u('{0}/{1}').format(toolBar.objectName(), actionName), 1)
                    else:
                        settings.setValue(
                            utils.u('{0}/{1}').format(toolBar.objectName(), actionName), 0)
                    if self.toolsWindow.actionsState[action][2]:
                        settings.setValue(utils.u('toolBarKid/{0}').format(actionName), 1)
                    else:
                        settings.setValue(utils.u('toolBarKid/{0}').format(actionName), 0)
        # blocage des unités (règle et équerre) :
        if self.toolsWindow.actionUnitsLock.isChecked():
            settings.setValue('unitsLocked', 1)
        else:
            settings.setValue('unitsLocked', 0)
        settings.setValue('instrumentsScale', self.instrumentsScale)
        # les pinceaux personnalisés :
        for i in range(5):
            a = 'pen{0}/'.format(i + 1)
            settings.setValue(a + 'Width', self.view.pens[i].width())
            settings.setValue(a + 'Color', self.view.pens[i].color())
            settings.setValue(a + 'Style', self.view.pens[i].style())
        # police :
        settings.setValue('font', self.view.font)
        settings.setValue('fontPointSize', self.view.font.pointSize())
        # les couleurs personnalisés :
        for action in self.toolsWindow.actionCustomColors:
            settings.setValue('custom/{0}'.format(action.objectName()), action.data())
        # les tailles personnalisés :
        for action in self.toolsWindow.actionCustomSizes:
            settings.setValue('custom/{0}'.format(action.objectName()), action.data())

    def configure(self):
        """
        Appel de la fenêtre de configuration du programme.
        """
        try:
            self.toolsWindow.hide()
            dialog = utils_config.ConfigurationDlg(parent=self)
            if dialog.exec_() == QtGui.QDialog.Accepted:
                self.toolsWindow.reloadToolBars()
                self.setWindowFlags(self.defaultFlags)
                self.calculDecalage()
                sg = QtGui.QApplication.desktop().screenGeometry(utils.SCREEN_NUMBER)
                size = sg.size()
                if utils.SCREEN_MODE == 'TESTS':
                    size = QtCore.QSize(500, 300)
                self.resize(size)
                pos = sg.topLeft()
                self.move(pos)
                self.setWindowFlags(self.defaultFlags | QtCore.Qt.FramelessWindowHint)
        finally:
            self.doRestore()
            self.toolsWindow.show()
            self.toolsWindow.repaint()

    def createDesktopFileLinux(self):
        try:
            result = False
            self.toolsWindow.hide()
            if sys.platform != 'linux2':
                print('NOT FOR THIS OS!')
                return
            title = QtCore.QCoreApplication.translate(
                'MainWindow', 'Choose the Directory where the desktop file will be created')
            directory = QtGui.QFileDialog.getExistingDirectory(
                self,
                title,
                QtCore.QDir.homePath(),
                QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly)
            if directory == '':
                return
            mustReplace = True
            # on remplacera CHEMIN par le chemin de l'installation (en enlevant le dernier /verac) :
            replaceWith = utils.u(self.beginDir)
            # on ouvre le fichier livré avec l'archive :
            desktopFileName = utils.u(self.beginDir + '/libs/Pylote.desktop')
            desktopFile = QtCore.QFile(desktopFileName)
            if not(desktopFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)):
                return
            stream = QtCore.QTextStream(desktopFile)
            stream.setCodec("UTF-8")
            lines = stream.readAll()
            # on remplace CHEMIN :
            lines = lines.replace('/CHEMIN', replaceWith)
            desktopFile.close()
            desktopFileName = utils.u('{0}/Pylote.desktop').format(directory)
            if mustReplace:
                QtCore.QFile(desktopFileName).remove()
            import io
            desktopFile = io.open(desktopFileName, 'wt', encoding='utf-8')
            for line in lines:
                desktopFile.write(line)
            desktopFile.close()
            QtCore.QFile(desktopFileName).setPermissions( \
                QtCore.QFile(desktopFileName).permissions() | \
                QtCore.QFile.ExeOwner | \
                QtCore.QFile.ExeUser | \
                QtCore.QFile.ExeGroup | \
                QtCore.QFile.ExeOther)
            result = True
        finally:
            if result == False:
                print('ERROR IN createDesktopFileLinux')
            self.toolsWindow.show()

    def createActions(self):
        """
        Ces actions sont là car elles sont disponibles depuis la trayicon
        """
        self.actionQuit = QtGui.QAction(
            QtCore.QCoreApplication.translate('MainWindow', 'Exit'), self)
        self.actionQuit.setShortcut(
            QtCore.QCoreApplication.translate('MainWindow', 'Ctrl+Q'))
        self.actionQuit.setIcon(QtGui.QIcon('images/application-exit.png'))
        self.actionQuit.triggered.connect(self.quit)

        self.actionHelp = QtGui.QAction(
            QtCore.QCoreApplication.translate('MainWindow', 'Help'), self)
        self.actionHelp.setShortcut(
            QtCore.QCoreApplication.translate('MainWindow', 'F1'))
        self.actionHelp.setIcon(QtGui.QIcon('images/help.png'))
        self.actionHelp.triggered.connect(self.helpPage)

        self.actionAbout = QtGui.QAction(
            QtCore.QCoreApplication.translate('MainWindow', 'About'), self)
        self.actionAbout.setIcon(QtGui.QIcon('images/help-about.png'))
        self.actionAbout.triggered.connect(self.about)

        self.actionNewScreenshot = QtGui.QAction(
            QtCore.QCoreApplication.translate('MainWindow', 'newScreenshot'), self)
        self.actionNewScreenshot.setIcon(QtGui.QIcon('images/camera.png'))
        self.actionNewScreenshot.triggered.connect(self.newScreenshot)

        self.minimizeAction = QtGui.QAction(
            QtCore.QCoreApplication.translate('MainWindow', 'Minimize'), self)
        self.minimizeAction.triggered.connect(self.doMinimize)

        self.restoreAction = QtGui.QAction(
            QtCore.QCoreApplication.translate('MainWindow', 'Restore'), self)
        self.restoreAction.triggered.connect(self.doRestore)

    def createTrayIcon(self):
        """
        Création de la trayicon et de son menu (obtenu par clic droit).
        """
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.actionHelp)
        self.trayIconMenu.addAction(self.actionAbout)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.actionNewScreenshot)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.minimizeAction)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.actionQuit)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def iconActivated(self, reason):
        """
        Séparation entre clic et double-clic (grâce à la variable iconDoubleClick).
        Un double-clic relance le screenshot.
        Le simple clic est géré après.
        """
        self.iconDoubleClick = False
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.iconDoubleClick = True
            self.newScreenshot()
        elif reason == QtGui.QSystemTrayIcon.Trigger:
            QtCore.QTimer.singleShot(500, self.iconClick)

    def iconClick(self):
        """
        Si on a bien à faire à un simple clic,
            on minimise ou restaure l'application.
        """
        if self.iconDoubleClick == False:
            if self.IsMinimized:
                self.doRestore()
            else:
                self.doMinimize()

    def unitsActions(self):
        """
        Gestion des actions (Save, Restore, Init) liées aux unités des instruments.
        """
        what = self.sender().objectName()
        if what == 'UnitsSave':
            self.instrumentsScale = self.ruler.scale()
        elif what == 'UnitsRestore':
            for instrument in self.listeInstruments:
                if instrument.units:
                    instrument.setScale(self.instrumentsScale)
        elif what == 'UnitsInit':
            #self.instrumentsScale = 1
            for instrument in self.listeInstruments:
                if instrument.units:
                    instrument.setScale(1)

    def eraseAll(self, doSave=True):
        """
        Efface tous les items.
        """
        for item in self.view.scene().items():
            if not(item in self.listeInstruments):
                try:
                    data = int(item.data(QtCore.Qt.UserRole))
                    self.view.scene().removeItem(item)
                    del item
                except:
                    pass
        if doSave:
            self.saveTempFile()

    def removeLast(self):
        """
        Efface le dernier item.
        """
        draws = []
        for item in self.view.scene().items():
            if not(item in self.listeInstruments):
                try:
                    data = int(item.data(QtCore.Qt.UserRole))
                    draws.append((item, data))
                except:
                    pass
        draws = sorted(draws, key=lambda data: data[1])
        if len(draws) > 0:
            item = draws[-1][0]
            self.view.scene().removeItem(item)
            del item
            self.saveTempFile()

    def removeSelected(self):
        """
        Supprime l'item sélectionné, après demande de confirmation.
        """
        item = self.view.state['selected']
        if item != None:
            try:
                self.toolsWindow.hide()
                data = int(item.data(QtCore.Qt.UserRole))
                if QtGui.QMessageBox.question(
                    self, utils.PROGLABEL,
                    QtCore.QCoreApplication.translate('MainWindow', 'Delete this item ?'),
                    QtGui.QMessageBox.Yes|QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                    self.view.scene().removeItem(item)
                    del item
                self.view.state['selected'] = None
            except:
                pass
            finally:
                self.saveTempFile()
                self.toolsWindow.show()

    def editText(self):
        """
        Édition d'un texte ou du nom d'un point.
        """
        result = False
        item = self.view.state['selected']
        if item != None:
            if isinstance(item, QtGui.QGraphicsTextItem):
                result = True
                try:
                    self.toolsWindow.hide()
                    # pour distinguer entre un texte et un point :
                    isText = (item.data(QtCore.Qt.UserRole) != None)
                    initialText = item.toPlainText()
                    if isText:
                        dialog = utils_dialogs.TextItemDlg(
                            parent=self.view, graphicsTextItem=item)
                        if dialog.exec_() != QtGui.QDialog.Accepted:
                            item.setPlainText(initialText)
                        else:
                            self.saveTempFile()
                    else:
                        text, ok = QtGui.QInputDialog.getText(
                            self, 
                            utils.PROGLABEL,
                            QtCore.QCoreApplication.translate('MainWindow', 'Point Name:'), 
                            QtGui.QLineEdit.Normal,
                            initialText)
                        if ok:
                            item.setPlainText(text)
                            item.parentItem().text = text
                            self.saveTempFile()
                finally:
                    self.toolsWindow.show()
        return result

    def whitePage(self):
        """
        Affiche une page blanche
        """
        self.backgroundPixmap = QtGui.QPixmap()
        self.brush.setTexture(self.backgroundPixmap)
        self.view.scene().setBackgroundBrush(self.brush)
        self.saveTempFile()

    def pointsPage(self):
        """
        Affiche une page de type papier pointé
        """
        image = QtGui.QImage('images/backgrounds/dots.svg')
        self.backgroundPixmap = QtGui.QPixmap.fromImage(image)
        self.brush.setTexture(self.backgroundPixmap)
        self.view.scene().setBackgroundBrush(self.brush)
        self.saveTempFile()

    def gridPage(self):
        """
        Affiche une grille
        """
        image = QtGui.QImage('images/backgrounds/grid.svg')
        self.backgroundPixmap = QtGui.QPixmap.fromImage(image)
        self.brush.setTexture(self.backgroundPixmap)
        self.view.scene().setBackgroundBrush(self.brush)
        self.saveTempFile()

    def chooseBackGround(self):
        """
        On sélectionne une image de fond
        """
        try:
            self.toolsWindow.hide()
            fileName = QtGui.QFileDialog.getOpenFileName(
                self, 
                QtCore.QCoreApplication.translate(
                    'MainWindow', 'Open Image'),
                self.backgroundsDir, 
                QtCore.QCoreApplication.translate(
                    'MainWindow', 'Image Files (*.png *.jpg *.jpeg *.svg)'))
            # pour PySide :
            if isinstance(fileName, tuple):
                fileName = fileName[0]
            if fileName == '':
                return
            self.backgroundsDir = QtCore.QFileInfo(fileName).absolutePath()
            image = QtGui.QImage(fileName)
            self.backgroundPixmap = QtGui.QPixmap.fromImage(image)
            brushTransform = QtGui.QTransform()
            brushTransform.translate(-self.decalX, -self.decalY)
            self.brush.setTransform(brushTransform)
            self.brush.setTexture(self.backgroundPixmap)
            self.view.scene().setBackgroundBrush(self.brush)
            self.saveTempFile()
        finally:
            self.toolsWindow.show()

    def fileSave(self):
        if self.fileName == '':
            self.fileSaveAs()
        else:
            try:
                self.toolsWindow.hide()
                self.saveFile(self.fileName)
            finally:
                self.toolsWindow.show()

    def selectFileName(self, title, proposedName, extension):
        fileName = QtGui.QFileDialog.getSaveFileName(self, title, proposedName, extension)
        # pour PySide :
        if isinstance(fileName, tuple):
            fileName = fileName[0]
        return fileName

    def fileSaveAs(self):
        """
        Enregistrement d'un fichier.
        On sauve le titre du programme en entête, 
            le fond et les items (sauf les instruments).
        """
        try:
            self.toolsWindow.hide()
            fileName = self.selectFileName(
                QtCore.QCoreApplication.translate('MainWindow', 'Save File'), 
                self.filesDir, 
                self.appExt)
            if fileName == '':
                return
            utils.doWaitCursor()
            fileName = utils.verifieExtension(fileName, 'plt')
            self.saveFile(fileName)
            self.filesDir = QtCore.QFileInfo(fileName).absolutePath()
            self.fileName = fileName
            baseName = QtCore.QFileInfo(fileName).baseName()
            title = utils.u('{0} [{1}]').format(
                QtCore.QCoreApplication.translate('MainWindow', 'Tools'), baseName)
            self.toolsWindow.setWindowTitle(title)
        finally:
            utils.restoreCursor()
            self.toolsWindow.show()

    def saveFile(self, fileName):
        outFile = QtCore.QFile(fileName)
        if not outFile.open(QtCore.QFile.WriteOnly):
            QtGui.QMessageBox.warning(
                self, utils.PROGLABEL,
                QtCore.QCoreApplication.translate(
                    'MainWindow', 'Failed to save\n  {0}').format(self.fileName))
            return
        try:
            stream = QtCore.QDataStream(outFile)
            stream.setVersion(QtCore.QDataStream.Qt_4_6)
            stream.writeQString('{0}_{1}'.format(utils.PROGNAME, utils.PROGVERSION))
            stream << self.brush
            # on trie pour enregistrer dans l'ordre de création :
            draws = []
            for item in self.view.scene().items():
                if not(item in self.listeInstruments):
                    try:
                        data = int(item.data(QtCore.Qt.UserRole))
                        draws.append((item, data))
                    except:
                        pass
            draws = sorted(draws, key=lambda data: data[1])
            for (item, data) in draws:
                # pour chaque item, on enregistre son type (Point, ...) 
                # puis les attributs utiles
                if isinstance(item, utils_instruments.PointItem):
                    stream.writeQString('Point')
                    stream << item.pos() << item.sceneTransform() \
                        << item.pen() << item.brush() << item.font
                    stream.writeQString(item.text)
                    stream << item.textItem.pos() << item.textItem.itemTransform(item)[0]
                elif isinstance(item, QtGui.QGraphicsTextItem):
                    stream.writeQString('Text')
                    stream << item.pos() << item.sceneTransform() \
                            << item.font()  << item.defaultTextColor()
                    stream.writeQString(item.toPlainText())
                elif isinstance(item, QtGui.QGraphicsPixmapItem):
                    stream.writeQString('Pixmap')
                    stream << item.pos() << item.sceneTransform() << item.pixmap()
                elif isinstance(item, QtGui.QGraphicsPathItem):
                    stream.writeQString('Path')
                    stream << item.pos() << item.sceneTransform() \
                        << item.pen() << item.path()
                elif isinstance(item, QtGui.QGraphicsLineItem):
                    stream.writeQString('Line')
                    stream << item.pos() << item.sceneTransform() \
                            << item.pen() << item.line()
        except:
            QtGui.QMessageBox.warning(
                self, utils.PROGLABEL,
                QtCore.QCoreApplication.translate(
                    'MainWindow', 'Failed to save\n  {0}').format(self.fileName))
        finally:
            outFile.close()

    def saveTempFile(self):
        self.tempFileNum += 1
        if self.tempFileNum < 10:
            fileName = utils.u('{0}/000{1}.plt').format(self.tempPath, self.tempFileNum)
        elif self.tempFileNum < 100:
            fileName = utils.u('{0}/00{1}.plt').format(self.tempPath, self.tempFileNum)
        elif self.tempFileNum < 1000:
            fileName = utils.u('{0}/0{1}.plt').format(self.tempPath, self.tempFileNum)
        else:
            fileName = utils.u('{0}/{1}.plt').format(self.tempPath, self.tempFileNum)
        self.saveFile(fileName)

    def undo(self):
        self.tempFileNum -= 1
        if self.tempFileNum < 0:
            self.tempFileNum = 0
        if self.tempFileNum < 10:
            fileName = utils.u('{0}/000{1}.plt').format(self.tempPath, self.tempFileNum)
        elif self.tempFileNum < 100:
            fileName = utils.u('{0}/00{1}.plt').format(self.tempPath, self.tempFileNum)
        elif self.tempFileNum < 1000:
            fileName = utils.u('{0}/0{1}.plt').format(self.tempPath, self.tempFileNum)
        else:
            fileName = utils.u('{0}/{1}.plt').format(self.tempPath, self.tempFileNum)
        self.openFile(fileName, doSave=False)

    def redo(self):
        self.tempFileNum += 1
        if self.tempFileNum < 10:
            fileName = utils.u('{0}/000{1}.plt').format(self.tempPath, self.tempFileNum)
        elif self.tempFileNum < 100:
            fileName = utils.u('{0}/00{1}.plt').format(self.tempPath, self.tempFileNum)
        elif self.tempFileNum < 1000:
            fileName = utils.u('{0}/0{1}.plt').format(self.tempPath, self.tempFileNum)
        else:
            fileName = utils.u('{0}/{1}.plt').format(self.tempPath, self.tempFileNum)
        if QtCore.QFileInfo(fileName).exists():
            self.openFile(fileName, doSave=False)
        else:
            self.tempFileNum -= 1

    def fileOpen(self):
        """
        Ouverture d'un fichier.
        On sélectionne puis on délègue à la fonction fileReload.
        """
        try:
            self.toolsWindow.hide()
            fileName = QtGui.QFileDialog.getOpenFileName(
                self,
                QtCore.QCoreApplication.translate('MainWindow', 'Open File'),
                self.filesDir,
                self.appExt)
            # pour PySide :
            if isinstance(fileName, tuple):
                fileName = fileName[0]
            if fileName == '':
                return
            self.fileName = fileName
            self.fileReload()
        finally:
            self.toolsWindow.show()

    def fileReload(self):
        """
        Réouverture du fichier. On commence par effacer tout.
        On vérifie l'entête, puis on récupère le fond et les items.
        """
        if self.fileName != '':
            self.filesDir = QtCore.QFileInfo(self.fileName).absolutePath()
            self.openFile(self.fileName)
            baseName = QtCore.QFileInfo(self.fileName).baseName()
            title = utils.u('{0} [{1}]').format(
                QtCore.QCoreApplication.translate('MainWindow', 'Tools'), baseName)
            self.toolsWindow.setWindowTitle(title)
        else:
            self.eraseAll()
        if self.toolsWindow.actionSelect.isChecked():
            self.toolsWindow.select()

    def openFile(self, fileName, doSave=True):
        inFile = None
        try:
            inFile = QtCore.QFile(fileName)
            inFile.open(QtCore.QIODevice.ReadOnly)
            self.eraseAll(doSave=doSave)
            stream = QtCore.QDataStream(inFile)
            progNameVersion = stream.readQString()
            if not(utils.PROGNAME in progNameVersion):
                QtGui.QMessageBox.warning(
                    self, utils.PROGLABEL,
                    QtCore.QCoreApplication.translate('MainWindow', 'not a valid file'))
                return
            if progNameVersion == utils.PROGNAME:
                progVersion = 0
            else:
                progVersion = int(10 * float(progNameVersion[-3:]))
            if progVersion < 14:
                stream.setVersion(QtCore.QDataStream.Qt_4_2)
            else:
                stream.setVersion(QtCore.QDataStream.Qt_4_6)
            self.readBackgroundFromStream(stream, progVersion)
            while not inFile.atEnd():
                self.readItemFromStream(stream, progVersion)
        except:
            QtGui.QMessageBox.warning(
                self, utils.PROGLABEL,
                QtCore.QCoreApplication.translate('MainWindow', 'Failed to open\n  {0}').format(fileName))
        finally:
            if inFile != None:
                inFile.close()

    def fileGoPrevious(self):
        if self.fileName != '':
            listFiles = []
            dirIterator = QtCore.QDirIterator(self.filesDir, 
                                            ['*.plt'], 
                                            QtCore.QDir.Files)
            while dirIterator.hasNext():
                listFiles.append(dirIterator.next())
            listFiles = sorted(listFiles)
            i = listFiles.index(self.fileName)
            if i > 0:
                self.fileName = listFiles[i - 1]
                self.fileReload()

    def fileGoNext(self):
        if self.fileName != '':
            listFiles = []
            dirIterator = QtCore.QDirIterator(self.filesDir, 
                                            ['*.plt'], 
                                            QtCore.QDir.Files)
            while dirIterator.hasNext():
                listFiles.append(dirIterator.next())
            listFiles = sorted(listFiles)
            i = listFiles.index(self.fileName)
            if i < len(listFiles) - 1:
                self.fileName = listFiles[i + 1]
                self.fileReload()

    def exportToPainter(self, what, export='SVG'):
        """
        Crée un painter pour le paramètre what et dessine dessus.
        Retourne le painter.
        what peut être un générateur de SVG, un printer (imprimante ou PDF)
        """
        if export == 'SVG':
            scale = 1
            what.setSize(self.view.size())
            what.setResolution(1.25 * what.resolution())
        elif self.printMode == 'FullPage':
            scale = what.pageRect().width() / self.view.width()
            yscale = what.pageRect().height() / self.view.height()
            if yscale < scale:
                scale = yscale
        else:
            paperWidth = what.paperSize(QtGui.QPrinter.Millimeter).width()
            pageWidth = what.pageRect(QtGui.QPrinter.Millimeter).width() \
                        - what.pageRect(QtGui.QPrinter.Millimeter).left()
            scale = paperWidth / pageWidth
            #print('paperWidth :', paperWidth)
            #print('pageWidth :', pageWidth)
            #print('scale :', scale)

        def drawTextToPainter(painter, textItem):
            """
            la taille et la position sont modifiées (pourquoi et comment ?)
            Les 2 variables ont été trouvés par tests (mais sont elles universelles ?)
            """
            if export == 'SVG':
                decalageFont = 3
                coeffFont = 1#1.3333
            elif export in ('PDF', 'PRINT'):
                decalageFont = 5
                coeffFont = 1.3333#1.02
            painter.setPen(QtGui.QPen(textItem.defaultTextColor()))
            font = textItem.font()
            font.setPointSizeF(font.pointSize() * coeffFont / scale)
            painter.setFont(font)
            boundingRect = textItem.boundingRect()
            boundingRect.setWidth(boundingRect.width() * scale)
            boundingRect.setHeight(boundingRect.height() * scale)
            boundingRect.setX(decalageFont)
            boundingRect.setY(decalageFont)
            painter.drawText(boundingRect, textItem.toPlainText())

        painter = QtGui.QPainter(what)
        painter.scale(scale, scale)
        # vérifier encore le décalage :
        origineX = self.view.width() // 2 - self.decalX
        origineY = self.view.height() // 2 - self.decalY
        brushWidth = self.brush.texture().width()
        if brushWidth == 0:
            brushWidth = 1
        brushHeight = self.brush.texture().height()
        if brushHeight == 0:
            brushHeight = 1
        columns = self.view.width() // brushWidth
        rows = self.view.height() // brushHeight
        for i in range(columns):
            for j in range(rows):
                decalage = QtCore.QPoint(origineX + i * brushWidth, origineY + j * brushHeight)
                painter.drawPixmap(decalage, self.brush.texture())

        draws = []
        for item in self.view.scene().items():
            if not(item in self.listeInstruments):
                try:
                    data = int(item.data(QtCore.Qt.UserRole))
                    draws.append((item, data))
                except:
                    pass
        draws = sorted(draws, key=lambda data: data[1])
        originPoint = QtCore.QPoint(self.size().width() // 2, self.size().height() // 2)
        for (item, data) in draws:
            painter.resetTransform()
            painter.scale(scale, scale)
            painter.translate(originPoint)
            if isinstance(item, utils_instruments.PointItem):
                painter.setTransform(item.sceneTransform(), True)
                painter.setPen(item.pen())
                painter.setBrush(item.brush())
                painter.drawPath(item.path)
                painter.resetTransform()
                painter.scale(scale, scale)
                painter.translate(originPoint)
                painter.setTransform(item.textItem.sceneTransform(), True)
                drawTextToPainter(painter, item.textItem)
            elif isinstance(item, QtGui.QGraphicsTextItem):
                painter.setTransform(item.sceneTransform(), True)
                drawTextToPainter(painter, item)
            elif isinstance(item, QtGui.QGraphicsPixmapItem):
                painter.setTransform(item.sceneTransform(), True)
                #painter.drawPixmap(item.pos(), item.pixmap())
                painter.drawPixmap(0, 0, item.pixmap())
            elif isinstance(item, QtGui.QGraphicsPathItem):
                painter.setTransform(item.sceneTransform(), True)
                painter.setPen(item.pen())
                painter.setBrush(item.brush())
                painter.drawPath(item.path())
            elif isinstance(item, QtGui.QGraphicsLineItem):
                painter.setTransform(item.sceneTransform(), True)
                painter.setPen(item.pen())
                painter.drawLine(item.line())
        painter.end()

    def createPrinter(self, fileName='', direct=False):
        """
        Initialisation d'un printer.
        Si fileName != '', on fait un PDF
        """
        result = False
        utils.doWaitCursor()
        try:
            printer = QtGui.QPrinter(QtGui.QPrinter.ScreenResolution)#QtGui.QPrinter.HighResolution)
            printer.setPaperSize(QtGui.QPrinter.A4)
            #printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
            printer.setOutputFormat(QtGui.QPrinter.NativeFormat)
            if self.printOrientation == 'Portrait':
                printer.setOrientation(QtGui.QPrinter.Portrait)
            else:
                printer.setOrientation(QtGui.QPrinter.Landscape)
            #printer.setFullPage(True)
            #printer.setPageMargins(10.0, 10.0, 10.0, 10.0, QtGui.QPrinter.Millimeter)
            result = printer
            if fileName != '':
                # on veut un PDF :
                printer.setOutputFormat(QtGui.QPrinter.PdfFormat)
                printer.setOutputFileName(fileName)
            elif not(direct):
                # on lance le dialog d'impression :
                utils.restoreCursor()
                printDialog = QtGui.QPrintDialog(printer)
                if printDialog.exec_() != QtGui.QDialog.Accepted:
                    result = False
                utils.doWaitCursor()
        finally:
            utils.restoreCursor()
            return result

    def exportSvg(self):
        """
        Export du fichier en svg, pour réutilisation dans Inkscape par exemple.
        """
        try:
            self.toolsWindow.hide()
            self.svgTitle = QtCore.QCoreApplication.translate(
                'MainWindow', 'Export as SVG File')
            self.svgExt = QtCore.QCoreApplication.translate(
                'MainWindow', 'SVG Files (*.svg)')
            if self.fileName != '':
                baseName = QtCore.QFileInfo(self.fileName).baseName()
                proposedName = utils.u('{0}/{1}.svg').format(self.filesDir, baseName)
            else:
                proposedName = self.filesDir
            fileName = self.selectFileName(self.svgTitle, proposedName, self.svgExt)
            if fileName == '':
                return
            utils.doWaitCursor()
            fileName = utils.verifieExtension(fileName, 'svg')
            self.filesDir = QtCore.QFileInfo(fileName).absolutePath()
            generator = QtSvg.QSvgGenerator()
            generator.setFileName(fileName)
            self.exportToPainter(generator)
        finally:
            utils.restoreCursor()
            self.toolsWindow.show()

    def exportPdf(self):
        try:
            self.toolsWindow.hide()
            self.pdfTitle = QtCore.QCoreApplication.translate(
                'MainWindow', 'Export as PDF File')
            self.pdfExt = QtCore.QCoreApplication.translate(
                'MainWindow', 'PDF Files (*.pdf)')
            if self.fileName != '':
                baseName = QtCore.QFileInfo(self.fileName).baseName()
                proposedName = utils.u('{0}/{1}.pdf').format(self.filesDir, baseName)
            else:
                proposedName = self.filesDir
            fileName = self.selectFileName(self.pdfTitle, proposedName, self.pdfExt)
            if fileName == '':
                return
            utils.doWaitCursor()
            fileName = utils.verifieExtension(fileName, 'pdf')
            self.filesDir = QtCore.QFileInfo(fileName).absolutePath()
            printer = self.createPrinter(fileName)
            if printer == False:
                return
            self.exportToPainter(printer, export='PDF')
        finally:
            utils.restoreCursor()
            self.toolsWindow.show()

    def documentPrint(self):
        try:
            self.toolsWindow.hide()
            printer = self.createPrinter()
            if printer == False:
                return
            self.exportToPainter(printer, export='PRINT')
        finally:
            self.toolsWindow.show()

    def documentPrintDirect(self):
        printer = self.createPrinter(direct=True)
        if printer == False:
            return
        self.exportToPainter(printer, export='PRINT')













    def readBackgroundFromStream(self, stream, progVersion):
        """
        On applique le fond du fichier
        """
        stream >> self.brush
        brushTransform = QtGui.QTransform()
        brushTransform.translate(-self.decalX, -self.decalY)
        self.brush.setTransform(brushTransform)
        self.view.scene().setBackgroundBrush(self.brush)

    def readItemFromStream(self, stream, progVersion):
        """
        Récupération des items et création
        """
        itemType = ''
        position = QtCore.QPointF()
        transform = QtGui.QTransform()
        itemType = stream.readQString()
        if progVersion < 1:
            matrix = QtGui.QMatrix()
            stream >> position >> matrix
        else:
            stream >> position >> transform
        if itemType == 'Point':
            pen = QtGui.QPen()
            brush = QtGui.QBrush()
            font = QtGui.QFont()
            text = ''
            textPos = QtCore.QPointF()
            stream >> pen >> brush >> font
            text = stream.readQString()
            stream >> textPos
            item = utils_instruments.PointItem(self, pen, brush, font, text)
            self.view.scene().addItem(item)
            if progVersion < 14:
                item.setPos(position)
                item.textItem.setPos(textPos)
            else:
                textTransform = QtGui.QTransform()
                stream >> textTransform
                item.setTransform(transform)
                item.textItem.setTransform(textTransform)
                textPos = QtCore.QPointF(0, 0)
                item.textItem.setPos(textPos)
            self.view.drawId += 1
            item.setData(QtCore.Qt.UserRole, self.view.drawId)
            item.setTransformOriginPoint(item.boundingRect().center())
        elif itemType == 'Text':
            font = QtGui.QFont()
            color = QtGui.QColor()
            text = ''
            stream >> font >> color
            text = stream.readQString()
            item = QtGui.QGraphicsTextItem()
            item.setPlainText(text)
            item.setFont(font)
            self.view.scene().addItem(item)
            item.setDefaultTextColor(color)
            if progVersion < 14:
                item.setPos(position)
            else:
                item.setTransform(transform)
            self.view.drawId += 1
            item.setData(QtCore.Qt.UserRole, self.view.drawId)
            item.setTransformOriginPoint(item.boundingRect().center())
        elif itemType == 'Pixmap':
            pixmap = QtGui.QPixmap()
            stream >> pixmap
            item = QtGui.QGraphicsPixmapItem(pixmap)
            self.view.scene().addItem(item)
            if progVersion < 14:
                item.setPos(position)
            else:
                item.setTransform(transform)
            self.view.drawId += 1
            item.setData(QtCore.Qt.UserRole, self.view.drawId)
            item.setTransformOriginPoint(item.boundingRect().center())
        elif itemType == 'Path':
            pen = QtGui.QPen()
            brush = QtGui.QBrush(QtCore.Qt.green, QtCore.Qt.NoBrush)
            path = QtGui.QPainterPath()
            stream >> pen >> path
            item = self.view.scene().addPath(path, pen, brush)
            if progVersion < 14:
                item.setPos(position)
            else:
                item.setTransform(transform)
            self.view.drawId += 1
            item.setData(QtCore.Qt.UserRole, self.view.drawId)
            item.setTransformOriginPoint(item.boundingRect().center())
        elif itemType == 'Line':
            pen = QtGui.QPen()
            line = QtCore.QLineF()
            stream >> pen >> line
            item = self.view.scene().addLine(line, pen)
            if progVersion < 14:
                item.setPos(position)
            else:
                item.setTransform(transform)
            self.view.drawId += 1
            item.setData(QtCore.Qt.UserRole, self.view.drawId)
            item.setTransformOriginPoint(item.boundingRect().center())

    def about(self):
        """
        Affiche la fenêtre À propos
        """
        try:
            self.toolsWindow.hide()
            import utils_about
            aboutdialog = utils_about.AboutDlg(self, self.lang, icon='./images/icon.png')
            aboutdialog.exec_()
        finally:
            self.toolsWindow.show()

    def helpPage(self):
        """
        Affiche la page d'aide dans le navigateur.
        """
        theUrl = utils.HELPPAGE
        utils.webhelp_in_browser(theUrl)

