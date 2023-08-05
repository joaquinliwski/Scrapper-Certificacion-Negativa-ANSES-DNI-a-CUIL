Descargar Chromedriver de: https://chromedriver.chromium.org/downloads
Un tutorial con intuiciones basicas de como hacerlo: https://www.youtube.com/watch?v=SPM1tm2ZdK4
Librerias necesarias (instalar desde consola o Conda). 
selenium
time
os
datetime
numpy
pandas
random

Sobre los archivos:
El archivo DNItoCUIL.py corre la funcion CUILArg que transforma un df con variables de sexo y DNI a CUIL. Hasta el año pasado el CUIL era una función del sexo y DNI. 
En base a estos dos generaba los dos primeros digitos y el digito verificador, explotamos eso. 
En este solo hay que cambiar lo siguiente:

# Inputs 
wd = r'C:/Users/Joaquin/Desktop/DNIs/'  # Cambiar por la carpeta en la cual esta todo.
dnis_file_name = r'DNIs'  # Cambiar por nombre del archivo que contiene los dnis/asegurarse que sea un csv
gender_column ='sexo'  # Nombre de la columna que contiene genero/sexo
dni_column = 'DNI'  # Nombre de la columna que contiene DNI
subfiles_number = 5 # En cuantos archivos distintos se va a guardar, o en cuantas computadoras distintas se va a correr. 
headless = True # True si no se quiere ver el driver, False si lo queremos ver. Es decir, True si no se quere ver la ventana de Chrome. Recomiendo verla para saber si esta saliendo access denied. 

SOBRE EL MES: Hay dos opciones, una a la que se le ponen inputs iniciales y finales de mes y año, y otra que extrae los ultimos seis meses desde el momento que se scrappea.
Si se desea usar la primera, se deja descomentado el codigo abajo de "# Fecha elegida por quien lo corra.", cambiando solo los numeros de mes y año se puede adaptar.
Si se desea usar la segunda, se debe descomentar lo que está abajo de "TODAY" y "SIX MONTHS AGO". Si se quiere hacer hace menos tiempo, cambiar el "timedelta(days=6*30)" por la cantidad de meses. Ejemplo, "timedelta(days=3*30)" para 3 meses.
RECUERDEN, solo se puede obtener los ultimos seis meses.


El archivo base es scrapper.py. Este realiza lo siguiente:
-ESTO ES LO QUE HAY QUE CAMBIAR: Establece las variables de entrada, como la ubicación de los archivos de entrada y salida, el nombre del archivo CSV con los DNIs, la ruta al driver de Chrome, y el número del primer fragmento.
	-SE CAMBIA SOLO LO QUE ESTA ENTRE ''.
		wd = r'C:/Users/Joaquin/Desktop/DNIs/'  # Path a la carpeta
		path_to_chromedriver = r'C:/Program Files/chromedriver.exe' #Path al driver
		dnis_file_name = r'DNICUILS.csv' # Nombre del archivo con CUILS
		chunk_size = 5 # De a cuantos DNIs vas a ir extrayendo antes de esperar un tiempito
	-Poner directorio en wd.
	-Guardar csv con dnis en Inputs
	-Pner nombre del archivo con dnis en dnis_file_name. No olvidar el csv.
	-Poner como se llama la columna con los dnis en dni_column_name.
-Se fija si existe el csv de certificaciones, si no, lo crea. 
-Define una lista de "User Agents": Se definen diferentes "User Agents" para el navegador, que son cadenas de texto utilizadas para simular diferentes navegadores y sistemas operativos. Esto se hace para evitar bloqueos de acceso por parte del sitio web. 
-Inicia el navegador Chrome.
-Lee los datos del archivo CSV que contiene los DNIs y los almacena en un DataFrame, se queda con los que no han sido scrappeados. 
-Bucle principal: El código se ejecuta en un bucle para procesar los DNIs en lotes (chunks). En cada iteración del bucle, se abre el navegador Chrome con un "User Agent" específico para evitar el bloqueo del acceso. Luego, se ingresa a un sitio web y se realizan varias operaciones para obtener información asociada a los DNIs.
-Extraer información del sitio web: Para cada DNI, se ingresa en el sitio web proporcionando ciertos datos (como el DNI, CUIL, fechas, etc.) y se extrae información como el nombre, CUIL, certificación, observaciones, etc.
-Procesar y guardar los datos: La información extraída se procesa y se guarda en un DataFrame. Se generan nuevas columnas en función de ciertas condiciones y se guarda el resultado en un archivo CSV.
-Repetir con diferentes "User Agents": Después de cada lote de DNIs procesado, se cambia el "User Agent" para evitar la detección y bloqueo del sitio web. Esto se realiza para asegurarse de que no se bloqueen las solicitudes después de un uso extensivo del sitio.
-Finalización del proceso: El código imprime un mensaje para indicar que ha finalizado su ejecución.

QUEDA GUARDADO EN OUTPUTS: certificaciones.csv es el archivo con todo. El mismo presenta las columnas descriptas en 'variables.txt'. Se extrae la informacion de observaciones. Si se emitio la certificacion negativa,en general no presenta nada, salvo AUH que no impide la misma. Si la presenta, se fija por que es. 
 

NOTA: En el codigo a veces aparece cuit en lugar de cuil. Esto es asi debido a un error de ANSES, cuando no esta disponible el cuil, salta
'CUIT incorrecto', ademas de que en el codigo de la pagina lo que corresponde al cuil esta guardado con cuit en el nombre. Importante,
NO cambiar esto a menos que cambie la pagina del ANSES.
Dado que ignora los accesos denegados, hay que ir fijandose si los mismos saltan. 

DNIs.csv es el csv con dnis que use para probar. 