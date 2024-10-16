# Importamos los autómatas desde los archivos correspondientes
from Automatas.APalabras_Reservadas import validar_palabra_reservada
from Automatas.AEnteros import validar_numero_entero
from Automatas.ADecimales import validar_numero_decimal
from Automatas.AOperadorLogico import validar_operador_logico
from Automatas.AVariables import validar_variable
from Automatas.AAsignacion import validar_operador_asignacion
from Automatas.AAritemticos import validar_operador_aritmetico
from Tarea1 import PreprocesarArchivo, RecorrerArchivo
import sys

# Función para dividir el contenido del archivo en tokens
def separar_tokens(linea):
    tokens = []
    token = ""

    for caracter in linea:
        if caracter in " =+-*/();":  # Si encontramos un delimitador
            if token:  # Agregar el token acumulado si no está vacío
                tokens.append(token)
                token = ""  # Reiniciar el token acumulado
            if caracter != " ":  # No añadir espacios vacíos
                tokens.append(caracter)  # Agregar el delimitador como token
        else:
            token += caracter  # Acumular caracteres en el token

    if token:  # Agregar el último token si existe
        tokens.append(token)

    return tokens


def analizar_codigo(codigo):
    tokens = []
    
    for linea in codigo:
        palabras = separar_tokens(linea)
        
        for palabra in palabras:
            if validar_palabra_reservada(palabra):
                tokens.append((palabra, 'Palabra Reservada'))
            elif validar_numero_entero(palabra):
                tokens.append((palabra, 'Numero Entero'))
            elif validar_numero_decimal(palabra):
                tokens.append((palabra, 'Numero Decimal'))
            elif validar_operador_logico(palabra):
                tokens.append((palabra, 'Operador Logico'))
            elif validar_variable(palabra):
                tokens.append((palabra, 'Variable'))
            elif validar_operador_asignacion(palabra):
                tokens.append((palabra, 'Asignacion'))
            elif validar_operador_aritmetico(palabra):
                tokens.append((palabra, 'Aritmetico'))
            else:
                tokens.append((palabra, 'Desconocido'))

    return tokens

# Función principal
def main():

    # Contador de tokens
    cont = 0

    #Preprocesamos el archivo
    PreprocesarArchivo('C:\\Pythonn\\miprograma.txt', 'C:\\Pythonn\\codigo.txt')
    ruta = 'C:\\Pythonn\\miprograma.txt'
    RecorrerArchivo(ruta)

    if RecorrerArchivo:
        # Leemos el archivo de texto
        with open('codigo.txt', 'r') as archivo:
            codigo = archivo.readlines()

        # Analizamos el código
        tokens = analizar_codigo(codigo)
    
        # Mostramos los tokens en la terminal
        for token, tipo in tokens:
            cont = cont + 1
            if token != "\n" and token != ";":
                print(f"Token: {cont}, Nombre: {token}, Tipo: {tipo}")

if __name__ == "__main__":
    
    # Redirige la salida estándar a un archivo
    with open('output.txt', 'w') as file:
        sys.stdout = file
        main()
