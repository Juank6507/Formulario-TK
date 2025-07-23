import os
import sys

# Añadir la ruta de Archivos_Comunes al sys.path
ruta_archivos_comunes = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Archivos_Comunes'))
sys.path.append(ruta_archivos_comunes)

from Formulario import Formulario, ConfiguracionTextbox, MessageBox

class EjemploFormulario(Formulario):
    def __init__(self):
        super().__init__("Ejemplo de Formulario Adaptativo", "icono.ico")
        self.crear_controles()

    def crear_controles(self):
        # Frame principal usando grid
        frame_principal = self.agregar_marco(self.ventana)
        frame_principal.grid(row=0, column=0, padx=10, pady=10)

        # Frame para controles usando pack
        frame_pack = self.agregar_marco(frame_principal)
        frame_pack.grid(row=0, column=0, padx=5, pady=5)

        # Frame para controles usando grid
        frame_grid = self.agregar_marco(frame_principal)
        frame_grid.grid(row=0, column=1, padx=5, pady=5)

        # Configuración de controles con caracteres fijos pasados como argumento
        config_fecha = ConfiguracionTextbox(
            titulo_control="Fecha (DD/MM/AAAA)",
            tipo_validacion="fecha",
            restricciones={"min": "1900-01-01", "max": "2099-12-31"},
            mascara="DD/MM/AAAA",
            caracteres_fijos="/"
        )

        # Controles en frame_pack (usando pack)
        self.fecha = self.agregar_textbox(frame_pack, config_fecha)
        self.fecha.pack(pady=5)

        config_hora = ConfiguracionTextbox(
            titulo_control="Hora (HH:MM)",
            tipo_validacion="hora",
            mascara="hh:mm",
            caracteres_fijos=":"
        )

        self.hora = self.agregar_textbox(frame_pack, config_hora)
        self.hora.pack(pady=5)
        
        self.momento = self.agregar_textbox(frame_pack, "Fecha y Hora", "momento", {}, "DD/MM/AAAA HH:MM", "/ :")
        self.momento.pack(pady=5)
        
        config_telefono = ConfiguracionTextbox(
            titulo_control="Teléfono",
            tipo_validacion="str",
            restricciones={"length": 10},
            mascara="(###) ##-##-##",
            caracteres_fijos="() -"
        )

        self.telefono = self.agregar_textbox(frame_pack, config_telefono)
        self.telefono.pack(pady=5)

        # Controles en frame_grid (usando grid)
        self.cp = self.agregar_textbox(frame_grid, ConfiguracionTextbox(
            titulo_control="Código Postal",
            tipo_validacion="str",
            restricciones={"length": 5},
            mascara="#####"
        ))
        self.cp.grid(row=0, column=0, padx=5, pady=5)
        
        config_entero = ConfiguracionTextbox(
            titulo_control="Número entero",
            tipo_validacion="int",
            restricciones={"min": 0, "max": 999},
            mascara="###"
        )

        self.entero = self.agregar_textbox(frame_grid, config_entero)
        self.entero.grid(row=1, column=0, padx=5, pady=5)

        self.decimal = self.agregar_textbox(frame_grid, ConfiguracionTextbox(
            titulo_control="Número decimal",
            tipo_validacion="float",
            restricciones={"min": 0, "max":999.99},
            mascara="###,##"
        ))
        self.decimal.grid(row=2, column=0, padx=5, pady=5)

        # OptionGroup en frame_principal (usando grid)
        opciones = ["Opción 1", "Opción 2", "Opción 3"]
        self.opcion_group = self.agregar_optiongroup(frame_principal, "Seleccione una opción", opciones)
        self.opcion_group.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Botones en frame_principal (usando grid)
        self.boton_validar = self.agregar_boton(frame_principal, "Validar", self.enviar_datos, 10)
        self.boton_validar.grid(row=2, column=0, padx=5, pady=5)

        self.boton_salir = self.agregar_boton(frame_principal, "Salir", self.salir, 10)
        self.boton_salir.grid(row=2, column=1, padx=5, pady=5)

if __name__ == "__main__":
    app = EjemploFormulario()
    app.mostrar()