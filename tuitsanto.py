# coding: utf-8
import xml.etree.ElementTree as ET
import time
import codecs
from twython import Twython
import os
import random
import json

with open('config.json', 'r') as f:
    config = json.load(f)

__author__ = "Ernesto Araiza"
__copyright__ = "Copyright 2014"
__version__ = "0.4"
__email__ = "yo@ernestoaraiza.com"
__status__ = "Production"

#twitter related:
APP_KEY = config['DEFAULT']['APP_KEY']
APP_SECRET = config['DEFAULT']['APP_SECRET']
OAUTH_TOKEN = config['DEFAULT']['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = config['DEFAULT']['OAUTH_TOKEN_SECRET']

class Santo:
        
    LENTUIT = 280
    twitter = Twython(APP_KEY, APP_SECRET)
    auth = twitter.get_authentication_tokens()
    twitter = Twython(APP_KEY, APP_SECRET,
                      OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    #this is the current directory (pwd)
    DIRFILES = config['DEV']['DIRFILES'] #DEV 

    FELICIDADES = ['Hoy felicitamos a', 'Hoy es santo de', 'Felicitemos a', 'Felicitaciones para', 'Felicidades', 'Santos de hoy:']
    TAMBIEN = ['También', 'y']
    MESNAME = ['','Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']

    tree = ET.parse(DIRFILES+'santos.xml')
    root = tree.getroot()

    def __init__(self):
        pass

    def get_nombres(self,mes,dia):
        nombres=""
        for nombre in self.root[mes-1][dia-1]:
            nombres=nombres+nombre.text+", "
        nombres=nombres[:-2]
        return nombres
        
    def y_a(self,tuit):
        indice=tuit.rfind(',')
        if indice != -1:
            tuit=tuit[:indice]+" y a "+tuit[indice+2:]
        return tuit

    #asumimos que status es mayor a LENTUIT
    def divide_en_tuits(self,status):
        
        segundo_tuit=""
        
        indice=status.rfind(',')
        right = status[indice+2:]
        left = status[:indice]
        segundo_tuit=right+segundo_tuit
        
        longitud=len(left)
        
        while longitud > LENTUIT-3:
            indice=left.rfind(',')
            right = left[indice+2:]
            left = left[:indice]
            segundo_tuit=right+", "+segundo_tuit
            longitud=len(left)
        
        left =  left+"..."
        segundo_tuit = random.choice(TAMBIEN) +" "+ y_a(segundo_tuit)
        return [left,segundo_tuit]

    def tuit(self): 
        thetime=time.localtime()
        mes=thetime[1] #mes=1
        dia=thetime[2] #dia=11

        fecha = "#"+str(dia)+self.MESNAME[mes]

        status=fecha+" "+random.choice(self.FELICIDADES)+" "+str(self.get_nombres(mes,dia).encode("utf-8"))
        if len(status)>self.LENTUIT-3:
            lista_tuits = divide_en_tuits(status)
            for tuit in lista_tuits:
                print tuit 
                self.twitter.update_status(status=tuit)
        else:
            status = self.y_a(status)
            print status 
            self.twitter.update_status(status=status)
s = Santo()
s.tuit()