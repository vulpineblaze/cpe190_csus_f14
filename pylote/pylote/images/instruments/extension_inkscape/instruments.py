#!/usr/bin/env python
# -*- coding: utf8 -*-

# Les deux lignes suivant sont necessaires seulement si le script n'est pas 
#  directement dans le dossier d'installation
import sys
sys.path.append('/usr/share/inkscape/extensions')

# Utilisation du module inkex avec des effets predefinis
import inkex 
# Le module simplestyle fournit des fonctions pour le parsing des styles
import simplestyle 


from math import *







def points_to_svgd(p):
    f = p[0]
    p = p[1:]
    svgd = 'M%.3f,%.3f' % f
    for x in p:
        svgd += 'L%.3f,%.3f' % x
    svgd += 'z'
    return svgd














class CHello(inkex.Effect):
    """
    Exemple Inkscape 
    Cree un nouveau calque et dessine des elements de base
    """
    def __init__(self):
        """
        Constructeur
        Definit l'option "--strTexte" du script
        """
        # Appel du constructeur.
        inkex.Effect.__init__(self)

        # Definit la chaine d'option "--strTexte" avec le raccourci "-w" et 
        #  la valeur par defaut "Hello".
        self.OptionParser.add_option('-w', '--strTexte', action = 'store',
                                     type = 'string', 
                                     dest = 'strTexte', default = 'Hello',
                                     help = 'Message a ecrire ?')

    def effect(self):
        """
        Fonction principale
        Surchage la fonction de la classe de base
        Dessine quelques elements sur le docuement SVG
        """

        # Recupere le document SVG principal
        svg = self.document.getroot()
        layer = self.current_layer

        # Recuperation de la hauteur et de la largeur de la feuille
        width  = inkex.unittouu(svg.get('width'))
        height = inkex.unittouu(svg.attrib['height'])

        
        
        """
        §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
        LA RÈGLE
        §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
        """
        x_org = 10#width / 20
        x_pas = width / 21
        y_org = 10#height / 10
        y_pas = 20
        nLargeurTrait = 1

        # Center text horizontally with CSS style.
        textstyle = {'text-align' : 'left', \
                 'text-anchor': 'top', \
                 'font-size': '12pt', \
                 'fill':'rgb(0, 0, 0)'}

        ligne = inkex.etree.Element(inkex.addNS('line', 'svg'))
        ligne.set('x1', str(x_org))
        ligne.set('y1', str(y_org))
        ligne.set('x2', str(x_org + 20 * x_pas))
        ligne.set('y2', str(y_org))
        ligne.set('stroke', 'rgb(0, 0, 0)')
        ligne.set('stroke-width', str(nLargeurTrait))
        layer.append(ligne)


        for n in range(21):
            x_pos = x_org + n * x_pas
            ligne = inkex.etree.Element(inkex.addNS('line', 'svg'))
            ligne.set('x1', str(x_pos))
            ligne.set('y1', str(y_org))
            ligne.set('x2', str(x_pos))
            ligne.set('y2', str(y_org + y_pas))
            ligne.set('stroke', 'rgb(0, 0, 0)')
            ligne.set('stroke-width', str(nLargeurTrait))
            layer.append(ligne)


            # Creation d'un element texte
            texte = inkex.etree.Element(inkex.addNS('text', 'svg'))
            texte.text = str(n)
            
            # Set text position to center of document.
            textDecal = 4
            if n > 9 :
                textDecal = 2 * textDecal
            texte.set('x', str(x_pos - textDecal))
            texte.set('y', str(y_org + 2 * y_pas))
            texte.set('style', simplestyle.formatStyle(textstyle))
            # Ajoute le texte au calque
            layer.append(texte)


        y_pas = 15
        for n in range(20):
            x_pos = x_org + x_pas/2 + n * x_pas
            ligne = inkex.etree.Element(inkex.addNS('line', 'svg'))
            ligne.set('x1', str(x_pos))
            ligne.set('y1', str(y_org))
            ligne.set('x2', str(x_pos))
            ligne.set('y2', str(y_org + y_pas))
            ligne.set('stroke', 'rgb(0, 0, 0)')
            ligne.set('stroke-width', str(nLargeurTrait))
            layer.append(ligne)

        x_pas = width / 210
        y_pas = 10
        for n in range(200):
            x_pos = x_org + n * x_pas
            ligne = inkex.etree.Element(inkex.addNS('line', 'svg'))
            ligne.set('x1', str(x_pos))
            ligne.set('y1', str(y_org))
            ligne.set('x2', str(x_pos))
            ligne.set('y2', str(y_org + y_pas))
            ligne.set('stroke', 'rgb(0, 0, 0)')
            ligne.set('stroke-width', str(nLargeurTrait))
            layer.append(ligne)


        """
        §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
        LE RAPPORTEUR
        §§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§§
        """
        # Creation du demi-cercle
        x_org = width / 2
        x_pas = width / 21
        y_org = height / 2
        y_pas = 20
        nLargeurTrait = 1
        radius = x_org

        demicercle = inkex.etree.Element(inkex.addNS('path', 'svg'))

        f = (0.0, y_org)
        svgd = 'M %.3f,%.3f ' % f
        a = (x_org, x_org)
        b = (width, y_org)
        svgd += 'A %.3f,%.3f 0 1 1 ' % a
        svgd += '%.3f,%.3f ' % b
        svgd += 'z'

        demicercle.set('d', svgd)

        demicercle.set('fill', 'none')
        demicercle.set('stroke', 'rgb(0, 0, 0)')
        demicercle.set('stroke-width', str(nLargeurTrait))
        
        # Ajout du cercle sur le calque
        layer.append(demicercle)

        # graduations
        x_org = width / 2
        x_pas = width / 21
        y_org = height / 2
        y_pas = 20
        nLargeurTrait = 1
        radius = x_org

        angle_pas = 10
        coeff = 0.70
        for n in range(19):
            ligne = inkex.etree.Element(inkex.addNS('line', 'svg'))
            angle = radians(n * angle_pas)
            c = radius * cos(angle)
            s = radius * sin(angle)
            x1 = x_org + c
            y1 = y_org - s
            ligne.set('x1', str(x1))
            ligne.set('y1', str(y1))
            x2 = str(x_org + coeff * c)
            y2 = str(y_org - coeff * s)
            ligne.set('x2', x2)
            ligne.set('y2', y2)
            ligne.set('stroke', 'rgb(0, 0, 0)')
            ligne.set('stroke-width', str(nLargeurTrait))
            layer.append(ligne)

            # Creation d'un element texte
            texte = inkex.etree.Element(inkex.addNS('text', 'svg'))
            layer.append(texte)
            texte.text = str(10 * n)# + '°'
            texte.set('style', simplestyle.formatStyle(textstyle))
            
            angle = radians(90 - n * angle_pas)
            f = (cos(angle), sin(angle), -sin(angle), cos(angle))
            matrix = 'matrix(%s, %s, %s, %s,0,0)' % f
            texte.set('transform', matrix)

            #texte.set('x', x2)
            #texte.set('y', y2)
            texte.set('x', '634')
            texte.set('y', '-290')





















        angle_pas = 10
        coeff = 0.80
        for n in range(18):
            ligne = inkex.etree.Element(inkex.addNS('line', 'svg'))
            angle = radians(5 + n * angle_pas)
            c = radius * cos(angle)
            s = radius * sin(angle)
            x1 = x_org + c
            y1 = y_org - s
            ligne.set('x1', str(x1))
            ligne.set('y1', str(y1))
            x2 = x_org + coeff * c
            y2 = y_org - coeff * s
            ligne.set('x2', str(x2))
            ligne.set('y2', str(y2))
            ligne.set('stroke', 'rgb(0, 0, 0)')
            ligne.set('stroke-width', str(nLargeurTrait))
            layer.append(ligne)

        angle_pas = 1
        coeff = 0.95
        for n in range(180):
            ligne = inkex.etree.Element(inkex.addNS('line', 'svg'))
            angle = radians(n * angle_pas)
            c = radius * cos(angle)
            s = radius * sin(angle)
            x1 = x_org + c
            y1 = y_org - s
            ligne.set('x1', str(x1))
            ligne.set('y1', str(y1))
            x2 = x_org + coeff * c
            y2 = y_org - coeff * s
            ligne.set('x2', str(x2))
            ligne.set('y2', str(y2))
            ligne.set('stroke', 'rgb(0, 0, 0)')
            ligne.set('stroke-width', str(nLargeurTrait))
            layer.append(ligne)


















# Execute la fonction "effect" de la classe "CHello"
hello = CHello()
hello.affect()
