# main.py (MicroPython)
import network
import socket
import time
import select
from machine import Pin, PWM

# =========================================================
# CONFIGURACIÓN DE PINES
# =========================================================
boton_morse = Pin(15, Pin.IN, Pin.PULL_DOWN)
switch_modo = Pin(14, Pin.IN, Pin.PULL_DOWN)

# ===== 74LS164 =====
dataPin = Pin(27, Pin.OUT)    # A/B del U1
clockPin = Pin(26, Pin.OUT)  # CLK compartido
clockPin.low()
dataPin.low()

# ===== LEDS LATERALES =====
fila0 = Pin(11, Pin.OUT)  # superior
fila1 = Pin(12, Pin.OUT)  # media
fila2 = Pin(13, Pin.OUT)  # inferior
fila0.low()
fila1.low()
fila2.low()

# ===== BUZZER =====
buzzer = PWM(Pin(5))
buzzer.duty_u16(0)

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================
SSID = "Casa Miguel 2.4G"
PASSWORD = "Res20est22"
PORT = 1717

inicio_presion = 0
inicio_silencio = 0
estado_boton_ant = 0
simbolo_actual = ""

morseDict_maqueta = {
    "A":".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.", 
    "H":"....", "I":"..", "J":".---", "K":"-.-", "L":".-..", "M":"--", "N":"-.", "O":"---", 
    "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T":"-", "U":"..-", "V":"...-", "W":".--",
    "X":"-..-","Y":"-.--", "Z":"--..", "0":"-----", "1":".----", "2":"..---", "3":"...--", 
    "4":"....-", "5":".....", "6":"-....", "7":"--...", "8":"---..", "9":"----."
}

mapa_simbolos = {
    "A": (0,0), "B": (1,0), "C": (0,1), "D": (1,1), "E": (0,2), "F": (1,2),
    "G": (0,3), "H": (1,3), "I": (0,4), "J": (1,4), "K": (0,5), "L": (1,5),
    "M": (0,6), "N": (1,6), "O": (0,7), "P": (1,7), "Q": (0,8), "R": (1,8),
    "S": (0,9), "T": (1,9), "U": (0,10), "V": (1,10), "W": (0,11), "X": (1,11),
    "Y": (0,12), "Z": (1,12), "0": (2,0), "1": (2,1), "2": (2,2), "3": (2,3),
    "4": (2,4), "5": (2,5), "6": (2,6), "7": (2,7), "8": (2,8), "9": (2,9)
}

# =========================================================
# FUNCIONES 74LS164
# =========================================================
def pulse():
    clockPin.high()
    time.sleep_us(50)
    clockPin.low()
    time.sleep_us(50)

def apagar_filas():
    fila0.low()
    fila1.low()
    fila2.low()

def limpiar_leds():
    apagar_filas()
    dataPin.low()
    for _ in range(16):
        pulse()

def encender_columna(columna):
    bits = [0] * 16
    bits[columna] = 1
    for bit in reversed(bits):
        dataPin.value(bit)
        pulse()

def mostrar_simbolo(simbolo):
    simbolo = simbolo.upper()
    if simbolo not in mapa_simbolos: return
    fila, columna = mapa_simbolos[simbolo]
    limpiar_leds()
    encender_columna(columna)
    if fila == 0: fila0.high()
    elif fila == 1: fila1.high()
    elif fila == 2: fila2.high()

# =========================================================
# REPRODUCIR FRASE (AHORA ACEPTA VELOCIDAD)
# =========================================================
def reproducir_frase(frase, estado_switch, velocidad_base):
    print(f"\n>>> REPRODUCIENDO: {frase} a {velocidad_base}ms")
    frase = frase.upper()
    for letra in frase:
        if letra == " ":
            time.sleep_ms(velocidad_base * 7)
            continue

        codigo = morseDict_maqueta.get(letra, "")
        for simbolo in codigo:
            if estado_switch == 1:
                buzzer.freq(600)
                buzzer.duty_u16(32768)
            else:
                mostrar_simbolo(letra)

            if simbolo == ".": time.sleep_ms(velocidad_base)
            else: time.sleep_ms(velocidad_base * 3)

            buzzer.duty_u16(0)
            limpiar_leds()
            time.sleep_ms(velocidad_base)

        time.sleep_ms(velocidad_base * 3)

# =========================================================
# WIFI
# =========================================================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Conectando WiFi...", end="")
    while not wlan.isconnected(): pass
    print("\nIP Lista:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

def iniciar_servidor_async(ip):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, PORT))
    s.listen(1)
    poller = select.poll()
    poller.register(s, select.POLLIN)
    return s, poller

# =========================================================
# INICIO Y LOOP PRINCIPAL
# =========================================================
limpiar_leds()
ip_local = connect_wifi()
server_sock, poller = iniciar_servidor_async(ip_local)
print("Sistema listo.")

cliente_sock = None
ultimo_estado_switch = switch_modo.value()
UNIDAD_ESTANDAR = 200

while True:
    estado_actual_switch = switch_modo.value()
    if estado_actual_switch != ultimo_estado_switch:
        if estado_actual_switch == 1: print(">>> MODO SONIDO ACTIVADO")
        else:
            print(">>> MODO LUCES ACTIVADO")
            buzzer.duty_u16(0)
            limpiar_leds()
        ultimo_estado_switch = estado_actual_switch

    estado_boton = boton_morse.value()
    tiempo_actual = time.ticks_ms()

    # Botón Presionado
    if estado_boton == 1 and estado_boton_ant == 0:
        inicio_presion = tiempo_actual
        if estado_actual_switch == 1:
            buzzer.freq(600)
            buzzer.duty_u16(32768)

    # Botón Soltado
    elif estado_boton == 0 and estado_boton_ant == 1:
        buzzer.duty_u16(0)
        duracion = time.ticks_diff(tiempo_actual, inicio_presion)
        inicio_silencio = tiempo_actual

        if duracion > 20:
            if duracion < UNIDAD_ESTANDAR * 2:
                simbolo_actual += "."
                print("Punto", end=" ")
            else:
                simbolo_actual += "-"
                print("Raya", end=" ")

    # Fin de letra
    if estado_boton == 0 and simbolo_actual != "":
        silencio = time.ticks_diff(tiempo_actual, inicio_silencio)
        if silencio >= UNIDAD_ESTANDAR * 3:
            print("\nLetra armada:", simbolo_actual)
            if cliente_sock:
                try: cliente_sock.send(f"MORSE:{simbolo_actual}".encode())
                except: pass
            simbolo_actual = ""
            
    estado_boton_ant = estado_boton

    # Red
    eventos = poller.poll(0)
    for sock, ev in eventos:
        if sock == server_sock:
            cliente_sock, addr = server_sock.accept()
            print("\nPC Conectada desde:", addr)
            poller.register(cliente_sock, select.POLLIN)
        elif sock == cliente_sock:
            try:
                data = cliente_sock.recv(1024)
                if data:
                    mensaje = data.decode().strip().upper()
                    if mensaje.startswith("FRASE:"):
                        frase_juego = mensaje.split(":")[1]
                        reproducir_frase(frase_juego, estado_actual_switch, UNIDAD_ESTANDAR)
                    elif mensaje.startswith("NIVEL:"):
                        # Formato NIVEL:1:HOLA
                        partes = mensaje.split(":")
                        nivel = int(partes[1])
                        frase_juego = partes[2]
                        # Ajustamos la velocidad según el nivel
                        if nivel == 1: vel = 250
                        elif nivel == 2: vel = 150
                        else: vel = 80
                        reproducir_frase(frase_juego, estado_actual_switch, vel)
                    else:
                        print("\nCompu dice:", mensaje)
            except:
                poller.unregister(cliente_sock)
                cliente_sock.close()
                cliente_sock = None
                print("PC Desconectada")

    time.sleep_ms(5)