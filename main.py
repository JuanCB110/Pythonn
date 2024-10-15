# Importamos los autómatas desde los archivos correspondientes
from Automatas.APalabras_Reservadas import validar_palabra_reservada
from Automatas.AEnteros import validar_numero_entero
from Automatas.ADecimales import validar_numero_decimal
from Automatas.AOperadorLogico import validar_operador_logico
from Automatas.AVariables import validar_variable
from Tarea1 import PreprocesarArchivo, RecorrerArchivo

# Función para dividir el contenido del archivo en tokens
def separar_tokens(linea):
    # Divide por espacios, operadores o caracteres especiales según sea necesario
    tokens = linea.replace('(', ' ').replace(')', ' ').replace(';', ' ').split()
    return tokens

def analizar_codigo(codigo):
    tokens = []
    
    for linea in codigo:
        palabras = separar_tokens(linea)
        
        for palabra in palabras:
            if validar_palabra_reservada(palabra):
                tokens.append((palabra, 'Palabra Reservada'))
            elif validar_numero_entero(palabra):
                tokens.append((palabra, 'Número Entero'))
            elif validar_numero_decimal(palabra):
                tokens.append((palabra, 'Número Decimal'))
            elif validar_operador_logico(palabra):
                tokens.append((palabra, 'Operador Lógico'))
            elif validar_variable(palabra):
                tokens.append((palabra, 'Variable'))
            else:
                tokens.append((palabra, 'Desconocido'))

    return tokens

# Función principal
def main():

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
            print(f"Token: {token}, Tipo: {tipo}")

if __name__ == "__main__":
    main()
