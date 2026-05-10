import random 
import morse_code 
import tkinter as tk
from tkinter import messagebox
from morse_code import *

"""
NOTA

Esta progra tiene un avance en la logica del juego #1, pero hay que cambiar el sistema de entradas por el boton de la maqueta, simplemente lo hago con Labels para ir probando 
la lógica del juego 

"""


#Variables 
puntos_jugador = 0 
multiplicador_ronda = 1
palabra_a_jugar = ""
frases = ["SOS", "SI", "NO", "HOLA", "TEC", "COMPUTADORES", "CE1104", "TKINTER", "STRANGER", "THINGS"] #Se puede guardar como una matriz, para ronda 1, ronda 2 y ronda 3 para ver puntos por dificultad

#Para obtener saber como usar el random, use este video de referencia https://www.youtube.com/watch?v=5TPsqSScEdg

#Jugabilidad básica
#__________________________________________________________________________________

#Funciones al comprobar la palabra

def frase_random(): # Se hace una funcion para poder llamarla más despues
    global palabra_a_jugar, palabra_a_jugar_label
    palabra_a_jugar = random.choice(frases)
    try :
        palabra_a_jugar_label.config(text= f"La nueva palabra es {palabra_a_jugar}")
    except:
        pass #Si no existe, pues nada

def cambio_ronda():
    global multiplicador_ronda, ronda_actual_label
    multiplicador_ronda += 1 
    ronda_actual_label.config(text=f"Ronda Actual: {multiplicador_ronda}, obtendras este multiplicador por cada letra correcta")

def obtener_entrada():
    entrada = entry_palabra_jugador.get()
    lista_entrada = entrada.split(" ")
    return lista_entrada

def actualizar_puntos():
    global puntos_jugador, puntos_jugador_label
    puntos_jugador_label.config(text= f"Puntos Actuales: {puntos_jugador}")

def revisar_rondas():
    global multiplicador_ronda, puntos_jugador
    if multiplicador_ronda == 4: #Si fuera igual a 3, solo nos dejaria jugar una ronda
        messagebox.showinfo("Resultado de la Partida", f"Bien Hecho, has obtenido{puntos_jugador}") 
        reset_game()

def reset_game():
    global multiplicador_ronda, puntos_jugador
    puntos_jugador = 0
    multiplicador_ronda -= 0
    cambio_ronda()
    actualizar_puntos()

# Funcion principal del juego

def comparar_entrada(entrada): #Por el momento será una entrada de teclado, toca rework para hacer funcionar el boton de la rasp.r
    global puntos_jugador, palabra_a_jugar 
    letras_correctas = []
    palabra_correcta = palabra_a_morse(palabra_a_jugar) #Vamos a traducir una frase a morse para hacer la comparacion, pero de todas maneras se puede hacer igual.
    puntos_ronda = 0 #Estos puntos no es necesario guardarlos

    for i in range(min(len(entrada), len(palabra_correcta))): #Basicamente, se toma el que tenga la longitud minima entre los dos, entonces plantea lo siguiente : Si el jugador no logra completar la palabra, se le dan puntos por intentar, Si el jugador excede la palabra, simplemente se evita un error y no se dan puntos extra por letras incorrectas
        if entrada[i] == palabra_correcta[i]:
            puntos_ronda += len(entrada[i]) * multiplicador_ronda #Sumar la cantidad de caracteres en el morse, cuestión de balancear las palabras correctas o incorrectas
            letras_correctas.append(morse_a_letra(entrada[i]))
            
    puntos_jugador += puntos_ronda

    messagebox.showinfo("Resultado", f"Resultado de la Ronda \n Letras Correctas: {letras_correctas}\nPuntos Obtenidos: {puntos_ronda}\n Ronda Jugada: {multiplicador_ronda}") 
    frase_random() #Cambiar la palabra
    cambio_ronda() #Cambiar la ronda
    actualizar_puntos() #Actualizar el label de los puntos
    revisar_rondas() #Sirve para reiniciar el juego
    


#Root
#_____________________________________________________________________________________
root = tk.Tk()
root.geometry(f"{800}x{600}")
root.title("Prueba de Juego 1")

boton = tk.Button(text="Juego", command=lambda:(ventana2(), frase_random())) # Los multiples comandos van en una tupla
boton.pack()

#Ventana TopLevel
#_______________________________________________________________________________________
def ventana2():
    global palabra_a_jugar, palabra_a_jugar_label, entry_palabra_jugador, puntos_jugador_label, ronda_actual_label
    ventana2 = tk.Toplevel()
    ventana2.geometry(f"{1000}x{800}")
    ventana2.title("TopLevel")
    ventana2.grab_set()#evita que toquemos otras ventanas del programa
    ventana2.focus()#Enfoca la ventana toplevel
    ventana2.resizable(False, False)#No va a permitir cambiar el tamaño de la ventana

    palabra_a_jugar_label = tk.Label(ventana2, text=f"La palabra es{palabra_a_jugar}")
    palabra_a_jugar_label.pack()

    entry_palabra_jugador = tk.Entry(ventana2)
    entry_palabra_jugador.pack() 
    
    boton_juego = tk.Button(ventana2, text="Confirmar Entrada", command= lambda: comparar_entrada(obtener_entrada()))
    boton_juego.pack()

    ronda_actual_label = tk.Label(ventana2, text=f"Ronda Actual: {multiplicador_ronda}, obtendras este multiplicador por cada letra correcta")
    ronda_actual_label.pack()

    puntos_jugador_label = tk.Label(ventana2, text=f"Puntos Actuales: {puntos_jugador}")
    puntos_jugador_label.pack()


#Main Loop()
#__________________________________________________________________________________________
root.mainloop()

"""
Nota, ver nombres, guardar highscores, etc.
"""