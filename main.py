from Automatas.APalabras_Reservadas import validar_palabra_reservada
from Automatas.AEnteros import validar_numero_entero
from Automatas.ADecimales import validar_numero_decimal
from Automatas.AOperadorLogico import validar_operador_logico
from Automatas.AVariables import validar_variable
from Automatas.AAsignacion import validar_operador_asignacion
from Automatas.AAritmeticos import validar_operador_aritmetico
from Tarea1 import PreprocesarArchivo, RecorrerArchivo
import logging
import sys

# Configuración del logger
logging.basicConfig(filename='errores.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Delimitadores y operadores definidos dinámicamente
DELIMITADORES = {'(': 'Paréntesis Izquierdo', ')': 'Paréntesis Derecho', 
                ';': 'Punto y Coma', '=': 'Asignación'}

# Tabla de símbolos
TABLA_SIMBOLOS = {}

def registrar_error(mensaje):
    """Registra un mensaje de error en el archivo de log."""
    logging.error(mensaje)

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

VALIDADORES = {
    'Palabra Reservada': validar_palabra_reservada,
    'Número Entero': validar_numero_entero,
    'Número Decimal': validar_numero_decimal,
    'Operador Lógico': validar_operador_logico,
    'Variable': validar_variable,
    'Asignación': validar_operador_asignacion,
    'Aritmético': validar_operador_aritmetico
}

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

def manejar_bloques(tokens):
    """
    Verifica la correcta apertura y cierre de bloques en el código.
    
    Parámetros:
        tokens (list): Lista de tuplas (token, tipo).
    """
    pila = []
    for token, tipo in tokens:
        if token == '{':
            pila.append('{')
        elif token == '}':
            if not pila:
                registrar_error("Error: Bloque cerrado sin apertura")
            else:
                pila.pop()
    if pila:
        registrar_error(f"Error: Bloques no cerrados: {len(pila)}")

def agregar_a_tabla_simbolos(nombre, tipo, valor=None):
    """
    Agrega una entrada a la tabla de símbolos.
    
    Parámetros:
        nombre (str): Nombre del símbolo.
        tipo (str): Tipo del símbolo.
        valor (any): Valor asociado al símbolo (opcional).
    """
    TABLA_SIMBOLOS[nombre] = {'tipo': tipo, 'valor': valor}

def imprimir_tabla_simbolos():
    """Imprime la tabla de símbolos en la salida estándar."""
    print("\nTabla de Símbolos:")
    for nombre, datos in TABLA_SIMBOLOS.items():
        print(f"{nombre}: {datos}")

def main():
    """
    Función principal: Preprocesa el archivo, analiza el código, verifica bloques,
    y genera la tabla de símbolos.
    """
    # Redirige la salida estándar a un archivo
    sys.stdout = open('output.txt', 'w')

    # Preprocesamos el archivo
    PreprocesarArchivo('C:\\Pythonn\\miprograma.txt', 'C:\\Pythonn\\codigo.txt')
    ruta = 'C:\\Pythonn\\miprograma.txt'
    RecorrerArchivo(ruta)

    if RecorrerArchivo:
        # Leemos el archivo de texto
        with open('codigo.txt', 'r') as archivo:
            codigo = archivo.readlines()

        # Analizamos el código
        tokens = analizar_codigo(codigo)
        manejar_bloques(tokens)

        # Mostramos los tokens en la terminal y llenamos la tabla de símbolos
        print("Tokens Analizados:")
        cont = 0
        for token, tipo in tokens:
            cont += 1
            if token not in ["\n", ";"]:
                print(f"Token {cont}: {token}, Tipo: {tipo}")
                if tipo == 'Variable':
                    agregar_a_tabla_simbolos(token, tipo)

        # Imprimimos la tabla de símbolos
        imprimir_tabla_simbolos()

if __name__ == "__main__":
    main()
