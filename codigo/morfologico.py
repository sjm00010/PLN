# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:34:26 2020

@author: sjm00010
"""

import spacy
from nltk.corpus import stopwords
import collections
import string, re

#-----------------------
# Variables auxiliares
#-----------------------

# Cargo Spacy
nlp = spacy.load("en_core_web_sm")

english_stops = set(stopwords.words('english'))

#-----------------------
# Funciones principales
#-----------------------

def aMorfo(men):
    men = men.replace('\xa0',' ')
    men = men.lower()
    doc = nlp(men)
    
    sol = {}
    
    # Número de frases
    sol["frases"]=len(list(doc.sents))
    
    # Número de tokens
    sol["tokens"]=len(doc)
    
    # Número de tokens no repetidos
    sol["tokensNR"]=len(set(word.text for word in doc))
    
    # Palábras vacías
    sol["vacias"]=len([word for word in doc if word.is_stop])
    
    # Palábras vacías no repetidas
    sol["vaciasNR"]=len(set(word.text for word in doc if word.is_stop ))
    
    # Top 5 palabras con su frecuencia, sin palabras vacías ni signos de puntuación
    top=collections.Counter(word.text for word in doc if not word.is_stop and word.text not in string.punctuation).most_common(5)
    
    # Por problemas para generar las graficas saco 1 a 1 las palabras del top
    sol["top1P"]=top[0][0]
    sol["top1F"]=top[0][1]
    sol["top2P"]=top[1][0]
    sol["top2F"]=top[1][1]
    sol["top3P"]=top[2][0]
    sol["top3F"]=top[2][1]
    sol["top4P"]=top[3][0]
    sol["top4F"]=top[3][1]
    sol["top5P"]=top[4][0]
    sol["top5F"]=top[4][1]
    
    # Número de adjetivos, adverbios, sustantivos y verbos
    nombres = 0 # Total de nombres
    adjetivos = 0 # Total de nombres
    verbos = 0 # Total de verbos
    adverbios = 0 # Total de adverbios
    
    reNom = r'\w*N{2}\w*' # Los nombres tienen NN en su clasificación, buscando la subcadena sé si es un nombre
    reAdj = r'\w*J{2}\w*' # Los verbos presentan JJ
    reVer = r'\w*VB\w*' # Los verbos presentan VB
    reAdv = r'\w*RB\w*' # Los adverbios presentan RB
    
    nombres += len([word for word in doc if not word.is_stop and word.text not in string.punctuation if re.search(reNom,word.tag_)])
    adjetivos += len([word for word in doc if not word.is_stop and word.text not in string.punctuation if re.search(reAdj,word.tag_)])
    verbos += len([word for word in doc if not word.is_stop and word.text not in string.punctuation if re.search(reVer,word.tag_)])
    adverbios += len([word for word in doc if not word.is_stop and word.text not in string.punctuation if re.search(reAdv,word.tag_)])
    
    sol["nombres"]=nombres
    sol["adverbios"]=adverbios
    sol["adjetivos"]=adjetivos
    sol["verbos"]=verbos
    
    return sol