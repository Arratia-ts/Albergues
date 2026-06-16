"""
Esta sera nuestra capa de logica
"""
import math # Importamos nuestras variables math para variables matematicas
import datos as dat #conecta esta capa con la capa de datos
from tabulate import tabulate # importa libreria externa para dibujar


dicc_albergues: dict[str, list] = {} #Nuestras variables locales Guarda datos de refugios
dicc_envios: dict[int, list] = {}  #Guarda los datos de los vuelos

def carga_datos_en_memoria() -> None: #Llama a las funciones de datos.py para leer los archivos CSV
    global dicc_albergues, dicc_envios #Que sean estas nuestras variables locales
    dicc_albergues = dat.lee_datos_de_archivo()
    dicc_envios = dat.lee_datos_de_archivo_envios()

def almacena_datos_en_archivo() -> None:
    dat.escribe_datos_en_archivo(dicc_albergues)
    dat.escribe_datos_en_archivo_envios(dicc_envios)  #Con esto los datos no se pierden al cerrar el programa

def avanza_dia_al_iniciar() -> None:
    dat.conteo_dias()          
    carga_datos_en_memoria()    #Flujo de inicio

def cerrar_dia_al_salir() -> None:
    procesamiento_consumo_medicamentos() #Flujo de cierre 

def procesamiento_consumo_medicamentos() -> None: #Recorre todos los albergues y saca cuanta gente y cuantas medicinas hay
    for nombre, datos in dicc_albergues.items():
        cant_personas = datos[3]       
        cant_medicamentos = datos[5]   
        consumo = int(cant_personas * 0.1)#Calculo del 10 porciento
        nueva_cantidad_med = max(0, cant_medicamentos - consumo) # Evita numeros negativos
        dicc_albergues[nombre][5] = nueva_cantidad_med
    almacena_datos_en_archivo()

def obtiene_nombres_albergues() -> list[str]: #Esto es para el RF1 Y RF3 consulta actualizaciones
    lista_albergues = list(dicc_albergues.keys()) # Ordena lista alfabeticamente rellenar los menus desplegables
    lista_albergues.sort()
    return lista_albergues

def obtiene_datos_albergue(nombre: str) -> list: # devuelve lista completa de caracteristicas de un albergue , si hay un nombre que no existe , usamos get para devolver una lista vacia y no un error
    return dicc_albergues.get(nombre, [])

def obtiene_numeros_vuelos() -> list[str]:
    """ Esto haria lo mismo practicamente solo que en vuelos """
    vuelos = list(dicc_envios.keys())
    vuelos.sort()
    return [str(v) for v in vuelos]

def agrega_albergue(nombre: str, latitud: float, longitud: float, cap_pers: int, cant_pers: int, cap_med: int, cant_med: int) -> bool:
    if nombre in dicc_albergues:
        return False
    dia_actual = dat.leer_dia_actual()
    dicc_albergues[nombre] = [
        dia_actual, latitud, longitud, 
        cant_pers, cap_pers, cant_med, cap_med
    ]
    almacena_datos_en_archivo()
    return True


def actualiza_ocupantes_y_medicamentos(nombre: str, cant_pers: int, cant_med: int) -> bool:
    """ Esta Funcion Actualiza a tantos ocupantes como medicamentos """
    if nombre not in dicc_albergues:
        return False
    cap_pers_max = dicc_albergues[nombre][4]
    cap_med_max = dicc_albergues[nombre][6]
    if cant_pers > cap_pers_max or cant_med > cap_med_max:
        return False
    dicc_albergues[nombre][3] = cant_pers  
    dicc_albergues[nombre][5] = cant_med   
    almacena_datos_en_archivo()
    return True

def registra_envio(numero_envio: int, albergue: str, cantidad: int) -> tuple[bool, str]:
    """ Con esto verificamos que si el albergue existe en el sistema 
    Al igual que verifica cuando el numero de envios si estan registrados en el sistema """

    if albergue not in dicc_albergues:
        return False, "El albergue seleccionado no existe en el sistema."
    if numero_envio in dicc_envios:
        return False, "El número de envío ya está registrado en el sistema."
            

    dia_actual = dat.leer_dia_actual()
    dicc_envios[numero_envio] = [dia_actual, numero_envio, albergue, float(cantidad)]
    almacena_datos_en_archivo()
    
    return True, "Vuelo registrado correctamente. Diríjase a 'Redistribución' para ver el reporte."

"""    Con esta Función logramos generar el informe   """

def generar_texto_informe() -> str:
    if not dicc_albergues:
        return "No hay datos de albergues para generar el informe." #entrara aca si no encuentra datos para generar el informe
    informe = " Estado Actual Albergues \n"
    for nombre, datos in dicc_albergues.items():
        dia_crea, lat, lon, p_actual, p_cap, m_actual, m_cap = datos
        informe += f"Nombre: {nombre:<10} | Coord: ({lat}, {lon}) | Personas: {p_actual}/{p_cap} | Medicamentos: {m_actual}/{m_cap}\n"
    informe += "\n Proyeccion para proximos 7 Dias \n"
    headers = ["Albergue", "Día 1", "Día 2", "Día 3", "Día 4", "Día 5", "Día 6", "Día 7"]
    tabla_proyeccion = []
    for nombre, datos in dicc_albergues.items():
        p_actual = datos[3]
        m_actual = datos[5]
        consumo_diario = p_actual / 10.0
        stock_dinamico = float(m_actual) 
        fila = [nombre]
        for _ in range(7):
            stock_dinamico -= consumo_diario
            if stock_dinamico < 0:
                stock_dinamico = 0
            if stock_dinamico == int(stock_dinamico):
                fila.append(int(stock_dinamico))
            else:
                fila.append(round(stock_dinamico, 1))
        tabla_proyeccion.append(fila)
    tabla_str = tabulate(tabla_proyeccion, headers=headers, numalign="center", stralign="left", tablefmt="grid")
    informe += tabla_str
    return informe #Con esto empieza a construir lo que es el informe con los debidos calculos para lograr generar una tabla con una estadistica de las proyeccion en 7 dias



"""    Con estas Funciones Logramos todo el Calculo que requiere el RF8   """
def calcular_distancia(lat1, lon1, lat2, lon2):
    distancia = math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
    return distancia

def buscar_albergue_mas_cercano(origen, usados, simulacion_meds):
    """ Busca distancia siempre considerando los datos simulados, no los reales """
    lat_origen = dicc_albergues[origen][1]
    lon_origen = dicc_albergues[origen][2]
    menor_distancia = float("inf")
    mejor_albergue = None

    for nombre, info in dicc_albergues.items():
        if nombre in usados:
            continue
            

        cant_med_simulada = simulacion_meds[nombre]
        cap_med = info[6]
        
  
        if cant_med_simulada >= cap_med:
            continue
        
        lat = info[1]
        lon = info[2]
        distancia = calcular_distancia(lat_origen, lon_origen, lat, lon)
        
        if distancia < menor_distancia:
            menor_distancia = distancia
            mejor_albergue = nombre
            
    return mejor_albergue

def ejecutar_reporte_redistribucion(numero_vuelo: int) -> str:
    """ 
    
    """
    if numero_vuelo not in dicc_envios:
        return "El número de envío no existe."

    envio = dicc_envios[numero_vuelo]
    dia = envio[0]
    destino = envio[2]
    carga = int(envio[3])


    reporte = f"Envío número {numero_vuelo}, días {dia}, destino: {destino}, carga: {carga}\n"


    simulacion_meds = {nombre: datos[5] for nombre, datos in dicc_albergues.items()}

    sobrante = carga
    usados = []
    actual = destino

    while sobrante > 0:
        if actual is None:
            break

        usados.append(actual)
        info = dicc_albergues[actual]
        
        cant_med_actual = simulacion_meds[actual]
        cap_med = info[6]
        espacio = cap_med - cant_med_actual

        if espacio <= 0:
            actual = buscar_albergue_mas_cercano(destino, usados, simulacion_meds)
            continue

        almacenado = min(sobrante, espacio)
        nuevo_total = cant_med_actual + almacenado
        

        simulacion_meds[actual] = nuevo_total
        sobrante -= almacenado


        reporte += f"{actual} pasa de {cant_med_actual}/{cap_med} a {nuevo_total}/{cap_med}, sobrando {sobrante}\n"

        if sobrante > 0:
            actual = buscar_albergue_mas_cercano(destino, usados, simulacion_meds)

    if sobrante > 0:
    
        reporte += f"Se reporta la pérdida de {sobrante} paquetes de medicamentos\n"


    return reporte

def test() -> None:
    """
    Esto simplemente lo tenemos para testear
    """
    print("--- Test Capa de Lógica ---")
    carga_datos_en_memoria()
    print("Albergues disponibles inicialmente:", obtiene_nombres_albergues())
    
    # Prueba de inserción simulada
    registro_nuevo = agrega_albergue("Refugio_Test", -39.814, -73.245, 100, 10, 200, 50)
    print(f"¿Se registró el nuevo albergue de prueba?: {registro_nuevo}")
    print("Albergues actualizados:", obtiene_nombres_albergues())

if __name__ == "__main__":
    test()
