"""
Ejemplo_03.py - Formulario completo usando las funciones desarrolladas en Formulario.py
Demuestra el uso de todos los controles disponibles
"""

import tkinter as tk
from tkinter import messagebox
import datetime
from Formulario import Formulario

class EjemploFormularioCompleto:
    def __init__(self):
        # Crear formulario principal
        self.formulario = Formulario(
            titulo="Ejemplo 03 - Formulario Completo",
            iconimagen="img_vacia_xsk_icon.ico",
            cerrar_al_salir=True
        )
        
        # Datos de ejemplo
        self.inicializar_datos()
        
        # Crear controles
        self.crear_controles()
        
        # Configurar ventana
        self.formulario.ventana.geometry("900x700")
        self.centrar_ventana()
    
    def inicializar_datos(self):
        """Inicializa los datos de ejemplo."""
        self.ciudades = {
            "001": "Madrid",
            "002": "Barcelona", 
            "003": "Valencia",
            "004": "Sevilla",
            "005": "Málaga",
            "006": "Murcia",
            "007": "Palma de Mallorca",
            "008": "Las Palmas",
            "009": "Bilbao",
            "010": "Alicante"
        }
        
        self.profesiones = {
            "ING": "Ingeniero/a",
            "MED": "Médico/a",
            "ABG": "Abogado/a",
            "DOC": "Docente",
            "ADM": "Administrador/a",
            "CON": "Contador/a",
            "ARQ": "Arquitecto/a",
            "PSI": "Psicólogo/a"
        }
        
        self.departamentos = {
            "RRHH": "Recursos Humanos",
            "CONT": "Contabilidad",
            "VENT": "Ventas",
            "MARK": "Marketing",
            "PROD": "Producción",
            "SIST": "Sistemas"
        }
    
    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.formulario.ventana.update_idletasks()
        ancho = 900
        alto = 700
        x = (self.formulario.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.formulario.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.formulario.ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def crear_controles(self):
        """Crea todos los controles usando las funciones del formulario."""
        
        # === MARCO PRINCIPAL ===
        self.marco_principal = self.formulario.agregar_marco(
            contenedor=self.formulario.ventana,
            bd=2,
            relief="groove"
        )
        self.formulario.posicionar_objeto(
            self.marco_principal, 
            'grid', 
            row=0, column=0, padx=10, pady=10, sticky="nsew"
        )
        
        # Configurar expansión
        self.formulario.ventana.grid_rowconfigure(0, weight=1)
        self.formulario.ventana.grid_columnconfigure(0, weight=1)
        
        # === SECCIÓN 1: INFORMACIÓN PERSONAL ===
        self.seccion_personal = self.formulario.agregar_etiqueta_marco(
            contenedor=self.marco_principal,
            descripcion="INFORMACIÓN PERSONAL"
        )
        self.formulario.posicionar_objeto(
            self.seccion_personal, 
            'grid', 
            row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        
        # Nombre completo
        self.nombre = self.formulario.agregar_textbox(
            self.seccion_personal,
            titulo_control="Nombre completo:",
            tipo_validacion="str",
            ancho=35
        )
        self.formulario.posicionar_objeto(
            self.nombre, 
            'grid', 
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Cédula con máscara
        self.cedula = self.formulario.agregar_textbox(
            self.seccion_personal,
            titulo_control="Cédula:",
            mascara="########-#",
            caracteres_fijos="-",
            tipo_validacion="str",
            ancho=15
        )
        self.formulario.posicionar_objeto(
            self.cedula, 
            'grid', 
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Edad
        self.edad = self.formulario.agregar_textbox(
            self.seccion_personal,
            titulo_control="Edad:",
            tipo_validacion="int",
            mascara="##",
            ancho=5
        )
        self.formulario.posicionar_objeto(
            self.edad, 
            'grid', 
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Email
        self.email = self.formulario.agregar_textbox(
            self.seccion_personal,
            titulo_control="Email:",
            tipo_validacion="str",
            ancho=35
        )
        self.formulario.posicionar_objeto(
            self.email, 
            'grid', 
            row=3, column=0, padx=5, pady=5, sticky="w"
        )
        
        # === SECCIÓN 2: FECHAS Y HORARIOS ===
        self.seccion_fechas = self.formulario.agregar_etiqueta_marco(
            contenedor=self.marco_principal,
            descripcion="FECHAS Y HORARIOS"
        )
        self.formulario.posicionar_objeto(
            self.seccion_fechas, 
            'grid', 
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        
        # Fecha de nacimiento (Textbox)
        self.fecha_nacimiento = self.formulario.agregar_textbox(
            self.seccion_fechas,
            titulo_control="Fecha nacimiento:",
            mascara="DD/MM/AAAA",
            caracteres_fijos="/",
            tipo_validacion="fecha",
            ancho=12
        )
        self.formulario.posicionar_objeto(
            self.fecha_nacimiento, 
            'grid', 
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Fecha (SelectorFecha)
        self.fecha_picker = self.formulario.agregar_selectorfecha(
            self.seccion_fechas,
            titulo="Fecha (SelectorFecha):",
            valor_inicial=datetime.date(1990, 1, 1)
        )
        self.formulario.posicionar_objeto(
            self.fecha_picker, 
            'grid', 
            row=0, column=1, padx=5, pady=5, sticky="w"
        )
        
        # Hora (Textbox)
        self.hora = self.formulario.agregar_textbox(
            self.seccion_fechas,
            titulo_control="Hora:",
            mascara="HH:MM",
            caracteres_fijos=":",
            tipo_validacion="hora",
            ancho=8
        )
        self.formulario.posicionar_objeto(
            self.hora, 
            'grid', 
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Hora (SelectorHora)
        self.hora_picker = self.formulario.agregar_selectorhora(
            self.seccion_fechas,
            titulo="Hora (SelectorHora):",
            valor_inicial=datetime.time(8, 0)
        )
        self.formulario.posicionar_objeto(
            self.hora_picker, 
            'grid', 
            row=1, column=1, padx=5, pady=5, sticky="w"
        )
        
        # === SECCIÓN 3: BÚSQUEDA Y SELECCIÓN ===
        self.seccion_busqueda = self.formulario.agregar_etiqueta_marco(
            contenedor=self.marco_principal,
            descripcion="BÚSQUEDA Y SELECCIÓN"
        )
        self.formulario.posicionar_objeto(
            self.seccion_busqueda, 
            'grid', 
            row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        
        # Ciudad (Textbox con búsqueda)
        self.ciudad = self.formulario.agregar_textbox(
            self.seccion_busqueda,
            titulo_control="Ciudad:",
            tipo_validacion="str",
            fuente_datos=self.ciudades,
            modo_busqueda="inicio",
            ancho=25
        )
        self.formulario.posicionar_objeto(
            self.ciudad, 
            'grid', 
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Profesión (Combobox)
        self.profesion = self.formulario.agregar_combobox(
            self.seccion_busqueda,
            titulo_control="Profesión:",
            valores=list(self.profesiones.values()),
            fuente_datos=self.profesiones,
            ancho=25
        )
        self.formulario.posicionar_objeto(
            self.profesion, 
            'grid', 
            row=0, column=1, padx=5, pady=5, sticky="w"
        )
        
        # Departamento (Listbox)
        self.departamento = self.formulario.agregar_listbox(
            self.seccion_busqueda,
            titulo_control="Departamento:",
            fuente_datos=self.departamentos,
            altura=4,
            ancho=25
        )
        self.formulario.posicionar_objeto(
            self.departamento, 
            'grid', 
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Estado civil (OptionGroup)
        opciones_estado = [
            ("S", "Soltero/a"),
            ("C", "Casado/a"),
            ("D", "Divorciado/a"),
            ("V", "Viudo/a")
        ]
        
        self.estado_civil = self.formulario.agregar_optiongroup(
            self.seccion_busqueda,
            "Estado civil:",
            opciones=opciones_estado,
            valor_inicial="S",
            orientacion="horizontal",
            comando=self.on_change
        )
        self.formulario.posicionar_objeto(
            self.estado_civil, 
            'grid', 
            row=1, column=1, padx=5, pady=5, sticky="w"
        )
        
        # === SECCIÓN 4: ARCHIVOS Y VALORES ===
        self.seccion_archivos = self.formulario.agregar_etiqueta_marco(
            contenedor=self.marco_principal,
            descripcion="ARCHIVOS Y VALORES"
        )
        self.formulario.posicionar_objeto(
            self.seccion_archivos, 
            'grid', 
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        
        # Archivo
        tipos_archivo = [
            ("Documentos", "*.pdf *.doc *.docx"),
            ("Todos", "*.*")
        ]
        self.archivo = self.formulario.agregar_cargarfichero(
            self.seccion_archivos,
            titulo="Curriculum:",
            tipos_archivo=tipos_archivo
        )
        self.formulario.posicionar_objeto(
            self.archivo, 
            'grid', 
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        
        # Salario
        self.salario = self.formulario.agregar_textbox(
            self.seccion_archivos,
            titulo_control="Salario:",
            tipo_validacion="float",
            mascara="####.##",
            ancho=15
        )
        self.formulario.posicionar_objeto(
            self.salario, 
            'grid', 
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Experiencia (Deslizante)
        self.experiencia = self.formulario.agregar_deslizante(
            self.seccion_archivos,
            titulo="Años experiencia:",
            valor_inicial=2,
            valor_minimo=0,
            valor_maximo=30
        )
        self.formulario.posicionar_objeto(
            self.experiencia, 
            'grid', 
            row=1, column=1, padx=5, pady=5, sticky="ew"
        )
        
        # === SECCIÓN 5: PREFERENCIAS ===
        self.seccion_preferencias = self.formulario.agregar_etiqueta_marco(
            contenedor=self.marco_principal,
            descripcion="PREFERENCIAS"
        )
        self.formulario.posicionar_objeto(
            self.seccion_preferencias, 
            'grid', 
            row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        
        # Disponible para viajar
        self.viajar = self.formulario.agregar_checkbox(
            self.seccion_preferencias,
            titulo="Disponible para viajar",
            valor_inicial=False
        )
        self.formulario.posicionar_objeto(
            self.viajar, 
            'grid', 
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        
        # Trabajo remoto
        self.remoto = self.formulario.agregar_checkbox(
            self.seccion_preferencias,
            titulo="Trabajo remoto",
            valor_inicial=True
        )
        self.formulario.posicionar_objeto(
            self.remoto, 
            'grid', 
            row=0, column=1, padx=5, pady=5, sticky="w"
        )
        
        # === BOTONES ===
        self.frame_botones = tk.Frame(self.marco_principal)
        self.formulario.posicionar_objeto(
            self.frame_botones, 
            'grid', 
            row=5, column=0, columnspan=2, pady=20
        )
        
        # Botón Validar
        self.btn_validar = self.formulario.agregar_boton(
            self.frame_botones,
            caption="Validar",
            comando=self.validar_formulario,
            ancho=12
        )
        self.formulario.posicionar_objeto(
            self.btn_validar, 
            'pack', 
            side=tk.LEFT, padx=5
        )
        
        # Botón Mostrar Datos
        self.btn_mostrar = self.formulario.agregar_boton(
            self.frame_botones,
            caption="Mostrar Datos",
            comando=self.mostrar_datos,
            ancho=12
        )
        self.formulario.posicionar_objeto(
            self.btn_mostrar, 
            'pack', 
            side=tk.LEFT, padx=5
        )
        
        # Botón Limpiar
        self.btn_limpiar = self.formulario.agregar_boton(
            self.frame_botones,
            caption="Limpiar",
            comando=self.limpiar_formulario,
            ancho=12
        )
        self.formulario.posicionar_objeto(
            self.btn_limpiar, 
            'pack', 
            side=tk.LEFT, padx=5
        )
        
        # Botón Datos de Prueba
        self.btn_datos = self.formulario.agregar_boton(
            self.frame_botones,
            caption="Datos Prueba",
            comando=self.cargar_datos_prueba,
            ancho=12
        )
        self.formulario.posicionar_objeto(
            self.btn_datos, 
            'pack', 
            side=tk.LEFT, padx=5
        )
    
    def validar_formulario(self):
        """Valida el formulario usando el método del formulario."""
        try:
            # Usar el método enviar_datos que ya valida todos los controles
            self.formulario.enviar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"Error en validación: {e}")
    
    def mostrar_datos(self):
        """Muestra todos los datos del formulario."""
        datos = []
        
        datos.append("=== INFORMACIÓN PERSONAL ===")
        datos.append(f"Nombre: {self.nombre.obtener_valor()}")
        datos.append(f"Cédula: {self.cedula.obtener_valor()}")
        datos.append(f"Edad: {self.edad.obtener_valor()}")
        datos.append(f"Email: {self.email.obtener_valor()}")
        
        datos.append("\n=== FECHAS Y HORARIOS ===")
        datos.append(f"Fecha (Textbox): {self.fecha_nacimiento.obtener_valor()}")
        datos.append(f"Fecha (SelectorFecha): {self.fecha_picker.get_str()}")
        datos.append(f"Hora (Textbox): {self.hora.obtener_valor()}")
        datos.append(f"Hora (SelectorHora): {self.hora_picker.get_str()}")
        
        datos.append("\n=== BÚSQUEDA Y SELECCIÓN ===")
        datos.append(f"Ciudad: {self.ciudad.obtener_valor()}")
        datos.append(f"Profesión: {self.profesion.get()}")
        datos.append(f"Departamento: {self.departamento.get_selected()}")
        datos.append(f"Estado civil: {self.estado_civil.get()}")
        
        datos.append("\n=== ARCHIVOS Y VALORES ===")
        datos.append(f"Archivo: {self.archivo.get() or 'No seleccionado'}")
        datos.append(f"Salario: {self.salario.obtener_valor()}")
        datos.append(f"Experiencia: {self.experiencia.get()} años")
        
        datos.append("\n=== PREFERENCIAS ===")
        datos.append(f"Viajar: {self.viajar.get()}")
        datos.append(f"Remoto: {self.remoto.get()}")
        
        messagebox.showinfo("Datos del Formulario", "\n".join(datos))
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario."""
        # Limpiar textboxes
        self.nombre.establecer_valor("")
        self.cedula.establecer_valor("")
        self.edad.establecer_valor("")
        self.email.establecer_valor("")
        self.fecha_nacimiento.establecer_valor("")
        self.hora.establecer_valor("")
        self.ciudad.establecer_valor("")
        self.salario.establecer_valor("")
        
        # Limpiar otros controles
        self.fecha_picker.set(datetime.date.today())
        self.hora_picker.set(datetime.time(8, 0))
        self.profesion.set("")
        self.estado_civil.set("S")
        self.archivo.set("")
        self.experiencia.set(2)
        self.viajar.set(False)
        self.remoto.set(True)
        
        messagebox.showinfo("Limpiar", "Formulario limpiado correctamente")
    
    def cargar_datos_prueba(self):
        """Carga datos de prueba en el formulario."""
        # Información personal
        self.nombre.establecer_valor("María García López")
        self.cedula.establecer_valor("12345678-9")
        self.edad.establecer_valor("28")
        self.email.establecer_valor("maria@email.com")
        
        # Fechas
        self.fecha_nacimiento.establecer_valor("15/03/1995")
        self.hora.establecer_valor("08:30")
        
        # Selecciones
        self.ciudad.establecer_valor("Madrid")
        self.profesion.set("Ingeniero/a")
        self.estado_civil.set("C")
        
        # Valores
        self.salario.establecer_valor("3500.50")
        self.experiencia.set(5)
        self.viajar.set(True)
        
        messagebox.showinfo("Datos de Prueba", "Datos cargados correctamente")
    
    def ejecutar(self):
        """Ejecuta la aplicación."""
        self.formulario.mostrar()

def main():
    """Función principal."""
    app = EjemploFormularioCompleto()
    app.ejecutar()

if __name__ == "__main__":
    main()