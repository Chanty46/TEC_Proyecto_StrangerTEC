# main.py (MicroPython)
import network
import socket
import time
from machine import Pin

SSID = "RedSanti" #No debe tener caracteres especiales
PASSWORD = "ce1234ce"

led = Pin(1, Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Conectando a WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConectado:", wlan.ifconfig())
    return wlan.ifconfig()[0]

def start_server(ip):
    s = socket.socket()
    s.bind((ip, 1717))
    s.listen(1)
    print("Esperando conexión del cliente...")
    conn, addr = s.accept()
    print("Conectado desde:", addr)
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = data.decode()
        print("Mensaje recibido:", msg)
        
        # Acciones según el mensaje
        if msg == "LED_ON":
            led.value(1)
            conn.send("LED encendido".encode())
        elif msg == "LED_OFF":
            led.value(0)
            conn.send("LED apagado".encode())
        else:
            # Enviar eco de vuelta
            conn.send(f"Echo: {msg}".encode())

ip = connect_wifi()
start_server(ip)
