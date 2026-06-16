error_cant_medicamentos = None
error_num_envio = None
error_albergue = None
error_envio_doble = None

def abrir_ventana_ingreso_envio(): ## Esta Funcion resuelve el reuisito (RF6)
    ventana_ingreso_envio = tk.Toplevel()
    ventana_ingreso_envio.title("Ingreso Envios")
    tk.Label(ventana_ingreso_envio,text="Ingrese el numero de vuelo(numero entero):").pack()

    entrada_numero_envio = tk.Entry(ventana_ingreso_envio)
    entrada_numero_envio.pack()

    tk.Label(ventana_ingreso_envio,text="Ingrese el nombre del albergue:").pack()

    entrada_nombre_albergue = tk.Entry(ventana_ingreso_envio)
    entrada_nombre_albergue.pack()

    tk.Label(ventana_ingreso_envio,text="Ingrese la cantidad de medicamentos").pack()

    entrada_cantidad_medicamento = tk.Entry(ventana_ingreso_envio)
    entrada_cantidad_medicamento.pack()
    
    def guardar_datos():# aqui hacemos la validacion y luego guardamos los datos en variables
        dicc_csv = lee_datos_de_archivo()
        print(dicc_csv)
        global error_envio_doble
        global error_albergue
        global error_num_envio
        global error_cant_medicamentos
        if error_envio_doble is not None:
            error_envio_doble.destroy()
        if error_albergue is not None:
            error_albergue.destroy()
        if error_cant_medicamentos is not None:
            error_cant_medicamentos.destroy()
        if error_num_envio is not None:
            error_num_envio.destroy()
        try:
            numero_envio = int(entrada_numero_envio.get())
            print(numero_envio)  # aquí tienes el valor ingresado
            dicc_envio = lee_datos_de_archivo_envios()
            for key,data in dicc_envio.items():
                if numero_envio == data[1]:
                    frase_de_error2 = "el numero de envio ya esta ocupado"
                    error_envio_doble = tk.Label(ventana_ingreso_envio,text= frase_de_error2,fg="red")
                    error_envio_doble.pack()
            if numero_envio < 0:
                raise ValueError
        except ValueError:
            frase_de_error = "el NUMERO DE ENVIO debe ser entero positivo"
            print(frase_de_error)
            error_num_envio = tk.Label(ventana_ingreso_envio,text= frase_de_error,fg="red")
            error_num_envio.pack()
        try:
            nombre_albergue = entrada_nombre_albergue.get()
            print(nombre_albergue)
            if nombre_albergue not in dicc_csv:
                raise ValueError
        except ValueError:
            frase_de_error = "El albergue no exsites"
            print(frase_de_error)
            error_albergue = tk.Label(ventana_ingreso_envio,text= frase_de_error,fg="red")
            error_albergue.pack()

        try:
            cantidad_medicamento = int(entrada_cantidad_medicamento.get())
            print(cantidad_medicamento)
            if cantidad_medicamento < 0:
                raise ValueError
        except ValueError:
            frase_de_error = "la cantidad de medicamento debe ser entero positivo"
            print(frase_de_error)
            error_cant_medicamentos = tk.Label(ventana_ingreso_envio,text= frase_de_error,fg="red")
            error_cant_medicamentos.pack()
    
        if error_envio_doble is None and error_albergue is None and error_cant_medicamentos is None and error_num_envio is None:
            frase_de_error3 = "Los datos se guardaron correctamente"
            correcto = tk.Label(ventana_ingreso_envio,text= frase_de_error3,fg="green")
            correcto.pack()
            #GUARDAR DATOOOS-------
            dicc_final = dict()
            dia = leer_dia_actual()
            dicc_final[nombre_albergue] = [dia,numero_envio,nombre_albergue,cantidad_medicamento]
            escribe_datos_en_archivo_envios(dicc_final)

        
    tk.Button(ventana_ingreso_envio ,text="Confirmar Envio", command=guardar_datos).pack()
