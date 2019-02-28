# -*- coding: utf-8 -*-
# -*- coding: UTF-8 -*-

import math
import os 
import os.path

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.gui import *
from qgis.core import *
from CarregaPasta import resources_rc  
import os
import os.path

class CarregaPasta:
    def __init__(self,iface):
        # Save reference to the QGIS interface
        self.iface = iface
        
    def initGui(self):
         
        # cria uma ação que iniciará a configuração do plugin 
        path = self.iface.mainWindow()
        icon_path = ':/plugins/Suavizacao/ac.png'
        self.action = QAction (QIcon (icon_path),'Carrega Shapefiles', path)
        self.action.setObjectName ('Carregar Shapefiles')
        self.action.setStatusTip('None')
        self.action.setWhatsThis('None')
        # QObject.connect (self.action, SIGNAL ("triggered()"), self.selecionaPasta)
        # Adicionar o botão da barra de ferramentas e item de menu 
        self.iface.addToolBarIcon (self.action) 
      

    def unload(self):
        self.iface.removeToolBarIcon(self.action)


    def selecionaPasta(self):
        fileDlg = QFileDialog()
        path = fileDlg.getExistingDirectory(None,u'Selecione diretório contendo Shapefiles','',QFileDialog.ShowDirsOnly)
        if path != "":
            self.carrega(path)


    def carrega(self, pasta):
        caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        shps = [arq for arq in arquivos if arq.lower().endswith(".shp")]
        shps.sort()

        root = QgsProject.instance().layerTreeRoot()

        #AQUI VOU CRIAR GRUPO COM O MESMO NOME DA PASTA CARREGADA E SEUS SUB GRUPOS ( AREA, LINHA, PONTO)
        nomeDaPasta = os.path.split(pasta)[1]
        grupoPai = root.insertGroup(0, nomeDaPasta)
        subGrupoPonto = grupoPai.addGroup(u"Ponto") # adiciona subgrupo ao grupo pai com nome de Ponto
        subGrupoLinha = grupoPai.addGroup(u"Linha") #adiciona subgrupo ao grupo pai com nome de Linha
        subGrupoArea = grupoPai.addGroup(u"Área") #adiciona subgrupo ao grupo pai com nome de Area
        
        #AQUI COMEÇA O LOOP   
        for shp in shps:
            nomeShape = os.path.split(shp)[1]
            nomeShape = nomeShape[:-4]

            layer = QgsVectorLayer(shp,nomeShape,"ogr")
            
            if (layer.geometryType() == QGis.Point): # se o tipo de geometria é igual a Ponto
                QgsMapLayerRegistry.instance().addMapLayer(layer,False)
                subGrupoLinha.addLayer(layer)
            elif(layer.geometryType() == QGis.Line): # se o tipo de geometria é igual a Linha
                QgsMapLayerRegistry.instance().addMapLayer(layer,False)
                subGrupoPonto.addLayer(layer)
            elif(layer.geometryType() == QGis.Polygon): # se o tipo de geometria é igual a Poligono
                QgsMapLayerRegistry.instance().addMapLayer(layer,False)
                subGrupoArea.addLayer(layer)
            else:
                return False

        grupoPai.removeChildrenGroupWithoutLayers()
        
