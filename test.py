import speedtest
import tkinter as tk
from tkinter import ttk
import threading
import time

class MedidorVelocidad:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Medidor de Velocidad de Internet")
        self.ventana.geometry("500x420")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f0f0")

        # Variables para la prueba
        self.etapa_actual = 0
        self.etapas_totales = 3  

        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame principal
        frame_principal = tk.Frame(self.ventana, bg="#f0f0f0", padx=20, pady=10)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = tk.Label(frame_principal, text="Test de Velocidad de Internet", 
                          font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
        titulo.pack(pady=(10, 5))

        # Descripción
        descripcion = tk.Label(frame_principal, text="Mide la velocidad de tu conexión a Internet",
                               font=("Helvetica", 10), bg="#f0f0f0", fg="#7f8c8d")
        descripcion.pack(pady=(0, 20))

        # Estado y progreso
        self.etiqueta_estado = tk.Label(frame_principal, text="Listo para iniciar la prueba",
                                        font=("Helvetica", 12), bg="#f0f0f0", fg="#3498db")
        self.etiqueta_estado.pack(pady=5)

        self.barra_progreso = ttk.Progressbar(frame_principal, orient="horizontal",
                                              length=400, mode="determinate")
        self.barra_progreso.pack(pady=10)

        self.etiqueta_etapa = tk.Label(frame_principal, text="", font=("Helvetica", 10),
                                       bg="#f0f0f0", fg="#7f8c8d")
        self.etiqueta_etapa.pack(pady=5)

        # Resultados
        self.etiqueta_descarga = tk.Label(frame_principal, text="Velocidad de descarga: --- Mbps",
                                          font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_descarga.pack()

        self.etiqueta_subida = tk.Label(frame_principal, text="Velocidad de subida: --- Mbps",
                                        font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_subida.pack()

        self.etiqueta_ping = tk.Label(frame_principal, text="Latencia (ping): --- ms",
                                      font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_ping.pack()

        # Estilos para botón
        estilo = ttk.Style()
        estilo.configure("TButton", font=("Helvetica", 12), padding=5)

        self.boton_iniciar = ttk.Button(frame_principal, text="Iniciar Prueba",
                                        command=self.iniciar_prueba, style="TButton")
        self.boton_iniciar.pack(pady=20)

        # Pie de página
        pie = tk.Label(frame_principal, text="Desarrollado con Python y Tkinter",
                       font=("Helvetica", 8), bg="#f0f0f0", fg="#95a5a6")
        pie.pack(side=tk.BOTTOM, pady=10)
    
    def actualizar_progreso(self, etapa, mensaje):
        self.etapa_actual = etapa
        progreso = (etapa / self.etapas_totales) * 100
        self.barra_progreso["value"] = progreso
        self.etiqueta_estado.config(text=mensaje)

        etapas = ["Buscando servidor...", "Midiendo velocidad de descarga...", "Midiendo velocidad de subida..."]
        if etapa < len(etapas):
            self.etiqueta_etapa.config(text=etapas[etapa])
        else:
            self.etiqueta_etapa.config(text="Prueba completada")

        self.ventana.update()
    
    def medir_velocidad(self):
        try:
            # Bloquear botón mientras corre la prueba
            self.boton_iniciar.config(state=tk.DISABLED, text="Ejecutando...")
            self.etiqueta_estado.config(text="Iniciando prueba...", fg="#3498db")
            self.barra_progreso["value"] = 0
            self.ventana.update()

            # Instancia de Speedtest
            st = speedtest.Speedtest()

            # Buscar mejor servidor
            self.actualizar_progreso(0, "Buscando el mejor servidor...")
            st.get_best_server()
            time.sleep(0.5)

            # Medir velocidad de descarga
            self.actualizar_progreso(1, "Midiendo velocidad de descarga...")
            velocidad_descarga = st.download() / 1_000_000  

            # Medir velocidad de subida
            self.actualizar_progreso(2, "Midiendo velocidad de subida...")
            velocidad_subida = st.upload() / 1_000_000  

            # Obtener ping
            ping = st.results.ping  

            # Completar barra de progreso
            self.barra_progreso["value"] = 100
            self.etiqueta_etapa.config(text="")

            # Mostrar resultados
            self.etiqueta_descarga.config(text=f"Velocidad de descarga: {velocidad_descarga:.2f} Mbps")
            self.etiqueta_subida.config(text=f"Velocidad de subida: {velocidad_subida:.2f} Mbps")
            self.etiqueta_ping.config(text=f"Latencia (ping): {ping:.2f} ms")

            self.etiqueta_estado.config(text="Prueba completada con éxito", fg="#27ae60")

        except Exception as e:
            self.etiqueta_estado.config(text=f"Error: {str(e)}", fg="#e74c3c")
            self.etiqueta_etapa.config(text="")

        finally:
            # Restaurar botón al finalizar
            self.boton_iniciar.config(state=tk.NORMAL, text="Iniciar Prueba")

    def iniciar_prueba(self):
        # Inicia la prueba en un nuevo hilo para evitar congelamiento de la UI
        hilo = threading.Thread(target=self.medir_velocidad, daemon=True)
        hilo.start()

# Iniciar aplicación
if __name__ == "__main__":
    ventana = tk.Tk()
    app = MedidorVelocidad(ventana)
    ventana.mainloop()
