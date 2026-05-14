# main_gui.py
import tkinter as tk
from tkinter import messagebox
import socket
import threading
import random
from morse_logic import palabra_a_morse, morse_a_letra

SERVER_IP = "192.168.0.106"
PORT = 1717

class JuegoStranger:
    def __init__(self, root): 
        self.root = root
        self.root.geometry("800x700")
        self.root.title("StrangerTEC - Central")
        
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea el socket para comunicarse con la Pico W, AF_INET significa el uso IPv4 y sock stream usa TCP
        self.frases = ["SOS", "SI", "NO", "HOLA", "TEC", "JAVA", "PYTHON", "MORSE", "LUZ", "WIFI"]
        self.top_10 = [50, 40, 30, 20, 10] # Tabla de puntajes dummy inicial
        
        # Variables Modo Escucha
        self.puntos_A = 0
        self.puntos_B = 0
        self.ronda = 1
        self.frase_actual = ""
        self.entrada_maqueta = ""
        
        # Variables Modo Simple
        self.nivel_actual = 1
        self.puntos_simple = 0

        # Contenedor principal
        self.contenedor = tk.Frame(self.root) #Seran nuestras distintas ventanas en Frame
        self.contenedor.pack(fill="both", expand=True)

        self.pantalla_menu()
        threading.Thread(target=self.conectar_wifi, daemon=True).start() #Usa un hilo separado para no bloquear la conexión al wifi
                           #Target, funcion que hara el hilo     Daemon, si el programa cierra, este hilo tambien
    def conectar_wifi(self): #Intenta conectarse a la Pico W por socket 
        try:
            self.socket_cliente.settimeout(3.0) # Tiene 3 segundos para conectarse
            self.socket_cliente.connect((SERVER_IP, PORT)) # Ip y puerto a conectar 
            self.socket_cliente.settimeout(None) # Al conectarse, se elimina el time out
            self.lbl_estado_wifi.config(text="WiFi: Conectado a la Maqueta", fg="green") #Actualizar la interfaz grafica
            threading.Thread(target=self.escuchar_maqueta, daemon=True).start() #Usa un hilo separado para no bloquear la interfaz
        except Exception as e:
            self.lbl_estado_wifi.config(text=f"WiFi Falló. ¿Está la Pico prendida?", fg="red") #Error, mostrar label con error de conexion

    def escuchar_maqueta(self):
        while True: #Corre en segundo plano, esperando los mensajes de
            try:
                msg = self.socket_cliente.recv(1024).decode() #Recibe hasta 1024 bytes y los convierte a texto
                if msg.startswith("MORSE:"): #Verifica que el mensaje sea un codigo morse (Juego)
                    codigo = msg.split(":")[1] #Separa el mensaje por : y toma lo segundo
                    letra = morse_a_letra(codigo) #Convierte el codigo Morse a letras
                    self.entrada_maqueta += letra #Lo agrega a la variable de la entrada
                    if hasattr(self, 'consola'): #Verifica que la consola exista antes de escribir en ella, si no daria error (La consola existe solo en ciertos frames)
                        self.log_consola(f"Jugador B ingresó: {letra} ({codigo})") #Si hay consola, se va mostrando que datos dio el jugador
            except:
                break

    def limpiar_pantalla(self):
        for widget in self.contenedor.winfo_children(): #Recorre todos los widgets que existen en el contenedor (nuestro Tk.Frame)
            widget.destroy()#los destruye

    # ===================================================
    # PANTALLA: MENÚ PRINCIPAL
    # ===================================================
    def pantalla_menu(self):
        self.limpiar_pantalla() #Limpiar la pantalla antes de ingresar a esta misma
        tk.Label(self.contenedor, text="StrangerTEC", font=("Arial", 30, "bold"), fg="red").pack(pady=40)
        self.lbl_estado_wifi = tk.Label(self.contenedor, text="Conectando WiFi...", font=("Arial", 12)) #Aqui se define la variable del label del wifi.
        self.lbl_estado_wifi.pack(pady=10) 

        tk.Button(self.contenedor, text="Modo Escucha y Transmisión (Versus)", font=("Arial", 14), width=35, command=self.iniciar_modo_escucha).pack(pady=10) #Cambiar de modo de juego
        tk.Button(self.contenedor, text="Modo Transmisión Simple (Un Jugador)", font=("Arial", 14), width=35, command=self.iniciar_modo_simple).pack(pady=10)

    # ===================================================
    # PANTALLA: MODO TRANSMISIÓN SIMPLE
    # ===================================================
    def iniciar_modo_simple(self):
        self.limpiar_pantalla() 
        self.nivel_actual = 1 #Resetear valores
        self.puntos_simple = 0
        
        tk.Button(self.contenedor, text="← Volver al Menú", command=self.pantalla_menu).pack(anchor="nw", padx=10, pady=10)
        tk.Label(self.contenedor, text="MODO TRANSMISIÓN SIMPLE", font=("Arial", 18, "bold")).pack()
        
        self.lbl_nivel = tk.Label(self.contenedor, text=f"Nivel {self.nivel_actual} de 3", font=("Arial", 14))
        self.lbl_nivel.pack(pady=10)
        
        tk.Button(self.contenedor, text="▶ Enviar Frase a Maqueta", font=("Arial", 12), bg="black", fg="white", command=self.lanzar_frase_simple).pack(pady=10)
        
        tk.Label(self.contenedor, text="¿Qué frase decodificaste?").pack()
        self.entrada_simple = tk.Entry(self.contenedor, width=30, font=("Arial", 14))
        self.entrada_simple.pack(pady=5)
        
        tk.Button(self.contenedor, text="Validar y Avanzar", command=self.validar_simple).pack(pady=10)

    def lanzar_frase_simple(self):
        self.frase_actual = random.choice(self.frases) #Escoge una frase aleatoria 
        try:
            self.socket_cliente.send(f"NIVEL:{self.nivel_actual}:{self.frase_actual}".encode()) #Intenta mandar el mensaje y le hace enconde para mandar en bytes
        except:
            messagebox.showerror("Error", "No hay conexión con la maqueta.")

    def validar_simple(self):
        ingreso = self.entrada_simple.get().upper() #.get obtiene la entrada del jugador .upper ya que el diccionario esta en morse
        puntos = sum(1 for i, c in enumerate(ingreso) if i < len(self.frase_actual) and c == self.frase_actual[i]) #Enumerate nos da el caracter (c) y el indice i a la vez, basicamente se suma los puntos si el indice en el ingreso es menor a la longitud y si el caracter es igual al de esa posicion
        self.puntos_simple += (puntos * 10 * self.nivel_actual) #Calculo de puntos 
        
        if self.nivel_actual < 3:
            messagebox.showinfo("Correcto", f"Era: {self.frase_actual}\n¡Prepárate, va más rápido!")
            self.nivel_actual += 1
            self.lbl_nivel.config(text=f"Nivel {self.nivel_actual} de 3")
            self.entrada_simple.delete(0, tk.END)
        else:
            self.evaluar_top_10() #Se evalua el top 10

    def evaluar_top_10(self):
        self.top_10.append(self.puntos_simple) #Se guardan los puntos simples
        self.top_10.sort(reverse=True) #De Mayor a menor
        self.top_10 = self.top_10[:10] # Mantener solo 10
        
        if self.puntos_simple in self.top_10: #Si nuestro puntaje esta en el top 10
            lugar = self.top_10.index(self.puntos_simple) + 1 #Mostrar la posicion en la lista
            msg = f"¡ENTRASTE AL TOP 10!\nLugar: #{lugar}\nPuntos Totales: {self.puntos_simple} "
        else:
            msg = f"Fin del juego.\nPuntos Totales: {self.puntos_simple}\nNo entraste al Top 10."
            
        messagebox.showinfo("Resultados Finales", msg) 
        self.pantalla_menu() #Al finalizar, se regresa al menu

    # ===================================================
    # PANTALLA: MODO ESCUCHA Y TRANSMISIÓN (El original)
    # ===================================================
    def iniciar_modo_escucha(self):
        self.limpiar_pantalla()
        self.puntos_A = 0
        self.puntos_B = 0
        self.ronda = 1
        
        tk.Button(self.contenedor, text="← Volver al Menú", command=self.pantalla_menu).pack(anchor="nw", padx=10, pady=10)
        
        marco_puntos = tk.Frame(self.contenedor) #Un frame dentro del contenedor principal. Sirve para agrupar los labes de puntos de ambos jugadores uno al lado del otro
        marco_puntos.pack(pady=10)
        self.lbl_pts_A = tk.Label(marco_puntos, text=f"Jugador A (PC): {self.puntos_A} pts", font=("Arial", 12, "bold"))
        self.lbl_pts_A.grid(row=0, column=0, padx=20)
        self.lbl_pts_B = tk.Label(marco_puntos, text=f"Jugador B (Maqueta): {self.puntos_B} pts", font=("Arial", 12, "bold"))
        self.lbl_pts_B.grid(row=0, column=1, padx=20)

        self.lbl_turno = tk.Label(self.contenedor, text="Esperando iniciar...", font=("Arial", 14, "bold"), fg="blue") #Predeterminadamente, espera a iniciar 
        self.lbl_turno.pack(pady=10) #Esta label indicara de quien es el turno

        tk.Button(self.contenedor, text="1. Enviar Frase a Maqueta", bg="black", fg="white", font=("Arial", 12), command=self.nueva_frase_escucha).pack(pady=10) #Este boton envia la frase a la maqueta

        tk.Label(self.contenedor, text="Jugador A: Digite frase").pack()
        self.entrada_jugador = tk.Entry(self.contenedor, width=30, font=("Arial", 14))
        self.entrada_jugador.pack(pady=5)
        
        self.btn_validar_A = tk.Button(self.contenedor, text="2. Validar Turno A", command=self.validar_A_escucha, state='disabled') #Usa varios estados, en este caso empiezan desactivados para forzar un orden de juego
        self.btn_validar_A.pack(pady=5)

        self.btn_validar_B = tk.Button(self.contenedor, text="3. Validar Turno B (Botón Maqueta)", command=self.validar_B_escucha, state='disabled')
        self.btn_validar_B.pack(pady=20)

        self.consola = tk.Text(self.contenedor, height=8, width=60, state='disabled')
        self.consola.pack(pady=10) #Empieza desactivado para que el jugador no pueda escribir en él directamente

    def log_consola(self, texto):
        self.consola.config(state='normal') #Activa la concsola para escribir en ella (lo hara el programa)
        self.consola.insert(tk.END, texto + "\n") #inserta el texto en la consola 
        self.consola.see(tk.END) #Scroll automatico hacia abajo para que siempre se vea el ultimo mensaje
        self.consola.config(state='disabled') #Se desactiva para que no se pueda escribir en ella

    def nueva_frase_escucha(self):
        self.frase_actual = random.choice(self.frases) #Se escoge una palabra aleatorias
        self.entrada_maqueta = "" #Limpia la entrada del jugador B
        self.entrada_jugador.delete(0, tk.END) #Limpiar la entry del Jugador A
        
        self.lbl_turno.config(text=f"TURNO A (PC) - ¡Atento a la maqueta!")
        self.btn_validar_A.config(state='normal')
        self.btn_validar_B.config(state='disabled')
        self.log_consola(f"\n--- RONDA {self.ronda} INICIADA ---")
        
        try: self.socket_cliente.send(f"FRASE:{self.frase_actual}".encode()) #Intenta mandar la frase actual generada al pulsar el boton al empezar la ronda
        except: self.log_consola("Error enviando datos.")

    def validar_A_escucha(self):
        entrada = self.entrada_jugador.get().upper() #Se obtiene la entrada del entry y le hacemos .upper()
        puntos = sum(1 for i, c in enumerate(entrada) if i < len(self.frase_actual) and c == self.frase_actual[i]) #Se recorren los puntos usando la logica
        self.puntos_A += (puntos * 10) #Sumar puntos
        self.lbl_pts_A.config(text=f"Jugador A (PC): {self.puntos_A} pts") #Se muestran los puntos en el label
        messagebox.showinfo("Turno A", f"Original: {self.frase_actual}\nIngresaste: {entrada}")
        
        self.lbl_turno.config(text=f"TURNO B (MAQUETA) - ¡Usa el botón!") #Cambia el turno
        self.btn_validar_A.config(state='disabled') #Desactiva el boton de A porque ya jugo
        self.btn_validar_B.config(state='normal') #Activa el boton de B porque ahora es su turno. 

    def validar_B_escucha(self):
        puntos = sum(1 for i, c in enumerate(self.entrada_maqueta) if i < len(self.frase_actual) and c == self.frase_actual[i])
        self.puntos_B += (puntos * 10)
        self.lbl_pts_B.config(text=f"Jugador B (Maqueta): {self.puntos_B} pts")
        
        ganador = "Jugador A" if self.puntos_A > self.puntos_B else "Jugador B" if self.puntos_B > self.puntos_A else "Empate" #Comoparar los puntos y mostrar un ganador.
        messagebox.showinfo("Fin de Ronda", f"Original: {self.frase_actual}\nBotón ingresó: {self.entrada_maqueta}\n\nLIDERA: {ganador}") #Messagebox al fin del a ronda
        
        self.ronda += 1
        self.lbl_turno.config(text="Fin de ronda.")
        self.btn_validar_B.config(state='disabled')

if __name__ == "__main__": #Solo se ejecuta si se corre el archivo directamente, no si se importa
    root = tk.Tk() #Abrir root
    app = JuegoStranger(root) #Se crea el objeto que es nuestra clase, y se le pasa la ventana root
    root.mainloop() #Main loop.