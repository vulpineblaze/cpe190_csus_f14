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
    La fenêtre "À propos"
"""

# importation des modules utiles :
import utils

if utils.PYSIDE:
    from PySide import QtCore, QtGui, QtWebKit
else:
    from PyQt4 import QtCore, QtGui, QtWebKit





"""
###########################################################
###########################################################

                La fenêtre 'À Propos' et ses onglets

###########################################################
###########################################################
"""

class AboutDlg(QtGui.QDialog):
    """
    explications
    """
    def __init__(self, parent=None, lang='', icon='./images/logo.png'):
        super(AboutDlg, self).__init__(parent)

        readmefile = utils.do_locale(lang, 'README', '.html')
        self.beginDir = parent.beginDir

        # En-tête de la fenêtre :
        taille = 128
        logoLabel = QtGui.QLabel()
        logoLabel.setMaximumSize(taille, taille)
        logoLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        logoLabel.setPixmap(QtGui.QPixmap(icon).scaled(taille, taille, 
                                                    QtCore.Qt.KeepAspectRatio,
                                                    QtCore.Qt.SmoothTransformation))
        title = utils.u('<h1>{0}</h1><h3>{1}</h3>').format(
            QtCore.QCoreApplication.translate(
                'AboutDlg', 'About {0}').format(utils.PROGLABEL),
            QtCore.QCoreApplication.translate(
                'AboutDlg', 'version {0}___{1}').format(utils.PROGVERSION, utils.PROGDATE))
        titleLabel = QtGui.QLabel(title)
        titleLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        titleGroupBox = QtGui.QGroupBox()
        titleLayout = QtGui.QHBoxLayout()
        titleLayout.addWidget(logoLabel)
        titleLayout.addWidget(titleLabel)
        titleGroupBox.setLayout(titleLayout)

        # Zone d'affichage :
        tabWidget = QtGui.QTabWidget()
        htmlFile = utils.do_locale(lang, 'translations/README', '.html')
        tabWidget.addTab(
            FileViewTab(parent=self, htmlFile=htmlFile), 
            QtCore.QCoreApplication.translate('AboutDlg', 'ReadMe'))
        tabWidget.addTab(
            FileViewTab(parent=self, txtFile='COPYING'), 
            QtCore.QCoreApplication.translate('AboutDlg', 'License'))
        htmlFile = utils.do_locale(lang, 'translations/CREDITS', '.html')
        tabWidget.addTab(
            FileViewTab(parent=self, htmlFile=htmlFile), 
            QtCore.QCoreApplication.translate('AboutDlg', 'Credits'))

        # Les boutons :
        okButton = QtGui.QPushButton(
            QtCore.QCoreApplication.translate('AboutDlg', '&Close'))
        okButton.clicked.connect(self.accept)
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(okButton)

        # Mise en place :
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(titleGroupBox)
        mainLayout.addWidget(tabWidget)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle(
            QtCore.QCoreApplication.translate('AboutDlg', 'About {0}').format(utils.PROGLABEL))

class FileViewTab(QtGui.QWidget):
    def __init__(self, parent=None, htmlFile='', txtFile=''):
        super(FileViewTab, self).__init__(parent)
        self.main = parent
        self.waiting = True
        if htmlFile != '':
            # un QWebView pour afficher si c'est un fichier html :
            self.bigTruc = QtWebKit.QWebView(self)
            self.bigTruc.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
            self.bigTruc.linkClicked.connect(self.link_clicked)
            cssFile = utils.u('{0}/{1}/{2}').format(parent.beginDir, 'libs', 'base.css')
            url = QtCore.QUrl().fromLocalFile(cssFile)
            self.bigTruc.settings().setUserStyleSheetUrl(url)
        else:
            # ou un QTextEdit pour un fichier texte :
            self.bigTruc = QtGui.QTextEdit()
            self.bigTruc.setReadOnly(True)
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(self.bigTruc)
        self.setLayout(mainLayout)
        # on ouvre le fichier :
        if htmlFile != '':
            htmlFile = utils.u('{0}/{1}').format(parent.beginDir, htmlFile)
            url = QtCore.QUrl().fromLocalFile(htmlFile)
            self.bigTruc.load(url)
        else:
            inFile = QtCore.QFile(txtFile)
            if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                stream = QtCore.QTextStream(inFile)
                stream.setCodec('UTF-8')
                self.bigTruc.setPlainText(stream.readAll())
                inFile.close()
        self.waiting = False

    def link_clicked(self, url):
        if self.waiting:
            return
        utils.myPrint('openLink : ', url)
        QtGui.QDesktopServices.openUrl(url)

