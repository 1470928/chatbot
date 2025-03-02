import re
import random
import json
from colorama import init, Fore, Style
from prettytable import PrettyTable

# Inicializar colorama
init(autoreset=True)

def cargar_respuestas():
    """Carga el archivo JSON con las respuestas del chatbot."""
    with open("respuestas.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)["respuestas"]

def get_respuesta(entrada, respuestas):
    """Procesa la entrada del usuario y devuelve la mejor respuesta."""
    split_mensaje = re.split(r'\s|[,:;\-?_]\s*', entrada.lower())
    return verifica_todo_msg(split_mensaje, respuestas)

def probabilidad_mensaje(mensaje, palabras_reconocidas, respuesta_simple=False, palabras_requeridas=[]):
    """Calcula la probabilidad de coincidencia entre el mensaje y las palabras clave."""
    certeza_mensaje = sum(1 for palabra in mensaje if palabra in palabras_reconocidas)
    porcentaje = float(certeza_mensaje) / float(len(palabras_reconocidas)) if palabras_reconocidas else 0
    if palabras_requeridas and not all(palabra in mensaje for palabra in palabras_requeridas):
        return 0

    return int(porcentaje * 100) if respuesta_simple or porcentaje > 0 else 0

def verifica_todo_msg(mensaje, respuestas):
    """Verifica cuál respuesta tiene mayor coincidencia con el mensaje del usuario."""
    probabilidad_mayor = {}
    for respuesta in respuestas:
        probabilidad_mayor[respuesta["mensaje"]] = probabilidad_mensaje(
            mensaje,
            respuesta["palabras_clave"],
            respuesta.get("respuesta_simple", False),
            respuesta.get("palabras_requeridas", [])
        )

    mejor_respuesta = max(probabilidad_mayor, key=probabilidad_mayor.get)
    return desconocida() if probabilidad_mayor[mejor_respuesta] < 1 else mejor_respuesta

def desconocida():
    """Responde con un mensaje por defecto si no encuentra coincidencias."""
    return random.choice([
        "Puedes decirlo de nuevo.", "No estoy seguro de lo que quieres.", "¿Podrías aclararlo?", 
        "No tengo información sobre eso."])

def mostrar_menu():
    """Muestra el menú de opciones en colores"""
    print(Fore.CYAN +   "+================================================+")
    print(Fore.YELLOW + "|          Bienvenido a nuestro chatbot          |")
    print(Fore.CYAN +   "|================================================|")
    
    tabla = PrettyTable()
    tabla.field_names = ["Opción", "Pregunta"]
    opciones = [
        ("1", "¿Dónde se encuentra el colegio?"),
        ("2", "¿A qué hora comienzan las clases?"),
        ("3", "¿Qué materias se imparten?"),
        ("4", "¿Cuándo es el examen?"),
        ("5", "¿Necesitas ayuda?"),
        ("6", "¿A qué hora abre y cierra el colegio?"),
        ("7", "¿Cómo me inscribo?"),
        ("8", "¿Cuándo se paga la mensualidad?"),
        ("9", "Salir")
    ]

    for opcion, pregunta in opciones:
        tabla.add_row([Fore.GREEN + opcion + Style.RESET_ALL, pregunta])
    
    print(tabla)

# Cargar respuestas desde JSON
respuestas = cargar_respuestas()

while True:
    mostrar_menu()
    rpta = input(Fore.MAGENTA + "Elige una opción (1-8) o escribe tu pregunta: " + Style.RESET_ALL).strip()

    if rpta == "9":
        print(Fore.RED + "Gracias por consultarnos. ¡Hasta luego!")
        break
    else:
        respuesta = get_respuesta(rpta, respuestas)
        print(Fore.BLUE + "Bot:" + Style.RESET_ALL, respuesta)
