def conteo_dias():
    try: #en este bloque de try creamos el archivo con el dia uno por defecto
        with open('dias.txt','x') as archivo:# con x creamos y da error cuando el archivo ya existe
            pass
        with open('dias.txt','w') as archivo:
            archivo.write(str(1))
    except FileExistsError:# entonces cuando da error por que el archivo ya existe, se ejecuta esto
        with open('dias.txt','r') as archivo:
            dia_actual = int(archivo.read())
        with open('dias.txt','w') as archivo:
            nuevo_dia = dia_actual + 1
            archivo.write(str(nuevo_dia))
