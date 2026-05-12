# main_gui.py
import tkinter as tk
from tkinter import messagebox
import socket
import threading
import random
from morse_logic import palabra_a_morse, morse_a_letra

SERVER_IP = "192.168.0.112"
PORT = 1717

class JuegoStranger:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("StrangerTEC - Control Central")
        
        # Variables de estado (Sin usar 'global')
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.puntos = 0
        self.ronda = 1
        self.frase_actual = ""
        self.frases = ["SOS", "SI", "NO", "HOLA", "TEC", "COMPUTADORES", "CE1104", "TKINTER"]
        
        self.crear_interfaz()
        self.conectar_wifi()

    def crear_interfaz(self):
        # Etiquetas
        self.lbl_estado = tk.Label(self.root, text="Buscando a Will en el Upside Down (Conectando...)", fg="red")
        self.lbl_estado.pack(pady=10)

        self.lbl_ronda = tk.Label(self.root, text=f"Ronda Actual: {self.ronda}")
        self.lbl_ronda.pack()
        
        self.lbl_puntos = tk.Label(self.root, text=f"Puntos: {self.puntos}")
        self.lbl_puntos.pack()

        self.lbl_frase = tk.Label(self.root, text="Frase a jugar: ---", font=("Helvetica", 14, "bold"))
        self.lbl_frase.pack(pady=20)

        # Entrada de texto (Modo Teclado)
        self.entrada_jugador = tk.Entry(self.root, width=50)
        self.entrada_jugador.pack(pady=5)
        
        # Botones
        tk.Button(self.root, text="Siguiente Frase Aleatoria", command=self.nueva_frase).pack(pady=5)
        tk.Button(self.root, text="Comprobar Teclado", command=self.comprobar_entrada).pack(pady=5)
        
        # Consola de mensajes del hardware
        self.consola = tk.Text(self.root, height=10, width=60, state='disabled')
        self.consola.pack(pady=10)

    def conectar_wifi(self):
        try:
            self.socket_cliente.connect((SERVER_IP, PORT))
            self.lbl_estado.config(text="Conexión Establecida con la Maqueta", fg="green")
            # El hilo evita que la interfaz se congele esperando datos
            threading.Thread(target=self.escuchar_maqueta, daemon=True).start()
        except Exception as e:
            self.lbl_estado.config(text=f"Fallo de conexión. Verifica la IP: {e}")

    def escuchar_maqueta(self):
        """ Escucha en segundo plano lo que manda la Pico W """
        while True:
            try:
                msg = self.socket_cliente.recv(1024).decode()
                if msg:
                    self.log_consola(f"Recibido de Maqueta: {msg}")
                    # Aquí podrías inyectar el código para comparar lo que mandó el botón físico
            except:
                self.log_consola("Desconectado de la maqueta.")
                break

    def log_consola(self, texto):
        self.consola.config(state='normal')
        self.consola.insert(tk.END, texto + "\n")
        self.consola.see(tk.END)
        self.consola.config(state='disabled')

    def nueva_frase(self):
        self.frase_actual = random.choice(self.frases)
        self.lbl_frase.config(text=f"Frase a jugar: {self.frase_actual}")
        # Enviar la frase seleccionada a la maqueta por WiFi
        try:
            self.socket_cliente.send(f"FRASE:{self.frase_actual}".encode())
        except Exception as e:
            self.log_consola("Error al enviar la frase a la maqueta.")

    def comprobar_entrada(self):
        entrada = self.entrada_jugador.get().upper().split(" ")
        morse_correcto = palabra_a_morse(self.frase_actual)
        
        puntos_ronda = 0
        letras_acertadas = []
        
        for i in range(min(len(entrada), len(morse_correcto))):
            if entrada[i] == morse_correcto[i]:
                puntos_ronda += 10 * self.ronda
                letras_acertadas.append(morse_a_letra(entrada[i]))
        
        self.puntos += puntos_ronda
        self.lbl_puntos.config(text=f"Puntos: {self.puntos}")
        
        messagebox.showinfo("Resultados", f"Acertaste: {letras_acertadas}\nPuntos obtenidos: {puntos_ronda}")
        
        self.ronda += 1
        self.lbl_ronda.config(text=f"Ronda Actual: {self.ronda}")
        self.entrada_jugador.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoStranger(root)
    root.mainloop()