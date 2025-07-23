# coding: utf-8
# Este archivo crea la base de datos 'wrestling_DB' y sus tablas

# Importando módulos python
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime, time, date
import logging
import unicodedata
import re
from collections import Counter
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Formulario:
    """
    Clase para crear y gestionar formularios utilizando tkinter.

    Attributes:
        ventana (tk.Tk): Ventana principal del formulario.
        objetos_centrar (list): Lista de objetos a centrar en la ventana.
    """

    def __init__(self, titulo, iconimagen, cerrar_al_salir=True):
        self.ventana = tk.Tk()
        self.ventana.title(titulo)
        self.configurar_icono(iconimagen)
        self.cerrar_al_salir = cerrar_al_salir
        self.objetos_centrar = []
        self.controles = []  # Solo controles de entrada
        self.ventana.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.ventana.bind("<Configure>", self.on_resize)
        self.ventana.bind("<<SiguienteWidget>>", self.mover_foco)

    def configurar_icono(self, iconimagen):
        ruta_icono = os.path.join(os.path.dirname(__file__), 'Imagenes', iconimagen)
        if not os.path.exists(ruta_icono):
            ruta_icono = os.path.join(os.path.dirname(__file__), 'Imagenes', 'img_vacia_xsk_icon.ico')
        self.ventana.iconbitmap(ruta_icono)

    def on_resize(self, event):
        for objeto_contenido, centrado, padx, pady in self.objetos_centrar:
            self.centrar_objeto(objeto_contenido, centrado, padx, pady)

    def registrar_control(self, control):
        """
        Registra un control en la lista de controles relevantes.
        Solo agrega controles que tengan el método get_widget (campos de entrada).
        """
        if not hasattr(self, "controles"):
            self.controles = []
        # Solo registrar controles de entrada (Textbox, OptionGroup, Combobox, Listbox, etc.)
        if hasattr(control, "get_widget"):
            self.controles.append(control)

    def posicionar_objeto(self, objeto, gestor, **kwargs):
        if gestor == 'grid':
            objeto.grid(**kwargs)
        elif gestor == 'pack':
            objeto.pack(**kwargs)
        elif gestor == 'place':
            objeto.place(**kwargs)
        else:
            logger.warning(f"Gestor de geometría desconocido para {objeto}. Usando grid por defecto.")
            objeto.grid(**kwargs)
        return objeto

    def posicionar_centrado(self, **kwargs):
        """
        Centra la ventana principal o un objeto específico en la pantalla.
        
        Args:
            objeto: El objeto a centrar. Si no se especifica, se centra la ventana principal.
            centrado: Tipo de centrado ('TC', 'CL', 'CR', 'BC'). Por defecto, centrado completo.
            padx: Padding horizontal.
            pady: Padding vertical.
        """
        objeto_contenido = kwargs.get('objeto', self.ventana)
        centrado = kwargs.get('centrado', None)
        padx = kwargs.get('padx', None)
        pady = kwargs.get('pady', None)
        self.ventana.update()
        
        if objeto_contenido == self.ventana:
            # Centrar la ventana principal en la pantalla
            ancho_ventana = self.ventana.winfo_width()
            alto_ventana = self.ventana.winfo_height()
            pos_x = (self.ventana.winfo_screenwidth() - ancho_ventana) // 2
            pos_y = (self.ventana.winfo_screenheight() - alto_ventana) // 2
            self.ventana.geometry(f"+{pos_x}+{pos_y}")
        else:
            # Centrar el objeto específico
            self.objetos_centrar.append((objeto_contenido, centrado, padx, pady))

    def centrar_objeto(self, objeto_contenido, centrado, padx, pady):
        ancho_contenedor, alto_contenedor = self.dimensiones_objeto_contenedor(objeto_contenido)
        ancho_contenido, alto_contenido = self.dimensiones_objeto(objeto_contenido)
        coordenada_x = (ancho_contenedor - ancho_contenido) // 2 
        coordenada_y = (alto_contenedor - alto_contenido) // 2
        if padx is not None and (ancho_contenido + padx) < ancho_contenedor:
            coordenada_x = coordenada_x + padx 
        if pady is not None and (alto_contenido + pady) < alto_contenedor:
            coordenada_y = coordenada_y + pady
        if centrado:
            if centrado == 'TC':
                coordenada_y = pady
            elif centrado == 'CL':
                coordenada_x = padx 
            elif centrado == 'CR':
                coordenada_x = ancho_contenedor - ancho_contenido - padx 
            elif centrado == 'BC':
                coordenada_y = alto_contenedor - alto_contenido - pady
        objeto_contenido.place(x=coordenada_x, y=coordenada_y)
        return objeto_contenido

    def dimensiones_objeto(self, objeto):
        objeto = self.ventana if objeto is None else objeto
        ancho = objeto.winfo_width()
        alto = objeto.winfo_height()
        return ancho, alto

    def dimensiones_objeto_contenedor(self, objeto_contenido):
        identificador_contenedor = objeto_contenido.winfo_parent()
        objeto_contenedor = objeto_contenido.nametowidget(identificador_contenedor)
        ancho_contenedor = objeto_contenedor.winfo_width()
        alto_contenedor = objeto_contenedor.winfo_height()
        return ancho_contenedor, alto_contenedor

    def configurar_fondo_con_imagen(self, **kwargs):
        contenedor = kwargs.get('contenedor', self.ventana)
        ruta_imagen = kwargs.get('ruta_imagen', None) 
        imagen_fondo = tk.PhotoImage(file=ruta_imagen)
        fondo = tk.Label(contenedor, image=imagen_fondo)
        fondo.image = imagen_fondo
        fondo.place(x=0, y=0, relwidth=1, relheight=1)
        return fondo

    def agregar_marco(self, contenedor=None, bd=None, relief=None):
        contenedor = self.ventana if contenedor is None else contenedor
        marco = ttk.Frame(contenedor, borderwidth=bd, relief=relief)
        marco.grid(row=0, column=0, padx=10, pady=10)
        return marco

    def agregar_etiqueta_marco(self, **kwargs):
        contenedor = kwargs.get('contenedor', self.ventana)
        descripcion = kwargs.get('descripcion', '')
        etiqueta_marco = ttk.LabelFrame(contenedor, text=descripcion) 
        etiqueta_marco.config(width=max(etiqueta_marco.winfo_reqwidth(), 200), height=max(etiqueta_marco.winfo_reqheight(), 100)) 
        return etiqueta_marco
        
    def agregar_etiqueta(self, **kwargs):
        contenedor = kwargs.get('contenedor', self.ventana)
        descripcion = kwargs.get('descripcion', '')
        etiqueta = ttk.Label(contenedor, text=descripcion) 
        return etiqueta

    def agregar_textbox(self, contenedor, *args, **kwargs):
        config = ConfiguracionTextbox.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_textbox = Textbox(contenedor, config)
        self.registrar_control(control_textbox)
        control_textbox.textbox.bind("<<SiguienteWidget>>", self.mover_foco)
        return control_textbox
        
    def agregar_optiongroup(self, contenedor, *args, **kwargs):
        config = ConfiguracionOptionGroup.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_optiongroup = OptionGroup(contenedor, config)
        self.registrar_control(control_optiongroup)
        return control_optiongroup

    def agregar_combobox(self, contenedor, *args, **kwargs):
        config = ConfiguracionCombobox.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_combobox = Combobox(contenedor, config)
        self.registrar_control(control_combobox)
        control_combobox.combobox.bind("<<SiguienteWidget>>", self.mover_foco)
        return control_combobox

    def agregar_listbox(self, contenedor, *args, **kwargs):
        config = ConfiguracionListbox.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_listbox = Listbox(contenedor, config)
        self.registrar_control(control_listbox)
        control_listbox.entry_busqueda.bind("<<SiguienteWidget>>", self.mover_foco)
        return control_listbox
        
    def agregar_page(self, contenedor, *args, **kwargs):
        """
        Agrega una nueva página al formulario.
        
        Args:
            contenedor: Contenedor padre (normalmente self.ventana)
            *args, **kwargs: Argumentos para ConfiguracionPage
        """
        if len(args) == 1 and isinstance(args[0], ConfiguracionPage):
            config = args[0]
        else:
            config = ConfiguracionPage.from_args(*args, **kwargs)
        
        # Crear una instancia de nuestra clase Page
        control_page = Page(contenedor, config)
        self.registrar_control(control_page)
        return control_page

    def agregar_checkbox(self, contenedor, *args, **kwargs):
        config = ConfiguracionCheckbox.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_checkbox = Checkbox(contenedor, config)
        self.registrar_control(control_checkbox)
        return control_checkbox

    def agregar_selectorfecha(self, contenedor, *args, **kwargs):
        config = ConfiguracionSelectorFecha.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_selectorfecha = SelectorFecha(contenedor, config)
        self.registrar_control(control_selectorfecha)
        return control_selectorfecha

    def agregar_selectorhora(self, contenedor, *args, **kwargs):
        config = ConfiguracionSelectorHora.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_selectorhora = SelectorHora(contenedor, config)
        self.registrar_control(control_selectorhora)
        return control_selectorhora

    def agregar_cargarfichero(self, contenedor, *args, **kwargs):
        config = ConfiguracionCargarFichero.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_cargarfichero = CargarFichero(contenedor, config)
        self.registrar_control(control_cargarfichero)
        return control_cargarfichero

    def agregar_deslizante(self, contenedor, *args, **kwargs):
        config = ConfiguracionDeslizante.from_args(*args, **kwargs)
        contenedor = self.ventana if contenedor is False else contenedor
        control_deslizante = Deslizante(contenedor, config)
        self.registrar_control(control_deslizante)
        return control_deslizante

    def agregar_boton(self, contenedor, caption, comando, ancho):
        contenedor = self.ventana if contenedor is False else contenedor
        boton = tk.Button(contenedor, text=caption, command=comando, width=ancho)
        # No registrar botones en self.controles
        return boton

    def on_closing(self):
        if self.cerrar_al_salir:
            self.ventana.destroy()
        else:
            self.ventana.withdraw()

    def salir(self):
        self.on_closing()

    def mostrar(self):
        self.ventana.deiconify()
        self.ventana.mainloop() 

    def mover_foco(self, event):
        try:
            self.flujo_formulario()
        except Exception as e:
            logger.error(f"Error al mover foco: {e}")
        return "break"
    
    def _detectar_gestor_geometria(self, widget):
        if isinstance(widget, tk.Tk):
            return 'grid'
        if widget.grid_slaves():
            return 'grid'
        elif widget.pack_slaves():
            return 'pack'
        elif widget.place_slaves():
            return 'place'
        else:
            return 'unknown'    

    def flujo_formulario(self):
        """
        Valida el control actual, aplica la máscara con caracteres comodines,
        y luego mueve el foco al siguiente control de entrada habilitado.
        """
        try:
            control_actual = self.ventana.focus_get()
            for idx, control in enumerate(self.controles):
                if not hasattr(control, "get_widget"):
                    continue
                if control.get_widget() == control_actual:
                    # Validar y formatear solo si el control tiene validar_y_formatear
                    if hasattr(control, "validar_y_formatear"):
                        if not control.validar_y_formatear():
                            MessageBox.mostrar_mensaje(
                                "Error de Validación",
                                f"El dato ingresado en {control} no es válido. Por favor, corríjalo.",
                                tipo="warning"
                            )
                            control.get_widget().focus_set()
                            return
                    # Mover el foco al siguiente control de entrada habilitado
                    for next_idx in range(idx + 1, len(self.controles)):
                        next_control = self.controles[next_idx]
                        if hasattr(next_control, "get_widget"):
                            widget = next_control.get_widget()
                            # Solo enfocar si está habilitado
                            if hasattr(widget, "cget") and widget.cget("state") == "normal":
                                widget.focus_set()
                                return
                    # Si no hay más controles habilitados, puedes enfocar un botón o mostrar mensaje final
                    if hasattr(self, "boton_validar"):
                        self.boton_validar.focus_set()
                    else:
                        MessageBox.mostrar_mensaje(
                            "Formulario Completado",
                            "Todos los datos son válidos.",
                            tipo="info"
                        )
                    return
        except Exception as e:
            logger.error(f"Error en el flujo del formulario: {e}")

    def deshabilitar_todos_los_controles(self):
        """
        Deshabilita todos los controles de entrada del formulario,
        dejando visualizado el valor ingresado en cada uno.
        """
        for control in [self.fecha, self.hora, self.momento, self.telefono, self.cp, self.entero, self.decimal]:
            control.set_estado("disabled")
        self.opcion_group.habilitar(False)

    def enviar_datos(self):
        try:
            resultados = []
            errores = False
            for control in self.controles:
                if hasattr(control, 'validar_dato'):
                    entrada_validada = control.validar_dato()
                    if entrada_validada:
                        resultados.append(f"{control} validado correctamente.")
                    else:
                        resultados.append(f"{control} no es válido.")
                        errores = True
                        if hasattr(control, 'focus_set'):
                            control.focus_set()
                        break
            if errores:
                MessageBox.mostrar_mensaje(
                    "Error de Validación",
                    "\n".join(resultados),
                    tipo="warning"
                )
            else:
                self.deshabilitar_todos_los_controles()
                MessageBox.mostrar_mensaje(
                    "Formulario Enviado",
                    "Los datos fueron enviados correctamente.",
                    tipo="info"
                )
        except Exception as e:
            logger.error(f"Error al enviar los datos: {e}")
            MessageBox.mostrar_mensaje(
                "Error del sistema",
                "Hubo un problema al enviar los datos. Por favor, inténtelo de nuevo.",
                tipo="error"
            )

class MessageBox:
    """Clase para mostrar diferentes tipos de mensajes en ventanas emergentes."""

    @staticmethod
    def mostrar_mensaje(titulo, mensaje, tipo='info'):
        """Muestra un mensaje en una ventana emergente."""
        tipos_mensaje = {
            'info': messagebox.showinfo,
            'warning': messagebox.showwarning,
            'error': messagebox.showerror,
            'question': messagebox.askquestion,
            'yesno': messagebox.askyesno
        }
        if tipo in tipos_mensaje:
            return tipos_mensaje[tipo](titulo, mensaje)
        else:
            logger.warning(f"Tipo de mensaje no válido: {tipo}")

@dataclass
class ConfiguracionTextbox:
    """
    Configuración robusta para un control Textbox, compatible con máscaras y autocompletado.
    """
    titulo_control: str = ""
    tipo_validacion: str = "str"
    restricciones: Dict[str, Any] = field(default_factory=dict)
    mascara: str = ""
    caracteres_fijos: str = ""
    ancho: int = 20
    mascara_color: str = 'gray70'
    texto_color: str = 'black'
    caracter_comodin: str = " "
    habilitado: bool = True
    # Parámetros de búsqueda/autocompletado
    fuente_datos: Any = None
    permite_agregar: bool = False
    modo_busqueda: str = "inicio"
    sensible_mayusculas: bool = False
    df_columna_id: str = None
    df_columna_valor: str = None

    def __post_init__(self):
        """
        Normaliza el campo restricciones para que siempre sea un diccionario estándar.
        """
        if isinstance(self.restricciones, tuple) and len(self.restricciones) == 2:
            self.restricciones = {"min": self.restricciones[0], "max": self.restricciones[1]}
        elif isinstance(self.restricciones, (int, float)):
            self.restricciones = {"length": self.restricciones}
        elif not isinstance(self.restricciones, dict):
            self.restricciones = {}

    @classmethod
    def from_args(cls, *args, **kwargs):
        """
        Permite crear una instancia desde argumentos posicionales o nombrados.
        Si el primer argumento es una instancia de ConfiguracionTextbox, la retorna.
        """
        if args and isinstance(args[0], cls):
            return args[0]
        # Permite inicializar con argumentos posicionales (compatibilidad con ambos ejemplos)
        return cls(
            titulo_control=args[0] if len(args) > 0 else kwargs.get("titulo_control", ""),
            tipo_validacion=args[1] if len(args) > 1 else kwargs.get("tipo_validacion", "str"),
            restricciones=args[2] if len(args) > 2 else kwargs.get("restricciones", {}),
            mascara=args[3] if len(args) > 3 else kwargs.get("mascara", ""),
            caracteres_fijos=args[4] if len(args) > 4 else kwargs.get("caracteres_fijos", ""),
            ancho=args[5] if len(args) > 5 else kwargs.get("ancho", 20),
            mascara_color=args[6] if len(args) > 6 else kwargs.get("mascara_color", 'gray70'),
            texto_color=args[7] if len(args) > 7 else kwargs.get("texto_color", 'black'),
            caracter_comodin=args[8] if len(args) > 8 else kwargs.get("caracter_comodin", " "),
            fuente_datos=kwargs.get("fuente_datos", None),
            permite_agregar=kwargs.get("permite_agregar", False),
            modo_busqueda=kwargs.get("modo_busqueda", "inicio"),
            sensible_mayusculas=kwargs.get("sensible_mayusculas", False),
            df_columna_id=kwargs.get("df_columna_id", None),
            df_columna_valor=kwargs.get("df_columna_valor", None)
        )

@dataclass
class ConfiguracionOpcion:
    """
    Configuración para una opción individual dentro del OptionGroup.
    """
    valor: str
    texto: str
    habilitado: bool = True
    tooltip: str = ""
    color_texto: str = ""
    color_fondo: str = ""
    fuente: tuple = None  # (familia, tamaño, estilo)
    posicion_personalizada: tuple = None  # (fila, columna) para grid
    comando_individual: callable = None
    datos_adicionales: dict = field(default_factory=dict)
    
    @classmethod
    def from_tuple(cls, tupla):
        """Crea ConfiguracionOpcion desde tupla (valor, texto)"""
        if isinstance(tupla, tuple) and len(tupla) >= 2:
            return cls(valor=tupla[0], texto=tupla[1])
        raise ValueError("Tupla debe tener al menos (valor, texto)")
    
    @classmethod
    def from_dict(cls, diccionario):
        """Crea ConfiguracionOpcion desde diccionario"""
        return cls(**diccionario)

@dataclass
class ConfiguracionOptionGroup:
    """
    Configuración para el control OptionGroup unificado.
    """
    def __init__(self, titulo_control="Opciones", opciones=None, valor_inicial=None,
                 orientacion="vertical", habilitado=True, comando=None, ancho=20,
                 usar_ttk=True, espaciado=5, padding=2):
        self.titulo_control = titulo_control
        self.opciones = opciones or []  # Lista de tuplas (valor, etiqueta) o (valor, etiqueta, habilitado)
        self.valor_inicial = valor_inicial
        self.orientacion = orientacion  # "vertical" o "horizontal"
        self.habilitado = habilitado
        self.comando = comando
        self.ancho = ancho
        self.usar_ttk = usar_ttk  # True para ttk.optiongroup, False para tk.
        self.espaciado = espaciado  # Espaciado entre opciones
        self.padding = padding  # Padding interno
    
    @classmethod
    def from_args(cls, *args, **kwargs):
        """
        Crea una instancia de ConfiguracionOptionGroup a partir de argumentos posicionales o keywords.
        """
        config = cls()
        
        # Procesar argumentos posicionales
        if len(args) >= 1:
            config.titulo_control = args[0]
        if len(args) >= 2:
            config.opciones = args[1]
        if len(args) >= 3:
            config.valor_inicial = args[2]
        if len(args) >= 4:
            config.orientacion = args[3]
        
        # Procesar argumentos por keyword
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config

@dataclass
class ConfiguracionCombobox:
    """Configuración robusta para un control Combobox."""
    titulo_control: str = ""
    ancho: int = 20
    valores: List[Any] = field(default_factory=list)
    estado: str = "readonly"
    fuente_datos: Any = None
    permite_agregar: bool = False
    modo_busqueda: str = "inicio"
    sensible_mayusculas: bool = False
    df_columna_id: str = None
    df_columna_valor: str = None

    @classmethod
    def from_args(cls, *args, **kwargs):
        if args and isinstance(args[0], cls):
            return args[0]
        return cls(
            titulo_control=args[0] if len(args) > 0 else kwargs.get("titulo_control", ""),
            ancho=args[1] if len(args) > 1 else kwargs.get("ancho", 20),
            valores=args[2] if len(args) > 2 else kwargs.get("valores", []),
            estado=args[3] if len(args) > 3 else kwargs.get("estado", "readonly"),
            fuente_datos=kwargs.get("fuente_datos", None),
            permite_agregar=kwargs.get("permite_agregar", False),
            modo_busqueda=kwargs.get("modo_busqueda", "inicio"),
            sensible_mayusculas=kwargs.get("sensible_mayusculas", False),
            df_columna_id=kwargs.get("df_columna_id", None),
            df_columna_valor=kwargs.get("df_columna_valor", None)
        )

@dataclass
class ConfiguracionListbox:
    """Configuración robusta para un control Listbox."""
    titulo_control: str = ""
    ancho: int = 20
    altura: int = 5
    seleccion_multiple: bool = False
    fuente_datos: Any = None
    permite_agregar: bool = False
    modo_busqueda: str = "inicio"
    sensible_mayusculas: bool = False
    titulo_busqueda: str = "Buscar:"
    df_columna_id: str = None
    df_columna_valor: str = None

    @classmethod
    def from_args(cls, *args, **kwargs):
        if args and isinstance(args[0], cls):
            return args[0]
        return cls(
            titulo_control=args[0] if len(args) > 0 else kwargs.get("titulo_control", ""),
            ancho=args[1] if len(args) > 1 else kwargs.get("ancho", 20),
            altura=args[2] if len(args) > 2 else kwargs.get("altura", 5),
            seleccion_multiple=args[3] if len(args) > 3 else kwargs.get("seleccion_multiple", False),
            fuente_datos=kwargs.get("fuente_datos", None),
            permite_agregar=kwargs.get("permite_agregar", False),
            modo_busqueda=kwargs.get("modo_busqueda", "inicio"),
            sensible_mayusculas=kwargs.get("sensible_mayusculas", False),
            titulo_busqueda=args[4] if len(args) > 4 else kwargs.get("titulo_busqueda", "Buscar:"),
            df_columna_id=kwargs.get("df_columna_id", None),
            df_columna_valor=kwargs.get("df_columna_valor", None)
        )

@dataclass    
class ConfiguracionPage:
    """
    Configuración para el control Page.
    """
    def __init__(self, titulo="Página", ancho=600, alto=400, padding=20, 
                 borde=True, estilo_borde="solid", color_borde="#cccccc",
                 color_fondo="#f0f0f0",  # Color gris por defecto
                 color_texto_pestaña="black",
                 fuente_pestaña=("Arial", 9),
                 padding_pestaña=(10, 5)):
        self.titulo = titulo
        self.ancho = ancho
        self.alto = alto
        self.padding = padding
        self.borde = borde
        self.estilo_borde = estilo_borde
        self.color_borde = color_borde
        self.color_fondo = color_fondo
        self.color_texto_pestaña = color_texto_pestaña
        self.fuente_pestaña = fuente_pestaña
        self.padding_pestaña = padding_pestaña
    
    @classmethod
    def from_args(cls, *args, **kwargs):
        """
        Crea una instancia de ConfiguracionPage a partir de argumentos posicionales o keywords.
        """
        config = cls()
        
        # Procesar argumentos posicionales básicos
        if len(args) >= 1:
            config.titulo = args[0]
        if len(args) >= 2:
            config.ancho = args[1]
        if len(args) >= 3:
            config.alto = args[2]
        
        # Procesar argumentos por keyword
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config

@dataclass                 
class ConfiguracionCheckbox:
    """
    Configuración para el control Checkbox.
    """
    def __init__(self, titulo="Opción", valor_inicial=False, 
                 habilitado=True, comando=None, ancho=20):
        self.titulo = titulo
        self.valor_inicial = valor_inicial
        self.habilitado = habilitado
        self.comando = comando
        self.ancho = ancho
    
    @classmethod
    def from_args(cls, *args, **kwargs):
        """
        Crea una instancia de ConfiguracionCheckbox a partir de argumentos posicionales o keywords.
        """
        config = cls()
        
        # Procesar argumentos posicionales
        if len(args) >= 1:
            config.titulo = args[0]
        if len(args) >= 2:
            config.valor_inicial = args[1]
        
        # Procesar argumentos por keyword
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config

@dataclass            
class ConfiguracionSelectorFecha:
    """
    Configuración para el control SelectorFecha.
    """
    def __init__(self, titulo="Fecha", valor_inicial=None, formato="%d/%m/%Y",
                 habilitado=True, comando=None, ancho=10, 
                 min_fecha=None, max_fecha=None):
        self.titulo = titulo
        # Usar datetime.datetime.now().date() en lugar de datetime.date.today()
        self.valor_inicial = valor_inicial or datetime.now().date()
        self.formato = formato
        self.habilitado = habilitado
        self.comando = comando
        self.ancho = ancho
        self.min_fecha = min_fecha
        self.max_fecha = max_fecha
    
    @classmethod
    def from_args(cls, *args, **kwargs):
        """
        Crea una instancia de ConfiguracionSelectorFecha a partir de argumentos posicionales o keywords.
        """
        config = cls()
        
        # Procesar argumentos posicionales
        if len(args) >= 1:
            config.titulo = args[0]
        if len(args) >= 2:
            config.valor_inicial = args[1]
        if len(args) >= 3:
            config.formato = args[2]
        
        # Procesar argumentos por keyword
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config

@dataclass         
class ConfiguracionSelectorHora:
    """
    Configuración para el control SelectorHora.
    """
    def __init__(self, titulo="Hora", valor_inicial=None, formato="%H:%M",
                 habilitado=True, comando=None, ancho=8, 
                 intervalo_minutos=5, mostrar_segundos=False):
        self.titulo = titulo
        self.valor_inicial = valor_inicial or datetime.now().time()
        self.formato = formato
        self.habilitado = habilitado
        self.comando = comando
        self.ancho = ancho
        self.intervalo_minutos = intervalo_minutos
        self.mostrar_segundos = mostrar_segundos
    
    @classmethod
    def from_args(cls, *args, **kwargs):
        """
        Crea una instancia de ConfiguracionSelectorHora a partir de argumentos posicionales o keywords.
        """
        config = cls()
        
        # Procesar argumentos posicionales
        if len(args) >= 1:
            config.titulo = args[0]
        if len(args) >= 2:
            config.valor_inicial = args[1]
        if len(args) >= 3:
            config.formato = args[2]
        
        # Procesar argumentos por keyword
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config

@dataclass        
class ConfiguracionCargarFichero:
    """
    Configuración para el control CargarFichero.
    """
    def __init__(self, titulo="Archivo", tipos_archivo=None, 
                 directorio_inicial=None, habilitado=True, 
                 comando=None, ancho=30, modo="abrir"):
        self.titulo = titulo
        self.tipos_archivo = tipos_archivo or [("Todos los archivos", "*.*")]
        self.directorio_inicial = directorio_inicial or os.path.expanduser("~")
        self.habilitado = habilitado
        self.comando = comando
        self.ancho = ancho
        self.modo = modo  # "abrir" o "guardar"
    
    @classmethod
    def from_args(cls, *args, **kwargs):
        """
        Crea una instancia de ConfiguracionCargarFichero a partir de argumentos posicionales o keywords.
        """
        config = cls()
        
        # Procesar argumentos posicionales
        if len(args) >= 1:
            config.titulo = args[0]
        if len(args) >= 2:
            config.tipos_archivo = args[1]
        
        # Procesar argumentos por keyword
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config

@dataclass        
class ConfiguracionDeslizante:
    """
    Configuración para el control Deslizante.
    """
    def __init__(self, titulo="Valor", valor_inicial=0, valor_minimo=0, valor_maximo=100,
                 orientacion="horizontal", habilitado=True, comando=None, 
                 ancho=200, mostrar_valor=True, incremento=1):
        self.titulo = titulo
        self.valor_inicial = valor_inicial
        self.valor_minimo = valor_minimo
        self.valor_maximo = valor_maximo
        self.orientacion = orientacion  # "horizontal" o "vertical"
        self.habilitado = habilitado
        self.comando = comando
        self.ancho = ancho
        self.mostrar_valor = mostrar_valor
        self.incremento = incremento
    
    @classmethod
    def from_args(cls, *args, **kwargs):
        """
        Crea una instancia de ConfiguracionDeslizante a partir de argumentos posicionales o keywords.
        """
        config = cls()
        
        # Procesar argumentos posicionales
        if len(args) >= 1:
            config.titulo = args[0]
        if len(args) >= 2:
            config.valor_inicial = args[1]
        if len(args) >= 3:
            config.valor_minimo = args[2]
        if len(args) >= 4:
            config.valor_maximo = args[3]
        
        # Procesar argumentos por keyword
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config

class BuscadorCadena:
    """
    Clase utilitaria para búsqueda y autocompletado en fuentes de datos externas.
    No gestiona eventos ni refresco visual, solo lógica de búsqueda.
    """
    def __init__(self, fuente_datos=None, modo_busqueda="inicio", sensible_mayusculas=False,
                 permite_agregar=False, df_columna_id=None, df_columna_valor=None):
        self.fuente_datos = fuente_datos
        self.modo_busqueda = modo_busqueda
        self.sensible_mayusculas = sensible_mayusculas
        self.permite_agregar = permite_agregar
        self.df_columna_id = df_columna_id
        self.df_columna_valor = df_columna_valor
        self.coincidencias = []
        self.texto_sugerido = None

    def _normalizar_texto(self, texto):
        import unicodedata
        texto_norm = ''.join(c for c in unicodedata.normalize('NFD', texto)
                             if unicodedata.category(c) != 'Mn')
        return texto_norm.lower()

    def busca_cadena(self, texto, modo_busqueda=None, sensible_mayusculas=None, max_resultados=None):
        if not texto:
            self.coincidencias = []
            self.texto_sugerido = None
            return []

        modo = modo_busqueda or self.modo_busqueda
        texto_busqueda = self._normalizar_texto(texto)
        resultados = []
        mejor_coincidencia = None
        mejor_coincidencia_normalizada = None

        # Determinar la fuente de datos a usar
        if isinstance(self.fuente_datos, list):
            datos_procesados = [(str(i), item) for i, item in enumerate(self.fuente_datos)]
        elif isinstance(self.fuente_datos, dict):
            datos_procesados = list(self.fuente_datos.items())
        elif self._es_dataframe(self.fuente_datos):
            datos_procesados = self._procesar_dataframe(self.fuente_datos)
        elif callable(self.fuente_datos):
            try:
                resultado = self.fuente_datos(texto_busqueda, modo_busqueda, max_resultados)
                return resultado if isinstance(resultado, list) else []
            except Exception:
                return []
        else:
            return []

        for identificador, valor in datos_procesados:
            valor_str = str(valor)
            valor_comparar = self._normalizar_texto(valor_str)
            if modo == "inicio":
                if valor_str.lower().startswith(texto.lower()):
                    resultados.append((valor_str, identificador))
                    if mejor_coincidencia is None:
                        mejor_coincidencia = (valor_str, identificador)
                elif valor_comparar.startswith(texto_busqueda):
                    resultados.append((valor_str, identificador))
                    if mejor_coincidencia_normalizada is None:
                        mejor_coincidencia_normalizada = (valor_str, identificador)
            elif modo == "contenido":
                if texto.lower() in valor_str.lower():
                    resultados.append((valor_str, identificador))
                    if mejor_coincidencia is None:
                        mejor_coincidencia = (valor_str, identificador)
                elif texto_busqueda in valor_comparar:
                    resultados.append((valor_str, identificador))
                    if mejor_coincidencia_normalizada is None:
                        mejor_coincidencia_normalizada = (valor_str, identificador)
            elif modo == "exacto":
                if valor_str.lower() == texto.lower():
                    resultados.append((valor_str, identificador))
                    if mejor_coincidencia is None:
                        mejor_coincidencia = (valor_str, identificador)
                elif valor_comparar == texto_busqueda:
                    resultados.append((valor_str, identificador))
                    if mejor_coincidencia_normalizada is None:
                        mejor_coincidencia_normalizada = (valor_str, identificador)

        if mejor_coincidencia:
            self.texto_sugerido = mejor_coincidencia[0]
        elif mejor_coincidencia_normalizada:
            self.texto_sugerido = mejor_coincidencia_normalizada[0]
        elif resultados:
            self.texto_sugerido = resultados[0][0]
        else:
            self.texto_sugerido = texto

        if max_resultados and len(resultados) > max_resultados:
            resultados = resultados[:max_resultados]

        self.coincidencias = resultados
        return resultados

    def autocompletar_en_widget(self, widget, texto_usuario, tipo_widget="text"):
        """
        Realiza autocompletado visual en el widget (tk.Text, ttk.Combobox o tk.Listbox) usando la lógica de BuscadorCadena.
        """
        coincidencias = self.busca_cadena(texto_usuario)
        texto_sugerido = self.texto_sugerido if coincidencias and self.texto_sugerido else texto_usuario
        idx = texto_sugerido.lower().find(texto_usuario.lower())
        if idx == -1:
            idx = 0
        final_pos = idx + len(texto_usuario)

        if tipo_widget == "text":
            widget.delete("1.0", "end")
            widget.insert("1.0", texto_sugerido)
            widget.tag_add("sel", f"1.{idx}", f"1.{final_pos}")
            widget.mark_set("insert", f"1.{final_pos}")
        elif tipo_widget == "combobox":
            widget.delete(0, "end")
            widget.insert(0, texto_sugerido)
            widget.icursor(final_pos)
            # No seleccionar la subcadena, solo posicionar el cursor
        elif tipo_widget == "listbox":
            # Limpiar la lista y mostrar solo las coincidencias
            widget.delete(0, "end")
            for valor, _ in coincidencias:
                widget.insert("end", valor)
            # Seleccionar el primer elemento si hay coincidencias
            if coincidencias:
                widget.selection_set(0)
                widget.activate(0)

    def _es_dataframe(self, obj):
        try:
            import pandas as pd
            return isinstance(obj, pd.DataFrame)
        except ImportError:
            return False

    def _procesar_dataframe(self, df):
        try:
            if self.df_columna_id:
                id_col = self.df_columna_id
            else:
                if 'id' in df.columns:
                    id_col = 'id'
                elif 'ID' in df.columns:
                    id_col = 'ID'
                elif 'Id' in df.columns:
                    id_col = 'Id'
                else:
                    id_col = None
            if self.df_columna_valor:
                valor_col = self.df_columna_valor
            else:
                columnas_preferidas = ['nombre', 'descripcion', 'valor', 'texto', 'label', 'etiqueta']
                valor_col = None
                for col_pref in columnas_preferidas:
                    if col_pref in df.columns:
                        valor_col = col_pref
                        break
                if valor_col is None:
                    for col in df.columns:
                        if df[col].dtype == 'object':
                            valor_col = col
                            break
                if valor_col is None:
                    valor_col = df.columns[0]
            datos_procesados = []
            for index, row in df.iterrows():
                if id_col and id_col in df.columns:
                    identificador = str(row[id_col])
                else:
                    identificador = str(index)
                valor = str(row[valor_col])
                datos_procesados.append((identificador, valor))
            return datos_procesados
        except Exception:
            return []

class Textbox(tk.Frame):
    """
    Clase Textbox que representa un campo de entrada de texto con enmascaramiento, validación y búsqueda.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        
        # 1. Cargar configuración
        if len(args) == 1 and isinstance(args[0], ConfiguracionTextbox):
            config = args[0]
        else:
            config = ConfiguracionTextbox.from_args(*args, **kwargs)

        self.mascara = config.mascara
        self.caracteres_fijos = config.caracteres_fijos

        # 2. Detección robusta del carácter comodín
        if hasattr(config, "caracter_comodin") and config.caracter_comodin not in (None, "", " "):
            self.caracter_comodin = config.caracter_comodin
        else:
            # Inicializar con valor predeterminado
            self.caracter_comodin = ' '
            
            # Busca el primer carácter de la máscara que NO sea fijo NI espacio
            for c in self.mascara:
                if c not in self.caracteres_fijos and c != ' ':
                    self.caracter_comodin = c
                    break
                
        # 3. Mapear otros parámetros
        self.tipo_validacion = config.tipo_validacion
        self.fuente_datos = getattr(config, "fuente_datos", None)
        self.ancho = getattr(config, "ancho", 20)
        self.mascara_color = getattr(config, "mascara_color", None)
        self.texto_color = getattr(config, "texto_color", None)
        self.restricciones = getattr(config, "restricciones", {})

        # 4. Inicializar variables internas
        self.texto_ingresado = ""
        self.texto_formateado = ""
        self.ultima_posicion_cursor = 0
        self.ultima_tecla = None
        self.separador = ""
        self.separador_fecha = "/"
        self.separador_hora = ":"
        self.separador_momento = " "
        self.separador_miles = ","
        self.separador_decimal = "."
        self._tecla_muerta = ""
        self.buffer_usuario = ""

        # 5. Definir separadores robustos según tipo y cantidad de caracteres fijos
        if self.tipo_validacion == "momento":
            partes_fijos = self.caracteres_fijos.split(" ") if self.caracteres_fijos else []
            if len(partes_fijos) >= 2:
                self.separador_fecha = partes_fijos[0]
                self.separador_hora = partes_fijos[1]
            elif len(partes_fijos) == 1:
                self.separador_fecha = partes_fijos[0]
                self.separador_hora = ":"
            else:
                self.separador_fecha = "/"
                self.separador_hora = ":"
        elif self.tipo_validacion == "fecha":
            self.separador_fecha = self.caracteres_fijos[0] if self.caracteres_fijos else "/"
        elif self.tipo_validacion == "hora":
            self.separador_hora = self.caracteres_fijos[0] if self.caracteres_fijos else ":"

        # 6. Crear widgets visuales
        if config.titulo_control:
            self.label = ttk.Label(self, text=config.titulo_control)
            self.label.grid(row=0, column=0, sticky="w")
        
        self.textbox = tk.Text(self, height=1, width=self.ancho)
        self.textbox.grid(row=0, column=1)

        # 7. Estado inicial según configuración
        if hasattr(config, "habilitado") and not config.habilitado:
            self.textbox.config(state="disabled")
        else:
            self.textbox.config(state="normal")

        # 8. Configurar eventos según el tipo de validación
        if self.tipo_validacion == "str" and isinstance(self.fuente_datos, (pd.DataFrame, list, tuple)):
            # Usar BuscadorCadena para autocompletado
            self.buscador = BuscadorCadena(
                fuente_datos=self.fuente_datos,
                modo_busqueda=getattr(config, "modo_busqueda", "inicio"),
                permite_agregar=getattr(config, "permite_agregar", False),
                sensible_mayusculas=getattr(config, "sensible_mayusculas", False),
                df_columna_id=getattr(config, "df_columna_id", None),
                df_columna_valor=getattr(config, "df_columna_valor", None)
            )
            self.textbox.bind("<KeyRelease>", self._evento_keypress_usuario)
        else:
            # Usar eventos tradicionales para otros tipos de validación
            self.textbox.bind("<KeyPress>", self._evento_actualizar_contenido)
            self.textbox.bind("<BackSpace>", self.manejar_retroceso)
            
        # 9. Aplicar máscara
        self.aplicar_mascara()
        
        # 10. Estado inicial según configuración
        if hasattr(config, "habilitado") and not config.habilitado:
            self.textbox.config(state="disabled")
        else:
            self.textbox.config(state="normal")
        
        # 11. Asegura que los colores estén correctos según el estado inicial
        self.actualizar_colores()

    def busca_cadena(self, texto, modo_busqueda=None, sensible_mayusculas=None, max_resultados=None):
        """Delega la búsqueda al BuscadorCadena si existe."""
        
        print(f"[DEBUG] BuscadorCadena.busca_cadena llamado con: '{texto}', modo: {modo_busqueda or self.modo_busqueda}")
        
        if hasattr(self, 'buscador'):
            return self.buscador.busca_cadena(texto, modo_busqueda, sensible_mayusculas, max_resultados)
        
        print(f"[DEBUG] Resultados encontrados: {self.buscador}")
        return []

    def _evento_keypress_usuario(self, event):
        # Debug general para todos los eventos
        print(f"[DEBUG][KeyPress] keysym: {event.keysym}, char: '{event.char}', tecla_muerta: {self._tecla_muerta}")

        if event.keysym in ("Return", "Tab"):
            # Usa el texto sugerido actual si existe, si no, el buffer del usuario
            texto_final = getattr(self.buscador, "texto_sugerido", None)
            if not texto_final:
                texto_final = self.buffer_usuario
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", texto_final)
            self.textbox.tag_remove("sel", "1.0", "end")
            self.textbox.mark_set("insert", f"1.{len(texto_final)}")
            self.buffer_usuario = texto_final
            self.textbox.tk_focusNext().focus_set()
            return "break"

        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Escape'):
            return

        # Manejo de teclas muertas (acentos)
        if event.char == '' and (event.keysym.startswith('dead_') or event.keysym == 'Multi_key'):
            self._tecla_muerta = event.keysym
            print(f"[DEBUG][TeclaMuerta] Detectada tecla muerta: {self._tecla_muerta}")
            return "break"

        if event.keysym == "BackSpace":
            if self.buffer_usuario:
                self.buffer_usuario = self.buffer_usuario[:-1]
            self._refrescar_autocompletado()
            return "break"

        # Combinación de tecla muerta y carácter base
        if self._tecla_muerta:
            acentos = {
                ('dead_acute', 'a'): 'á', ('dead_acute', 'e'): 'é', ('dead_acute', 'i'): 'í',
                ('dead_acute', 'o'): 'ó', ('dead_acute', 'u'): 'ú',
                ('dead_grave', 'a'): 'à', ('dead_grave', 'e'): 'è', ('dead_grave', 'i'): 'ì',
                ('dead_grave', 'o'): 'ò', ('dead_grave', 'u'): 'ù',
                ('dead_circumflex', 'a'): 'â', ('dead_circumflex', 'e'): 'ê', ('dead_circumflex', 'i'): 'î',
                ('dead_circumflex', 'o'): 'ô', ('dead_circumflex', 'u'): 'û',
                ('dead_tilde', 'n'): 'ñ', ('dead_tilde', 'a'): 'ã', ('dead_tilde', 'o'): 'õ',
                # Soporte para teclados que usan 'Multi_key' como tecla muerta
                ('Multi_key', 'a'): 'á', ('Multi_key', 'e'): 'é', ('Multi_key', 'i'): 'í',
                ('Multi_key', 'o'): 'ó', ('Multi_key', 'u'): 'ú', ('Multi_key', 'n'): 'ñ'
            }
            combinacion = (self._tecla_muerta, event.char)
            resultado = acentos.get(combinacion)
            print(f"[DEBUG][TeclaMuerta] muerta: {self._tecla_muerta}, char: '{event.char}', resultado: '{resultado}'")
            if resultado:
                self.buffer_usuario += resultado
            elif event.char:
                self.buffer_usuario += event.char
            # Si no hay resultado y event.char está vacío, no agregues nada
            self._tecla_muerta = ""
            self._refrescar_autocompletado()
            return "break"

        # Teclas normales
        if event.char and event.char.isprintable():
            self.buffer_usuario += event.char
            self._refrescar_autocompletado()
            return "break"

    def _refrescar_autocompletado(self):
        if hasattr(self, 'buscador'):
            self.buscador.autocompletar_en_widget(self.textbox, self.buffer_usuario, tipo_widget="text")

    def get_widget(self):
        """
        Devuelve el widget interno (tk.Text) que se usará para la navegación o validación.
        """
        return self.textbox

    def set_estado(self, estado):
        """
        Cambia el estado del textbox (habilitado o deshabilitado) y actualiza los colores del control.

        Args:
            estado (str): El estado a establecer para el textbox. Debe ser "normal" para habilitar
                        o "disabled" para deshabilitar el control.

        Ejemplo de uso:
            self.cp.set_estado("normal")    # Habilita el control
            self.cp.set_estado("disabled")  # Deshabilita el control

        Al cambiar el estado, el método también actualiza automáticamente el color de fondo y el aspecto visual
        del control para reflejar el nuevo estado.
        """
        if isinstance(self.textbox, (tk.Text, tk.Entry)):
            self.textbox.config(state=estado)
        self.actualizar_colores()

    def aplicar_mascara(self, event=None):
        """
        Inicializa el textbox con la máscara configurada, sin hardcodear formatos.
        """
        if self.texto_ingresado:
            self.actualizar_colores()
            current_pos = self.textbox.index("insert")
            self.textbox.mark_set("insert", current_pos)
            self.textbox.see("insert")
            return

        self.textbox.delete("1.0", tk.END)
        if self.mascara:
            self.textbox.insert("1.0", self.mascara)
        else:
            self.textbox.insert("1.0", "")

        self.actualizar_colores()
        posicion_inicial = self.calcular_primera_posicion_editable()
        self.textbox.mark_set("insert", f"1.{posicion_inicial}")
        self.textbox.see("insert")

    def _evento_actualizar_contenido(self, event=None):
        """
        Maneja el evento de actualización de contenido cuando se presiona una tecla.
        Actualiza el texto ingresado y aplica el formato correspondiente.
        """
        print(f"[DEBUG] Tecla presionada: {event.keysym} - Texto actual: '{self.textbox.get('1.0', 'end-1c')}'")
              
        keysym = getattr(event, 'keysym', None)
        if keysym in ("Return", "Tab"):
            self.master.event_generate("<<SiguienteWidget>>")
            return "break"

        tecla_presionada = event.char

        if not tecla_presionada:  # Ignorar eventos sin caracteres
            return

        # Limitar la longitud de los dígitos para fecha
        if self.tipo_validacion == "fecha":
            digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
            if tecla_presionada.isdigit() and len(digitos) >= 8:
                print("[DEBUG] Longitud máxima de fecha alcanzada, ignorando entrada extra.")
                return

        if self.tipo_validacion == "float":
            separador_decimal = "." if "." in self.mascara else ("," if "," in self.mascara else ".")
            partes_mascara = self.mascara.split(separador_decimal)
            longitud_entera = partes_mascara[0].count(self.caracter_comodin)

            # Solo permitir dígitos y el separador decimal
            if not (tecla_presionada.isdigit() or tecla_presionada in (".", ",")):
                return "break"
            
            # Normalizar el separador decimal ingresado
            if tecla_presionada in (".", ","):
                tecla_presionada = separador_decimal
            
            # Si ya hay un separador decimal, no permitir otro
            if tecla_presionada == separador_decimal and separador_decimal in self.texto_ingresado:
                return "break"

            # --- Aquí detectamos si se completó la parte entera ---
            texto_sin_sep = self.texto_ingresado.replace(".", "").replace(",", "")
            if tecla_presionada.isdigit() and len(texto_sin_sep) == longitud_entera:
                # Insertar separador decimal automáticamente
                self.texto_ingresado += separador_decimal + tecla_presionada
                self.refrescar_textbox()
                # Mover el cursor después del separador y del primer decimal
                self.textbox.mark_set("insert", f"1.{longitud_entera + 2}")
                self.textbox.see("insert")
                return "break"

            # Agregar el carácter normalmente
            self.texto_ingresado += tecla_presionada
            self.refrescar_textbox()
            return "break"

        if self.tipo_validacion == "momento":
            if " " not in self.texto_ingresado:
                bloque = "fecha"
                separador_actual = self.separador_fecha
            else:
                bloque = "hora"
                separador_actual = self.separador_hora
                

            # Permitir solo dígitos y el separador correspondiente usando isdigit()
            if not (tecla_presionada.isdigit() or tecla_presionada == separador_actual or tecla_presionada == " "):
                print(f"[DEBUG] Caracter '{tecla_presionada}' no permitido en bloque {bloque}")
                return "break"

            # Lógica de inserción de separador automática y manual
            if tecla_presionada.isdigit():
                self.texto_ingresado += tecla_presionada

                if bloque == "fecha":
                    digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
                    if len(digitos) in (2, 4) and self.texto_ingresado.count(self.separador_fecha) < 2:
                        self.texto_ingresado += self.separador_fecha
                    elif len(digitos) == 8 and " " not in self.texto_ingresado:
                        self.texto_ingresado += " "
                else:  # bloque == "hora"
                    partes = self.texto_ingresado.split(" ")
                    parte_hora = partes[1] if len(partes) > 1 else ""
                    digitos_hora = ''.join(c for c in parte_hora if c.isdigit())
                    if len(digitos_hora) == 2 and self.separador_hora not in parte_hora:
                        self.texto_ingresado += self.separador_hora

            elif tecla_presionada == separador_actual:
                if bloque == "fecha":
                    self.manejar_separador('fecha_manual')
                else:
                    self.manejar_separador('hora_manual')

            elif tecla_presionada == " " and bloque == "fecha" and " " not in self.texto_ingresado:
                self.texto_ingresado += " "

            self.refrescar_textbox()
            return "break"

        # --- Lógica para tipo hora ---
        if self.tipo_validacion == "hora":
            if not (tecla_presionada.isdigit() or tecla_presionada == self.separador_hora):
                print(f"[DEBUG] Caracter '{tecla_presionada}' no permitido en hora")
                return "break"
            if tecla_presionada.isdigit():
                self.texto_ingresado += tecla_presionada
                digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
                if len(digitos) == 2 and self.separador_hora not in self.texto_ingresado:
                    self.texto_ingresado += self.separador_hora
            elif tecla_presionada == self.separador_hora:
                self.manejar_separador('hora_manual')
            self.refrescar_textbox()
            return "break"

        # --- Lógica para tipo fecha ---
        if self.tipo_validacion == "fecha":
            if not (tecla_presionada.isdigit() or tecla_presionada == self.separador_fecha):
                print(f"[DEBUG] Caracter '{tecla_presionada}' no permitido en fecha")
                return "break"
            if tecla_presionada.isdigit():
                self.texto_ingresado += tecla_presionada
                digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
                self.manejar_separador('fecha_auto', digitos)
            elif tecla_presionada == self.separador_fecha:
                self.manejar_separador('fecha_manual')
            self.refrescar_textbox()
            return "break"

        # --- Lógica para tipo float ---
        if self.tipo_validacion == "float":
            separador_decimal = "." if "." in self.mascara else ("," if "," in self.mascara else ".")
            partes_mascara = self.mascara.split(separador_decimal)
            longitud_entera = partes_mascara[0].count(self.caracter_comodin)

            # Solo permitir dígitos y el separador decimal
            if not (tecla_presionada.isdigit() or tecla_presionada in (".", ",")):
                return "break"
            
            # Normalizar el separador decimal ingresado
            if tecla_presionada in (".", ","):
                tecla_presionada = separador_decimal
            
            # Si ya hay un separador decimal, no permitir otro
            if tecla_presionada == separador_decimal and separador_decimal in self.texto_ingresado:
                return "break"

            # --- Aquí detectamos si se completó la parte entera ---
            texto_sin_sep = self.texto_ingresado.replace(".", "").replace(",", "")
            if tecla_presionada.isdigit() and len(texto_sin_sep) == longitud_entera:
                # Insertar separador decimal automáticamente
                self.texto_ingresado += separador_decimal + tecla_presionada
                self.refrescar_textbox()
                # Mover el cursor después del separador y del primer decimal
                self.textbox.mark_set("insert", f"1.{longitud_entera + 2}")
                self.textbox.see("insert")
                return "break"

            # Agregar el carácter normalmente
            self.texto_ingresado += tecla_presionada
            self.refrescar_textbox()
            return "break"

        # --- Lógica para tipo email ---
        if self.tipo_validacion == "email":
            # Convertir a minúsculas inmediatamente
            tecla_presionada = tecla_presionada.lower()
            self.texto_ingresado += tecla_presionada
            self.refrescar_textbox()
            return "break"

        # --- Lógica para otros tipos ---
        self.texto_ingresado += tecla_presionada
        self.refrescar_textbox()
        return "break"

    def manejar_separador(self, tipo_separador, digitos=None):
        """
        Maneja la inserción de separadores en el texto ingresado.
        Args:
            tipo_separador (str): Tipo de separador a manejar ('fecha_auto', 'fecha_manual', 'hora_manual')
            digitos (str, optional): Dígitos extraídos del texto ingresado. Necesario para 'fecha_auto'.
        """
        # Determinar el separador correcto según el contexto
        if tipo_separador.startswith('fecha'):
            sep = self.separador_fecha
        elif tipo_separador.startswith('hora'):
            sep = self.separador_hora
        else:
            sep = self.separador  # Solo si tienes un caso general, si no, puedes omitir esto

        if tipo_separador == 'fecha_auto' and digitos:
            # Manejo automático de separadores para fechas
            if self.tipo_validacion == "fecha":
                if len(digitos) == 2 and self.texto_ingresado.count(sep) == 0:
                    self.texto_ingresado += sep
                elif len(digitos) == 4 and self.texto_ingresado.count(sep) == 1:
                    self.texto_ingresado += sep
            elif self.tipo_validacion == "momento":
                if self.separador_momento not in self.texto_ingresado:
                    # Estamos en la parte de fecha del momento
                    if len(digitos) == 2 and self.texto_ingresado.count(self.separador_fecha) == 0:
                        self.texto_ingresado += self.separador_fecha
                    elif len(digitos) == 4 and self.texto_ingresado.count(self.separador_fecha) == 1:
                        self.texto_ingresado += self.separador_fecha
                    elif len(digitos) == 8 and self.texto_ingresado.count(self.separador_fecha) == 2:
                        self.texto_ingresado += self.separador_momento  # Espacio entre fecha y hora
                else:
                    # Estamos en la parte de hora del momento
                    partes = self.texto_ingresado.split(self.separador_momento)
                    parte_hora = partes[1] if len(partes) > 1 else ""
                    digitos_hora = ''.join(c for c in parte_hora if c.isdigit())
                    if len(digitos_hora) == 2 and self.separador_hora not in parte_hora:
                        self.texto_ingresado += self.separador_hora

        elif tipo_separador == 'fecha_manual':
            # Manejo manual de separadores para fechas
            if self.tipo_validacion == "fecha":
                partes = self.texto_ingresado.split(sep)
                bloque_actual = partes[-1]
                # Si el bloque actual tiene un solo dígito, rellenarlo con cero
                if len(bloque_actual) == 1 and bloque_actual.isdigit():
                    partes[-1] = "0" + bloque_actual
                    self.texto_ingresado = sep.join(partes) + sep
                else:
                    self.texto_ingresado += sep
            elif self.tipo_validacion == "momento":
                partes = self.texto_ingresado.split(self.separador_fecha)
                bloque_actual = partes[-1]
                if len(bloque_actual) == 1 and bloque_actual.isdigit():
                    partes[-1] = "0" + bloque_actual
                    self.texto_ingresado = self.separador_fecha.join(partes) + self.separador_fecha
                else:
                    self.texto_ingresado += self.separador_fecha

        elif tipo_separador == 'hora_manual':
            # Manejo manual de separadores para horas
            if self.tipo_validacion == "momento":
                partes = self.texto_ingresado.split(self.separador_momento)
                parte_hora = partes[1] if len(partes) > 1 else ""
                # Si la parte de hora tiene un solo dígito, rellenarla con cero
                if len(parte_hora) == 1 and parte_hora.isdigit():
                    partes[1] = "0" + parte_hora
                    self.texto_ingresado = self.separador_momento.join(partes) + self.separador_hora
                else:
                    self.texto_ingresado += self.separador_hora
            else:
                # Para el tipo hora
                if len(self.texto_ingresado) == 1 and self.texto_ingresado.isdigit():
                    self.texto_ingresado = "0" + self.texto_ingresado + sep
                else:
                    self.texto_ingresado += sep

    def formatear_texto(self, texto=None):
        if texto is None:
            texto = self.texto_ingresado
            

        # --- TV FECHA y TV HORA ---
        if self.tipo_validacion in ("fecha", "hora"):
            digitos = ''.join(c for c in texto if c.isdigit())
            bloques = []
            bloque_actual = ""
            separadores = []
            for char in self.mascara:
                if char in self.caracteres_fijos:
                    if bloque_actual:
                        bloques.append(bloque_actual)
                        bloque_actual = ""
                    separadores.append(char)
                else:
                    bloque_actual += char
            if bloque_actual:
                bloques.append(bloque_actual)

            resultado = ""
            idx = 0
            for i, bloque in enumerate(bloques):
                tam = len(bloque)
                parte_digitos = digitos[idx:idx+tam]
                if parte_digitos:
                    if len(bloque) == 4:  # Año: rellenar izquierda a derecha con la letra de la máscara
                        parte = parte_digitos.ljust(tam, bloque[0])
                    else:  # Día, mes, hora, minuto: rellenar con ceros a la izquierda
                        parte = parte_digitos.rjust(tam, "0")
                else:
                    parte = bloque
                resultado += parte
                idx += len(parte_digitos)
                if i < len(separadores):
                    resultado += separadores[i]
            return resultado

        # --- TV MOMENTO ---
        if self.tipo_validacion == "momento":
            if " " in self.mascara:
                mascara_fecha, mascara_hora = self.mascara.split(" ", 1)
            else:
                mascara_fecha, mascara_hora = self.mascara, ""
            partes = texto.split(" ", 1)
            fecha_txt = partes[0] if len(partes) > 0 else ""
            hora_txt = partes[1] if len(partes) > 1 else ""
            # Formatear fecha
            self.tipo_validacion = "fecha"
            self.mascara = mascara_fecha
            fecha_formateada = self.formatear_texto(fecha_txt)
            # Formatear hora
            self.tipo_validacion = "hora"
            self.mascara = mascara_hora
            hora_formateada = self.formatear_texto(hora_txt)
            # Restaurar tipo y máscara
            self.tipo_validacion = "momento"
            self.mascara = mascara_fecha + (" " + mascara_hora if mascara_hora else "")
            resultado = f"{fecha_formateada} {hora_formateada}".strip()
            return resultado

        # --- TV FLOAT ---
        if self.tipo_validacion == "float":
            separador_mascara = "." if "." in self.mascara else ("," if "," in self.mascara else ".")
            partes_mascara = self.mascara.split(separador_mascara)
            longitud_entera = partes_mascara[0].count(self.caracter_comodin)
            longitud_decimal = partes_mascara[1].count(self.caracter_comodin) if len(partes_mascara) > 1 else 0

            texto_normalizado = texto.replace(",", ".")
            
            # Determinar si estamos en modo decimal por la presencia del separador
            modo_decimal = "." in texto_normalizado
            digitos = ''.join(c for c in texto_normalizado if c.isdigit())

            # Parte entera
            if modo_decimal:
                parte_entera_txt = texto_normalizado.split(".", 1)[0]
                digitos_entera = ''.join(c for c in parte_entera_txt if c.isdigit())[:longitud_entera]
            else:
                digitos_entera = digitos[:longitud_entera]
            parte_entera = digitos_entera.rjust(longitud_entera, "0")

            # Parte decimal
            if modo_decimal:
                parte_decimal_txt = texto_normalizado.split(".", 1)[1]
                decimales = ''.join(c for c in parte_decimal_txt if c.isdigit())
            else:
                decimales = digitos[longitud_entera:]

            if len(decimales) == 0:
                parte_decimal = "0" * longitud_decimal
                buffer_decimal = ""
            else:
                # Mantener todos los decimales que quepan en la máscara
                if len(decimales) <= longitud_decimal:
                    parte_decimal = decimales.ljust(longitud_decimal, "0")
                    buffer_decimal = decimales
                else:
                    # Si hay más decimales que los permitidos, mantener todos menos el último que se reemplaza
                    parte_decimal = decimales[:longitud_decimal-1] + decimales[-1]
                    buffer_decimal = parte_decimal

            # Siempre incluir el separador y la parte decimal si la máscara lo requiere
            resultado = parte_entera + separador_mascara + parte_decimal

            # Actualiza el buffer: mantener el separador si estamos en modo decimal
            if modo_decimal:
                self.texto_ingresado = digitos_entera + separador_mascara + buffer_decimal
            else:
                self.texto_ingresado = digitos_entera + buffer_decimal

            return resultado

        # --- TV INT ---
        if self.tipo_validacion == "int":
            longitud = self.mascara.count(self.caracter_comodin)
            digitos = ''.join(c for c in texto if c.isdigit())
            if len(digitos) > longitud:
                # Mantener los primeros (N-1) y el último
                digitos = digitos[:longitud-1] + digitos[-1]
            resultado = digitos.rjust(longitud, '0')
            self.texto_ingresado = digitos
            return resultado

        # --- TV STR con máscara de comodín (CP) ---
        if self.tipo_validacion == "str" and self.caracter_comodin in self.mascara:
            longitud = self.mascara.count(self.caracter_comodin)
            caracteres = ''.join(c for c in texto if c.isalnum())
            if len(caracteres) > longitud:
                # Mantener los primeros (N-1) y el último
                caracteres = caracteres[:longitud-1] + caracteres[-1]
            resultado = ""
            indice_caracter = 0
            for char in self.mascara:
                if char == self.caracter_comodin:
                    if indice_caracter < len(caracteres):
                        resultado += caracteres[indice_caracter]
                        indice_caracter += 1
                    else:
                        resultado += self.caracter_comodin
                else:
                    resultado += char
            self.texto_ingresado = caracteres
            return resultado

        # --- TV STR sin máscara ---
        if self.tipo_validacion == "str":
            self.texto_ingresado = texto
            return texto

        # --- TV EMAIL ---
        if self.tipo_validacion == "email":
            # Eliminar espacios al inicio y final
            texto_limpio = texto.strip()
            # Convertir a minúsculas
            texto_limpio = texto_limpio.lower()
            # Eliminar espacios en medio
            texto_limpio = texto_limpio.replace(" ", "")
            self.texto_ingresado = texto_limpio
            return texto_limpio

        # --- Por defecto ---
        self.texto_ingresado = texto
        return texto

    def _determinar_parte_oscura(self):
        """
        Determina qué parte del texto formateado debe mostrarse en color oscuro,
        según el tipo de validación (fecha, hora, momento, int, float, str con máscara).
        """
        if not self.texto_ingresado:
            return ""

        texto = self.texto_ingresado
        digitos = ''.join(c for c in texto if c.isalnum())

        # --- TV FECHA y TV HORA ---
        if self.tipo_validacion in ("fecha", "hora"):
            bloques = []
            bloque_actual = ""
            separadores = []
            for char in self.mascara:
                if char in self.caracteres_fijos:
                    if bloque_actual:
                        bloques.append(bloque_actual)
                        bloque_actual = ""
                    separadores.append(char)
                else:
                    bloque_actual += char
            if bloque_actual:
                bloques.append(bloque_actual)

            parte_oscura = ""
            idx = 0
            for i, bloque in enumerate(bloques):
                tam = len(bloque)
                parte_digitos = digitos[idx:idx+tam]
                if parte_digitos:
                    if len(bloque) == 4:  # Año: solo los dígitos ingresados en oscuro
                        parte = parte_digitos
                    else:  # Día, mes, hora, minuto: ceros de relleno y dígitos en oscuro
                        faltan = tam - len(parte_digitos)
                        parte = "0" * faltan + parte_digitos
                else:
                    parte = ""
                parte_oscura += parte
                # Solo avanza al siguiente bloque si el bloque actual está completo
                if len(parte_digitos) == tam:
                    idx += tam
                else:
                    break  # No avanzar más, el usuario aún no ha completado este bloque
                # Añade el separador si el bloque está completo
                if i < len(separadores):
                    parte_oscura += separadores[i]
            return parte_oscura

        # --- TV MOMENTO ---
        if self.tipo_validacion == "momento":
            if " " not in self.texto_ingresado:
                self.tipo_validacion = "fecha"
                parte_oscura = self._determinar_parte_oscura()
                self.tipo_validacion = "momento"
                return parte_oscura
            else:
                partes = self.texto_ingresado.split(" ")
                parte_fecha = partes[0]
                parte_hora = partes[1] if len(partes) > 1 else ""
                self.tipo_validacion = "fecha"
                self.texto_ingresado = parte_fecha
                oscura_fecha = self._determinar_parte_oscura()
                self.tipo_validacion = "hora"
                self.texto_ingresado = parte_hora
                oscura_hora = self._determinar_parte_oscura()
                self.tipo_validacion = "momento"
                self.texto_ingresado = texto
                return oscura_fecha + (" " if oscura_hora else "") + oscura_hora

        # --- TV FLOAT ---
        if self.tipo_validacion == "float":
            separador_decimal = "." if "." in self.mascara else ("," if "," in self.mascara else ".")
            partes_mascara = self.mascara.split(separador_decimal)
            longitud_entera = partes_mascara[0].count(self.caracter_comodin)
            longitud_decimal = partes_mascara[1].count(self.caracter_comodin) if len(partes_mascara) > 1 else 0
            
            # Normalizar el texto ingresado para usar el separador de la máscara
            texto_normalizado = texto.replace(".", separador_decimal).replace(",", separador_decimal)
                        
            # Determinar si estamos en modo decimal
            modo_decimal = separador_decimal in texto_normalizado
            
            # Si hay separador en el texto ingresado, incluirlo en la parte oscura
            if modo_decimal:
                parte_entera_txt, parte_decimal_txt = texto_normalizado.split(separador_decimal, 1)
                
                digitos_entera = ''.join(c for c in parte_entera_txt if c.isdigit())[:longitud_entera]
                digitos_decimal = ''.join(c for c in parte_decimal_txt if c.isdigit())
                
                # Formatear parte entera y separador (siempre incluir el separador si está presente)
                parte_entera = digitos_entera.rjust(longitud_entera, "0")
                parte_oscura = parte_entera + separador_decimal
                
                # Formatear parte decimal si existe
                if digitos_decimal:
                    # Mantener todos los decimales que quepan en la máscara
                    if len(digitos_decimal) <= longitud_decimal:
                        parte_decimal = digitos_decimal.ljust(longitud_decimal, "0")
                    else:
                        # Si hay más decimales que los permitidos, mantener todos menos el último que se reemplaza
                        parte_decimal = digitos_decimal[:longitud_decimal-1] + digitos_decimal[-1]
                    parte_oscura += parte_decimal
            else:
                # Si no hay separador, solo formatear la parte entera
                digitos = ''.join(c for c in texto_normalizado if c.isdigit())
                digitos_entera = digitos[:longitud_entera]
                parte_entera = digitos_entera.rjust(longitud_entera, "0")
                parte_oscura = parte_entera
            
            return parte_oscura

        # --- TV INT ---
        if self.tipo_validacion == "int":
            longitud = self.mascara.count(self.caracter_comodin)
            digitos = ''.join(c for c in texto if c.isdigit())
            if len(digitos) > longitud:
                digitos = digitos[:longitud-1] + digitos[-1]
            parte_oscura = digitos.rjust(longitud, '0')
            return parte_oscura

        # --- TV STR con máscara de comodín (CP, teléfono, etc) ---
        if self.tipo_validacion == "str" and self.caracter_comodin in self.mascara:
            longitud = self.mascara.count(self.caracter_comodin)
            caracteres = ''.join(c for c in texto if c.isalnum())
            if len(caracteres) > longitud:
                caracteres = caracteres[:longitud-1] + caracteres[-1]
            parte_oscura = ""
            indice_caracter = 0
            for char in self.mascara:
                if char == self.caracter_comodin:
                    if indice_caracter < len(caracteres):
                        parte_oscura += caracteres[indice_caracter]
                        indice_caracter += 1
                    else:
                        break
                else:
                    parte_oscura += char
            return parte_oscura

        # --- TV STR sin máscara ---
        if self.tipo_validacion == "str":
            return texto

        # --- TV EMAIL ---
        if self.tipo_validacion == "email":
            return texto

        # --- Por defecto ---
        return texto

    def actualizar_colores(self):
        """
        Fondo blanco si habilitado, gris claro si deshabilitado.
        Letras oscuras para parte editada, claras para la máscara.
        """
        COLOR_FONDO_HABILITADO = "#ffffff"
        COLOR_FONDO_DESHABILITADO = "#f0f0f0"

        # Limpiar etiquetas previas
        self.textbox.tag_remove("texto", "1.0", tk.END)
        self.textbox.tag_remove("mascara", "1.0", tk.END)

        parte_oscura = self._determinar_parte_oscura()

        # Fondo según estado habilitado/deshabilitado
        if self.textbox['state'] != 'normal':
            self.textbox.config(bg=COLOR_FONDO_DESHABILITADO)
            self.textbox.tag_add("mascara", "1.0", tk.END)
            self.textbox.tag_config("mascara", foreground=self.mascara_color)
            return  # <-- IMPORTANTE: salir aquí para no sobrescribir el fondo   
        else:
            self.textbox.config(bg=COLOR_FONDO_HABILITADO)

        # Aplica colores a texto y máscara (como ya tienes)
        if parte_oscura:
            self.textbox.tag_add("texto", "1.0", f"1.{len(parte_oscura)}")
            self.textbox.tag_add("mascara", f"1.{len(parte_oscura)}", tk.END)
            self.textbox.tag_config("texto", foreground=self.texto_color)
            self.textbox.tag_config("mascara", foreground=self.mascara_color)
            # Posicionar el cursor correctamente
            if self.tipo_validacion == "str" and "#" in self.mascara:
                texto_formateado = self.formatear_texto()
                posicion_cursor = self.calcular_posicion_cursor(texto_formateado, self.texto_ingresado)
                self.textbox.mark_set("insert", f"1.{posicion_cursor}")
            else:
                self.textbox.mark_set("insert", f"1.{len(parte_oscura)}")
        else:
            self.textbox.tag_add("mascara", "1.0", tk.END)
            self.textbox.tag_config("mascara", foreground=self.mascara_color)
            self.textbox.mark_set("insert", "1.0")

    def manejar_retroceso(self, event=None):
        """
        Maneja el evento de retroceso (backspace) en el Textbox.
        Elimina el último carácter del texto ingresado y actualiza el control,
        teniendo en cuenta los caracteres fijos de la máscara y el tipo de validación.
        """
        if self.texto_ingresado:
            # --- TV FECHA ---
            if self.tipo_validacion == "fecha":
                # Obtener solo los dígitos ingresados
                digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
                
                if digitos:
                    # Eliminar el último dígito
                    digitos = digitos[:-1]
                    # Actualizar el texto ingresado con solo los dígitos
                    self.texto_ingresado = digitos
                else:
                    # Si no quedan dígitos, limpiar el texto ingresado
                    self.texto_ingresado = ""
            
            # --- TV HORA ---
            elif self.tipo_validacion == "hora":
                # Obtener solo los dígitos ingresados
                digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
                
                if digitos:
                    # Eliminar el último dígito
                    digitos = digitos[:-1]
                    # Actualizar el texto ingresado con solo los dígitos
                    self.texto_ingresado = digitos
                else:
                    # Si no quedan dígitos, limpiar el texto ingresado
                    self.texto_ingresado = ""

            # --- TV EMAIL ---
            elif self.tipo_validacion == "email":
                if self.texto_ingresado:
                    # Simplemente eliminar el último carácter
                    self.texto_ingresado = self.texto_ingresado[:-1]
                    # El formateo se encargará de limpiar espacios y convertir a minúsculas
            
            # --- TV MOMENTO ---
            elif self.tipo_validacion == "momento":
                # Obtener solo los dígitos ingresados
                digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
                
                if digitos:
                    # Eliminar el último dígito
                    digitos = digitos[:-1]
                    
                    # Si hay un espacio en el texto ingresado, mantenerlo
                    if " " in self.texto_ingresado and len(digitos) >= 8:
                        # Dividir los dígitos entre fecha y hora
                        fecha_digitos = digitos[:8]
                        hora_digitos = digitos[8:]
                        
                        # Reconstruir el texto con el espacio
                        self.texto_ingresado = fecha_digitos + " " + hora_digitos
                    else:
                        # Si no hay espacio o no hay suficientes dígitos para la fecha
                        self.texto_ingresado = digitos
                else:
                    # Si no quedan dígitos, limpiar el texto ingresado
                    self.texto_ingresado = ""
            
            # --- TV INT ---
            elif self.tipo_validacion == "int":
                # Obtener solo los dígitos ingresados
                digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
                
                if digitos:
                    # Eliminar el último dígito
                    digitos = digitos[:-1]
                    # Actualizar el texto ingresado con solo los dígitos
                    self.texto_ingresado = digitos
                else:
                    # Si no quedan dígitos, limpiar el texto ingresado
                    self.texto_ingresado = ""
            
            # --- TV FLOAT ---
            elif self.tipo_validacion == "float":
                # Manejar el caso especial de float con separador decimal
                texto_normalizado = self.texto_ingresado.replace(",", ".")
                
                if texto_normalizado:
                    # Si hay un punto decimal, manejar de forma especial
                    if "." in texto_normalizado:
                        parte_entera, parte_decimal = texto_normalizado.split(".", 1)
                        
                        if parte_decimal:
                            # Si hay parte decimal, eliminar el último dígito de la parte decimal
                            parte_decimal = parte_decimal[:-1]
                            if parte_decimal:
                                # Si aún queda parte decimal, reconstruir con el punto
                                self.texto_ingresado = parte_entera + "." + parte_decimal
                            else:
                                # Si no queda parte decimal, eliminar el punto también
                                self.texto_ingresado = parte_entera
                        else:
                            # Si solo está el punto, eliminarlo
                            self.texto_ingresado = parte_entera
                    else:
                        # Si no hay punto decimal, eliminar el último dígito de la parte entera
                        self.texto_ingresado = texto_normalizado[:-1]
                else:
                    # Si no queda texto, limpiar el texto ingresado
                    self.texto_ingresado = ""
            
            # --- TV STR con máscara de comodín (como teléfono) ---
            elif self.tipo_validacion == "str" and "#" in self.mascara:
                # Obtener solo los dígitos ingresados
                digitos = ''.join(c for c in self.texto_ingresado if c.isdigit())
                
                if digitos:
                    # Eliminar el último dígito
                    digitos = digitos[:-1]
                    
                    # Reconstruir el texto ingresado con los caracteres fijos
                    nuevo_texto = ""
                    indice_mascara = 0
                    indice_digito = 0
                    
                    while indice_mascara < len(self.mascara) and indice_digito < len(digitos):
                        char_mascara = self.mascara[indice_mascara]
                        
                        if char_mascara == '#':
                            # Si es un comodín y hay dígitos, agregar el dígito
                            nuevo_texto += digitos[indice_digito]
                            indice_digito += 1
                        elif char_mascara in self.caracteres_fijos:
                            # Si es un carácter fijo, agregarlo
                            nuevo_texto += char_mascara
                        
                        indice_mascara += 1
                    
                    # Actualizar el texto ingresado
                    self.texto_ingresado = nuevo_texto
                else:
                    # Si no quedan dígitos, limpiar el texto ingresado
                    self.texto_ingresado = ""
            else:
                # Para otros tipos de validación, simplemente eliminar el último carácter
                self.texto_ingresado = self.texto_ingresado[:-1]
            
            # Refrescar el Textbox
            self.refrescar_textbox()
            
        return "break"  # Evitar el comportamiento predeterminado de la tecla de retroceso

    def refrescar_textbox(self):
        """
        Actualiza el contenido del Textbox con el texto formateado.
        Mantiene la posición del cursor en la posición correcta.
        """
        texto_ingresado = self.texto_ingresado
        texto_formateado = self.formatear_texto(texto_ingresado)  # Solo texto
        posicion_cursor = self.calcular_posicion_cursor(texto_formateado, texto_ingresado)  # Solo posición

        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0", texto_formateado)
        self.actualizar_colores()
        self.textbox.mark_set("insert", f"1.{posicion_cursor}")
        self.textbox.see("insert")

    def validar_dato(self):

        # --- TV FECHA ---
        if self.tipo_validacion == "fecha":
            texto_formateado = self.formatear_texto()
            bloques = []
            separadores = []
            bloque_actual = ""
            for char in self.mascara:
                if char not in self.caracteres_fijos:
                    bloque_actual += char
                else:
                    if bloque_actual:
                        bloques.append(bloque_actual)
                        bloque_actual = ""
                    separadores.append(char)
            if bloque_actual:
                bloques.append(bloque_actual)
            patron = '|'.join(map(re.escape, separadores))
            valores = re.split(patron, texto_formateado)
            valores = [v for v in valores if v]

            # Identificar bloques por longitud y contenido
            idx_anio = idx_mes = idx_dia = None
            for idx, bloque in enumerate(bloques):
                if len(bloque) == 4:
                    idx_anio = idx
                elif len(bloque) == 2:
                    if 'M' in bloque.upper():
                        idx_mes = idx
                    elif 'D' in bloque.upper():
                        idx_dia = idx

            # Si no se identifican por letra, usar heurística por posición
            if None in (idx_anio, idx_mes, idx_dia):
                # Si el año no se identificó pero hay un bloque de 4 dígitos
                for idx, bloque in enumerate(bloques):
                    if len(bloque) == 4:
                        idx_anio = idx
                        break

                # Los otros dos bloques son día y mes
                otros_indices = [i for i in range(len(bloques)) if i != idx_anio]
                if len(otros_indices) == 2:
                    # Por defecto, asumimos formato DD/MM/AAAA
                    idx_dia, idx_mes = otros_indices
                    # A menos que la máscara indique lo contrario
                    if bloques[otros_indices[0]].upper().startswith('M'):
                        idx_mes, idx_dia = otros_indices

            if None in (idx_anio, idx_mes, idx_dia):
                print("[DEBUG validar_dato FECHA] Error: No se pudieron identificar los bloques de fecha")
                return False

            try:
                anio = valores[idx_anio]
                mes = valores[idx_mes]
                dia = valores[idx_dia]
            except IndexError:
                print("[DEBUG validar_dato FECHA] Error: Valores incompletos")
                return False

            # Validaciones intermedias para mejor feedback
            if not (dia.isdigit() and len(dia) == 2):
                print(f"[DEBUG validar_dato FECHA] Error: Día inválido '{dia}'")
                return False
            if not (mes.isdigit() and len(mes) == 2):
                print(f"[DEBUG validar_dato FECHA] Error: Mes inválido '{mes}'")
                return False
            if not (anio.isdigit() and len(anio) == 4):
                print(f"[DEBUG validar_dato FECHA] Error: Año inválido '{anio}'")
                return False

            # Validaciones de rango básicas antes de crear el objeto datetime
            dia_int = int(dia)
            mes_int = int(mes)
            anio_int = int(anio)

            if not (1 <= mes_int <= 12):
                print(f"[DEBUG validar_dato FECHA] Error: Mes fuera de rango (1-12): {mes_int}")
                return False

            # Días por mes (considerando años bisiestos)
            dias_por_mes = [0, 31, 29 if anio_int % 4 == 0 and (anio_int % 100 != 0 or anio_int % 400 == 0) else 28,
                          31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            if not (1 <= dia_int <= dias_por_mes[mes_int]):
                print(f"[DEBUG validar_dato FECHA] Error: Día fuera de rango (1-{dias_por_mes[mes_int]}): {dia_int}")
                return False

            try:
                fecha_obj = datetime(anio_int, mes_int, dia_int)
                print(f"[DEBUG validar_dato FECHA] Fecha válida: {fecha_obj.strftime('%Y-%m-%d')}")
            except ValueError as e:
                print(f"[DEBUG validar_dato FECHA] Error al crear objeto datetime: {str(e)}")
                return False

            # Validar restricciones de rango si existen
            fecha_iso = fecha_obj.strftime("%Y-%m-%d")
            min_fecha = self.restricciones.get("min")
            max_fecha = self.restricciones.get("max")
            
            if min_fecha and fecha_iso < min_fecha:
                print(f"[DEBUG validar_dato FECHA] Error: Fecha menor que el mínimo permitido ({min_fecha})")
                return False
            if max_fecha and fecha_iso > max_fecha:
                print(f"[DEBUG validar_dato FECHA] Error: Fecha mayor que el máximo permitido ({max_fecha})")
                return False

            return texto_formateado

        # --- TV HORA ---
        if self.tipo_validacion == "hora":
            texto_formateado = self.formatear_texto()
            bloques = []
            separadores = []
            bloque_actual = ""
            for char in self.mascara:
                if char not in self.caracteres_fijos:
                    bloque_actual += char
                else:
                    if bloque_actual:
                        bloques.append(bloque_actual)
                        bloque_actual = ""
                    separadores.append(char)
            if bloque_actual:
                bloques.append(bloque_actual)
            patron = '|'.join(map(re.escape, separadores))
            valores = re.split(patron, texto_formateado)
            valores = [v for v in valores if v]
            if len(valores) != 2:
                return False
            hora, minuto = valores
            if not (hora.isdigit() and minuto.isdigit()):
                return False
            if 0 <= int(hora) <= 23 and 0 <= int(minuto) <= 59:
                return texto_formateado
            return False

        # --- TV MOMENTO ---
        if self.tipo_validacion == "momento":
            texto_formateado = self.formatear_texto()
            partes = texto_formateado.split(" ", 1)
            if len(partes) != 2:
                return False
            fecha_parte, hora_parte = partes
            tipo_original = self.tipo_validacion
            texto_original = self.texto_ingresado
            mascara_original = self.mascara
            caracteres_fijos_original = self.caracteres_fijos

            # Validar fecha
            self.tipo_validacion = "fecha"
            self.mascara = mascara_original.split(" ", 1)[0] if " " in mascara_original else "DD/MM/AAAA"
            self.caracteres_fijos = self.separador_fecha
            self.texto_ingresado = fecha_parte
            resultado_fecha = self.validar_dato()

            # Validar hora
            self.tipo_validacion = "hora"
            self.mascara = mascara_original.split(" ", 1)[1] if " " in mascara_original else "HH:MM"
            self.caracteres_fijos = self.separador_hora
            self.texto_ingresado = hora_parte
            resultado_hora = self.validar_dato()

            # Restaurar estado original
            self.tipo_validacion = tipo_original
            self.texto_ingresado = texto_original
            self.mascara = mascara_original
            self.caracteres_fijos = caracteres_fijos_original

            if resultado_fecha and resultado_hora:
                return texto_formateado
            return False

        # --- TV FLOAT ---
        if self.tipo_validacion == "float":
            texto_formateado = self.formatear_texto()
            texto_formateado = texto_formateado.replace(",", ".")
            try:
                valor = float(texto_formateado)
            except ValueError:
                return False
            min_valor = self.restricciones.get("min", float("-inf"))
            max_valor = self.restricciones.get("max", float("inf"))
            if min_valor <= valor <= max_valor:
                return valor
            return False

        # --- TV INT ---
        if self.tipo_validacion == "int":
            texto_formateado = self.formatear_texto()
            try:
                valor = int(texto_formateado)
            except ValueError:
                return False
            min_valor = self.restricciones.get("min", float("-inf"))
            max_valor = self.restricciones.get("max", float("inf"))
            if min_valor <= valor <= max_valor:
                return valor
            return False

        # --- TV STR con máscara de comodín (CP, teléfono, etc) ---
        if self.tipo_validacion == "str" and self.caracter_comodin in self.mascara:
            # Obtener el texto formateado completo
            texto_formateado = self.formatear_texto(self.texto_ingresado)
            
            # Extraer caracteres editables usando la máscara como guía
            caracteres_editables = ""
            for i, char in enumerate(texto_formateado):
                # Solo considerar posiciones existentes en la máscara
                if i < len(self.mascara):
                    # Solo agregar caracteres de posiciones editables
                    if self.mascara[i] not in self.caracteres_fijos:
                        caracteres_editables += char
            
            # Contar comodines en la máscara
            num_comodines = sum(1 for char in self.mascara if char not in self.caracteres_fijos)
            
            if len(caracteres_editables) == num_comodines:
                return texto_formateado
            return False

        if self.tipo_validacion == "str" and "#" in self.mascara and all(char == "#" for char in self.mascara):
            texto_formateado = self.formatear_texto()
            longitud = self.mascara.count("#")
            if texto_formateado.isalnum() and len(texto_formateado) == longitud:
                return texto_formateado
            return False

        # --- TV STR sin máscara ---
        if self.tipo_validacion == "str":
            max_length = self.restricciones.get('length', float('inf'))
            if len(self.texto_ingresado) <= max_length:
                return self.texto_ingresado
            return False

        # --- TV EMAIL ---
        if self.tipo_validacion == "email":
            # Expresión regular para validar email
            patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(patron_email, self.texto_ingresado):
                return self.texto_ingresado
            return False

        # --- Por defecto ---
        return self.texto_ingresado

    def manejar_suprimir(self, event):
        if self.texto_ingresado:
            self.texto_ingresado = self.texto_ingresado[1:]
            self.refrescar_textbox()
        return "break"

    def generar_texto_enmascarado(self):
        """
        Genera el texto final combinando la máscara con los datos ingresados por el usuario.
        Rellena los espacios vacíos con el carácter comodín y respeta los caracteres fijos.
        """
        nuevo_texto = ''
        indice_ingresado = 0
        for char in self.mascara:
            if char in self.caracteres_fijos:
                nuevo_texto += char
            elif indice_ingresado < len(self.texto_ingresado):
                nuevo_texto += self.texto_ingresado[indice_ingresado]
                indice_ingresado += 1
            else:
                nuevo_texto += char
        return nuevo_texto

    def calcular_primera_posicion_editable(self):
        """
        Calcula la primera posición editable en función de la máscara.
        Salta automáticamente los caracteres fijos iniciales.
        """
        for i, char in enumerate(self.mascara):
            if char not in self.caracteres_fijos:
                return i
        return len(self.mascara)  # Si solo hay caracteres fijos, coloca el cursor al final

    def calcular_posicion_cursor(self, texto_formateado, texto_ingresado):
        """
        Calcula la posición del cursor en el texto formateado,
        considerando el tipo de validación y la máscara.
        Compatible con cualquier carácter comodín.
        """
        # --- TV FECHA y TV HORA ---
        if self.tipo_validacion in ("fecha", "hora"):
            digitos = ''.join(c for c in texto_ingresado if c.isdigit())
            indice_digito = 0
            for i, char in enumerate(texto_formateado):
                if char in self.caracteres_fijos:
                    continue
                if indice_digito < len(digitos):
                    indice_digito += 1
                else:
                    return i
            return len(texto_formateado)

        # --- TV MOMENTO ---
        if self.tipo_validacion == "momento":
            if " " in texto_formateado:
                mascara_fecha, mascara_hora = self.mascara.split(" ", 1)
                partes_formateado = texto_formateado.split(" ", 1)
                partes_ingresado = texto_ingresado.split(" ", 1)
                fecha_formateada = partes_formateado[0]
                hora_formateada = partes_formateado[1] if len(partes_formateado) > 1 else ""
                fecha_ingresada = partes_ingresado[0]
                hora_ingresada = partes_ingresado[1] if len(partes_ingresado) > 1 else ""
                self.tipo_validacion = "fecha"
                self.mascara = mascara_fecha
                pos_fecha = self.calcular_posicion_cursor(fecha_formateada, fecha_ingresada)
                if texto_ingresado.strip().endswith(" ") or hora_ingresada:
                    self.tipo_validacion = "hora"
                    self.mascara = mascara_hora
                    pos_hora = self.calcular_posicion_cursor(hora_formateada, hora_ingresada)
                    self.tipo_validacion = "momento"
                    self.mascara = mascara_fecha + " " + mascara_hora
                    return len(fecha_formateada) + 1 + pos_hora
                else:
                    self.tipo_validacion = "momento"
                    self.mascara = mascara_fecha + " " + mascara_hora
                    return pos_fecha
            else:
                self.tipo_validacion = "fecha"
                pos_fecha = self.calcular_posicion_cursor(texto_formateado, texto_ingresado)
                self.tipo_validacion = "momento"
                return pos_fecha

        # --- TV STR con máscara de comodín (incluye teléfono, CP, etc) ---
        if self.tipo_validacion == "str" and self.caracter_comodin in self.mascara:
            caracteres = ''.join(c for c in texto_ingresado if c.isalnum())
            count = 0
            for i, char in enumerate(self.mascara):
                if char == self.caracter_comodin:
                    if count < len(caracteres):
                        count += 1
                    else:
                        return i
            return len(self.mascara)

        # --- TV FLOAT ---
        if self.tipo_validacion == "float":
            separador_decimal = "." if "." in self.mascara else ("," if "," in self.mascara else ".")
            partes_mascara = self.mascara.split(separador_decimal)
            longitud_entera = partes_mascara[0].count(self.caracter_comodin)
            
            # Normalizar el texto ingresado para usar el separador de la máscara
            texto_ingresado_norm = texto_ingresado.replace(".", separador_decimal).replace(",", separador_decimal)
            
            # Obtener posición del separador decimal en el texto formateado
            pos_separador = texto_formateado.find(separador_decimal)
            
            # Si hay separador en el texto ingresado, estamos en modo decimal
            if separador_decimal in texto_ingresado_norm:
                parte_decimal = texto_ingresado_norm.split(separador_decimal, 1)[1]
                digitos_decimal = ''.join(c for c in parte_decimal if c.isdigit())
                
                if digitos_decimal:  # Si hay dígitos decimales
                    # Posicionar después del último dígito decimal ingresado
                    pos_cursor = pos_separador + 1 + len(digitos_decimal)
                    return pos_cursor
                # Si no hay dígitos decimales o acabamos de ingresar el separador
                return pos_separador + 1
            else:  # Si no hay separador, estamos en modo entero
                # Posicionar justo antes del separador decimal
                return pos_separador

        # --- TV INT ---
        if self.tipo_validacion == "int":
            pos = len(texto_formateado)
            return pos

        # --- TV STR sin máscara ---
        if self.tipo_validacion == "str":
            pos = len(texto_ingresado)
            return pos

        # --- Por defecto ---
        pos = len(texto_formateado)
        return pos
  
    def _aplicar_separador_miles(self, texto, separador):
        """
        Aplica el separador de miles al texto formateado.
        """
        partes = texto.split(separador)
        parte_entera = partes[0]
        parte_decimal = partes[1] if len(partes) > 1 else ""
        
        # Aplicar separador de miles a la parte entera
        parte_entera_con_separadores = ""
        for i, char in enumerate(reversed(parte_entera)):
            if i > 0 and i % 3 == 0:
                parte_entera_con_separadores = separador + parte_entera_con_separadores
            parte_entera_con_separadores = char + parte_entera_con_separadores
        
        # Reconstruir el texto con los separadores de miles
        if parte_decimal:
            return f"{parte_entera_con_separadores}{separador}{parte_decimal}"
        else:
            return parte_entera_con_separadores

    def validar_y_formatear(self):
        """
        Valida el dato ingresado y lo formatea según la máscara.
        Retorna True si el dato es válido, False en caso contrario.
        """
        valor_validado = self.validar_dato()
        if valor_validado is False:
            return False
        self.texto_ingresado = str(valor_validado)
        
        # Usar formatear_texto en lugar de formatear_con_mascara
        texto_formateado = self.formatear_texto()
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0", texto_formateado)
        self.actualizar_colores()
        
        return True

    def obtener_valor(self):
        """
        Retorna el valor actual del control.
        """
        return self.texto_ingresado

    def establecer_valor(self, valor):
        """
        Establece el valor del control y actualiza la visualización.
        """
        valor_str = str(valor)
        # Convertir a minúsculas si es tipo email
        if self.tipo_validacion == "email":
            valor_str = valor_str.lower()
        self.texto_ingresado = valor_str
        # Usar refrescar_textbox en lugar de formatear_con_mascara
        self.refrescar_textbox()
 
    def __str__(self):
        """
        Devuelve una representación en cadena del control Textbox.
        Se utiliza cuando se imprime el objeto o se convierte a cadena.
        """
        titulo = self.label.cget("text") if hasattr(self, "label") else ""
        valor = self.texto_ingresado if hasattr(self, "texto_ingresado") else ""
        return f"control '{titulo}' de tipo {self.tipo_validacion}: {valor}'"

    def __repr__(self):
        """
        Devuelve una representación oficial del objeto Textbox.
        Se utiliza en la representación de depuración y en el intérprete interactivo.
        """
        titulo = self.label.cget("text") if hasattr(self, "label") else ""
        valor = self.texto_ingresado if hasattr(self, "texto_ingresado") else ""
        return f"Textbox(titulo='{titulo}', tipo_validacion='{self.tipo_validacion}', valor='{valor}')"

    def _debug_evento_buscador(self, event):
        texto = self.textbox.get("1.0", "end-1c").strip()
        print(f"[DEBUG][Textbox] KeyRelease: '{event.keysym}' | Texto actual: '{texto}'")
        if hasattr(self, "buscador"):
            resultados = self.buscador.busca_cadena(texto)
            print(f"[DEBUG][Textbox] Resultados busca_cadena('{texto}'): {resultados}")
        else:
            print("[DEBUG][Textbox] No hay buscador asociado a este textbox.")

class OptionGroup(tk.Frame):
    """
    Control OptionGroup unificado que combina las mejores características de OptionGroup.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        
        # Determinar si se pasó una configuración o argumentos sueltos
        if len(args) == 1 and isinstance(args[0], ConfiguracionOptionGroup
):
            config = args[0]
        else:
            config = ConfiguracionOptionGroup.from_args(*args, **kwargs)
        
        # Configurar propiedades
        self.titulo_control = config.titulo_control
        self.opciones = self._procesar_opciones(config.opciones)
        self.orientacion = config.orientacion
        self.habilitado = config.habilitado
        self.comando = config.comando
        self.ancho = config.ancho
        self.usar_ttk = config.usar_ttk
        self.espaciado = config.espaciado
        self.padding = config.padding
        
        # Variable para almacenar el valor seleccionado
        self.valor = tk.StringVar()
        if config.valor_inicial is not None:
            self.valor.set(str(config.valor_inicial))
        
        # Diccionario para almacenar los optiongroups y sus estados
        self.option_group = {}
        self.estados_individuales = {}
        
        # Crear la interfaz
        self._crear_interfaz()
        
        # Configurar estado inicial
        self._configurar_estado_inicial()
    
    def _procesar_opciones(self, opciones):
        """
        Procesa las opciones para manejar diferentes formatos.
        
        Args:
            opciones: Lista de tuplas (valor, etiqueta) o (valor, etiqueta, habilitado)
        
        Returns:
            list: Lista normalizada de opciones
        """
        opciones_procesadas = []
        
        for opcion in opciones:
            if len(opcion) == 2:
                # Formato (valor, etiqueta)
                valor, etiqueta = opcion
                habilitado = True
            elif len(opcion) == 3:
                # Formato (valor, etiqueta, habilitado)
                valor, etiqueta, habilitado = opcion
            else:
                # Formato inválido, usar valores por defecto
                valor = str(opcion)
                etiqueta = str(opcion)
                habilitado = True
            
            opciones_procesadas.append((valor, etiqueta, habilitado))
        
        return opciones_procesadas
    
    def _crear_interfaz(self):
        """
        Crea la interfaz del control.
        """
        # Crear etiqueta de título si se proporciona
        if self.titulo_control:
            self.label_titulo = ttk.Label(
                self,
                text=self.titulo_control,
                font=("Arial", 9, "normal")
            )
            self.label_titulo.pack(anchor=tk.W, pady=(0, self.padding))
        
        # Crear frame para los radio buttons
        self.frame_opciones = tk.Frame(self)
        self.frame_opciones.pack(fill=tk.X, expand=True)
        
        # Crear los radio buttons
        self._crear_option_group()
    
    def _crear_option_group(self):
        """
        Crea los radio buttons según la configuración.
        """
        # Seleccionar el tipo de optiongroup
        OptionGroupClass = ttk.Radiobutton if self.usar_ttk else tk.Radiobutton
        
        for i, (valor, etiqueta, habilitado_individual) in enumerate(self.opciones):
            # Crear el OptionGroup
            rb = OptionGroupClass(
                self.frame_opciones,
                text=etiqueta,
                variable=self.valor,
                value=str(valor),
                command=self._on_change,
                width=self.ancho
            )
            
            # Almacenar referencia y estado
            self.option_group[str(valor)] = rb
            self.estados_individuales[str(valor)] = habilitado_individual
            
            # Posicionar según orientación
            if self.orientacion == "horizontal":
                rb.grid(
                    row=0, 
                    column=i, 
                    padx=self.espaciado, 
                    pady=self.padding,
                    sticky=tk.W
                )
            else:  # vertical
                rb.grid(
                    row=i, 
                    column=0, 
                    padx=self.padding, 
                    pady=self.espaciado,
                    sticky=tk.W
                )
            
            # Configurar estado individual
            if not habilitado_individual:
                rb.configure(state="disabled")
    
    def _configurar_estado_inicial(self):
        """
        Configura el estado inicial del control.
        """
        # Configurar estado general
        if not self.habilitado:
            self.habilitar(False)
        
        # Si hay un valor inicial y no está seleccionado, seleccionarlo
        if self.valor.get() and self.valor.get() in self.option_group:
            # El valor ya está configurado por la variable
            pass
        elif self.opciones:
            # Si no hay valor inicial, seleccionar la primera opción habilitada
            for valor, etiqueta, habilitado_individual in self.opciones:
                if habilitado_individual:
                    self.valor.set(str(valor))
                    break
    
    def _on_change(self):
        """
        Manejador de evento cuando cambia la selección.
        """
        if self.comando and callable(self.comando):
            try:
                self.comando(self.get())
            except Exception as e:
                print(f"Error en callback de OptionGroup: {e}")
    
    # === MÉTODOS PÚBLICOS ===
    
    def get(self):
        """
        Obtiene el valor actual seleccionado.
        
        Returns:
            str: Valor seleccionado
        """
        return self.valor.get()
    
    def set(self, valor):
        """
        Establece el valor seleccionado.
        
        Args:
            valor: Valor a seleccionar
        """
        valor_str = str(valor)
        if valor_str in self.option_group:
            self.valor.set(valor_str)
        else:
            print(f"Advertencia: Valor '{valor}' no encontrado en las opciones")
    
    def get_texto_seleccionado(self):
        """
        Obtiene el texto de la opción seleccionada.
        
        Returns:
            str: Texto de la opción seleccionada
        """
        valor_actual = self.get()
        for valor, etiqueta, _ in self.opciones:
            if str(valor) == valor_actual:
                return etiqueta
        return ""
    
    def habilitar(self, estado=True):
        """
        Habilita o deshabilita todo el control.
        
        Args:
            estado (bool): True para habilitar, False para deshabilitar
        """
        self.habilitado = estado
        estado_tk = "normal" if estado else "disabled"
        
        for valor, rb in self.option_group.items():
            # Solo habilitar si el estado individual también lo permite
            if estado and self.estados_individuales.get(valor, True):
                rb.configure(state="normal")
            else:
                rb.configure(state="disabled")
    
    def habilitar_opcion(self, valor, estado=True):
        """
        Habilita o deshabilita una opción específica.
        
        Args:
            valor: Valor de la opción a habilitar/deshabilitar
            estado (bool): True para habilitar, False para deshabilitar
        """
        valor_str = str(valor)
        if valor_str in self.option_group:
            self.estados_individuales[valor_str] = estado
            
            # Aplicar el estado solo si el control general está habilitado
            if self.habilitado and estado:
                self.option_group[valor_str].configure(state="normal")
            else:
                self.option_group[valor_str].configure(state="disabled")
        else:
            print(f"Advertencia: Opción '{valor}' no encontrada")
    
    def agregar_opcion(self, valor, etiqueta, habilitado=True, posicion=None):
        """
        Agrega una nueva opción al control.
        
        Args:
            valor: Valor de la nueva opción
            etiqueta: Texto a mostrar
            habilitado (bool): Si la opción está habilitada
            posicion (int): Posición donde insertar (None para agregar al final)
        """
        nueva_opcion = (valor, etiqueta, habilitado)
        
        if posicion is None:
            self.opciones.append(nueva_opcion)
        else:
            self.opciones.insert(posicion, nueva_opcion)
        
        # Recrear la interfaz
        self._limpiar_option_group()
        self._crear_option_group()
    
    def remover_opcion(self, valor):
        """
        Remueve una opción del control.
        
        Args:
            valor: Valor de la opción a remover
        """
        valor_str = str(valor)
        
        # Remover de la lista de opciones
        self.opciones = [
            (v, e, h) for v, e, h in self.opciones 
            if str(v) != valor_str
        ]
        
        # Si la opción removida estaba seleccionada, seleccionar otra
        if self.get() == valor_str and self.opciones:
            self.set(self.opciones[0][0])
        
        # Recrear la interfaz
        self._limpiar_option_group()
        self._crear_option_group()
    
    def _limpiar_option_group(self):
        """
        Limpia los radio buttons existentes.
        """
        for rb in self.option_group.values():
            rb.destroy()
        self.option_group.clear()
        self.estados_individuales.clear()
    
    def get_opciones(self):
        """
        Obtiene todas las opciones del control.
        
        Returns:
            list: Lista de tuplas (valor, etiqueta, habilitado)
        """
        return self.opciones.copy()
    
    def set_comando(self, comando):
        """
        Establece o cambia el comando de callback.
        
        Args:
            comando: Función a ejecutar cuando cambie la selección
        """
        self.comando = comando
    
    def get_indice_seleccionado(self):
        """
        Obtiene el índice de la opción seleccionada.
        
        Returns:
            int: Índice de la opción seleccionada (-1 si no hay selección)
        """
        valor_actual = self.get()
        for i, (valor, _, _) in enumerate(self.opciones):
            if str(valor) == valor_actual:
                return i
        return -1
    
    def seleccionar_por_indice(self, indice):
        """
        Selecciona una opción por su índice.
        
        Args:
            indice (int): Índice de la opción a seleccionar
        """
        if 0 <= indice < len(self.opciones):
            valor = self.opciones[indice][0]
            self.set(valor)
        else:
            print(f"Advertencia: Índice {indice} fuera de rango")

class Combobox(tk.Frame):
    """
    Clase Combobox que representa un campo de selección desplegable con búsqueda.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        
        # Comprobar si se pasó una instancia de ConfiguracionCombobox
        if len(args) == 1 and isinstance(args[0], ConfiguracionCombobox):
            config = args[0]
        else:
            config = ConfiguracionCombobox.from_args(*args, **kwargs)
        
        # Asignar los valores de la configuración
        self.ancho = config.ancho
        self.valores = config.valores
        self.estado = config.estado
        
        # Widgets
        self.label = ttk.Label(self, text=config.titulo_control)
        self.label.grid(row=0, column=0)
        
        self.combobox = ttk.Combobox(self, width=self.ancho, state=self.estado)
        self.combobox.grid(row=0, column=1)
        
        # Establecer los valores
        self._actualizar_valores(self.valores)
        
        # Crear el buscador de cadenas si se proporcionan los parámetros
        if config.fuente_datos is not None:
            # Si la fuente de datos es un DataFrame, lista o diccionario, actualizamos los valores
            if isinstance(config.fuente_datos, pd.DataFrame):
                self._actualizar_valores_desde_fuente(config.fuente_datos)
            elif isinstance(config.fuente_datos, dict):
                self._actualizar_valores_desde_fuente(config.fuente_datos)
            elif isinstance(config.fuente_datos, list) and set(config.fuente_datos) != set(self.valores):
                self._actualizar_valores_desde_fuente(config.fuente_datos)
            
            # Modificar el estado para permitir la edición si se usa búsqueda
            if self.estado == "readonly":
                self.combobox.configure(state="normal")
            
            # Crear BuscadorCadena - se encarga automáticamente de todos los eventos
            self.buscador = BuscadorCadena(
                fuente_datos=config.fuente_datos,
                permite_agregar=config.permite_agregar,
                modo_busqueda=config.modo_busqueda,
                sensible_mayusculas=config.sensible_mayusculas,
                df_columna_id=getattr(config, "df_columna_id", None),
                df_columna_valor=getattr(config, "df_columna_valor", None)
            )
            
        if hasattr(self, 'buscador'):
            self.combobox.bind("<KeyRelease>", self._evento_keyrelease_usuario)
    
    def _actualizar_valores(self, valores):
        """Actualiza los valores del combobox."""
        if valores:
            self.combobox['values'] = valores
    
    def _actualizar_valores_desde_fuente(self, fuente_datos):
        """Actualiza los valores del combobox desde la fuente de datos."""
        if isinstance(fuente_datos, list):
            self.combobox['values'] = fuente_datos
        elif isinstance(fuente_datos, dict):
            self.combobox['values'] = list(fuente_datos.values())
        elif isinstance(fuente_datos, pd.DataFrame):
            # Si se especificaron columnas para ID y valor
            if hasattr(self, 'buscador') and self.buscador.df_columna_valor:
                valores = fuente_datos[self.buscador.df_columna_valor].tolist()
            else:
                # Usar la primera columna de texto
                columnas_texto = fuente_datos.select_dtypes(include=['object']).columns
                if len(columnas_texto) > 0:
                    valores = fuente_datos[columnas_texto[0]].tolist()
                else:
                    # Si no hay columnas de texto, usar la primera columna
                    valores = fuente_datos[fuente_datos.columns[0]].tolist()
            self.combobox['values'] = valores
            # Configurar el estado del combobox para permitir búsqueda
            if hasattr(self, 'buscador'):
                self.combobox.configure(state="normal")
        elif callable(fuente_datos):
            try:
                valores = fuente_datos(obtener_todos=True)
                if valores:
                    self.combobox['values'] = [valor for valor, _ in valores]
            except Exception as e:
                print(f"Error al obtener valores desde fuente personalizada: {e}")
    
    def get(self):
        """Obtiene el valor actual del combobox."""
        return self.combobox.get()
    
    def set(self, valor):
        """Establece el valor del combobox."""
        self.combobox.set(valor)
    
    def busca_cadena(self, texto, modo_busqueda=None, sensible_mayusculas=None, max_resultados=None):
        """Delega la búsqueda al BuscadorCadena si existe."""
        if hasattr(self, 'buscador'):
            return self.buscador.busca_cadena(texto, modo_busqueda, sensible_mayusculas, max_resultados)
        return []

    def get_widget(self):
        """Devuelve el widget interno (ttk.Combobox)."""
        return self.combobox

    def _evento_keyrelease_usuario(self, event):
        if hasattr(self, 'buscador'):
            self.buscador.autocompletar_en_widget(self.combobox, self.combobox.get(), tipo_widget="combobox")

class Listbox(tk.Frame):
    """
    Clase Listbox que representa una lista de selección con búsqueda.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        
        # Comprobar si se pasó una instancia de ConfiguracionListbox
        if len(args) == 1 and isinstance(args[0], ConfiguracionListbox):
            config = args[0]
        else:
            config = ConfiguracionListbox.from_args(*args, **kwargs)
        
        # Asignar los valores de la configuración
        self.ancho = config.ancho
        self.altura = config.altura
        self.seleccion_multiple = config.seleccion_multiple
        self.titulo_busqueda = config.titulo_busqueda
        
        # Widgets
        self.label = ttk.Label(self, text=config.titulo_control)
        self.label.grid(row=0, column=0, columnspan=2)
        
        # Frame para la búsqueda
        self.frame_busqueda = tk.Frame(self)
        self.frame_busqueda.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.label_busqueda = ttk.Label(self.frame_busqueda, text=self.titulo_busqueda)
        self.label_busqueda.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.entry_busqueda = ttk.Entry(self.frame_busqueda, width=self.ancho)
        self.entry_busqueda.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Listbox
        self.listbox = tk.Listbox(
            self, 
            width=self.ancho, 
            height=self.altura, 
            selectmode="multiple" if self.seleccion_multiple else "browse"
        )
        self.listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.scrollbar.grid(row=2, column=2, sticky="ns")
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        
        # Crear el buscador de cadenas si se proporcionan los parámetros
        if config.fuente_datos is not None:
            # Si la fuente de datos es un DataFrame o una lista, actualizamos los valores
            if isinstance(config.fuente_datos, (pd.DataFrame, list)):
                self._actualizar_valores_desde_fuente(config.fuente_datos)
            
            # Crear BuscadorCadena - se encarga automáticamente de todos los eventos
            self.buscador = BuscadorCadena(
                fuente_datos=config.fuente_datos,
                permite_agregar=config.permite_agregar,
                modo_busqueda=config.modo_busqueda,
                sensible_mayusculas=config.sensible_mayusculas,
                df_columna_id=getattr(config, "df_columna_id", None),
                df_columna_valor=getattr(config, "df_columna_valor", None)
            )
    
    def _actualizar_valores_desde_fuente(self, fuente_datos):
        """Actualiza los valores del listbox desde la fuente de datos."""
        self.listbox.delete(0, tk.END)
        
        if isinstance(fuente_datos, list):
            for item in fuente_datos:
                self.listbox.insert(tk.END, str(item))
        elif isinstance(fuente_datos, dict):
            for valor in fuente_datos.values():
                self.listbox.insert(tk.END, str(valor))
        elif callable(fuente_datos):
            try:
                valores = fuente_datos(obtener_todos=True)
                if valores:
                    for valor, _ in valores:
                        self.listbox.insert(tk.END, str(valor))
            except Exception as e:
                print(f"Error al obtener valores desde fuente personalizada: {e}")
  
    def busca_cadena(self, texto, modo_busqueda=None, sensible_mayusculas=None, max_resultados=None):
        """Delega la búsqueda al BuscadorCadena si existe."""
        if hasattr(self, 'buscador'):
            return self.buscador.busca_cadena(texto, modo_busqueda, sensible_mayusculas, max_resultados)
        return [] 

    def _evento_keyrelease_busqueda(self, event):
        if hasattr(self, 'buscador'):
            texto_usuario = self.entry_busqueda.get()
            self.buscador.autocompletar_en_widget(self.listbox, texto_usuario, tipo_widget="listbox")
    
    def get_selected(self):
        """Obtiene el valor seleccionado en el listbox."""
        seleccion = self.listbox.curselection()
        if seleccion:
            return self.listbox.get(seleccion[0])
        return None
    
    def get_selected_all(self):
        """Obtiene todos los valores seleccionados en el listbox."""
        seleccion = self.listbox.curselection()
        return [self.listbox.get(i) for i in seleccion]

    def get_widget(self):
        """Devuelve el widget interno (ttk.Entry)."""
        return self.entry_busqueda

class Page(ttk.Frame):  # Cambiado de tk.Frame a ttk.Frame
    """
    Control Page que actúa como contenedor para otros controles.
    """
    _notebook = None  # Variable de clase para mantener referencia al notebook

    def __init__(self, parent, *args, **kwargs):
        # Determinar si se pasó una configuración o argumentos sueltos
        if len(args) == 1 and isinstance(args[0], ConfiguracionPage):
            config = args[0]
        else:
            config = ConfiguracionPage.from_args(*args, **kwargs)
        
        # Crear el notebook si no existe
        if Page._notebook is None:
            # Configurar el estilo
            style = ttk.Style()
            
            # Configurar el estilo base del Notebook y Frame
            style.configure("Custom.TNotebook", 
                          background='white')
            style.configure("Page.TFrame",
                          background='white')  # Fondo blanco para el frame
            
            # Configurar el estilo de las pestañas
            style.configure("Custom.TNotebook.Tab",
                          background='#f0f0f0',   # Color de fondo gris por defecto
                          foreground='black',      # Color de texto
                          padding=(10, 5))         # Padding de las pestañas
            
            # Mapear los estados de las pestañas (invertimos los colores)
            style.map("Custom.TNotebook.Tab",
                background=[
                    ("selected", "#f0f0f0"),      # Gris cuando está seleccionada
                    ("!selected", "white")         # Blanco cuando no está seleccionada
                ],
                foreground=[
                    ("selected", "black"),         # Negro cuando está seleccionada
                    ("!selected", "black")         # Negro cuando no está seleccionada
                ]
            )
            
            # Crear el notebook
            Page._notebook = ttk.Notebook(parent, style="Custom.TNotebook")
            Page._notebook.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
            
            # Configurar el grid del contenedor padre
            parent.grid_rowconfigure(0, weight=1)
            parent.grid_columnconfigure(0, weight=1)
        
        # Inicializar el Frame con el estilo personalizado
        super().__init__(parent, style="Page.TFrame")
        
        # Crear el frame contenedor principal de la página
        self.frame_contenedor = ttk.Frame(self, style="Page.TFrame")
        self.frame_contenedor.grid(row=0, column=0, sticky='nsew')
        
        # Configurar el grid de la página y su contenedor
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame_contenedor.grid_rowconfigure(0, weight=1)
        self.frame_contenedor.grid_columnconfigure(0, weight=1)
        
        # Añadir la página al notebook
        Page._notebook.add(self, text=config.titulo)

    def agregar_frame_seccion(self, titulo):
        """
        Agrega un frame con título (LabelFrame) dentro de la página.
        """
        frame_seccion = ttk.LabelFrame(
            self.frame_contenedor,
            text=titulo,
            padding=(10, 5)
        )
        
        # Configurar el grid del frame
        frame_seccion.grid_columnconfigure(0, weight=1)
        
        return frame_seccion

class Checkbox(tk.Frame):
    """
    Control Checkbox que representa una opción que puede estar marcada o desmarcada.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        
        # Determinar si se pasó una configuración o argumentos sueltos
        if len(args) == 1 and isinstance(args[0], ConfiguracionCheckbox):
            config = args[0]
        else:
            config = ConfiguracionCheckbox.from_args(*args, **kwargs)
        
        # Configurar propiedades
        self.titulo = config.titulo
        self.valor = tk.BooleanVar(value=config.valor_inicial)
        self.habilitado = config.habilitado
        self.comando = config.comando
        self.ancho = config.ancho
        
        # Crear el checkbox
        self.checkbox = ttk.Checkbutton(
            self,
            text=self.titulo,
            variable=self.valor,
            command=self._on_change,
            width=self.ancho
        )
        self.checkbox.pack(fill=tk.X, expand=True)
        
        # Configurar estado inicial
        if not self.habilitado:
            self.checkbox.configure(state="disabled")
    
    def _on_change(self):
        """
        Manejador de evento cuando cambia el valor del checkbox.
        """
        if self.comando and callable(self.comando):
            self.comando(self.get())
    
    def get(self):
        """
        Obtiene el valor actual del checkbox.
        """
        return self.valor.get()
    
    def set(self, valor):
        """
        Establece el valor del checkbox.
        """
        self.valor.set(bool(valor))
    
    def toggle(self):
        """
        Invierte el valor actual del checkbox.
        """
        self.set(not self.get())
    
    def habilitar(self, estado=True):
        """
        Habilita o deshabilita el checkbox.
        """
        self.checkbox.configure(state="normal" if estado else "disabled")
        self.habilitado = estado

class SelectorFecha(tk.Frame):
    """
    Control para seleccionar una fecha usando un calendario desplegable.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Inicializa un control SelectorFecha.
        """
        super().__init__(parent)
        
        # Importar tkcalendar si está disponible
        try:
            from tkcalendar import DateEntry
            self.tiene_calendario = True
        except ImportError:
            self.tiene_calendario = False
            logger.warning("tkcalendar no está instalado. Se usará un entry normal.")
            logger.info("Para instalar tkcalendar: pip install tkcalendar")
        
        # Comprobar si se pasó una instancia de ConfiguracionSelectorFecha
        if len(args) == 1 and isinstance(args[0], ConfiguracionSelectorFecha):
            config = args[0]
        else:
            config = ConfiguracionSelectorFecha.from_args(*args, **kwargs)
        
        # Configurar variables
        self.formato = config.formato
        self.comando = config.comando
        self.habilitado = config.habilitado
        
        # Procesar fechas mínima y máxima
        self.min_fecha = self._procesar_fecha_limite(config.min_fecha)
        self.max_fecha = self._procesar_fecha_limite(config.max_fecha)
        
        # Convertir valor inicial a date si es necesario
        if isinstance(config.valor_inicial, str):
            try:
                valor_inicial = datetime.strptime(config.valor_inicial, self.formato).date()
            except ValueError:
                valor_inicial = date.today()
        elif isinstance(config.valor_inicial, datetime):
            valor_inicial = config.valor_inicial.date()
        elif isinstance(config.valor_inicial, date):
            valor_inicial = config.valor_inicial
        else:
            valor_inicial = date.today()
        
        # Crear widgets
        self.label = ttk.Label(self, text=config.titulo)
        self.label.grid(row=0, column=0, sticky="w")
        
        if self.tiene_calendario:
            # Convertir formato Python a formato tkcalendar
            # %d/%m/%Y -> dd/mm/yyyy
            date_pattern = self.formato.replace('%d', 'dd').replace('%m', 'mm').replace('%Y', 'yyyy')
            
            # Crear DateEntry con calendario
            self.date_entry = DateEntry(
                self,
                width=config.ancho,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern=date_pattern,
                firstweekday='monday',
                showweeknumbers=False,
                year=valor_inicial.year,
                month=valor_inicial.month,
                day=valor_inicial.day,
                state="readonly" if not self.habilitado else "normal",
                selectmode='day'
            )
            
            # Configurar fecha mínima y máxima si están definidas
            if self.min_fecha:
                self.date_entry.config(mindate=self.min_fecha)
            if self.max_fecha:
                self.date_entry.config(maxdate=self.max_fecha)
            
            self.date_entry.grid(row=0, column=1, padx=(5, 0))
            self.date_entry.bind("<<DateEntrySelected>>", self._on_change)
            
        else:
            # Variable para almacenar la fecha en modo texto
            self.date_var = tk.StringVar(value=valor_inicial.strftime(self.formato))
            
            # Crear entry normal si no está disponible tkcalendar
            self.date_entry = ttk.Entry(
                self,
                textvariable=self.date_var,
                width=config.ancho,
                state="readonly" if not config.habilitado else "normal"
            )
            self.date_entry.grid(row=0, column=1, padx=(5, 0))
            
            # Configurar validación y eventos
            self.date_entry.bind("<FocusOut>", self._validar_fecha)
            self.date_var.trace_add("write", self._on_change)

    def _procesar_fecha_limite(self, fecha):
        """
        Procesa una fecha límite (mínima o máxima) y la convierte a objeto date.
        
        Args:
            fecha: Puede ser None, str en formato ISO, datetime o date
            
        Returns:
            date o None
        """
        if fecha is None:
            return None
        
        if isinstance(fecha, str):
            try:
                return datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                return None
        elif isinstance(fecha, datetime):
            return fecha.date()
        elif isinstance(fecha, date):
            return fecha
        return None

    def _on_change(self, *args):
        """
        Manejador de evento cuando cambia la fecha.
        """
        if self.comando and callable(self.comando):
            self.comando(self.get())

    def _validar_fecha(self, event=None):
        """
        Valida que la fecha ingresada sea válida y esté dentro del rango permitido.
        """
        if not self.tiene_calendario:
            texto = self.date_var.get()
            try:
                fecha = datetime.strptime(texto, self.formato).date()
                
                # Validar restricciones
                if self.min_fecha and fecha < self.min_fecha:
                    self.date_var.set(date.today().strftime(self.formato))
                    return False
                
                if self.max_fecha and fecha > self.max_fecha:
                    self.date_var.set(date.today().strftime(self.formato))
                    return False
                
                return True
            except ValueError:
                self.date_var.set(date.today().strftime(self.formato))
                return False
        return True
    
    def get(self):
        """
        Obtiene la fecha actual como un objeto date.
        """
        if self.tiene_calendario:
            return self.date_entry.get_date()
        else:
            try:
                return datetime.strptime(self.date_var.get(), self.formato).date()
            except ValueError:
                return date.today()
    
    def get_str(self):
        """
        Obtiene la fecha actual como una cadena formateada.
        """
        if self.tiene_calendario:
            return self.date_entry.get()
        else:
            return self.date_var.get()
    
    def set(self, fecha):
        """
        Establece el valor del control y actualiza la visualización.
        
        Args:
            fecha: Puede ser un objeto date, datetime o una cadena en el formato especificado.
        """
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, self.formato).date()
            except ValueError:
                fecha = date.today()
        elif isinstance(fecha, datetime):
            fecha = fecha.date()
        elif not isinstance(fecha, date):
            fecha = date.today()
        
        if self.tiene_calendario:
            self.date_entry.set_date(fecha)
        else:
            self.date_var.set(fecha.strftime(self.formato))

    def habilitar(self, estado=True):
        """
        Habilita o deshabilita el control.
        """
        self.habilitado = estado
        self.date_entry.configure(state="normal" if estado else "readonly")

class SelectorHora(tk.Frame):
    """
    Control SelectorHora que permite seleccionar una hora.
    """
    def __init__(self, parent, *args, **kwargs):
        """
        Inicializa un control SelectorHora.
        """
        super().__init__(parent)
        
        # Comprobar si se pasó una instancia de ConfiguracionSelectorHora
        if len(args) == 1 and isinstance(args[0], ConfiguracionSelectorHora):
            config = args[0]
        else:
            config = ConfiguracionSelectorHora.from_args(*args, **kwargs)
        
        # Configurar variables
        self.formato = config.formato
        self.comando = config.comando
        self.mostrar_segundos = config.mostrar_segundos
        self.intervalo_minutos = config.intervalo_minutos
        
        # Convertir valor inicial a time si es necesario
        if isinstance(config.valor_inicial, str):
            try:
                tiempo = datetime.strptime(config.valor_inicial, self.formato).time()
            except ValueError:
                tiempo = time.now()
        elif isinstance(config.valor_inicial, time):
            tiempo = config.valor_inicial
        else:
            tiempo = time.now()
        
        self.hora_var = tk.StringVar(value=f"{tiempo.hour:02d}")
        self.minuto_var = tk.StringVar(value=f"{tiempo.minute:02d}")
        self.segundo_var = tk.StringVar(value=f"{tiempo.second:02d}")
        
        # Crear widgets
        self.label = ttk.Label(self, text=config.titulo)
        self.label.grid(row=0, column=0, columnspan=5, sticky="w")
        
        # Spinbox para hora (0-23)
        self.hora_spinbox = ttk.Spinbox(
            self,
            from_=0,
            to=23,
            width=2,
            textvariable=self.hora_var,
            wrap=True,
            state="readonly" if not config.habilitado else "normal"
        )
        self.hora_spinbox.grid(row=1, column=0)
        
        ttk.Label(self, text=":").grid(row=1, column=1)
        
        # Spinbox para minutos (0-59)
        self.minuto_spinbox = ttk.Spinbox(
            self,
            from_=0,
            to=59,
            width=2,
            textvariable=self.minuto_var,
            wrap=True,
            increment=self.intervalo_minutos,
            state="readonly" if not config.habilitado else "normal"
        )
        self.minuto_spinbox.grid(row=1, column=2)
        
        if self.mostrar_segundos:
            ttk.Label(self, text=":").grid(row=1, column=3)
            
            # Spinbox para segundos (0-59)
            self.segundo_spinbox = ttk.Spinbox(
                self,
                from_=0,
                to=59,
                width=2,
                textvariable=self.segundo_var,
                wrap=True,
                state="readonly" if not config.habilitado else "normal"
            )
            self.segundo_spinbox.grid(row=1, column=4)
        
        # Configurar validación y eventos
        self.hora_spinbox.bind("<FocusOut>", self._validar_hora)
    def _validar_hora(self, event=None):
        """
        Valida que la hora esté en el rango correcto.
        """
        try:
            hora = int(self.hora_var.get())
            if hora < 0:
                hora = 0
            elif hora > 23:
                hora = 23
            self.hora_var.set(f"{hora:02d}")
        except ValueError:
            self.hora_var.set("00")
        self._on_change()
    
    def _validar_minuto(self, event=None):
        """
        Valida que los minutos estén en el rango correcto.
        """
        try:
            minuto = int(self.minuto_var.get())
            if minuto < 0:
                minuto = 0
            elif minuto > 59:
                minuto = 59
            
            # Ajustar al intervalo más cercano
            if self.intervalo_minutos > 1:
                minuto = (minuto // self.intervalo_minutos) * self.intervalo_minutos
            
            self.minuto_var.set(f"{minuto:02d}")
        except ValueError:
            self.minuto_var.set("00")
        self._on_change()
    
    def _validar_segundo(self, event=None):
        """
        Valida que los segundos estén en el rango correcto.
        """
        try:
            segundo = int(self.segundo_var.get())
            if segundo < 0:
                segundo = 0
            elif segundo > 59:
                segundo = 59
            self.segundo_var.set(f"{segundo:02d}")
        except ValueError:
            self.segundo_var.set("00")
        self._on_change()
    
    def get(self):
        """
        Obtiene la hora seleccionada como objeto datetime.time.
        """
        try:
            hora = int(self.hora_var.get())
            minuto = int(self.minuto_var.get())
            segundo = int(self.segundo_var.get()) if self.mostrar_segundos else 0
            
            return datetime.time(hora, minuto, segundo)
        except ValueError:
            return datetime.time.now()
    
    def get_str(self):
        """
        Obtiene la hora seleccionada como string formateado.
        """
        return self.get().strftime(self.formato)
    
    def set(self, tiempo):
        """
        Establece la hora seleccionada.
        """
        if isinstance(tiempo, str):
            try:
                tiempo = datetime.strptime(tiempo, self.formato).time()
            except ValueError:
                tiempo = datetime.time.now()
        elif not isinstance(tiempo, datetime.time):
            tiempo = datetime.time.now()
        
        self.hora_var.set(f"{tiempo.hour:02d}")
        self.minuto_var.set(f"{tiempo.minute:02d}")
        if self.mostrar_segundos:
            self.segundo_var.set(f"{tiempo.second:02d}")
    
    def habilitar(self, estado=True):
        """
        Habilita o deshabilita el control.
        """
        estado_tk = "normal" if estado else "disabled"
        self.hora_spinbox.configure(state=estado_tk)
        self.minuto_spinbox.configure(state=estado_tk)
        if self.mostrar_segundos:
            self.segundo_spinbox.configure(state=estado_tk)
        self.habilitado = estado
 
class CargarFichero(tk.Frame):
    """
    Control CargarFichero que permite seleccionar un archivo.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        
        # Determinar si se pasó una configuración o argumentos sueltos
        if len(args) == 1 and isinstance(args[0], ConfiguracionCargarFichero):
            config = args[0]
        else:
            config = ConfiguracionCargarFichero.from_args(*args, **kwargs)
        
        # Configurar propiedades
        self.titulo = config.titulo
        self.tipos_archivo = config.tipos_archivo
        self.directorio_inicial = config.directorio_inicial
        self.habilitado = config.habilitado
        self.comando = config.comando
        self.ancho = config.ancho
        self.modo = config.modo
        
        # Variable para almacenar la ruta del archivo
        self.ruta_archivo = tk.StringVar()
        
        # Crear etiqueta
        self.label = ttk.Label(self, text=self.titulo)
        self.label.grid(row=0, column=0, sticky=tk.W)
        
        # Crear entry para mostrar la ruta
        self.entry = ttk.Entry(
            self,
            textvariable=self.ruta_archivo,
            width=self.ancho
        )
        self.entry.grid(row=0, column=1, padx=(5, 5))
        
        # Crear botón para abrir el diálogo
        self.boton = ttk.Button(
            self,
            text="...",
            width=3,
            command=self._abrir_dialogo
        )
        self.boton.grid(row=0, column=2)
        
        # Configurar estado inicial
        if not self.habilitado:
            self.entry.configure(state="disabled")
            self.boton.configure(state="disabled")
    
    def _abrir_dialogo(self):
        """
        Abre el diálogo de selección de archivo.
        """
        if self.modo == "abrir":
            ruta = filedialog.askopenfilename(
                title=self.titulo,
                initialdir=self.directorio_inicial,
                filetypes=self.tipos_archivo
            )
        else:  # guardar
            ruta = filedialog.asksaveasfilename(
                title=self.titulo,
                initialdir=self.directorio_inicial,
                filetypes=self.tipos_archivo
            )
        
        if ruta:  # Si se seleccionó un archivo
            self.ruta_archivo.set(ruta)
            if self.comando and callable(self.comando):
                self.comando(ruta)
    
    def get(self):
        """
        Obtiene la ruta del archivo seleccionado.
        """
        return self.ruta_archivo.get()
    
    def set(self, ruta):
        """
        Establece la ruta del archivo.
        """
        self.ruta_archivo.set(ruta)
    
    def habilitar(self, estado=True):
        """
        Habilita o deshabilita el control.
        """
        estado_tk = "normal" if estado else "disabled"
        self.entry.configure(state=estado_tk)
        self.boton.configure(state=estado_tk)
        self.habilitado = estado

class Deslizante(tk.Frame):
    """
    Control deslizante que permite seleccionar un valor en un rango.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        
        # Determinar si se pasó una configuración o argumentos sueltos
        if len(args) == 1 and isinstance(args[0], ConfiguracionDeslizante):
            config = args[0]
        else:
            config = ConfiguracionDeslizante.from_args(*args, **kwargs)
        
        # Configurar propiedades
        self.titulo = config.titulo
        self.valor_minimo = config.valor_minimo
        self.valor_maximo = config.valor_maximo
        self.orientacion = config.orientacion
        self.habilitado = config.habilitado
        self.comando = config.comando
        self.ancho = config.ancho
        self.mostrar_valor = config.mostrar_valor
        self.incremento = config.incremento
        
        # Variable para almacenar el valor
        self.valor = tk.DoubleVar(value=config.valor_inicial)
        
        # Crear etiqueta
        self.label = ttk.Label(self, text=self.titulo)
        self.label.grid(row=0, column=0, sticky=tk.W)
        
        # Crear deslizante
        self.deslizante = ttk.Scale(
            self,
            from_=self.valor_minimo,
            to=self.valor_maximo,
            orient=tk.HORIZONTAL if self.orientacion == "horizontal" else tk.VERTICAL,
            variable=self.valor,
            command=self._on_change
        )
        
        # Configurar tamaño
        if self.orientacion == "horizontal":
            self.deslizante.configure(length=self.ancho)
        else:
            self.deslizante.configure(length=self.ancho)
        
        self.deslizante.grid(row=0, column=1, padx=(5, 5))
        
        # Crear etiqueta para mostrar el valor
        if self.mostrar_valor:
            self.valor_label = ttk.Label(self, width=5)
            self.valor_label.grid(row=0, column=2)
            self._actualizar_etiqueta_valor()
        
        # Configurar estado inicial
        if not self.habilitado:
            self.deslizante.configure(state="disabled")
    
    def _on_change(self, event=None):
        """
        Manejador de evento cuando cambia el valor del deslizante.
        """
        # Ajustar al incremento
        if self.incremento > 0:
            valor_actual = self.valor.get()
            valor_ajustado = round(valor_actual / self.incremento) * self.incremento
            if valor_actual != valor_ajustado:
                self.valor.set(valor_ajustado)
        
        # Actualizar etiqueta de valor
        if self.mostrar_valor:
            self._actualizar_etiqueta_valor()
        
        # Llamar al comando
        if self.comando and callable(self.comando):
            self.comando(self.get())
    
    def _actualizar_etiqueta_valor(self):
        """
        Actualiza la etiqueta que muestra el valor actual.
        """
        valor = self.get()
        if valor == int(valor):
            # Si es un entero, mostrar sin decimales
            self.valor_label.configure(text=f"{int(valor)}")
        else:
            # Si tiene decimales, mostrar con formato adecuado
            self.valor_label.configure(text=f"{valor:.1f}")
    
    def get(self):
        """
        Obtiene el valor actual del deslizante.
        """
        return self.valor.get()
    
    def set(self, valor):
        """
        Establece el valor del deslizante.
        """
        # Validar que esté en el rango
        if valor < self.valor_minimo:
            valor = self.valor_minimo
        elif valor > self.valor_maximo:
            valor = self.valor_maximo
        
        self.valor.set(valor)
        
        # Actualizar etiqueta de valor
        if self.mostrar_valor:
            self._actualizar_etiqueta_valor()
    
    def habilitar(self, estado=True):
        """
        Habilita o deshabilita el control.
        """
        self.deslizante.configure(state="normal" if estado else "disabled")
        self.habilitado = estado
                              