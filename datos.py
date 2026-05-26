#Constantes Archivos
ARCHIVO_ALBERGUES = "albergues.csv"
ARCHIVO_DIA = "dia.txt"
def actualización_medicamento():
    resultado = {}
    with open('albergues.csv','r') as archivo:
        lineas = archivo.readlines()
    for i in lineas[1:]:
        datos = i.strip().replace('"',"").split(",")
        Med_modificacion = int(datos[4]) * 0.1 - int(datos[6])
        datos[6] = Med_modificacion
        nombre = datos[1]
        datos[0] = int(datos[0])
        datos[1] = float(datos[2])
        datos[2] = float(datos[3])
        datos[3] = int(datos[4])
        datos[4] = int(datos[5])
        datos[5] = int(datos[6])
        datos[6] = int(datos[7])
        datos.pop()
        resultado[nombre] = datos
    escribe_datos_en_archivo(resultado)




def leer_dia_actual() -> int:
    try:
        # Intentamos abrir el archivo exclusivamente para LEER ('r') el día actual
        with open(ARCHIVO_DIA, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read().strip()
            return int(contenido)  
            
    except FileNotFoundError:

        print(f"El archivo {ARCHIVO_DIA} no existe. Inicializando en el Día 1.")
        
        # Creamos el archivo nuevo en modo de escritura ('w') e inyectamos el valor "1"
        with open(ARCHIVO_DIA, 'w', encoding='utf-8') as archivo:
            archivo.write("1")
            
        return 1


# ------Seccion RF2 para leer archivos--------#
def lee_datos_de_archivo() -> dict[str, list[int, float, float, int, int, int, int]]:
    """
    Lee albergues.csv y carga los datos en memoria en un diccionario (RF2)[cite: 48].
    Clave: nombre del albergue (str) [cite: 32, 76]
    Valor: [dia_crea, latitud, longitud, cant_pers, cap_pers, cant_med, cap_med] [cite: 32, 77]
    """
    dicc_albergues = {}
    try:
        with open(ARCHIVO_ALBERGUES, 'r', encoding='utf-8') as arch:
            lineas = arch.readlines()
            
            if not lineas:
                return dicc_albergues
                
            # Omitimos la primera línea de encabezado (dia_crea,nombre,...) 
            for linea in lineas[1:]:
                linea = linea.strip()
                if not linea:
                    continue
                
                campos = linea.split(',') 
                
                # Limpieza de comillas dobles y conversión de tipos
                dia_crea = int(campos[0].strip('"'))
                nombre = campos[1].strip('"')
                latitud = float(campos[2].strip('"'))
                longitud = float(campos[3].strip('"'))
                cant_pers = int(campos[4].strip('"'))
                cap_pers = int(campos[5].strip('"'))
                cant_med = int(campos[6].strip('"'))
                cap_med = int(campos[7].strip('"'))
                
                dicc_albergues[nombre] = [
                    dia_crea, latitud, longitud, 
                    cant_pers, cap_pers, cant_med, cap_med
                ]
    except FileNotFoundError:
        # Si el archivo no existe, retorna el diccionario vacío de forma controlada [cite: 95]
        pass
    
    return dicc_albergues

# ------ 3 Escritura si el csv no existe --------#

def escribe_datos_en_archivo(dicc_albergues: dict[str, list[int, float, float, int, int, int, int]]) -> bool:
    """
    Toma el diccionario de albergues y sobrescribe el archivo albergues.csv (RF2)[cite: 96].
    Garantiza que exista una única línea por cada albergue (evita duplicados)[cite: 40].
    """
    try:
        with open(ARCHIVO_ALBERGUES, 'w', encoding='utf-8') as arch:
            # Encabezado obligatorio requerido para pruebas externas [cite: 101]
            arch.write("dia_crea,nombre,latitud,longitud,cant_pers,cap_pers,cant_med,cap_med\n")
            
            for nombre, datos in dicc_albergues.items():
                # Formato estricto: todos los campos encerrados en comillas dobles [cite: 43, 106]
                linea_csv = f'"{datos[0]}","{nombre}","{datos[1]}","{datos[2]}","{datos[3]}","{datos[4]}","{datos[5]}","{datos[6]}"\n'
                arch.write(linea_csv)
        return True
    except Exception:
        return False


# ------4 Bloque de prueba--------#
def test():
    print("Test capa de datos")
    
    # 1. Probar lectura/creación del día
    dia = leer_dia_actual()
    print(f"Día actual en el sistema: {dia}")
    
    # 2. Probar lectura de albergues
    albergues = lee_datos_de_archivo()
    print("Albergues cargados originalmente:", albergues)
    
    # 3. Simulamos añadir un registro tal como vendría de la lógica
    albergues["Paillaco"] = [dia, -42.0667, -72.8786, 90, 125, 90, 300] 

    albergues["Niebla"] = [dia , -40.0667, -72.8786, 90 , 125, 80 ,300]
    
    albergues["Rancagua"] = [dia , -40.0667, -72.8786, 90 , 125, 80 ,300]
    
    # 4. Guardar cambios en el archivo plano
    exito = escribe_datos_en_archivo(albergues)
    print(f"¿Se guardaron los datos en albergues.csv?: {exito}")



#Constantes Archivos
ARCHIVO_ENVIOS = "envios.csv"
#RF5 Sección dias

def lee_datos_de_archivo_envios() -> dict[str, list[int, float, float, int, int, int, int]]:
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
            
                
                dicc_envios[destino] = [
                    dia_crea, numero_de_vuelo, destino, carga
                ]
    except FileNotFoundError:

        pass
    
    return dicc_envios


def escribe_datos_en_archivo_envios(dicc_envios: dict[str, list[int, float, float, int, int, int, int]]) -> bool:
    
    try:
        with open(ARCHIVO_ENVIOS, 'w', encoding='utf-8') as arch:
            # Encabezado obligatorio requerido para pruebas externas [cite: 101]
            arch.write("dia_crea,numero_de_vuelo,destino,carga\n")
            
            for destino, datos in dicc_envios.items():
                # Formato estricto: todos los campos encerrados en comillas dobles [cite: 43, 106]
                linea_csv = f'"{datos[0]}","{datos[1]}","{datos[2]}","{datos[3]}"\n'
                arch.write(linea_csv)
        return True
    except Exception:
        return False


def test2():
    """
    """
    print("=== TEST CAPA DE DATOS ===")
    
    # 1. Probar lectura/creación del día
    dia = leer_dia_actual()
    print(f"Día actual en el sistema: {dia}")
    
    # 2. Probar lectura de envios
    envios = lee_datos_de_archivo_envios()
    print("Envios cargados originalmente:", envios)
    
    # 3. Simulamos añadir un registro tal como vendría de la lógica
    envios["Paillaco"] = [dia, 5, "Paillaco", 150,] 
    envios["Niebla"] = [dia , 6, "Niebla", 200]
    envios["Rancagua"] = [dia , 7, "Rancagua", 250]
    envios["Valdivia"] = [dia , 8, "Valdivia", 300]
    
    # 4. Guardar cambios en el archivo plano
    exito = escribe_datos_en_archivo_envios(envios)
    print(f"¿Se guardaron los datos en envios.csv?: {exito}")

if __name__ == "__main__":
    test()
    test2()
