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
    La fenêtre de configuration.
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

                DIALOG DE CONFIGURATION

###########################################################
###########################################################
"""

class ScreenPage(QtGui.QWidget):
    """
    Configuration de l'écran :
        variable globale SCREEN_MODE
        variable globale SCREEN_NUMBER
    """
    def __init__(self, parent=None):
        super(ScreenPage, self).__init__(parent)
        self.main = parent.main

        # configuration de la variable globale SCREEN_MODE :
        groupBoxScreenMode = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'ScreenMode')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b></p>').format(title))
        radio1 = QtGui.QRadioButton(QtGui.QApplication.translate('main', 'FullSpace'))
        self.radioScreenMode = QtGui.QRadioButton(QtGui.QApplication.translate('main', 'FullScreen'))
        if utils.SCREEN_MODE == 'FULL_SCREEN': 
            self.radioScreenMode.setChecked(True)
        else:
            radio1.setChecked(True)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addWidget(radio1)
        vLayout.addWidget(self.radioScreenMode)
        vLayout.addStretch(1)
        groupBoxScreenMode.setLayout(vLayout)
        bigEditorScreenMode = QtGui.QTextEdit()
        bigEditorScreenMode.setReadOnly(True)
        bigEditorScreenMode.setText(
            QtGui.QApplication.translate('main', ''
                    '<p align=left><b>FullSpace: </b>'
                    'the application use all the free space on desktop.</p>'
                    '<p></p>'
                    '<p align=left><b>FullScreen: </b>'
                    'choose this if you ave problems with FullSpace mode.</p>'
                    '<p></p>'
                    '<p align=center><b>If you change this, you need to restart application.</b></p>'))
        # configuration de la variable globale SCREEN_NUMBER :
        groupBoxScreenNumber = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'ScreenNumber')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b></p>').format(title))
        self.comboBoxScreenNumber = QtGui.QComboBox()
        total = QtGui.QApplication.desktop().screenCount()
        if utils.SCREEN_NUMBER >= total:
            total = utils.SCREEN_NUMBER + 1
        for i in range(total):
            self.comboBoxScreenNumber.addItem(utils.u('{0} {1}').format(QtGui.QApplication.translate('main', 'Screen'), i), i)
        self.comboBoxScreenNumber.setCurrentIndex(utils.SCREEN_NUMBER)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addWidget(self.comboBoxScreenNumber)
        vLayout.addStretch(1)
        groupBoxScreenNumber.setLayout(vLayout)
        bigEditorScreenNumber = QtGui.QTextEdit()
        bigEditorScreenNumber.setReadOnly(True)
        bigEditorScreenNumber.setText(
            QtGui.QApplication.translate('main', '<P></P>'
                    '<P ALIGN=LEFT>Here you can select on which screen you will to work.</P>'))

        # mise en place :
        layout = QtGui.QGridLayout()
        layout.addWidget(groupBoxScreenMode,        0, 0)
        layout.addWidget(bigEditorScreenMode,       0, 1)
        layout.addWidget(groupBoxScreenNumber,      1, 0)
        layout.addWidget(bigEditorScreenNumber,     1, 1)
        self.setLayout(layout)


class ToolsWindowPage(QtGui.QWidget):
    """
    Configuration de la fenêtre d'outils :
        iconSize
        actions affichées dans les toolsBars
    """
    def __init__(self, parent=None):
        super(ToolsWindowPage, self).__init__(parent)
        self.main = parent.main

        # configuration de la variable iconSize :
        groupBoxIconSize = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'IconSize')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b></p>').format(title))
        integerLabel = QtGui.QLabel(QtGui.QApplication.translate('main', 
            'Enter a value between {0} and {1}:').format(8, 128))
        self.integerSpinBoxIconSize = QtGui.QSpinBox()
        self.integerSpinBoxIconSize.setRange(8, 128)
        self.integerSpinBoxIconSize.setSingleStep(1)
        self.integerSpinBoxIconSize.setValue(self.main.iconSize.width())
        hLayout = QtGui.QHBoxLayout()
        hLayout.addWidget(integerLabel)
        hLayout.addWidget(self.integerSpinBoxIconSize)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        groupBoxIconSize.setLayout(vLayout)

        # configuration des actions visibles dans les toolBars :
        groupBoxVisibleActions = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'VisibleActions')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b></p>').format(title))
        self.toolbarActionsList = QtGui.QListWidget()
        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        for toolBar in self.main.toolsWindow.toolBarsList:
            item = QtGui.QListWidgetItem(utils.u('{0} :').format(toolBar.windowTitle()))
            item.setFont(boldFont)
            self.toolbarActionsList.addItem(item)
            for action in self.main.toolsWindow.toolBars[toolBar]:
                if action in self.main.toolsWindow.actionsState:
                    actionName = self.main.toolsWindow.actionsState[action][0]
                    if isinstance(action, QtGui.QWidgetAction):
                        item = QtGui.QListWidgetItem(action.defaultWidget().itemIcon(0), actionName)
                    elif isinstance(action, QtGui.QAction):
                        item = QtGui.QListWidgetItem(action.icon(), actionName)
                    if self.main.toolsWindow.actionsState[action][1]:
                        item.setCheckState(QtCore.Qt.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)
                    item.setData(QtCore.Qt.UserRole, action)
                    self.toolbarActionsList.addItem(item)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addWidget(self.toolbarActionsList)
        groupBoxVisibleActions.setLayout(vLayout)

        # mise en place :
        layout = QtGui.QVBoxLayout()
        layout.addWidget(groupBoxIconSize)
        layout.addWidget(groupBoxVisibleActions)
        self.setLayout(layout)


class KidWindowPage(QtGui.QWidget):
    """
    Configuration de la fenêtre d'outils :
        iconSize
        actions affichées dans les toolsBars
    """
    def __init__(self, parent=None):
        super(KidWindowPage, self).__init__(parent)
        self.main = parent.main

        # configuration de la variable iconSize :
        groupBoxIconSize = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'IconSize')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b></p>').format(title))
        integerLabel = QtGui.QLabel(QtGui.QApplication.translate('main', 
            'Enter a value between {0} and {1}:').format(8, 128))
        self.integerSpinBoxIconSize = QtGui.QSpinBox()
        self.integerSpinBoxIconSize.setRange(8, 128)
        self.integerSpinBoxIconSize.setSingleStep(1)
        self.integerSpinBoxIconSize.setValue(self.main.iconSizeKid.width())
        hLayout = QtGui.QHBoxLayout()
        hLayout.addWidget(integerLabel)
        hLayout.addWidget(self.integerSpinBoxIconSize)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        groupBoxIconSize.setLayout(vLayout)

        # configuration des actions visibles dans les toolBars :
        groupBoxVisibleActions = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'VisibleActions')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b></p>').format(title))
        self.toolbarActionsList = QtGui.QListWidget()
        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        for toolBar in self.main.toolsWindow.toolBarsList:
            item = QtGui.QListWidgetItem(utils.u('{0} :').format(toolBar.windowTitle()))
            item.setFont(boldFont)
            self.toolbarActionsList.addItem(item)
            for action in self.main.toolsWindow.toolBars[toolBar]:
                if action in self.main.toolsWindow.actionsState:
                    actionName = self.main.toolsWindow.actionsState[action][0]
                    if isinstance(action, QtGui.QWidgetAction):
                        item = QtGui.QListWidgetItem(action.defaultWidget().itemIcon(0), actionName)
                    elif isinstance(action, QtGui.QAction):
                        item = QtGui.QListWidgetItem(action.icon(), actionName)
                    if self.main.toolsWindow.actionsState[action][2]:
                        item.setCheckState(QtCore.Qt.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)
                    item.setData(QtCore.Qt.UserRole, action)
                    self.toolbarActionsList.addItem(item)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addWidget(self.toolbarActionsList)
        groupBoxVisibleActions.setLayout(vLayout)

        # mise en place :
        layout = QtGui.QVBoxLayout()
        layout.addWidget(groupBoxIconSize)
        layout.addWidget(groupBoxVisibleActions)
        self.setLayout(layout)


class OtherPage(QtGui.QWidget):
    """
    Configuration diverses
    """
    def __init__(self, parent=None):
        super(OtherPage, self).__init__(parent)
        self.main = parent.main

        # configuration de la variable screenShotDelay :
        groupBoxScreenShotDelay = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'ScreenShotDelay')
        title2 = QtGui.QApplication.translate('main', 'in milliseconds')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b> ({1})</p>').format(title, title2))
        integerLabel = QtGui.QLabel(QtGui.QApplication.translate('main', 
            'Enter a value between {0} and {1}:').format(10, 10000))
        self.integerSpinBoxScreenShotDelay = QtGui.QSpinBox()
        self.integerSpinBoxScreenShotDelay.setRange(10, 10000)
        self.integerSpinBoxScreenShotDelay.setSingleStep(100)
        self.integerSpinBoxScreenShotDelay.setValue(self.main.screenShotDelay)
        hLayout = QtGui.QHBoxLayout()
        hLayout.addWidget(integerLabel)
        hLayout.addWidget(self.integerSpinBoxScreenShotDelay)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        vLayout.addStretch()
        groupBoxScreenShotDelay.setLayout(vLayout)

        # configuration de la variable attachDistance :
        groupBoxAttachDistance = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'AttachDistance')
        title2 = QtGui.QApplication.translate('main', 'between lines or points and ruler or square')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b> ({1})</p>').format(title, title2))
        integerLabel = QtGui.QLabel(QtGui.QApplication.translate('main', 
            'Enter a value between {0} and {1}:').format(0, 100))
        self.integerSpinBoxAttachDistance = QtGui.QSpinBox()
        self.integerSpinBoxAttachDistance.setRange(0, 100)
        self.integerSpinBoxAttachDistance.setSingleStep(1)
        self.integerSpinBoxAttachDistance.setValue(self.main.attachDistance)
        hLayout = QtGui.QHBoxLayout()
        hLayout.addWidget(integerLabel)
        hLayout.addWidget(self.integerSpinBoxAttachDistance)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        vLayout.addStretch()
        groupBoxAttachDistance.setLayout(vLayout)

        # configuration de l'impression :
        groupBoxPrintConfig = QtGui.QGroupBox('')
        title = QtGui.QApplication.translate('main', 'PrintConfig')
        titleLabel = QtGui.QLabel(utils.u('<p align="center"><b>{0}</b></p>').format(title))
        # le mode d'impression (FullPage ou TrueSize) :
        title = QtGui.QApplication.translate('main', 'PrintMode')
        groupBoxPrintMode = QtGui.QGroupBox(title)
        self.radioPrintFullPage = QtGui.QRadioButton(QtGui.QApplication.translate('main', 'FullPage'))
        self.radioPrintTrueSize = QtGui.QRadioButton(QtGui.QApplication.translate('main', 'TrueSize'))
        if self.main.printMode == 'FullPage':
            self.radioPrintFullPage.setChecked(True)
        else:
            self.radioPrintTrueSize.setChecked(True)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(self.radioPrintFullPage)
        vLayout.addWidget(self.radioPrintTrueSize)
        groupBoxPrintMode.setLayout(vLayout)
        # orientation (Portrait ou Landscape) :
        title = QtGui.QApplication.translate('main', 'Orientation')
        groupBoxPrintOrientation = QtGui.QGroupBox(title)
        self.radioPrintPortrait = QtGui.QRadioButton(QtGui.QApplication.translate('main', 'Portrait'))
        self.radioPrintLandscape = QtGui.QRadioButton(QtGui.QApplication.translate('main', 'Landscape'))
        if self.main.printOrientation == 'Portrait':
            self.radioPrintPortrait.setChecked(True)
        else:
            self.radioPrintLandscape.setChecked(True)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(self.radioPrintPortrait)
        vLayout.addWidget(self.radioPrintLandscape)
        groupBoxPrintOrientation.setLayout(vLayout)
        # on agence tout ça :
        hLayout = QtGui.QHBoxLayout()
        hLayout.addWidget(groupBoxPrintMode)
        hLayout.addWidget(groupBoxPrintOrientation)
        vLayout = QtGui.QVBoxLayout()
        vLayout.addWidget(titleLabel)
        vLayout.addLayout(hLayout)
        # les explications :
        bigEditorPrintMode = QtGui.QTextEdit()
        bigEditorPrintMode.setReadOnly(True)
        bigEditorPrintMode.setText(
            QtGui.QApplication.translate('main', ''
                    '<p align=left><b>FullPage: </b>'
                    'printing will be adapted to the dimensions of the page.</p>'
                    '<p></p>'
                    '<p align=left><b>TrueSize: </b>'
                    'the printed document comply with the dimensions of your figures.</p>'
                    '<p></p>'))
        vLayout.addWidget(bigEditorPrintMode)
        vLayout.addStretch(1)
        groupBoxPrintConfig.setLayout(vLayout)

        # mise en place :
        layout = QtGui.QVBoxLayout()
        layout.addWidget(groupBoxScreenShotDelay)
        layout.addWidget(groupBoxAttachDistance)
        layout.addWidget(groupBoxPrintConfig)
        self.setLayout(layout)


class ConfigurationDlg(QtGui.QDialog):
    """
    explications
    """
    def __init__(self, parent=None):
        super(ConfigurationDlg, self).__init__(parent)

        self.main = parent
        self.setWindowTitle(QtGui.QApplication.translate('main', 'Configuration'))

        self.contentsWidget = QtGui.QListWidget()
        self.contentsWidget.setMaximumWidth(128)
        self.contentsWidget.setMinimumWidth(128)
        self.contentsWidget.setMinimumHeight(400)
        self.contentsWidget.setSpacing(6)
        self.contentsWidget.setViewMode(QtGui.QListView.IconMode)
        self.contentsWidget.setIconSize(QtCore.QSize(80, 80))

        self.pagesWidget = QtGui.QStackedWidget()

        title = QtGui.QApplication.translate("main", "Screen")
        icon = "images/config-screen.png"
        listWidgetItem = QtGui.QListWidgetItem(title, self.contentsWidget)
        listWidgetItem.setIcon(QtGui.QIcon(icon))
        listWidgetItem.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.pagesWidget.addWidget(ScreenPage(self))

        title = QtGui.QApplication.translate("main", "ToolsWindow")
        icon = "images/config-toolswindow.png"
        listWidgetItem = QtGui.QListWidgetItem(title, self.contentsWidget)
        listWidgetItem.setIcon(QtGui.QIcon(icon))
        listWidgetItem.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.pagesWidget.addWidget(ToolsWindowPage(self))

        title = QtGui.QApplication.translate("main", "KidWindow")
        icon = "images/config-kidwindow.png"
        listWidgetItem = QtGui.QListWidgetItem(title, self.contentsWidget)
        listWidgetItem.setIcon(QtGui.QIcon(icon))
        listWidgetItem.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.pagesWidget.addWidget(KidWindowPage(self))

        title = QtGui.QApplication.translate("main", "Other")
        icon = "images/config-other.png"
        listWidgetItem = QtGui.QListWidgetItem(title, self.contentsWidget)
        listWidgetItem.setIcon(QtGui.QIcon(icon))
        listWidgetItem.setTextAlignment(QtCore.Qt.AlignHCenter)
        self.pagesWidget.addWidget(OtherPage(self))

        self.contentsWidget.currentItemChanged.connect(self.changePage)
        self.contentsWidget.setCurrentRow(0)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.addWidget(self.contentsWidget)
        horizontalLayout.addWidget(self.pagesWidget)

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok| QtGui.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch(1)
        buttonsLayout.addWidget(buttonBox)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(horizontalLayout)
        mainLayout.addStretch(1)
        mainLayout.addSpacing(12)
        mainLayout.addLayout(buttonsLayout)

        self.setLayout(mainLayout)
        self.setMinimumWidth(700)
        #self.setMinimumHeight(400)
        self.show()


    def changePage(self, current, previous):
        if not current:
            current = previous
        self.pagesWidget.setCurrentIndex(self.contentsWidget.row(current))

    def accept(self):
        """
        On met à jour les modifications avant de fermer
        """
        # page Screen :
        if self.pagesWidget.widget(0).radioScreenMode.isChecked():
            utils.changeScreenMode('FULL_SCREEN')
        else:
            utils.changeScreenMode('FULL_SPACE')
        utils.changeScreenNumber(self.pagesWidget.widget(0).comboBoxScreenNumber.currentIndex())

        # page ToolsWindow :
        newSize = self.pagesWidget.widget(1).integerSpinBoxIconSize.value()
        self.main.iconSize = QtCore.QSize(newSize, newSize)
        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        for i in range(self.pagesWidget.widget(1).toolbarActionsList.count()):
            item = self.pagesWidget.widget(1).toolbarActionsList.item(i)
            try:
                action = item.data(QtCore.Qt.UserRole)
                if item.checkState() == QtCore.Qt.Checked:
                    self.main.toolsWindow.actionsState[action][1] = True
                else:
                    self.main.toolsWindow.actionsState[action][1] = False
            except:
                continue

        # page KidWindow :
        newSize = self.pagesWidget.widget(2).integerSpinBoxIconSize.value()
        self.main.iconSizeKid = QtCore.QSize(newSize, newSize)
        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        for i in range(self.pagesWidget.widget(2).toolbarActionsList.count()):
            item = self.pagesWidget.widget(2).toolbarActionsList.item(i)
            try:
                action = item.data(QtCore.Qt.UserRole)
                if item.checkState() == QtCore.Qt.Checked:
                    self.main.toolsWindow.actionsState[action][2] = True
                else:
                    self.main.toolsWindow.actionsState[action][2] = False
            except:
                continue

        # page Other :
        self.main.screenShotDelay = self.pagesWidget.widget(3).integerSpinBoxScreenShotDelay.value()
        self.main.attachDistance = self.pagesWidget.widget(3).integerSpinBoxAttachDistance.value()        
        if self.pagesWidget.widget(3).radioPrintFullPage.isChecked():
            self.main.printMode = 'FullPage'
        else:
            self.main.printMode = 'TrueSize'
        if self.pagesWidget.widget(3).radioPrintPortrait.isChecked():
            self.main.printOrientation = 'Portrait'
        else:
            self.main.printOrientation = 'Landscape'

        # on ferme :
        QtGui.QDialog.accept(self)


