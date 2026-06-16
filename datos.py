"""
Esta es nuestra capa de datos gestiona e escribe en caso de que no existan
los csv de envios y de albergues a la vez que modifica el archivo de texto de dias para 
el transcurso de los dias en nuestra plataforma
"""

# Estan serán nuestras constantes globales

ARCHIVO_ALBERGUES = "albergues.csv"
ARCHIVO_DIA = "dia.txt"
ARCHIVO_ENVIOS = "envios.csv"


def leer_dia_actual() -> int:
    """
    Esta funcion abre el archivo dia.txt en modo lectura para leer el numero
    quitando cualquier espacio o salto de linea y lo convierte en entero
    """
    try:
        with open(ARCHIVO_DIA, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read().strip()
            return int(contenido)    
    except FileNotFoundError: #En caso de que el archivo no exista lo creamos en modo escritura asi evitamos errores cuando no este el archivo
        with open(ARCHIVO_DIA, 'w', encoding='utf-8') as archivo:
            archivo.write("1")
        return 1 # devuelve y escribe uno como el dia 1

def conteo_dias() -> int:
    """
    Con esta funcion hacemos que lea el dia actual del dia.txt 
    tambien tiene su exepción si el archivo no llegase a existir en el momento de contar
    simplemente empieza desde el dia 1 sin sumar nada
    """
    try:
   
        with open(ARCHIVO_DIA, 'r', encoding='utf-8') as archivo:
            dia_actual = int(archivo.read().strip())
            
    
        nuevo_dia = dia_actual + 1
        with open(ARCHIVO_DIA, 'w', encoding='utf-8') as archivo:
            archivo.write(str(nuevo_dia))
            
        print(f"Conteo exitoso. El sistema avanzó al Día: {nuevo_dia}")
        return nuevo_dia
        
    except FileNotFoundError: # Esto es lo que permite que no entre en error y empieze contando desde el dia 1
 
        print(f"Primer inicio detectado. Inicializando sistema en el Día 1.")  # con este print podemos ver como va sumando los dias
        with open(ARCHIVO_DIA, 'w', encoding='utf-8') as archivo:
            archivo.write("1")
        return 1

def lee_datos_de_archivo() -> dict[str, list]:
    """
    Con esta funcion lee y guarda en la base de datos principal de los refugios
    """
    dicc_albergues = {} # creamos un diccionario vacio que iremos llenando con nuestros datos
    try: # en que caso de que nuestro archivo no existiese usamos una exepcion para que no se nos caiga el programa
        with open(ARCHIVO_ALBERGUES, 'r', encoding='utf-8') as arch: # abre el archivo que es nuestro csv
            lineas = arch.readlines() #devuelve una lista de string que seran cada elemento que corresponde a nuestros renglones del csv
            if not lineas:
                return dicc_albergues
            for linea in lineas[1:]:
                linea = linea.strip()
                if not linea:
                    continue
                campos = linea.split(',') 
                dia_crea = int(campos[0].strip('"'))
                nombre = campos[1].strip('"')
                latitud = float(campos[2].strip('"'))
                longitud = float(campos[3].strip('"'))
                cant_pers = int(campos[4].strip('"'))
                cap_pers = int(campos[5].strip('"'))
                cant_med = int(campos[6].strip('"'))
                cap_med = int(campos[7].strip('"'))  # Lo que va ir haciendo esto es basicamente estructurar las bases de nuestro csv con esto podemos añadirle mas reglones si lo necesitamos
                
                dicc_albergues[nombre] = [
                    dia_crea, latitud, longitud, 
                    cant_pers, cap_pers, cant_med, cap_med
                ]
    except FileNotFoundError:
        pass             # en este caso si no existe el archivo lo crea simplemente
    return dicc_albergues

def escribe_datos_en_archivo(dicc_albergues: dict[str, list]) -> bool:
    """ Esta funcion toma el diccionario que tenemos en memoria y lo guarda fisicamente en el csv """
    try:
        with open(ARCHIVO_ALBERGUES, 'w', encoding='utf-8') as arch:
            arch.write("dia_crea,nombre,latitud,longitud,cant_pers,cap_pers,cant_med,cap_med\n")
            for nombre, datos in dicc_albergues.items(): #empieza a recorrer el diccionario y saca las parejas de datos del diccionario
                linea_csv = f'"{datos[0]}","{nombre}","{datos[1]}","{datos[2]}","{datos[3]}","{datos[4]}","{datos[5]}","{datos[6]}"\n'
                arch.write(linea_csv) # aqui se irian escribiendo todos esos datos
        return True
    except Exception:
        return False #en caso de cualquier error para que no se trabe devuelve false

def lee_datos_de_archivo_envios() -> dict[int, list]:
    """
    Con esto vamos a leer los archibos de envios basicamente lo mismo que hicimos en el anterior pero con los envios
    """
    dicc_envios = {}
    try:
        with open(ARCHIVO_ENVIOS, 'r', encoding='utf-8') as arch:
            lineas = arch.readlines()
            
            if not lineas:
                return dicc_envios
            
            for linea in lineas[1:]:
                linea = linea.strip()
                if not linea:
                    continue
                
                campos = linea.split(',') 
                
                dia_crea = int(campos[0].strip('"'))
                numero_de_vuelo = int(campos[1].strip('"'))
                destino = campos[2].strip('"')
                carga = float(campos[3].strip('"'))
            
                # Usamos el número de vuelo como clave
                dicc_envios[numero_de_vuelo] = [
                    dia_crea, numero_de_vuelo, destino, carga
                ] #Esto en si es la misma teoria empezamos a creer un csv pero para los envios con los parametros necesarios
    except FileNotFoundError:
        pass
    
    return dicc_envios

def escribe_datos_en_archivo_envios(dicc_envios: dict[int, list]) -> bool:
    """
    Aqui tomaria el csv de envios , escribe y los guarda basicamente lo mismo que hace el anterior
    """
    try:
        with open(ARCHIVO_ENVIOS, 'w', encoding='utf-8') as arch:
            arch.write("dia_crea,numero_de_vuelo,destino,carga\n")
            
            for num_vuelo, datos in dicc_envios.items():
                linea_csv = f'"{datos[0]}","{datos[1]}","{datos[2]}","{datos[3]}"\n'
                arch.write(linea_csv)
        return True
    except Exception:
        return False


def test() -> None: #esta seccion es paraa simplemente ver como se guardan todo en la memoria
    print("TEST 1: CAPA DE DATOS (ALBERGUES)")
    dia = leer_dia_actual()
    print(f"Día actual en el sistema: {dia}")
    
    albergues = lee_datos_de_archivo()
    print("Albergues cargados originalmente:", albergues)
    
    albergues["Paillaco"] = [dia, -42.0667, -72.8786, 90, 125, 90, 300] 
    albergues["Niebla"] = [dia, -40.0667, -72.8786, 90, 125, 80, 300]
    albergues["Rancagua"] = [dia, -40.0667, -72.8786, 90, 125, 80, 300]
    
    exito = escribe_datos_en_archivo(albergues)
    print(f"¿Se guardaron los datos en albergues.csv?: {exito}\n")

def test2() -> None:
    print("TEST 2: CAPA DE DATOS (ENVIOS)")
    dia = leer_dia_actual()
    envios = lee_datos_de_archivo_envios()
    print("Envíos cargados originalmente:", envios)
    
    envios["Paillaco"] = [dia, 5, "Paillaco", 150.0] 
    envios["Niebla"] = [dia, 6, "Niebla", 200.0]
    envios["Rancagua"] = [dia, 7, "Rancagua", 250.0]
    envios["Valdivia"] = [dia, 8, "Valdivia", 300.0]
    
    exito = escribe_datos_en_archivo_envios(envios)
    print(f"¿Se guardaron los datos en envios.csv?: {exito}\n")

if __name__ == "__main__":
    test()
    test2()
