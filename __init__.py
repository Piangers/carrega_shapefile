# -*- coding: utf-8 -*-
from .CarregaPasta import CarregaPasta

def classFactory(iface): 
    return CarregaPasta(iface)
