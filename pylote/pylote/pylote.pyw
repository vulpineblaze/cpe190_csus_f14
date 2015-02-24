#!/usr/bin/env python
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
# Ce programme est un logiciel libre ; vous pouvez le redistribuer et/ou le
# modifier conformément aux dispositions de la Licence Publique Générale GNU,
# telle que publiée par la Free Software Foundation ; version 3 de la licence,
# ou encore toute version ultérieure.
# 
# Ce programme est distribué dans l'espoir qu'il sera utile,
# mais SANS AUCUNE GARANTIE ; sans même la garantie implicite de COMMERCIALISATION
# ou D'ADAPTATION A UN OBJET PARTICULIER. Pour plus de détail,
# voir la Licence Publique Générale GNU.
# 
# Vous devez avoir reçu un exemplaire de la Licence Publique Générale GNU en même
# temps que ce programme ; si ce n'est pas le cas, voir <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------------


"""
DESCRIPTION :
    Fichier de lancement du logiciel.
"""


# importation des modules utiles :
from __future__ import division, print_function
import sys
import os

# récupération du chemin :
try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except:
    HERE = os.path.dirname(sys.argv[0])
# ajout du chemin au path (+ libs) :
sys.path.insert(0, HERE)
sys.path.insert(0, HERE + os.sep + 'libs')
# on démarre dans le bon dossier :
os.chdir(HERE)

# importation des modules perso :
import utils
import main

# PyQt4 ou PySide :
if utils.PYSIDE:
    from PySide import QtCore, QtGui, QtSvg
else:
    from PyQt4 import QtCore, QtGui, QtSvg









"""
###########################################################
###########################################################

                LANCEMENT DU PROGRAMME

###########################################################
###########################################################
"""

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    ###########################################
    # Installation de l'internationalisation :
    ###########################################
    locale = QtCore.QLocale.system().name()
    lang = locale.split('_')[0]
    # recherche d'un i18n passé en argument (par exemple LANG=fr_FR) :
    for arg in sys.argv:
        if arg.split('=')[0] == 'LANG':
            locale = arg.split('=')[1]
            lang = locale.split('_')[0]
    #print('locale:', locale, 'lang:', lang)
    QtTranslationsPath = QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath)
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load('qt_' + locale, QtTranslationsPath):
        app.installTranslator(qtTranslator)
    trans_dir = QtCore.QDir('./translations')
    localefile = trans_dir.filePath('pylote_' + locale)
    appTranslator = QtCore.QTranslator()
    if appTranslator.load(localefile, ''):
        app.installTranslator(appTranslator)    

    app.setWindowIcon(QtGui.QIcon('./images/icon.png'))

    ##################################################
    # Définition de SCREEN_MODE et de WITH_TRAY_ICON :
    ##################################################
    # on peut passer SCREEN_MODE en argument (utile pour TESTS)
    for arg in sys.argv:
        if arg in ('FULL_SCREEN', 'FULL_SPACE', 'TESTS'):
            utils.changeScreenMode(sys.argv[1])
    # valeur par défaut suivant l'os :
    if utils.SCREEN_MODE != 'TESTS':
        settings = QtCore.QSettings(utils.PROGNAME, 'config')
        if sys.platform == 'win32':
            utils.changeScreenMode(settings.value('SCREEN_MODE', 'FULL_SCREEN'))
        else:
            utils.changeScreenMode(settings.value('SCREEN_MODE', 'FULL_SPACE'))
    utils.myPrint('SCREEN_MODE:', utils.SCREEN_MODE)
    # pas de TrayIcon si le système ne le supporte pas :
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        utils.changeWithTrayIcon(False)
    # pas besoin de TrayIcon en mode FULL_SCREEN :
    if utils.SCREEN_MODE == 'FULL_SCREEN':
        utils.changeWithTrayIcon(False)

    ##################################################
    # Création et lancement du programme :
    ##################################################
    mainWindow = main.MainWindow(lang, appTranslator)
    # en fonction de SCREEN_MODE :
    if utils.SCREEN_MODE == 'TESTS':
        mainWindow.show()
    elif utils.SCREEN_MODE == 'FULL_SPACE':
        rect = QtGui.QApplication.desktop().availableGeometry(mainWindow.screenNumber)
        mainWindow.resize(int(rect.width()), int(rect.height()))
        mainWindow.showMaximized()
    elif utils.SCREEN_MODE == 'FULL_SCREEN':
        mainWindow.showFullScreen()
    else:
        mainWindow.showFullScreen()

    app.exec_()
    #sys.exit(app.exec_())

