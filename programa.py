# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 18:13:14 2020

@author: sjm00010
"""

import time
from flask import Flask, flash, request, redirect, render_template, Markup
import webbrowser
from random import randrange

# Archivos con las funciones para procesar el texto, dentro de la carpeta codigo
from codigo import semantico, morfologico, entidades

# Variables para Flask
app = Flask(__name__)
app.secret_key = "secret key"

# Variable para comprobar si hay algun texto cargado
cargado = False
mensaje = "" # Mensaje
cargas = [Markup('<img src="https://media.giphy.com/media/Ke3GYvneyIfsC2nNIQ/source.gif" width="100%" height="100%" style="position:absolute" frameBorder="0"></img>'),
          Markup('<img src="https://media.giphy.com/media/feN0YJbVs0fwA/source.gif" width="100%" height="100%" style="position:absolute" frameBorder="0"></img>'),
          Markup('<img src="https://media.giphy.com/media/d7nds6a6J66thCAiwH/source.gif" width="100%" height="100%" style="position:absolute" frameBorder="0"></img>'),
          Markup('<img src="https://media.giphy.com/media/l4FGFE9n1nHFagC0E/source.gif" width="100%" height="100%" style="position:absolute" frameBorder="0"></img>'),
          Markup('<img src="https://media.giphy.com/media/lNG8ZbSxsj9QcNikGJ/source.gif" width="100%" height="100%" style="position:absolute" frameBorder="0"></img>'),
          Markup('<img src="https://media.giphy.com/media/2LxosfDt7NIbu/source.gif" width="100%" height="100%" style="position:absolute" frameBorder="0"></img>'),
          Markup('<img src="https://media.giphy.com/media/l2Sq845sXUMa6RjtS/source.gif" width="100%" height="100%" style="position:absolute" frameBorder="0"></img>')
          ]

def comprueba(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt'
	
@app.route('/')
def inicio():
	return render_template('inicio.html', AR=cargado, CAR=cargas[randrange(len(cargas))])

@app.route('/archivo', methods=['POST'])
def subirArchivo():
	global cargado
	global mensaje
    
	if request.method == 'POST':
        # Comprueba si el archivo se ha cargado correctamente
		if 'file' not in request.files:
			flash('Error al cargar el archivo.')
			return redirect('/')
		file = request.files['file']
		if file.filename == '':
			flash('No se ha seleccionado ningun archivo para cargar.')
			return redirect('/')
		if file and comprueba(file.filename):
			mensaje = file.stream.read().decode('UTF-8')
			flash('Archivo cargado con exito.')
			cargado=True
			return redirect('/')
		else:
			flash('Solo se soportan .txt')
			return redirect('/')

@app.route('/texto', methods=['POST'])
def subirTexto():
    global cargado
    global mensaje
    
    if request.method == 'POST':
        texto = request.form['texto']
        if len(texto) < 5:
            flash('La longitud de texto debe ser mayor a 5.')
            return redirect('/')
        elif len(texto) == 0:
            flash('Se debe introducir un texto.')
            return redirect('/')
    mensaje=texto
    flash('Texto cargado con exito.')
    cargado=True
    return redirect('/')

@app.route('/borrar', methods=['POST'])
def resetear():
    global cargado
    global mensaje
    
    cargado=False
    mensaje=""
    flash('Archivo y texto eliminados.')
    return redirect('/')

# -------------------------------------
# Funciones para el análisis del texto
# -------------------------------------
    
# Desambiguación (semantico.py)
@app.route('/desambiguar')
def desambigua():
    global mensaje
    solucion = Markup(semantico.desambiguar(mensaje))
    time.sleep(2)
    return render_template('desambiguar.html', SOL=solucion, AR=cargado, CAR=cargas[randrange(len(cargas))])

@app.route('/sinonimos')
def sinonimo():
    global mensaje
    solucion = Markup(semantico.sinonimos(mensaje))
    time.sleep(2)
    return render_template('sinonimos.html', SOL=solucion, AR=cargado, CAR=cargas[randrange(len(cargas))])

@app.route('/antonimos')
def antonimo():
    global mensaje
    solucion = Markup(semantico.antonimos(mensaje))
    time.sleep(2)
    return render_template('antonimos.html', SOL=solucion, AR=cargado, CAR=cargas[randrange(len(cargas))])

@app.route('/amorfo')
def analmorfo():
    global mensaje
    solucion = morfologico.aMorfo(mensaje)
    time.sleep(2)
    return render_template('analisis_morfologico.html', SOL=solucion, AR=cargado, CAR=cargas[randrange(len(cargas))])

@app.route('/entidad')
def entidad():
    global mensaje
    solucion = Markup(entidades.reconoce(mensaje))
    time.sleep(2)
    return render_template('entidades.html', SOL=solucion, AR=cargado, CAR=cargas[randrange(len(cargas))])

# -------------------------------------
# Función main
# -------------------------------------

if __name__ == "__main__":
    # Abro la pagina en el navegador
    webbrowser.open('http://localhost:5000/', new=2)
    
    # Inicio el servidor
    app.run(debug=True)