# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:51:35 2020

@author: sjm00010
"""

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.chunk import tree2conlltags

# Tokenizador
tokenizer = RegexpTokenizer(r"\w+(?:'\w+)?")

# Etiquetador gramatical
_POS_TAGGER = 'taggers/maxent_treebank_pos_tagger/english.pickle'
tagger = nltk.data.load(_POS_TAGGER)

# Color de la palabra
categorias = {}

# Pills
pill1="<span class=\"badge badge-primary\">"
pill2="<span class=\"badge badge-secondary\">"
pill3="<span class=\"badge badge-success\">"
pill4="<span class=\"badge badge-danger\">"
pill5="<span class=\"badge badge-warning\">"
pill6="<span class=\"badge badge-info\">"

pillInterior=" <span class=\"badge badge-light\">"
finpill="</span></span>"

# Función para crear pildoras
def creaPil(token, cat):
     global categorias
    
     if categorias[cat] == 0:
          conten = pill1
     elif categorias[cat] == 1:
          conten = pill2
     elif categorias[cat] == 2:
          conten = pill3
     elif categorias[cat] == 3:
          conten = pill4
     elif categorias[cat] == 4:
          conten = pill5
     else:
          conten = pill6
    
     conten += token + pillInterior + cat + finpill
    
     return conten


def reconoce(text):
     global categorias
     color=0
     
     # Tokenizamos el texto y lo etiquetamos gramaticalmente
     tags = tagger.tag(tokenizer.tokenize(text))
    
     # Reconocimiento de entidades con el modelo multiclase
     _MULTICLASS_NE_CHUNKER = 'chunkers/maxent_ne_chunker/english_ace_multiclass.pickle'
     multiclass_ner = nltk.data.load(_MULTICLASS_NE_CHUNKER)
     ne_tree_multiclass = multiclass_ner.parse(tags)
    
     # Salida en forma de tupla
     iob_tagged_multiclass = tree2conlltags(ne_tree_multiclass)
    
     # Creo el nuevo texto
     cont = 0
     for palabra, __del__, cat in iob_tagged_multiclass:
          if cat != 'O':
               
               # Actualizo la categoria para quitar la letra
               cate = cat.split('-')[1] 
               
               # Asigno un color a una categoría, máximo 5
               if categorias.get(cate) is None:
                    categorias[cate] = color 
                    print(cat, cate, color)
                    color = (color + 1) % 6
                    
               # Busco la palabra en el texto, a partir de la posicion cont
               cont = text.find(palabra, cont)
               
               # Creo la pildora
               sus = creaPil(palabra, cate)
               
               # Reemplazo la palabra por la pildora creada
               text = text[:cont] + text[cont:].replace(palabra, sus, 1)
               
               # Avanzo en el texto
               cont += len(sus)
          else:
               # Avanzo en el texto
               cont += len(palabra)
    
     return text