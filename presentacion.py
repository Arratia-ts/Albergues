"""
Esta Seria nuestra Capa de Presentación
"""
#Importamos todas nuestras librerias
import tkinter as tk
import tkinter.messagebox as msgbox
import tkinter.ttk as ttk
import logica as log #con esto conectamos la capa logica con esta capa

def inicia_programa():
    log.avanza_dia_al_iniciar() 



def modulo_actualizar_datos(notebook_con_tabs):
    def handler_actualizar():
        albergue = albergue_seleccionado.get()
        if albergue == '':
            msgbox.showinfo('Error', 'Debe seleccionar un albergue')
            return
        try:
            nuevas_personas = int(entry_cant_pers.get())
            nuevos_meds = int(entry_cant_med.get())
            if nuevas_personas < 0 or nuevos_meds < 0:
                msgbox.showinfo('Error', 'Las cantidades deben ser enteros positivos o cero')
                return
            exito = log.actualiza_ocupantes_y_medicamentos(albergue, nuevas_personas, nuevos_meds)
            if exito:
                msgbox.showinfo('Éxito', f'Datos del albergue "{albergue}" actualizados correctamente.')
                entry_cant_pers.delete(0, tk.END)
                entry_cant_med.delete(0, tk.END)
                lbl_capacidades.config(text="")
                combobox_albergues.set('')
            else:
                msgbox.showinfo('Error', 'Las cantidades ingresadas superan la capacidad máxima de este albergue.')
        except ValueError:
            msgbox.showinfo('Error', 'Debe ingresar valores numéricos enteros')

    def handler_mostrar_capacidades(event):
        albergue = albergue_seleccionado.get()
        datos = log.obtiene_datos_albergue(albergue)
        if datos:
            lbl_capacidades.config(text=f"Límites -> Capacidad: {datos[4]} pers. | Medicamentos: {datos[6]} paq.")

    tab_actualizar = tk.Frame(notebook_con_tabs, borderwidth=10)
    tk.Label(tab_actualizar, text='Actualizar Ocupación y Suministros ').grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
    tk.Label(tab_actualizar, text='Seleccione Albergue:').grid(row=1, column=0, sticky="e", pady=5)
    albergue_seleccionado = tk.StringVar()
    combobox_albergues = ttk.Combobox(tab_actualizar, textvariable=albergue_seleccionado, state="readonly")
    combobox_albergues['values'] = log.obtiene_nombres_albergues()
    combobox_albergues.grid(row=1, column=1, sticky="w", pady=5, padx=15)
    combobox_albergues.bind('<<ComboboxSelected>>', handler_mostrar_capacidades)
    lbl_capacidades = tk.Label(tab_actualizar, text="", fg="blue")
    lbl_capacidades.grid(row=2, column=0, columnspan=2, pady=2)
    tk.Label(tab_actualizar, text='Nueva Cantidad Personas:').grid(row=3, column=0, sticky="e", pady=5)
    entry_cant_pers = tk.Entry(tab_actualizar, width=20)
    entry_cant_pers.grid(row=3, column=1, sticky="w", pady=5, padx=15)
    tk.Label(tab_actualizar, text='Nueva Cantidad Medicamentos:').grid(row=4, column=0, sticky="e", pady=5)
    entry_cant_med = tk.Entry(tab_actualizar, width=20)
    entry_cant_med.grid(row=4, column=1, sticky="w", pady=5, padx=15)
    tk.Button(tab_actualizar, text='Guardar Cambios', command=handler_actualizar).grid(row=5, column=1, pady=10)
    return tab_actualizar, combobox_albergues

def modulo_crear_albergue(notebook_con_tabs, combobox_actualizar, combobox_envio):
    def handler_crear():
        nombre = entry_nombre.get().strip()
        if nombre == '':
            msgbox.showinfo('Error', 'Debe ingresar un nombre para el albergue.')
            return
        try:
            lat = float(entry_lat.get())
            lon = float(entry_lon.get())
            cap_p = int(entry_cap_p.get())
            cant_p = int(entry_cant_p.get())
            cap_m = int(entry_cap_m.get())
            cant_m = int(entry_cant_m.get())
            
            if cant_p > cap_p or cant_m > cap_m:
                msgbox.showinfo('Error', 'La cantidad actual no puede ser mayor a su capacidad máxima.')
                return

            resp = log.agrega_albergue(nombre, lat, lon, cap_p, cant_p, cap_m, cant_m)
            if not resp:
                msgbox.showinfo('Error', 'El albergue ya existe en el sistema.')
                return
                
            combobox_actualizar['values'] = log.obtiene_nombres_albergues()
            combobox_envio['values'] = log.obtiene_nombres_albergues()
            
            msgbox.showinfo('Éxito', f'El albergue "{nombre}" fue inscrito exitosamente.')
            entry_nombre.delete(0, tk.END)
            entry_lat.delete(0, tk.END)
            entry_lon.delete(0, tk.END)
            entry_cap_p.delete(0, tk.END)  
            entry_cant_p.delete(0, tk.END)  
            entry_cap_m.delete(0, tk.END)
            entry_cant_m.delete(0, tk.END) 
        except ValueError:
            msgbox.showinfo('Error', 'Verifique los formatos ingresados.')

    tab_nuevo = tk.Frame(notebook_con_tabs, borderwidth=10)  
    tk.Label(tab_nuevo, text='Ingrese Datos del Nuevo Albergue ').grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
    tk.Label(tab_nuevo, text='Nombre Albergue:').grid(row=1, column=0, sticky="e", pady=3)
    entry_nombre = tk.Entry(tab_nuevo, width=20)
    entry_nombre.grid(row=1, column=1, sticky="w", pady=3, padx=15)
    tk.Label(tab_nuevo, text='Latitud:').grid(row=2, column=0, sticky="e", pady=3)
    entry_lat = tk.Entry(tab_nuevo, width=20)
    entry_lat.grid(row=2, column=1, sticky="w", pady=3, padx=15)
    tk.Label(tab_nuevo, text='Longitud:').grid(row=3, column=0, sticky="e", pady=3)
    entry_lon = tk.Entry(tab_nuevo, width=20)
    entry_lon.grid(row=3, column=1, sticky="w", pady=3, padx=15)
    tk.Label(tab_nuevo, text='Capacidad Personas:').grid(row=4, column=0, sticky="e", pady=3)
    entry_cap_p = tk.Entry(tab_nuevo, width=20)
    entry_cap_p.grid(row=4, column=1, sticky="w", pady=3, padx=15)
    tk.Label(tab_nuevo, text='Cantidad Personas:').grid(row=5, column=0, sticky="e", pady=3)
    entry_cant_p = tk.Entry(tab_nuevo, width=20)
    entry_cant_p.grid(row=5, column=1, sticky="w", pady=3, padx=15)
    tk.Label(tab_nuevo, text='Capacidad Medicamentos:').grid(row=6, column=0, sticky="e", pady=3)
    entry_cap_m = tk.Entry(tab_nuevo, width=20)
    entry_cap_m.grid(row=6, column=1, sticky="w", pady=3, padx=15)
    tk.Label(tab_nuevo, text='Cantidad Medicamentos:').grid(row=7, column=0, sticky="e", pady=3)
    entry_cant_m = tk.Entry(tab_nuevo, width=20)
    entry_cant_m.grid(row=7, column=1, sticky="w", pady=3, padx=15)
    tk.Button(tab_nuevo, text='Inscribir Albergue', command=handler_crear).grid(row=8, column=1, pady=10)
    return tab_nuevo

def modulo_ingreso_envios(notebook_con_tabs):
    def handler_guardar():
        try:
            num_envio = int(entry_num_envio.get())
            if num_envio < 0:
                msgbox.showinfo("Error", "El número de envío debe ser entero positivo.")
                return
        except ValueError:
            msgbox.showinfo("Error", "El número de envío debe ser un número entero.")
            return
            
        albergue = combobox_albergues_envio.get()
        if albergue == '':
            msgbox.showinfo("Error", "Debe seleccionar un albergue.")
            return
            
        try:
            cant_med = int(entry_cant_med.get())
            if cant_med < 0:
                msgbox.showinfo("Error", "La cantidad de medicamentos debe ser entero positivo.")
                return
        except ValueError:
            msgbox.showinfo("Error", "La cantidad de medicamentos debe ser un número entero.")
            return

        exito, mensaje = log.registra_envio(num_envio, albergue, cant_med)
        if exito:
            msgbox.showinfo("Éxito", mensaje)
            entry_num_envio.delete(0, tk.END)
            combobox_albergues_envio.set('')
            entry_cant_med.delete(0, tk.END)
        else:
            msgbox.showinfo("Error", mensaje)

    tab_envio = tk.Frame(notebook_con_tabs, borderwidth=10)
    tk.Label(tab_envio, text='Ingresar Nuevo Envío Médico ').grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
    tk.Label(tab_envio, text='Número de Vuelo/Envío:').grid(row=1, column=0, sticky="e", pady=5)
    entry_num_envio = tk.Entry(tab_envio, width=20)
    entry_num_envio.grid(row=1, column=1, sticky="w", pady=5, padx=15)
    tk.Label(tab_envio, text='Seleccione Albergue:').grid(row=2, column=0, sticky="e", pady=5)
    albergue_seleccionado = tk.StringVar()
    combobox_albergues_envio = ttk.Combobox(tab_envio, textvariable=albergue_seleccionado, state="readonly")
    combobox_albergues_envio['values'] = log.obtiene_nombres_albergues()
    combobox_albergues_envio.grid(row=2, column=1, sticky="w", pady=5, padx=15)
    tk.Label(tab_envio, text='Cantidad de Medicamentos:').grid(row=3, column=0, sticky="e", pady=5)
    entry_cant_med = tk.Entry(tab_envio, width=20)
    entry_cant_med.grid(row=3, column=1, sticky="w", pady=5, padx=15)
    tk.Button(tab_envio, text='Registrar Vuelo', command=handler_guardar).grid(row=4, column=1, pady=10)
    return tab_envio, combobox_albergues_envio



def abrir_ventana_informe(root):
    """ Toplevel para el Informe de Proyección  """
    ventana_informe = tk.Toplevel(root)
    ventana_informe.title("Informe y Proyección de Medicamentos")
    ventana_informe.geometry("700x450") 
    
    def handler_generar_informe():
        texto_informe = log.generar_texto_informe()
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, texto_informe)
        text_area.config(state=tk.DISABLED)

    tk.Button(ventana_informe, text='Actualizar Informe', command=handler_generar_informe, font=('Arial', 10, 'bold')).pack(pady=10)
    
    text_area = tk.Text(ventana_informe, wrap=tk.NONE, font=('Courier', 10), bg="#f4f4f4")
    text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    scroll_y = tk.Scrollbar(text_area, orient=tk.VERTICAL, command=text_area.yview)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.configure(yscrollcommand=scroll_y.set)
    handler_generar_informe()


def abrir_ventana_redistribucion(root):
    """ Toplevel para el Reporte de Redistribución  """
    ventana_redis = tk.Toplevel(root)
    ventana_redis.title("Redistribución de Envíos ")
    ventana_redis.geometry("600x400")
    
    # Contenedor para controles superiores
    frame_controles = tk.Frame(ventana_redis)
    frame_controles.pack(pady=10)
    
    tk.Label(frame_controles, text="Seleccione N° de Vuelo a distribuir:").grid(row=0, column=0, padx=5)
    
    vuelo_seleccionado = tk.StringVar()
    combo_vuelos = ttk.Combobox(frame_controles, textvariable=vuelo_seleccionado, state="readonly")
    combo_vuelos['values'] = log.obtiene_numeros_vuelos()
    combo_vuelos.grid(row=0, column=1, padx=5)

    def handler_ejecutar():
        if vuelo_seleccionado.get() == '':
            msgbox.showinfo("Error", "Debe seleccionar un número de vuelo.", parent=ventana_redis)
            return
        
        numero_vuelo = int(vuelo_seleccionado.get())
      
        texto_reporte = log.ejecutar_reporte_redistribucion(numero_vuelo)
        
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, texto_reporte)
        text_area.config(state=tk.DISABLED)

    tk.Button(frame_controles, text='Ejecutar y Ver Reporte', command=handler_ejecutar, bg="#84d48a").grid(row=0, column=2, padx=5)
    
    
    text_area = tk.Text(ventana_redis, wrap=tk.WORD, font=('Courier', 10), bg="#f4f4f4")
    text_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    
    scroll_y = tk.Scrollbar(text_area, orient=tk.VERTICAL, command=text_area.yview)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    text_area.configure(yscrollcommand=scroll_y.set)



def crear_barra_superior(root):    
    barra = tk.Frame(root)
    barra.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
    
    btn_informe = tk.Button(barra, text=" Ver Proyección ", command=lambda: abrir_ventana_informe(root), bg="#52baeb", font=('Arial', 10))
    btn_informe.pack(side=tk.LEFT, padx=5)
    
    
    btn_redis = tk.Button(barra, text=" Redistribución ", command=lambda: abrir_ventana_redistribucion(root), bg="#ffe600", font=('Arial', 10))
    btn_redis.pack(side=tk.LEFT, padx=5)

    def handler_salir():
       if msgbox.askyesno("Confirmar Salida", "¿Desea cerrar la jornada actual?"):
           log.cerrar_dia_al_salir() 
           root.destroy()
           
    btn_salir = tk.Button(barra, text='Cerrar Jornada y Salir', command=handler_salir, relief=tk.GROOVE, bg="#f06161")
    btn_salir.pack(side=tk.RIGHT, padx=5)



def main():
    inicia_programa() 
    root = tk.Tk()
    root.title('SENAPRED - Gestión Integrada')
    
    crear_barra_superior(root)
    
    notebook_con_tabs = ttk.Notebook(root)
    tab_actualizar, combobox_actualizar = modulo_actualizar_datos(notebook_con_tabs)
    tab_envio, combobox_envio = modulo_ingreso_envios(notebook_con_tabs)
    tab_nuevo = modulo_crear_albergue(notebook_con_tabs, combobox_actualizar, combobox_envio)
    
    notebook_con_tabs.add(tab_actualizar, text=" Actualizar Datos ")
    notebook_con_tabs.add(tab_nuevo, text=" Nuevo Albergue ")
    notebook_con_tabs.add(tab_envio, text=" Registrar Envío ")
    notebook_con_tabs.grid(row=1, column=0, padx=10, pady=10) 

    root.mainloop() 

if __name__ == "__main__":
    main()


"""
Resumiendo todo lo que es la capa de presentación es la capa donde van todos nuestros botones es mas la capa visual , que por algo va conectado con la logica que es la capa
que hace todo el pensamiento matematico y el que verifica si existen los albergues etc , Aca colocamos todo lo que es visualización , Todo lo que es Visual es Implementada en esta pagina

"""
