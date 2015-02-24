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
    Ce module contient des variables et fonctions utiles au programme.
    Certaines parties spécialisées sont dans les fichiers utils_aaa.py
"""

# importation des modules utiles :
from __future__ import division, print_function
import sys
import os
import math

PYTHONVERSION = sys.version_info[0] * 10 + sys.version_info[1]

# PyQt ou PySide ?
PYSIDE = False
if not('PYQT' in sys.argv):
    try:
        from PySide import QtCore, QtGui
        PYSIDE = True
    except:
        pass
if not(PYSIDE):
    import sip
    sip.setapi('QString', 2)
    sip.setapi('QVariant', 2)
    from PyQt4 import QtCore, QtGui


def myPrint(*args):
    if len(args) > 1:
        print(args)
    else:
        arg = args[0]
        try:
            print(arg)
        except:
            try:
                print(u(arg))
            except:
                try:
                    print(s(arg))
                except:
                    print('PB in utils.myPrint')

# TESTS affichera plus de messages :
TESTS = False
if 'TESTS' in sys.argv:
    TESTS = True


# quelques variables :
PROGNAME = 'pylote'
PROGLABEL = 'Pylote'
PROGVERSION = 1.4
PROGDATE = '24-10-2014'
PROGAUTHOR = 'Pascal Peter'
PROGYEAR = '2009-2014'
PROGMAIL = 'pascal.peter at free.fr'
PROGWEB = 'http://pascal.peter.free.fr'
HELPPAGE = 'http://pascal.peter.free.fr/wiki/Logiciels/Pylote'
LICENCETITLE = 'GNU General Public License version 3'



myPrint('TESTS: ', TESTS)
myPrint('PYTHONVERSION: ', PYTHONVERSION)
myPrint('PYSIDE: ', PYSIDE)





"""
La variable globale SCREEN_MODE définit la façon dont le logiciel occupe l'espace.
FULL_SCREEN : tout l'écran est occupé, y compris les barres de tâches et autres tableaux de bord.
FULL_SPACE : l'espace libre est utilisé par le logiciel ; on peut toujours utiliser le tableau de bord.
            Il peut y avoir des problèmes de positionnement sur certains systèmes.
TESTS : le logiciel ne s'affiche que dans une petite fenêtre.
            utile juste pour voir les retours de la console en direct.
            à passer en argument.
"""
SCREEN_MODE = 'FULL_SPACE'
SCREEN_NUMBER = 0

def changeScreenMode(newValue):
    global SCREEN_MODE
    SCREEN_MODE = newValue

def changeScreenNumber(newValue):
    global SCREEN_NUMBER
    SCREEN_NUMBER = newValue


"""
La variable globale WITH_TRAY_ICON sera mis automatiquement à False 
        si SCREEN_MODE vaut FULL_SCREEN où s'il y a problème.
On peut le changer ici manuellement si on n'en veut pas dans d'autres cas.
"""
WITH_TRAY_ICON = True

def changeWithTrayIcon(newValue):
    global WITH_TRAY_ICON
    WITH_TRAY_ICON = newValue














"""
###########################################################
###########################################################

                Fonctions de conversion, etc

###########################################################
###########################################################
"""

def u(text):
    # retourne une version unicode de text
    if PYTHONVERSION >= 30:
        try:
            if isinstance(text, str):
                return text
            else:
                return str(text)
        except:
            myPrint('ERROR utils.u', type(text), text)
            return text
    else:
        try:
            return unicode(text)
        except:
            if isinstance(text, str):
                return text.decode('utf-8')
            elif isinstance(text, QtCore.QByteArray):
                return str(text).decode('utf-8')
            else:
                myPrint('ERROR utils.u', type(text), text)
                return text

def s(text):
    # retourne une version str de text
    if PYTHONVERSION >= 30:
        if isinstance(text, str):
            return text
        else:
            try:
                return str(text)
            except:
                myPrint('ERROR utils.s', type(text), text)
                return text
    else:
        try:
            return text.encode('utf8')
        except:
            if isinstance(text, str):
                return text
            else:
                try:
                    return str(text)
                except:
                    myPrint('ERROR utils.s', type(text), text)
                    return text

def toLong(text):
    # retourne une version int ou long de text
    if PYTHONVERSION >= 30:
        return int(text)
    else:
        return long(text)


def do_locale(lang, beginfilename, endfilename):
    """
    Teste l'existence d'un fichier localisé.
    Par exemple, insère _fr entre beginfilename et endfilename.
    Renvoie le fichier par défaut sinon.
    """
    localefilename = beginfilename + '_' + lang + endfilename
    localefileFile = QtCore.QFileInfo(localefilename)
    if not(localefileFile.exists()):
        localefilename = beginfilename + endfilename
    return localefilename

def webhelp_in_browser(weburl):
    """
    Ouvre une url dans le navigateur.
    """
    url = QtCore.QUrl(weburl)
    QtGui.QDesktopServices.openUrl(url)


def doWaitCursor():
    QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

def restoreCursor():
    QtGui.QApplication.restoreOverrideCursor()


def createTempAppDir():
    """
    (re)création du dossier temporaire
    on cree un sous-dossier /tmp/PROGNAME
    à améliorer avec tests sous windob
    """
    tempDir = QtCore.QDir.temp()
    emptyDir(QtCore.QDir.tempPath() + "/" + PROGNAME)
    tempDir.rmdir(PROGNAME)
    tempAppDir = QtCore.QDir(QtCore.QDir.tempPath() + "/" + PROGNAME + "/")
    if tempAppDir.exists():
        tempAppPath = tempAppDir.path()
    elif tempDir.mkdir(PROGNAME):
        tempAppPath = QtCore.QDir(QtCore.QDir.tempPath() + "/" + PROGNAME + "/").path()
    else:
        utils.myPrint("tempAppDir sera temp")
        tempAppPath = QtCore.QDir.tempPath()
    return tempAppPath

def emptyDir(dirName, deleteThisDir=True, filesToKeep=[]):
    """
    Vidage récursif d'un dossier.
    Si deleteThisDir est mis à False, le dossier lui-même n'est pas supprimé.
    filesToKeep est une liste de noms de fichiers à ne pas effacer 
        (filesToKeep=['.htaccess'] par exemple).
    """
    has_err = False
    aDir = QtCore.QDir(dirName)
    if aDir.exists():
        entries = aDir.entryInfoList(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs | QtCore.QDir.Files | QtCore.QDir.Hidden)
        for entryInfo in entries:
            path = entryInfo.absoluteFilePath()
            if entryInfo.isDir():
                # on fait suivre filesToKeep, mais deleteThisDir sera True :
                has_err = emptyDir(path, filesToKeep=filesToKeep)
            elif entryInfo.isFile():
                if not(entryInfo.fileName() in filesToKeep):
                    f = QtCore.QFile(path)
                    if f.exists():
                        if not(f.remove()):
                            print("PB: ", path)
                            has_err = True
        if deleteThisDir:
            if not(aDir.rmdir(aDir.absolutePath())):
                print("Erreur de suppression de : " + aDir.absolutePath())
                has_err = True
    return has_err


def verifieExtension(fileName, extension):
    """
    Pour ajouter l'extension au nom du fichier si besoin
    """
    r = fileName.split('.')[0] + '.' + extension
    return r






"""
###########################################################
###########################################################

                Fonctions géométriques

###########################################################
###########################################################
"""

def distance(A, B):
    return math.hypot((A.x() - B.x()), (A.y() - B.y()))

def rotation(P, centre, angle):
    x = centre.x() + math.cos(angle) * (P.x() - centre.x()) - math.sin(angle) * (P.y() - centre.y())
    y = centre.y() + math.sin(angle) * (P.x() - centre.x()) + math.cos(angle) * (P.y() - centre.y())
    return QtCore.QPointF(x, y)

def projectionOrthogonale(P, A, B):
    """
    projection orthogonale sur la droite (AB)
    """
    if B.x() == A.x():
      angle = math.pi / 2
    else:
      angle = math.atan((B.y() - A.y()) / (B.x() - A.x()))
    P2 = rotation(P, A, - angle)
    PH2 = QtCore.QPointF(P2.x(), A.y())
    PH1 = rotation(PH2, A, angle)
    return PH1

def distanceSegment(P, A, B):
    """
    distance entre le point P et le segment [AB]
    """
    result = distance(P, A)
    distance_B = distance(P, B)
    if distance_B < result:
        result = distance_B
    H = projectionOrthogonale(P, A, B)
    if distance(H, A) + distance(H, B) <= distance(A, B):
        distance_H = distance(P, H)
        if distance_H < result:
            result = distance_H
    return result



