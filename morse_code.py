"""
Para hacer el diccionario de codigo morse y las funciones de traducción, tome en cuenta el siguiente video : https://www.youtube.com/watch?v=Xa0tgjY6zS0&t=3s 
"""
#Diccionario
#______________________________________________________________________________________________________________________________________________________________________________
# Como el diccionario se va a trabajar solo con mayúsculas, hay que usar .upper() al traducir los mensajes
morseDict_1 = {" ":"/", #Espacio
              "A":".-", "B":"-..." , "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.", "H":"....", "I":"..", "J":".---", "K":"-.-", "L":".-..", 
              "M":"--", "N":"-.", "O":"---", "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T":"-", "U":"..-", "V":"...-", "W":".--","X":"-..-","Y":"-.--",
              "Z":"--..", # Letras
              "1":".----", "2":"..---", "3":"...--", "4":"....-" ,"5":".....","6":"-....","7":"--...","8":"---..","9":"----.","0":"-----" # Numeros
              ,"+":".-.-.","-":"-....-" #Otros signos
              }

morseDict_2 = {"/":" ", #Espacio
              ".-":"A", "-...":"B" , "-.-.":"C", "-..":"D", ".":"E", "..-.":"F", "--.":"G", "....":"H", "..":"I", ".---":"J", "-.-":"K", ".-..":"L", 
              "--":"M", "-.":"N", "---":"O", ".--.":"P", "--.-":"Q", ".-.":"R", "...":"S", "-":"T", "..-":"U", "..-":"V", ".--":"W","-..-":"X","-.--":"Y",
              "--..":"Z", # Letras
              ".----":"1", "..---":"2", "...--":"3", "....-":"4" ,".....":"5","-....":"6","--...":"7","---..":"8","----.":"9","-----":"0" # Numeros
              ,".-.-.":"+","-....-":"-" #Otros signos
              }

#Funciones Traductoras
#______________________________________________________________________________________________________________________________________________________________________________
def palabra_a_morse(msg):
    morseMsg = []
    msg = msg.upper() # Siempre usar el mensaje en todas mayusculas para que nos coincida con el diccionario
    for i in msg:
        morseMsg.append(morseDict_1[i])

    return morseMsg #Devuelve una lista por cuestion de orden con los espacios y para que se la funcion 2 la pueda leer, ya que si no solo lee E y T

def morse_a_letra(msg):
  return morseDict_2[msg]