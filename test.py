import speedtest
import tkinter as tk
from tkinter import ttk
import threading
import time

class MedidorVelocidad:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Medidor de Velocidad de Internet")
        self.ventana.geometry("500x450")  # Ajuste en altura para el nuevo botón
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f0f0")

        # Variables para la prueba
        self.etapa_actual = 0
        self.etapas_totales = 3  

        self.crear_widgets()
        
    def crear_widgets(self):
        frame_principal = tk.Frame(self.ventana, bg="#f0f0f0", padx=20, pady=10)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(frame_principal, text="Test de Velocidad de Internet", 
                          font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
        titulo.pack(pady=(10, 5))

        descripcion = tk.Label(frame_principal, text="Mide la velocidad de tu conexión a Internet",
                               font=("Helvetica", 10), bg="#f0f0f0", fg="#7f8c8d")
        descripcion.pack(pady=(0, 20))

        self.etiqueta_estado = tk.Label(frame_principal, text="Listo para iniciar la prueba",
                                        font=("Helvetica", 12), bg="#f0f0f0", fg="#3498db")
        self.etiqueta_estado.pack(pady=5)

        self.barra_progreso = ttk.Progressbar(frame_principal, orient="horizontal",
                                              length=400, mode="determinate")
        self.barra_progreso.pack(pady=10)

        self.etiqueta_etapa = tk.Label(frame_principal, text="", font=("Helvetica", 10),
                                       bg="#f0f0f0", fg="#7f8c8d")
        self.etiqueta_etapa.pack(pady=5)

        self.etiqueta_descarga = tk.Label(frame_principal, text="Velocidad de descarga: --- Mbps",
                                          font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_descarga.pack()

        self.etiqueta_subida = tk.Label(frame_principal, text="Velocidad de subida: --- Mbps",
                                        font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_subida.pack()

        self.etiqueta_ping = tk.Label(frame_principal, text="Latencia (ping): --- ms",
                                      font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_ping.pack()

        estilo = ttk.Style()
        estilo.configure("TButton", font=("Helvetica", 12), padding=5)

        self.boton_iniciar = ttk.Button(frame_principal, text="Iniciar Prueba",
                                        command=self.iniciar_prueba, style="TButton")
        self.boton_iniciar.pack(pady=10)

        # Botón para volver a hacer la prueba
        self.boton_reiniciar = ttk.Button(frame_principal, text="Volver a hacer la prueba",
                                          command=self.reiniciar_prueba, style="TButton")
        self.boton_reiniciar.pack(pady=10)
        self.boton_reiniciar.config(state=tk.DISABLED)  # Deshabilitado hasta que termine la primera prueba

        pie = tk.Label(frame_principal, text="Desarrollado con Python y Tkinter",
                       font=("Helvetica", 8), bg="#f0f0f0", fg="#95a5a6")
        pie.pack(side=tk.BOTTOM, pady=10)
    
    def actualizar_progreso(self, etapa, mensaje):
        self.etapa_actual = etapa
        progreso = (etapa / self.etapas_totales) * 100
        self.barra_progreso["value"] = progreso
        self.etiqueta_estado.config(text=mensaje)

        etapas = ["Buscando servidor...", "Midiendo velocidad de descarga...", "Midiendo velocidad de subida..."]
        self.etiqueta_etapa.config(text=etapas[etapa] if etapa < len(etapas) else "Prueba completada")

        self.ventana.update()
    
    def medir_velocidad(self):
        try:
            self.boton_iniciar.config(state=tk.DISABLED, text="Ejecutando...")
            self.boton_reiniciar.config(state=tk.DISABLED)  # Bloqueamos el botón mientras corre la prueba
            self.etiqueta_estado.config(text="Iniciando prueba...", fg="#3498db")
            self.barra_progreso["value"] = 0
            self.ventana.update()

            st = speedtest.Speedtest()

            self.actualizar_progreso(0, "Buscando el mejor servidor...")
            st.get_best_server()
            time.sleep(0.5)

            self.actualizar_progreso(1, "Midiendo velocidad de descarga...")
            velocidad_descarga = st.download() / 1_000_000  

            self.actualizar_progreso(2, "Midiendo velocidad de subida...")
            velocidad_subida = st.upload() / 1_000_000  

            ping = st.results.ping  

            self.barra_progreso["value"] = 100
            self.etiqueta_etapa.config(text="")

            self.etiqueta_descarga.config(text=f"Velocidad de descarga: {velocidad_descarga:.2f} Mbps")
            self.etiqueta_subida.config(text=f"Velocidad de subida: {velocidad_subida:.2f} Mbps")
            self.etiqueta_ping.config(text=f"Latencia (ping): {ping:.2f} ms")

            self.etiqueta_estado.config(text="Prueba completada con éxito", fg="#27ae60")
            self.boton_reiniciar.config(state=tk.NORMAL)  # Habilitamos el botón de "Volver a hacer la prueba"

        except Exception as e:
            self.etiqueta_estado.config(text=f"Error: {str(e)}", fg="#e74c3c")
            self.etiqueta_etapa.config(text="")

        finally:
            self.boton_iniciar.config(state=tk.NORMAL, text="Iniciar Prueba")

    def iniciar_prueba(self):
        hilo = threading.Thread(target=self.medir_velocidad, daemon=True)
        hilo.start()

    def reiniciar_prueba(self):
        """Restablece la UI para volver a hacer la prueba"""
        self.etiqueta_estado.config(text="Listo para iniciar la prueba", fg="#3498db")
        self.etiqueta_etapa.config(text="")
        self.barra_progreso["value"] = 0
        self.etiqueta_descarga.config(text="Velocidad de descarga: --- Mbps")
        self.etiqueta_subida.config(text="Velocidad de subida: --- Mbps")
        self.etiqueta_ping.config(text="Latencia (ping): --- ms")
        self.boton_reiniciar.config(state=tk.DISABLED)  # Se deshabilita hasta que termine otra prueba
        self.boton_iniciar.config(state=tk.NORMAL)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = MedidorVelocidad(ventana)
    ventana.mainloop()
