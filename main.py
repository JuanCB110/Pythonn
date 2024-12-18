from Automatas.APalabras_Reservadas import validar_palabra_reservada
from Automatas.AEnteros import validar_numero_entero
from Automatas.ADecimales import validar_numero_decimal
from Automatas.AOperadorLogico import validar_operador_logico
from Automatas.AVariables import validar_variable
from Automatas.AAsignacion import validar_operador_asignacion
from Automatas.AAritmeticos import validar_operador_aritmetico
from Automatas.ARelacionales import validar_operador_relacional
from Tarea1 import PreprocesarArchivo, RecorrerArchivo
import sys
import os
__all__ = ['analizar_codigo']
from analizador_sintactico import AnalizadorSintactico

# Delimitadores definidos dinámicamente
DELIMITADORES = {'(': 'Paréntesis Izquierdo', ')': 'Paréntesis Derecho',
                ';': 'Punto y Coma', '=': 'Operador de Asignación'}

# Agregar al final de la función de separar_tokens
def separar_tokens(linea):
    """
    Divide una línea de código en una lista de tokens.
    """
    tokens = []
    token = ""
    delimitadores = list(DELIMITADORES.keys()) + ['+', '-', '*', '/', '%']
    
    i = 0
    while i < len(linea):
        caracter = linea[i]
        
        # Si es un delimitador
        if caracter in delimitadores:
            if token:
                tokens.append(token)
                token = ""
            tokens.append(caracter)
        # Si es un espacio
        elif caracter == " ":
            if token:
                tokens.append(token)
                token = ""
        # Si es un número
        elif caracter.isdigit():
            if token:
                token += caracter
            else:
                # Consumir todo el número
                numero = caracter
                j = i + 1
                while j < len(linea) and linea[j].isdigit():
                    numero += linea[j]
                    j += 1
                tokens.append(numero)
                i = j - 1
        else:
            token += caracter
        
        i += 1

    if token:
        tokens.append(token)

    # Aquí es donde capturamos errores léxicos
    for token in tokens:
        if token not in VALIDADORES.keys() and not token.isdigit() and not token in delimitadores:
            print(f"Error Léxico: El token '{token}' no es reconocido")

    return tokens


# Diccionario de validadores
VALIDADORES = {
    'Palabra Reservada': validar_palabra_reservada,
    'Numero Entero': validar_numero_entero,
    'Numero Decimal': validar_numero_decimal,
    'Operador Logico': validar_operador_logico,
    'Variable': validar_variable,
    'Asignacion': validar_operador_asignacion,
    'Aritmetico': validar_operador_aritmetico,
    'Operador Relacional' : validar_operador_relacional
}

# Función para analizar el código
def analizar_codigo(codigo):
    """
    Analiza el código línea por línea, generando una lista de tokens clasificados.
    """
    tokens = []
    numero_linea = 1

    for linea in codigo:
        linea = linea.strip()
        if not linea:  # Saltar líneas vacías
            continue

        palabras = separar_tokens(linea)

        for palabra in palabras:
            match palabra:
                case ";":
                    tokens.append((palabra, "Punto y Coma"))
                case "+" | "-" | "*" | "/" | "(" | ")":
                    tokens.append((palabra, "Aritmetico"))
                case "=":
                    tokens.append((palabra, "Asignacion"))
                case _ if validar_numero_entero(palabra):
                    tokens.append((palabra, "Numero Entero"))
                case _ if validar_numero_decimal(palabra):
                    tokens.append((palabra, "Numero Decimal"))
                case _ if validar_variable(palabra):
                    tokens.append((palabra, "Variable"))
                case _ if validar_palabra_reservada(palabra):
                    tokens.append((palabra, "Palabra Reservada"))
                case _ if validar_operador_relacional(palabra):
                    tokens.append((palabra, "Operador Relacional"))
                case _:
                    tokens.append((palabra, "Desconocido"))

    return tokens


# Función principal
def main():
    """
    Función principal: Preprocesa el archivo, analiza el código, y genera tokens clasificados.
    """
    # Preprocesamos el archivo y lo guardamos en codigo.txt
    ruta_original = 'complicado.txt'
    ruta_preprocesada = 'codigo.txt'

    PreprocesarArchivo(ruta_original, ruta_preprocesada)
    RecorrerArchivo(ruta_preprocesada)  # Esto guarda en codigo.txt

    # Leemos el archivo preprocesado
    with open(ruta_preprocesada, 'r') as archivo:
        codigo = archivo.readlines()

    # Analizamos el código
    tokens = analizar_codigo(codigo)
    
    # Guardamos solo tokens y análisis sintáctico en output.txt
    with open('output.txt', 'w') as archivo_salida:
        sys.stdout = archivo_salida
        
        print("=== ANALISIS LEXICO ===\n")
        linea_actual = 1
        for i, (token, tipo) in enumerate(tokens, 1):
            if token not in ["\n", ";"]:
                print(f"[Linea {linea_actual}] Token: {token}, Tipo: {tipo}")
            if token == ";":
                linea_actual += 1
                print()

        print("\nAnalisis Sintactico:")
        analizador = AnalizadorSintactico(tokens)
        arboles = analizador.analizar()
        
        for i, arbol in enumerate(arboles, 1):
            print(f"\nArbol {i}:")
            arbol.mostrar()

    # Restauramos la salida estándar
    sys.stdout = sys.__stdout__
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
    os.system('cls' if os.name == 'nt' else 'clear')
