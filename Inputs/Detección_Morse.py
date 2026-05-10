import time
from machine import Pin

boton = Pin(17, Pin.IN, Pin.PULL_DOWN)

UNIDAD = 200
FIN_MENSAJE = 5000
DEBOUNCE = 50
morse = []

def leer_morse():

    simbolo_actual = []
    
    while True: 
        inicio_silencio = time.ticks_ms() #Contar cuanto tiempo el boton no se esta presionando
        
        while boton.value() == 0: 
            silencio = time.ticks_diff(time.ticks_ms(), inicio_silencio)
            if silencio >= FIN_MENSAJE:
                print("Fin del mensaje")
                return morse
        
        # El debounce se pone para evitar el ruido entre señales ya que al probar el codigo no nos funcionaba
        # Debounce al presionar 
        time.sleep_ms(DEBOUNCE)
        if boton.value() == 0:  # si ya se soltó era rebote, ignorar
            continue
            
        inicio_presion = time.ticks_ms()
        while boton.value() == 1:
            pass
            
        # Debounce al soltar
        time.sleep_ms(DEBOUNCE)
        
        duracion = time.ticks_diff(time.ticks_ms(), inicio_presion)
        
        # Comparacion contra la unidad para reconocer la duracion de la presion del boton
        if duracion < UNIDAD * 2:
            simbolo_actual.append(".")
            print("Punto")
        else:
            simbolo_actual.append("-")
            print("Raya")
        
        inicio_silencio = time.ticks_ms()
        while boton.value() == 0:
            silencio = time.ticks_diff(time.ticks_ms(), inicio_silencio)
            if silencio >= UNIDAD * 3:
                letra += ["".join(simbolo_actual)]
                morse.append(letra)
                print("Letra:", letra)
                simbolo_actual = []
                break
            
leer_morse()