# -*- coding: utf-8 -*-
# -*- coding: UTF-8 -*-

import math
import os 
import os.path
from PyQt4.QtCore import QObject, SIGNAL
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QAction, QFileDialog, QIcon, QMessageBox
from qgis.core import QGis, QgsMapLayerRegistry, QgsPoint, QgsVectorLayer, QgsProject
import resources_rc

class CarregaPasta:
    def __init__(self,iface):
        # Save reference to the QGIS interface
        self.iface = iface
        
    def initGui(self):
         
        # cria uma ação que iniciará a configuração do plugin 
        pai = self.iface.mainWindow()
        icon_path = ':/plugins/Suavizacao/ac.png'
        self.action = QAction (QIcon (icon_path),'Carrega Shapefiles', pai)
        self.action.setObjectName ('Carregar Shapefiles')
        self.action.setStatusTip('None')
        self.action.setWhatsThis('None')
        QObject.connect (self.action, SIGNAL ("triggered()"), self.selecionaPasta)
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
        subGrupoPonto = grupoPai.addGroup(u"Ponto")
        subGrupoLinha = grupoPai.addGroup(u"Linha")
        subGrupoArea = grupoPai.addGroup(u"Área")
        
        #AQUI COMEÇA O LOOP
        
        for shp in shps:
            nomeShape = os.path.split(shp)[1]
            nomeShape = nomeShape[:-4]

            layer = QgsVectorLayer(shp,nomeShape,"ogr")
            
            if (layer.geometryType() == QGis.Point):
                QgsMapLayerRegistry.instance().addMapLayer(layer,False)
                subGrupoLinha.addLayer(layer)
            elif(layer.geometryType() == QGis.Line):
                QgsMapLayerRegistry.instance().addMapLayer(layer,False)
                subGrupoPonto.addLayer(layer)
            elif(layer.geometryType() == QGis.Polygon):
                QgsMapLayerRegistry.instance().addMapLayer(layer,False)
                subGrupoArea.addLayer(layer)
            else:
                return False

        grupoPai.removeChildrenGroupWithoutLayers()
        
