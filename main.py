from Automatas.APalabras_Reservadas import validar_palabra_reservada
from Automatas.AEnteros import validar_numero_entero
from Automatas.ADecimales import validar_numero_decimal
from Automatas.AOperadorLogico import validar_operador_logico
from Automatas.AVariables import validar_variable
from Automatas.AAsignacion import validar_operador_asignacion
from Automatas.AAritmeticos import validar_operador_aritmetico
from Tarea1 import PreprocesarArchivo, RecorrerArchivo
import sys

# Delimitadores definidos dinámicamente
DELIMITADORES = {'(': 'Paréntesis Izquierdo', ')': 'Paréntesis Derecho',
                ';': 'Punto y Coma', '=': 'Operador de Asignación'}

# Función para dividir una línea de código en tokens
def separar_tokens(linea):
    """
    Divide una línea de código en una lista de tokens.

    Parámetros:
        linea (str): Una línea de código fuente.

    Retorna:
        list: Lista de tokens separados.
    """
    tokens = []
    token = ""

    for caracter in linea:
        if caracter in DELIMITADORES.keys():  # Detecta delimitadores dinámicamente
            if token:
                tokens.append(token)
                token = ""
            tokens.append(caracter)
        elif caracter == " ":
            if token:
                tokens.append(token)
                token = ""
        else:
            token += caracter

    if token:
        tokens.append(token)

    return tokens

# Diccionario de validadores
VALIDADORES = {
    'Palabra Reservada': validar_palabra_reservada,
    'Número Entero': validar_numero_entero,
    'Número Decimal': validar_numero_decimal,
    'Operador Lógico': validar_operador_logico,
    'Variable': validar_variable,
    'Asignación': validar_operador_asignacion,
    'Aritmético': validar_operador_aritmetico
}

# Función para analizar el código
def analizar_codigo(codigo):
    """
    Analiza el código línea por línea, generando una lista de tokens clasificados.

    Parámetros:
        codigo (list): Lista de líneas de código fuente.

    Retorna:
        list: Lista de tuplas (token, tipo).
    """
    tokens = []
    for linea in codigo:
        palabras = separar_tokens(linea)
        for palabra in palabras:
            for tipo, validador in VALIDADORES.items():
                if validador(palabra):
                    tokens.append((palabra, tipo))
                    break
            else:
                tokens.append((palabra, 'Desconocido'))
    return tokens

# Función principal
def main():
    """
    Función principal: Preprocesa el archivo, analiza el código, y genera tokens clasificados.
    """
    # Redirige la salida estándar a un archivo
    sys.stdout = open('output.txt', 'w')

    # Preprocesamos el archivo
    ruta_original = 'C:\\Pythonn\\miprograma.txt'
    ruta_preprocesada = 'C:\\Pythonn\\codigo.txt'

    PreprocesarArchivo(ruta_original, ruta_preprocesada)
    RecorrerArchivo(ruta_preprocesada)

    # Leemos el archivo preprocesado
    with open(ruta_preprocesada, 'r') as archivo:
        codigo = archivo.readlines()

    # Analizamos el código
    tokens = analizar_codigo(codigo)

    # Mostramos los tokens en la salida
    print("Tokens Analizados:")
    cont = 0
    for token, tipo in tokens:
        cont += 1
        if token not in ["\n", ";"]:
            print(f"Token {cont}: {token}, Tipo: {tipo}")

if __name__ == "__main__":
    main()
