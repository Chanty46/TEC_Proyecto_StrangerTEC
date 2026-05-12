# main.py (MicroPython)
import network
import socket
import time
import select
from machine import Pin

# --- CONFIGURACIÓN DE PINES ---
# Importante activar el PULL_DOWN interno para estos componentes
boton_morse = Pin(15, Pin.IN, Pin.PULL_DOWN) 
switch_modo = Pin(14, Pin.IN, Pin.PULL_DOWN) 

# --- VARIABLES DE ESTADO NO BLOQUEANTES ---
# WiFi
SSID = "RedSanti"
PASSWORD = "ce1234ce"
PORT = 1717

# Lógica del Botón
UNIDAD = 200 # ms
inicio_presion = 0
inicio_silencio = 0
estado_boton_ant = 0
simbolo_actual = ""

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando WiFi...", end="")
    while not wlan.isconnected():
        pass # Aquí si es válido esperar porque no ha arrancado el juego
    print("\nIP Lista:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

def iniciar_servidor_async(ip):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, PORT))
    s.listen(1)
    
    # Configuramos el poller para no bloquear el procesador esperando WiFi
    poller = select.poll()
    poller.register(s, select.POLLIN)
    return s, poller

# Conectar e inicializar
ip_local = connect_wifi()
server_sock, poller = iniciar_servidor_async(ip_local)

print("Sistema listo. Mueve el switch o presiona el botón.")
cliente_sock = None
ultimo_estado_switch = switch_modo.value()

# EL LOOP PRINCIPAL DE LA MÁQUINA DE ESTADOS
while True:
    # 1. REVISAR SWITCH (Sin trabar el ciclo)
    estado_actual_switch = switch_modo.value()
    if estado_actual_switch != ultimo_estado_switch:
        if estado_actual_switch == 1:
            print(">>> MODO SONIDO ACTIVADO")
        else:
            print(">>> MODO LUCES ACTIVADO")
        ultimo_estado_switch = estado_actual_switch

    # 2. REVISAR BOTÓN MORSE (Sin usar sleep)
    estado_boton = boton_morse.value()
    tiempo_actual = time.ticks_ms()
    
    # Si acaba de presionar (Flanco de subida)
    if estado_boton == 1 and estado_boton_ant == 0:
        inicio_presion = tiempo_actual
        
    # Si acaba de soltar (Flanco de bajada)
    elif estado_boton == 0 and estado_boton_ant == 1:
        duracion = time.ticks_diff(tiempo_actual, inicio_presion)
        inicio_silencio = tiempo_actual # Empieza a contar el espacio
        
        # Validar si fue punto o raya
        if duracion > 20: # Debounce mínimo de 20ms
            if duracion < UNIDAD * 2:
                simbolo_actual += "."
                print("Punto", end=" ")
            else:
                simbolo_actual += "-"
                print("Raya", end=" ")
    
    # Procesar silencio (Si soltó y pasó suficiente tiempo)
    if estado_boton == 0 and simbolo_actual != "":
        silencio = time.ticks_diff(tiempo_actual, inicio_silencio)
        if silencio >= UNIDAD * 3: # Fin de letra
            print(f"\nLetra armada: {simbolo_actual}")
            # Si hay una compu conectada, enviarle el dato
            if cliente_sock:
                try:
                    cliente_sock.send(f"MORSE:{simbolo_actual}".encode())
                except:
                    pass
            simbolo_actual = "" # Resetear para la siguiente letra
            
    estado_boton_ant = estado_boton

    # 3. REVISAR WIFI (Non-blocking)
    # Revisa si hay eventos de red con 0ms de espera
    eventos = poller.poll(0) 
    for sock, ev in eventos:
        if sock == server_sock:
            # Nuevo cliente se conectó
            cliente_sock, addr = server_sock.accept()
            print("\nPC Conectada desde:", addr)
            poller.register(cliente_sock, select.POLLIN)
        elif sock == cliente_sock:
            # El cliente nos mandó un mensaje (probablemente la frase aleatoria)
            try:
                data = cliente_sock.recv(1024)
                if data:
                    mensaje = data.decode()
                    print("\nCompu dice:", mensaje)
                    # Acá meterías la lógica del registro de corrimiento para encender los LEDs
            except:
                poller.unregister(cliente_sock)
                cliente_sock.close()
                cliente_sock = None
                print("PC Desconectada")

    # Pequeña pausa para no quemar el procesador al 100% (No afecta la lectura)
    time.sleep_ms(5)