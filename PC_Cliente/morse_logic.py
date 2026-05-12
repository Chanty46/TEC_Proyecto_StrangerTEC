# morse_logic.py
morseDict_1 = {
    " ":"/", "A":".-", "B":"-...", "C":"-.-.", "D":"-..", "E":".", "F":"..-.", "G":"--.", 
    "H":"....", "I":"..", "J":".---", "K":"-.-", "L":".-..", "M":"--", "N":"-.", "O":"---", 
    "P":".--.", "Q":"--.-", "R":".-.", "S":"...", "T":"-", "U":"..-", "V":"...-", "W":".--",
    "X":"-..-","Y":"-.--", "Z":"--..", 
    "1":".----", "2":"..---", "3":"...--", "4":"....-" ,"5":".....","6":"-....","7":"--...",
    "8":"---..","9":"----.","0":"-----", "+":".-.-.","-":"-....-"
}

# Invertimos el diccionario automáticamente, es más seguro y limpio
morseDict_2 = {v: k for k, v in morseDict_1.items()}

def palabra_a_morse(msg):
    morseMsg = []
    msg = msg.upper()
    for char in msg:
        # El .get() evita errores si el usuario digita un símbolo raro
        morseMsg.append(morseDict_1.get(char, "?")) 
    return morseMsg

def morse_a_letra(msg):
    # Si ingresan un morse inválido, devuelve '?' en vez de crashear
    return morseDict_2.get(msg, "?")