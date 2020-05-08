# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:33:16 2020

@author: sjm00010
"""

import spacy
import nltk.data
from nltk.wsd import lesk
from nltk.corpus import wordnet as wn

#-----------------------
# Variables auxiliares
#-----------------------

# Cargo Spacy
nlp = spacy.load("en_core_web_sm") # Para procesar las frases

# Este tokenizer realiza una tokenización mejor
sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

# Color de la palabra
color=0

cont = 0

# popover
popover1="<span class=\"badge badge-primary\" data-toggle=\"popover\" data-content=\"<ul>"
popover2="<span class=\"badge badge-info\" data-toggle=\"popover\" data-content=\"<ul>"
popover3="<span class=\"badge badge-warning\" data-toggle=\"popover\" data-content=\"<ul>"

#-----------------------
# Funciones auxiliares
#-----------------------

def creaPildora(token, synset, frase):
    global color
    global cont
    
    if color % 3 == 0:
        conten = popover1
    elif color % 3 == 1:
        conten = popover2
    else:
        conten = popover3
    color +=1
    
    for ss in wn.synsets(token):
        if ss.name() == synset:
            conten += "<li><b>"+ss.name()+"</b> : "+ss.definition()+"</li>"
        else:
            conten += '<li><i>'+ss.name()+'</i> : '+ss.definition().replace('"','\'')+'</li>'
    
    conten += '</ul>" title="'+token+'\">'+token+"</span>"
    
    frase = frase[:cont] + frase[cont:].replace(token, conten, 1)
    cont += len(conten)
    
    return frase

def creaPilSin(token, sin, synset, frase):
    global color
    global cont
    
    if color == 0:
        conten = popover1
    elif color == 1:
        conten = popover2
    else:
        conten = popover3
    
    conten += "Synset : <i>"+synset.name()+"</i>"
    for ss in synset.lemma_names():
        if ss == sin:
            conten += "<li><b>"+ss+"</b></li>"
        else:
            conten += '<li><i>'+ss+'</i></li>'
    
    conten += '</ul>" title=" Palabra original : <b>'+token+'</b> \">'+sin.replace('_', ' ')+"</span>"
    
    frase = frase[:cont] + frase[cont:].replace(token, conten,1)
    cont += len(conten)
    
    return frase

def creaPilAnt(token, ant, synset, frase):
    global color
    global cont
    
    if color == 0:
        conten = popover1
    elif color == 1:
        conten = popover2
    else:
        conten = popover3
    
    conten += "Synset : <i>"+synset.name()+"</i>"
    for ss in synset.lemmas():
        if(ss.antonyms()):
            for an in ss.antonyms(): 
                if an.name() == ant:
                    conten += "<li><b>"+an.name()+"</b></li>"
                else:
                    conten += '<li><i>'+an.name()+'</i></li>'
    
    conten += '</ul>" title=" Palabra original : <b>'+token+'</b> \">'+ant.replace('_', ' ')+"</span>"
    
    frase = frase[:cont] + frase[cont:].replace(token, conten,1)
    cont += len(conten)
    
    return frase

#-----------------------
# Funciones principales
#-----------------------

def desambiguar(men):
    # Para que no den problemas los carateres los reemplazo
    global cont
    
    # Separo el texto en frases
    frases = sentence_tokenizer.tokenize(men)
    
    for frase in frases:
        
        nfrase = frase #Nueva frase
        
        # Proceso la frase
        doc = nlp(frase)
        cont = 0
        # Busco las palabras ambiguas de la frase
        for token in doc:
            cont = nfrase.find(token.text,cont)
            
            # Intento desambiguar
            synset = lesk(doc, token.text)
            if synset and len(wn.synsets(token.text)) > 1:
                nfrase = creaPildora(token.text, synset.name(), nfrase)
            else:
                cont += len(token.text)
        men = men.replace(frase,nfrase,1)
    
    return men

def sinonimos(men):
    global cont
    global color
    
    # Separo el texto en frases
    frases = sentence_tokenizer.tokenize(men)
    
    for frase in frases:
        
        nfrase = frase #Nueva frase
        
        # Proceso la frase
        doc = nlp(frase)
        cont = 0
        # Busco las palabras ambiguas de la frase
        for token in doc:
            cont = nfrase.find(token.text,cont)
            
            # Intento desambiguar
            synset = lesk(doc, token.text)
            if synset and synset.name().split(".")[1] in [wn.ADJ, wn.NOUN, wn.VERB]:
                # Busco un sinónimo
                for sin in synset.lemma_names():
                    if token.text.lower() != sin.lower():
                        # Compruebo que es para asignarle un color
                        if synset.name().split(".")[1] in wn.ADJ:
                            color=0
                        elif synset.name().split(".")[1] in wn.NOUN:
                            color=1
                        else:
                            color=2
                        
                        # Sustituyo el sinonimo en la frase
                        nfrase = creaPilSin(token.text, sin, synset, nfrase)
                        break
            else:
                cont += len(token.text)
        men = men.replace(frase,nfrase,1)
    
    return men

def antonimos(men):
    global cont
    global color
    
    # Separo el texto en frases
    frases = sentence_tokenizer.tokenize(men)
    
    for frase in frases:
        
        nfrase = frase #Nueva frase
        
        # Proceso la frase
        doc = nlp(frase)
        cont = 0
        # Busco las palabras ambiguas de la frase
        for token in doc:
            cont = nfrase.find(token.text,cont)
            
            # Intento desambiguar
            synset = lesk(doc, token.text)
            if synset:
                
                # Busco un antónimo para el adjetivo encontrado
                for lema in wn.synset(synset.name()).lemmas():
                    if lema.antonyms():
                        
                        # Compruebo que es para asignarle un color
                        if synset.name().split(".")[1] in wn.ADJ:
                            color=0
                        elif synset.name().split(".")[1] in wn.NOUN:
                            color=1
                        else:
                            color=2
                        
                        for ant in lema.antonyms():
                            if ant.name() != token.text:
                                # Sustituyo el antónimo en la frase
                                nfrase = creaPilAnt(token.text, ant.name(), synset, nfrase)
                                break
                        break
            else:
                cont += len(token.text)
        men = men.replace(frase,nfrase,1)
    
    return men