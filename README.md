# PLN
## Implementación

### programa.py
Este archivo es el principal, es la “función main” de la aplicación. Es el encargado hacer de servidor, recibe las peticiones y utiliza las funciones de los demás ficheros para procesar el texto. Además es el encargado de leer el texto.

### semantico.py
Este fichero es el que contiene las distintas funciones para las peticiones del análisis semántico (Desambiguación, Sinónimos y Antónimos).

### morfologico.py
Este fichero es el que contiene la función para realizar el análisis morfológico del texto.

### entidades.py
Por último, este fichero es el que contiene la función para realizar el reconocimiento de entidades del texto.

*El código de todos los archivos está comentado, de la forma más detallada posible.*

Las distintas carpetas contienen :

● **codigo** : contiene los ficheros de apoyo al programa.py .

● **static** : contiene la imagen con el logotipo de la página.

● **templates** : contiene las páginas html.

No se han necesitado rutas externas ya que una vez leído el fichero ya no se vuelve a necesitar. Todas las rutas son relativas al fichero programa.py , por lo que si no se mueve no debería haber problemas.

Además de las librerías incluidas en el archivo requirements.txt se han usado otras que ya vienen instaladas con la versión de Pyhton mencionada en dicho archivo.

## Ejecución
### Paso 1
Ejecutar el archivo programa.py que se encuentra dentro de la carpeta Practica 10.

### Paso 2
Por un problema que no e conseguido paliar se abrirá automáticamente dos ventanas en el navegador, cerrar la primera de ellas para no confundirte durante la ejecución.

### Paso 3
Cargue un archivo o introduzca un texto, después seleccione procesar. En el ejemplo se cargará un archivo, no se muestra pero solo admite ficheros *.txt* .

● Pulsar Seleccionar archivo

● Buscar el fichero y abrirlo

● Pulsar Procesar archivo

Una vez realizados estos pasos la interfaz cambiará ligeramente, habilitandose un menú, y se nos informará que el archivo se cargó con éxito.
