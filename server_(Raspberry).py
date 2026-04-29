# # main.py (MicroPython)
# import network
# import socket
# import time
# from machine import Pin

# SSID = "RedSanti" #No debe tener caracteres especiales
# PASSWORD = "ce1234ce"

# led = Pin(1, Pin.OUT)

# def connect_wifi():
#     wlan = network.WLAN(network.STA_IF)
#     wlan.active(True)
#     wlan.connect(SSID, PASSWORD)
    
#     print("Conectando a WiFi...", end="")
#     while not wlan.isconnected():
#         print(".", end="")
#         time.sleep(0.5)
#     print("\nConectado:", wlan.ifconfig())
#     return wlan.ifconfig()[0]

# def start_server(ip):
#     s = socket.socket()
#     s.bind((ip, 1717))
#     s.listen(1)
#     print("Esperando conexión del cliente...")
#     conn, addr = s.accept()
#     print("Conectado desde:", addr)
    
#     while True:
#         data = conn.recv(1024)
#         if not data:
#             break
#         msg = data.decode()
#         print("Mensaje recibido:", msg)
        
#         # Acciones según el mensaje
#         if msg == "LED_ON":
#             led.value(1)
#             conn.send("LED encendido".encode())
#         elif msg == "LED_OFF":
#             led.value(0)
#             conn.send("LED apagado".encode())
#         else:
#             # Enviar eco de vuelta
#             conn.send(f"Echo: {msg}".encode())

# ip = connect_wifi()
# start_server(ip)


"""
Código de Talleres Vistos en Clase 



#________________________________________________________________________________________________________________________________________________________________________
Registro de Corrimiento

import machine
from time import sleep

# Configuración de pines
pinEntradaAB = machine.Pin(14, machine.Pin.OUT)  # Pin GPIO 16 para A/B
pinClock = machine.Pin(15, machine.Pin.OUT)  # Pin GPIO 17 para el clock

#Secuencia que se envia al registro 
pinEntradaAB.value(1)
pinClock.value(1)      
pinClock.value(0)


'''Explicación: este código permite ver el compartamiento del registro de corrimiento.
Cada vez que se ejecute, el registro guardará el valor de 'pinEntradaAB', ya sea 1 o 0 
y desplazará los valores antes guardados '''

#________________________________________________________________________________________________________________________________________________________________________

import machine
import time

AB = machine.Pin(14, machine.Pin.OUT)
CLK = machine.Pin(15, machine.Pin.OUT)

secuencia0 = [1,0,0,0,0,0,0,0]
secuencia1 = [0,1,1,0,0,1,1,0]

def EjecutarSecuencia(secuencia):
    for i in range(8):  
        bit = secuencia[7-i]  # tomar los valores de derecha a izquiera
        AB(bit)                 
        CLK(1)                          
        CLK(0)
        
EjecutarSecuencia(secuencia0)
time.sleep (2)


'''Con la función EjecutarSecuencia es posible mostrar al registro la secuencia que
se necesite, solo se deben definir en una lista y llamar a la función'''
"""