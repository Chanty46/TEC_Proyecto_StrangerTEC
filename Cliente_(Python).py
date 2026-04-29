# cliente_gui.py
import socket
import threading
import tkinter as tk
import morse_code as morse
import random # Se usa para generar frases aleatorias

SERVER_IP = "192.168.173.78"  # Cambia esto con la IP de la Pico W
PORT = 1717

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""

░█████╗░░█████╗░███╗░░██╗███████╗██╗░░██╗██╗░█████╗░███╗░░██╗  ░██╗░░░░░░░██╗██╗░░░░░░███████╗██╗
██╔══██╗██╔══██╗████╗░██║██╔════╝╚██╗██╔╝██║██╔══██╗████╗░██║  ░██║░░██╗░░██║██║░░░░░░██╔════╝██║
██║░░╚═╝██║░░██║██╔██╗██║█████╗░░░╚███╔╝░██║██║░░██║██╔██╗██║  ░╚██╗████╗██╔╝██║█████╗█████╗░░██║
██║░░██╗██║░░██║██║╚████║██╔══╝░░░██╔██╗░██║██║░░██║██║╚████║  ░░████╔═████║░██║╚════╝██╔══╝░░██║
╚█████╔╝╚█████╔╝██║░╚███║███████╗██╔╝╚██╗██║╚█████╔╝██║░╚███║  ░░╚██╔╝░╚██╔╝░██║░░░░░░██║░░░░░██║
░╚════╝░░╚════╝░╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝╚═╝░╚════╝░╚═╝░░╚══╝  ░░░╚═╝░░░╚═╝░░╚═╝░░░░░░╚═╝░░░░░╚═╝
"""

def connect():
    try:
        client_socket.connect((SERVER_IP, PORT))
        threading.Thread(target=receive_messages, daemon=True).start()
        status_label.config(text="Conectado al servidor")
    except Exception as e:
        status_label.config(text=f"Error: {e}")

def send_message():
    msg = entry.get()
    if msg:
        client_socket.send(msg.encode())
        entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            text_area.insert(tk.END, f"Raspberry: {msg}\n")
        except:
            break

def salir():
    try:
        client_socket.close()
    except:
        pass
    root.destroy()

"""

██╗░░░░░░█████╗░░██████╗░██╗░█████╗░░█████╗░  ░░░░░██╗██╗░░░██╗███████╗░██████╗░░█████╗
██║░░░░░██╔══██╗██╔════╝░██║██╔══██╗██╔══██╗  ░░░░░██║██║░░░██║██╔════╝██╔════╝░██╔══██╗
██║░░░░░██║░░██║██║░░██╗░██║██║░░╚═╝███████║  ░░░░░██║██║░░░██║█████╗░░██║░░██╗░██║░░██║
██║░░░░░██║░░██║██║░░╚██╗██║██║░░██╗██╔══██║  ██╗░░██║██║░░░██║██╔══╝░░██║░░╚██╗██║░░██║
███████╗╚█████╔╝╚██████╔╝██║╚█████╔╝██║░░██║  ╚█████╔╝╚██████╔╝███████╗╚██████╔╝╚█████╔╝
╚══════╝░╚════╝░░╚═════╝░╚═╝░╚════╝░╚═╝░░╚═╝  ░╚════╝░░╚═════╝░╚══════╝░╚═════╝░░╚════╝
"""

frases = ["SOS", "SI", "NO", "HOLA", "TEC", "COMPUTADORES", "CE1104", "TKINTER", "STRANGER", "THINGS"]
#Para obtener saber como usar el random, use este video de referencia https://www.youtube.com/watch?v=5TPsqSScEdg

def frase_random(): # Se hace una funcion para poder llamarla más despues
    frase_random = random.choice(frases) #Esto nos da una nueva frase cada vez que se usa
    return frase_random 

"""

░██████╗░██╗░░░██╗██╗
██╔════╝░██║░░░██║██║
██║░░██╗░██║░░░██║██║
██║░░╚██╗██║░░░██║██║
╚██████╔╝╚██████╔╝██║
░╚═════╝░░╚═════╝░╚═╝
"""
root = tk.Tk()
root.title("Cliente GUI")

entry = tk.Entry(root, width=50)
entry.pack()

send_btn = tk.Button(root, text="Enviar", command=send_message)
send_btn.pack()

text_area = tk.Text(root, height=10, width=60)
text_area.pack()

status_label = tk.Label(root, text="Desconectado")
status_label.pack()

salir_btn = tk.Button(root, text="Salir", command=salir)
salir_btn.pack()

connect()
root.mainloop()
