from machine import Pin
import time

# 1. Tienes que definir la variable aquí, en el nivel superior del archivo
switch = Pin(0, Pin.IN)
ultimo_estado = switch.value() 

def selector_gamemode():
    # 2. Ahora sí, global puede encontrar 'ultimo_estado' en este archivo
    global ultimo_estado
    
    print("Selector listo. Cambia la posición para iniciar un modo.")
    
    while True:
        estado_actual = switch.value()
        
        if estado_actual != ultimo_estado:
            if estado_actual == 1:
                print(">>> Cambio detectado: Entrando a MODO DE JUEGO 1")
            else:
                print(">>> Cambio detectado: Entrando a MODO DE JUEGO 2")
                
            ultimo_estado = estado_actual
        
        time.sleep(0.05)