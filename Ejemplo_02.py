import os
import sys
import tkinter as tk
from tkinter import ttk

# Añadir la ruta de Archivos_Comunes al sys.path
ruta_archivos_comunes = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Archivos_Comunes'))
sys.path.append(ruta_archivos_comunes)

# Importar las clases generales
from Formulario import Formulario, MessageBox
# Importar las clases de configuración necesarias
from Formulario import ConfiguracionTextbox, ConfiguracionCombobox, ConfiguracionListbox
# Importar las clases de los contrloes necesarios
from Formulario import  Textbox, Combobox, Listbox

class EjemploBuscadorCadena(Formulario):
    def __init__(self):
        super().__init__("Ejemplo de BuscadorCadena", "icono.ico")
        
        # Definir fuentes de datos para las búsquedas
        self.lista_ciudades = [
            "Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", 
            "Zaragoza", "Málaga", "Murcia", "Palma", "Las Palmas",
            "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón"
        ]
        
        self.diccionario_productos = {
            1: "Ordenador portátil",
            2: "Monitor LCD",
            3: "Teclado mecánico",
            4: "Ratón inalámbrico",
            5: "Impresora láser",
            6: "Tablet Android",
            7: "Smartphone",
            8: "Auriculares Bluetooth",
            9: "Altavoces",
            10: "Webcam HD"
        }
        
        self.crear_controles()

    def crear_controles(self):
        # Frame principal
        frame_principal = self.agregar_marco(self.ventana)
        frame_principal.grid(row=0, column=0, padx=10, pady=10)
        

        config_fecha = ConfiguracionTextbox(
            titulo_control="Fecha (MM YYYY DD)",
            tipo_validacion="fecha",
            restricciones={"min": "1900-01-01", "max": "2099-12-31"},
            mascara="MM YYYY DD",
            caracteres_fijos=" "
        )

        # Controles en frame_principal (usando pack)
        self.fecha = self.agregar_textbox(frame_principal, config_fecha)
        self.fecha.grid(pady=5)
        
        
        # Frame para TextBox con búsqueda por inicio
        frame_textbox1 = self.agregar_etiqueta_marco(contenedor=frame_principal, descripcion="TextBox - Búsqueda por inicio")
        frame_textbox1.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # TextBox con búsqueda por inicio
        config_ciudad1 = ConfiguracionTextbox(
            titulo_control="CiudadI:",
            tipo_validacion="str",
            fuente_datos=self.lista_ciudades,
            permite_agregar=True,
            modo_busqueda="inicio"
        )
        
        self.ciudad1 = self.agregar_textbox(frame_textbox1, config_ciudad1)
        self.ciudad1.pack(pady=5)
        
        # Frame para TextBox con búsqueda por contenido
        frame_textbox2 = self.agregar_etiqueta_marco(contenedor=frame_principal, descripcion="TextBox - Búsqueda por contenido")
        frame_textbox2.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        
        # TextBox con búsqueda por contenido
        config_ciudad2 = ConfiguracionTextbox(
            titulo_control="CiudadC:",
            tipo_validacion="str",
            fuente_datos=self.lista_ciudades,
            permite_agregar=True,
            modo_busqueda="contenido"
        )
        
        self.ciudad2 = self.agregar_textbox(frame_textbox2, config_ciudad2)
        self.ciudad2.pack(pady=5)
        
        # Frame para ComboBox
        frame_combobox = self.agregar_etiqueta_marco(contenedor=frame_principal, descripcion="ComboBox con búsqueda")
        frame_combobox.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        
        # ComboBox
        config_producto = ConfiguracionCombobox(
            titulo_control="Producto:",
            ancho=30,
            fuente_datos=self.diccionario_productos,
            permite_agregar=False,
            modo_busqueda="contenido"
        )
        
        self.producto = self.agregar_combobox(frame_combobox, config_producto)
        self.producto.grid(row=0, column=0, padx=5, pady=5)
        
        # Frame para ListBox
        frame_listbox = self.agregar_etiqueta_marco(contenedor=frame_principal, descripcion="ListBox con búsqueda")
        frame_listbox.grid(row=4, column=0, padx=10, pady=5, sticky="nsew")
        
        # ListBox
        config_listbox = ConfiguracionListbox(
            titulo_control="Ciudades:",
            ancho=30,
            altura=5,
            fuente_datos=self.lista_ciudades,
            permite_agregar=True,
            modo_busqueda="contenido",
            titulo_busqueda="Buscar ciudad:"
        )
        
        self.listbox_ciudades = self.agregar_listbox(frame_listbox, config_listbox)
        self.listbox_ciudades.grid(row=0, column=0, padx=5, pady=5)
        
        # Botones
        frame_botones = self.agregar_marco(frame_principal)
        frame_botones.grid(row=5, column=0, pady=10)
        
        self.boton_validar = self.agregar_boton(frame_botones, "Validar", self.validar_selecciones, 10)
        self.boton_validar.grid(row=0, column=0, padx=5)
        
        self.boton_salir = self.agregar_boton(frame_botones, "Salir", self.salir, 10)
        self.boton_salir.grid(row=0, column=1, padx=5)

    def validar_selecciones(self):
        """
        Valida las selecciones actuales y muestra un mensaje con los resultados.
        """
        # Obtener valores
        ciudad1_texto = self.ciudad1.textbox.get("1.0", tk.END).strip()
        ciudad2_texto = self.ciudad2.textbox.get("1.0", tk.END).strip()
        producto_texto = self.producto.get()
        ciudad_listbox = self.listbox_ciudades.get_selected()
        
        # Preparar mensaje de resultados
        resultados = []
        
        # Validar ciudad1 (búsqueda por inicio)
        coincidencias = self.ciudad1.busca_cadena(ciudad1_texto, modo_busqueda="exacto")
        if coincidencias:
            valor, identificador = coincidencias[0]
            resultados.append(f"Ciudad (inicio): {valor} - Válida (ID: {identificador})")
        else:
            resultados.append(f"Ciudad (inicio): {ciudad1_texto} - No válida")
        
        # Validar ciudad2 (búsqueda por contenido)
        coincidencias = self.ciudad2.busca_cadena(ciudad2_texto, modo_busqueda="exacto")
        if coincidencias:
            valor, identificador = coincidencias[0]
            resultados.append(f"Ciudad (contenido): {valor} - Válida (ID: {identificador})")
        else:
            resultados.append(f"Ciudad (contenido): {ciudad2_texto} - No válida")
        
        # Validar producto
        coincidencias = self.producto.busca_cadena(producto_texto, modo_busqueda="exacto")
        if coincidencias:
            valor, identificador = coincidencias[0]
            resultados.append(f"Producto: {valor} - Válido (ID: {identificador})")
        else:
            resultados.append(f"Producto: {producto_texto} - No válido")
        
        # Validar listbox
        if ciudad_listbox:
            coincidencias = self.listbox_ciudades.busca_cadena(ciudad_listbox, modo_busqueda="exacto")
            if coincidencias:
                valor, identificador = coincidencias[0]
                resultados.append(f"Ciudad (listbox): {valor} - Válida (ID: {identificador})")
            else:
                resultados.append(f"Ciudad (listbox): {ciudad_listbox} - No válida")
        else:
            resultados.append("Ciudad (listbox): No se ha seleccionado ninguna ciudad")
        
        # Mostrar resultados
        MessageBox.mostrar_mensaje(
            "Validación", 
            "\n".join(resultados), 
            tipo="info"
        )

if __name__ == "__main__":
    app = EjemploBuscadorCadena()
    app.mostrar()