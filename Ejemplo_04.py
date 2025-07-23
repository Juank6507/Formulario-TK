#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import datetime
import tkinter as tk
from tkinter import ttk
from Formulario import (
    Formulario, ConfiguracionPage, ConfiguracionTextbox, 
    ConfiguracionOptionGroup, ConfiguracionCombobox, ConfiguracionListbox,
    ConfiguracionCheckbox, ConfiguracionSelectorFecha, ConfiguracionSelectorHora,
    ConfiguracionCargarFichero, ConfiguracionDeslizante
)

# Añadir la ruta de Archivos_Comunes al sys.path
ruta_archivos_comunes = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Archivos_Comunes'))
sys.path.append(ruta_archivos_comunes)

class Ejemplo04:
    def __init__(self):
        self.formulario = Formulario("Ejemplo de Controles", "icono.ico")
        self.crear_datos_ejemplo()
        self.crear_paginas()
        self.formulario.mostrar()

    def crear_datos_ejemplo(self):
        # DataFrame para ejemplos de búsqueda
        self.df_paises = pd.DataFrame({
            'id': range(1, 11),
            'pais': ['México', 'España', 'Argentina', 'Colombia', 'Perú',
                    'Chile', 'Brasil', 'Uruguay', 'Venezuela', 'Ecuador']
        })

    def crear_paginas(self):
        # Página 1: Textbox
        self.page_textbox = self.formulario.agregar_page(
            self.formulario.ventana,
            ConfiguracionPage(
                titulo="TEXTBOX - TIPOS DE VALIDACIÓN"
            )
        )
        self.crear_controles_textbox(self.page_textbox)

        # Página 2: OptionGroup
        self.page_optiongroup = self.formulario.agregar_page(
            self.formulario.ventana,
            ConfiguracionPage(
                titulo="OPTIONGROUP - DIFERENTES CONFIGURACIONES"
            )
        )
        self.crear_controles_optiongroup(self.page_optiongroup)

        # Página 3: Búsquedas
        self.page_busquedas = self.formulario.agregar_page(
            self.formulario.ventana,
            ConfiguracionPage(
                titulo="CONTROLES CON BÚSQUEDA"
            )
        )
        self.crear_controles_busqueda(self.page_busquedas)

        # Página 4: Otros Controles
        self.page_otros = self.formulario.agregar_page(
            self.formulario.ventana,
            ConfiguracionPage(
                titulo="OTROS CONTROLES"
            )
        )
        self.crear_controles_otros(self.page_otros)

    def crear_controles_textbox(self, contenedor):
        # Frame para datos personales
        frame_datos = contenedor.agregar_frame_seccion("Datos de Entrada")
        frame_datos.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        
        # Textbox para texto simple
        self.txt_texto = self.formulario.agregar_textbox(
            frame_datos,
            titulo_control="Texto Simple",
            tipo_validacion="str",
            ancho=30
        )
        self.txt_texto.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Frame para datos numéricos
        frame_numeros = contenedor.agregar_frame_seccion("Datos Numéricos")
        frame_numeros.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        
        # Contenedor para los controles numéricos
        frame_numeros_controles = ttk.Frame(frame_numeros)
        frame_numeros_controles.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        frame_numeros_controles.grid_columnconfigure(1, weight=1)  # Espacio entre controles
        
        # Textbox para números enteros
        self.txt_entero = self.formulario.agregar_textbox(
            frame_numeros_controles,
            titulo_control="Número Entero",
            tipo_validacion="int",
            restricciones={"min": 0, "max": 999},
            mascara="###",
            ancho=10
        )
        self.txt_entero.grid(row=0, column=0, padx=10, pady=5)
        
        # Textbox para números decimales (antes currency)
        self.txt_decimal = self.formulario.agregar_textbox(
            frame_numeros_controles,
            titulo_control="Moneda",
            tipo_validacion="float",
            restricciones={"min": 0.0, "max": 9999.99},
            mascara="####.##",
            ancho=12
        )
        self.txt_decimal.grid(row=0, column=2, padx=10, pady=5)
        
        # Frame para datos de contacto
        frame_contacto = contenedor.agregar_frame_seccion("Datos de Contacto")
        frame_contacto.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
        
        # Textbox para teléfono (usando str con máscara)
        self.txt_telefono = self.formulario.agregar_textbox(
            frame_contacto,
            titulo_control="Teléfono",
            tipo_validacion="str",
            mascara="(###) ## ## ##",
            caracteres_fijos="() ",
            ancho=15
        )
        self.txt_telefono.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Textbox para email (usando el nuevo tipo email)
        self.txt_email = self.formulario.agregar_textbox(
            frame_contacto,
            titulo_control="Email",
            tipo_validacion="email",
            ancho=30
        )
        self.txt_email.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Frame para datos fiscales
        frame_fiscal = contenedor.agregar_frame_seccion("Datos Fiscales")
        frame_fiscal.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')
        
        # Textbox para RFC (usando str con máscara)
        self.txt_rfc = self.formulario.agregar_textbox(
            frame_fiscal,
            titulo_control="RFC",
            tipo_validacion="str",
            mascara="XXXX######XXX",
            ancho=15
        )
        self.txt_rfc.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def crear_controles_optiongroup(self, contenedor):
        # Frame para OptionGroup vertical
        frame_vertical = contenedor.agregar_frame_seccion("OptionGroup Vertical")
        frame_vertical.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        
        opciones_vertical = ["Opción 1", "Opción 2", "Opción 3"]
        self.opt_vertical = self.formulario.agregar_optiongroup(
            frame_vertical,
            "Seleccione una opción:",
            opciones_vertical,
            orientacion="vertical"
        )
        self.opt_vertical.pack(padx=10, pady=5)
        
        # Frame para OptionGroup horizontal
        frame_horizontal = contenedor.agregar_frame_seccion("OptionGroup Horizontal")
        frame_horizontal.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        
        opciones_horizontal = ["Sí", "No", "Tal vez"]
        self.opt_horizontal = self.formulario.agregar_optiongroup(
            frame_horizontal,
            "¿Está de acuerdo?",
            opciones_horizontal,
            orientacion="horizontal"
        )
        self.opt_horizontal.pack(padx=10, pady=5)

    def crear_controles_busqueda(self, contenedor):
        # Frame para búsqueda con combobox
        frame_combo = contenedor.agregar_frame_seccion("Combobox con Búsqueda")
        frame_combo.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        
        # Combobox con búsqueda
        self.cmb_pais = self.formulario.agregar_combobox(
            frame_combo,
            titulo_control="País",
            fuente_datos=self.df_paises,
            permite_agregar=True,
            modo_busqueda="inicio",
            df_columna_id='id',
            df_columna_valor='pais'
        )
        self.cmb_pais.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Frame para búsqueda con listbox
        frame_list = contenedor.agregar_frame_seccion("Listbox con Búsqueda")
        frame_list.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        
        # Listbox con búsqueda
        self.lst_pais = self.formulario.agregar_listbox(
            frame_list,
            titulo_control="País",
            fuente_datos=self.df_paises,
            permite_agregar=True,
            modo_busqueda="inicio",
            df_columna_id='id',
            df_columna_valor='pais'
        )
        self.lst_pais.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Frame para búsqueda con textbox
        frame_auto = contenedor.agregar_frame_seccion("Textbox con Autocompletado")
        frame_auto.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
        
        # Textbox con autocompletado
        self.txt_pais = self.formulario.agregar_textbox(
            frame_auto,
            titulo_control="País",
            tipo_validacion="str",
            ancho=30,
            fuente_datos=self.df_paises,
            permite_agregar=True,
            modo_busqueda="inicio",
            df_columna_id='id',
            df_columna_valor='pais'
        )
        self.txt_pais.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def crear_controles_otros(self, contenedor):
        # Frame para fecha y hora
        frame_datetime = contenedor.agregar_frame_seccion("Fecha y Hora")
        frame_datetime.grid(row=0, column=0, padx=10, pady=5, sticky='ew')
        
        # Contenedor para los controles de fecha/hora
        frame_datetime_controles = ttk.Frame(frame_datetime)
        frame_datetime_controles.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        frame_datetime_controles.grid_columnconfigure(1, weight=1)  # Espacio entre controles
        
        # Selector de Fecha
        self.sel_fecha = self.formulario.agregar_selectorfecha(
            frame_datetime_controles,
            titulo="Fecha de evento",
            valor_inicial=datetime.datetime.now(),
            formato="%d/%m/%Y",
            min_fecha=datetime.datetime(2024, 1, 1),
            max_fecha=datetime.datetime(2024, 12, 31)
        )
        self.sel_fecha.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Selector de Hora
        self.sel_hora = self.formulario.agregar_selectorhora(
            frame_datetime_controles,
            titulo="Hora del evento",
            valor_inicial=datetime.datetime.now().time(),
            formato="%H:%M:%S",
            mostrar_segundos=True,
            intervalo_minutos=15
        )
        self.sel_hora.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Frame para controles de archivo y checkbox
        frame_misc = contenedor.agregar_frame_seccion("Controles Diversos")
        frame_misc.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        
        # Checkbox
        self.chk_activar = self.formulario.agregar_checkbox(
            frame_misc,
            titulo="Activar funcionalidad",
            valor_inicial=True,
            comando=self.on_checkbox_change
        )
        self.chk_activar.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Cargar Fichero
        self.sel_archivo = self.formulario.agregar_cargarfichero(
            frame_misc,
            titulo="Seleccionar documento",
            tipos_archivo=[
                ("Documentos PDF", "*.pdf"),
                ("Documentos Word", "*.docx"),
                ("Todos los archivos", "*.*")
            ],
            modo="abrir"
        )
        self.sel_archivo.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Frame para control deslizante
        frame_slider = contenedor.agregar_frame_seccion("Control Deslizante")
        frame_slider.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
        
        # Control Deslizante
        self.deslizante = self.formulario.agregar_deslizante(
            frame_slider,
            titulo="Nivel de volumen",
            valor_inicial=50,
            valor_minimo=0,
            valor_maximo=100,
            orientacion="horizontal",
            mostrar_valor=True,
            incremento=5
        )
        self.deslizante.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def on_checkbox_change(self):
        estado = "activado" if self.chk_activar.get() else "desactivado"
        print(f"Checkbox {estado}")

if __name__ == "__main__":
    app = Ejemplo04()