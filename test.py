import speedtest
import tkinter as tk
from tkinter import ttk
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MedidorVelocidad:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Medidor de Velocidad de Internet")
        self.ventana.geometry("800x650")  
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f0f0")

        self.etapa_actual = 0
        self.etapas_totales = 3  
        self.resultados = {"descarga": 0, "subida": 0, "ping": 0}

        self.crear_widgets()
        
    def crear_widgets(self):
        frame_principal = tk.Frame(self.ventana, bg="#f0f0f0", padx=20, pady=10)
        frame_principal.pack(fill=tk.BOTH, expand=True)

        titulo = tk.Label(frame_principal, text="Test de Velocidad de Internet", 
                          font=("Helvetica", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
        titulo.pack(pady=(10, 5))

        self.etiqueta_estado = tk.Label(frame_principal, text="Listo para iniciar la prueba",
                                        font=("Helvetica", 12), bg="#f0f0f0", fg="#3498db")
        self.etiqueta_estado.pack(pady=5)

        self.barra_progreso = ttk.Progressbar(frame_principal, orient="horizontal",
                                              length=400, mode="determinate")
        self.barra_progreso.pack(pady=10)

        self.etiqueta_descarga = tk.Label(frame_principal, text="Velocidad de descarga: --- Mbps",
                                          font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_descarga.pack()

        self.etiqueta_subida = tk.Label(frame_principal, text="Velocidad de subida: --- Mbps",
                                        font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_subida.pack()

        self.etiqueta_ping = tk.Label(frame_principal, text="Latencia (ping): --- ms",
                                      font=("Helvetica", 12), bg="#f0f0f0")
        self.etiqueta_ping.pack()
        
        self.etiqueta_servidor = tk.Label(frame_principal, text="Servidor: ---",
                                          font=("Helvetica", 12), bg="#f0f0f0", fg="#2c3e50")
        self.etiqueta_servidor.pack()

        self.boton_iniciar = ttk.Button(frame_principal, text="Iniciar Prueba",
                                        command=self.iniciar_prueba)
        self.boton_iniciar.pack(pady=10)

        self.boton_reiniciar = ttk.Button(frame_principal, text="Volver a hacer la prueba",
                                          command=self.reiniciar_prueba)
        self.boton_reiniciar.pack(pady=10)
        self.boton_reiniciar.config(state=tk.DISABLED)

        # Crear el gráfico de barras
        self.figura, self.ax = plt.subplots(figsize=(5, 3))
        self.barras = self.ax.bar(["Descarga", "Subida", "Ping"], [0, 0, 0], color=['blue', 'green', 'red'])
        self.ax.set_ylabel("Velocidad (Mbps) / Latencia (ms)")
        self.ax.set_ylim(0, 100)
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_principal)
        self.canvas.get_tk_widget().pack()

    def actualizar_progreso(self, etapa, mensaje):
        progreso = (etapa / self.etapas_totales) * 100
        self.barra_progreso["value"] = progreso
        self.etiqueta_estado.config(text=mensaje)
        self.ventana.update()
    
    def medir_velocidad(self):
        try:
            self.boton_iniciar.config(state=tk.DISABLED, text="Ejecutando...")
            self.etiqueta_estado.config(text="Iniciando prueba...", fg="#3498db")
            self.barra_progreso["value"] = 0
            self.ventana.update()

            st = speedtest.Speedtest()
            
            self.actualizar_progreso(0, "Buscando el mejor servidor...")
            servidor = st.get_best_server()  
            self.etiqueta_servidor.config(text=f"Servidor: {servidor['sponsor']} ({servidor['name']}, {servidor['country']})")
            
            time.sleep(0.5)

            self.actualizar_progreso(1, "Midiendo velocidad de descarga...")
            self.resultados["descarga"] = st.download() / 1_000_000  

            self.actualizar_progreso(2, "Midiendo velocidad de subida...")
            self.resultados["subida"] = st.upload() / 1_000_000  

            self.resultados["ping"] = st.results.ping  
            
            self.barra_progreso["value"] = 100

            self.etiqueta_descarga.config(text=f"Velocidad de descarga: {self.resultados['descarga']:.2f} Mbps")
            self.etiqueta_subida.config(text=f"Velocidad de subida: {self.resultados['subida']:.2f} Mbps")
            self.etiqueta_ping.config(text=f"Latencia (ping): {self.resultados['ping']:.2f} ms")

            self.etiqueta_estado.config(text="Prueba completada con éxito", fg="#27ae60")
            self.boton_reiniciar.config(state=tk.NORMAL)  
            
            self.actualizar_grafica()

        except Exception as e:
            self.etiqueta_estado.config(text=f"Error: {str(e)}", fg="#e74c3c")
        finally:
            self.boton_iniciar.config(state=tk.NORMAL, text="Iniciar Prueba")

    def actualizar_grafica(self):
        valores = [self.resultados['descarga'], self.resultados['subida'], self.resultados['ping']]
        for barra, valor in zip(self.barras, valores):
            barra.set_height(valor)
        self.ax.set_ylim(0, max(valores) + 10)
        self.canvas.draw()

    def iniciar_prueba(self):
        hilo = threading.Thread(target=self.medir_velocidad, daemon=True)
        hilo.start()

    def reiniciar_prueba(self):
        self.etiqueta_estado.config(text="Listo para iniciar la prueba", fg="#3498db")
        self.barra_progreso["value"] = 0
        self.etiqueta_descarga.config(text="Velocidad de descarga: --- Mbps")
        self.etiqueta_subida.config(text="Velocidad de subida: --- Mbps")
        self.etiqueta_ping.config(text="Latencia (ping): --- ms")
        self.etiqueta_servidor.config(text="Servidor: ---")
        self.boton_reiniciar.config(state=tk.DISABLED)  
        self.boton_iniciar.config(state=tk.NORMAL)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = MedidorVelocidad(ventana)
    ventana.mainloop()