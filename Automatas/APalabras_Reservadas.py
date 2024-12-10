# Lista de palabras reservadas
palabras_reservadas = [
    "ALGORITMO", "FIN_ALGORITMO", "ENTERO", "REAL", "BOOLEAN", "CADENA", "CARACTER", "MATRIZ",
    "CONST", "DIMENSION", "SUBRANGO", "LEER", "ESCRIBIR", "SI", "ENTONCES", "SINO", "FIN_SI",
    "SEGUN", "HACER", "FIN_SEGUN", "MIENTRAS", "FIN_MIENTRAS", "REPETIR", "HASTA", "PARA", 
    "FIN_PARA", "FUNCION", "FIN_FUNCION", "PROCEDIMIENTO", "FIN_PROCEDIMIENTO", "RETORNAR", 
    "MOD", "NO", "AND", "OR", "VERDADERO", "FALSO", "DE", "INICIO", "FIN"
]

def validar_palabra_reservada(cadena: str) -> bool:
    # Convertimos la cadena a mayúsculas para comparación
    palabra = cadena.upper()

    # Si la palabra está en la lista de palabras reservadas, es válida
    if palabra in palabras_reservadas:
        return True
    else:
        return False

# Ejemplo de uso
# cadena = "falso"
# if validar_palabra_reservada(cadena):
#     print("La cadena es valida.")
# else:
#     print("La cadena no es valida.")

# print(validar_palabra_reservada("algoritmo"))       # True
# print(validar_palabra_reservada("FIN_ALGORITMO"))   # True
# print(validar_palabra_reservada("inicio"))          # True
# print(validar_palabra_reservada("variable"))        # False
# print(validar_palabra_reservada("FUNCION"))         # True
# print(validar_palabra_reservada("escribir"))        # True
# print(validar_palabra_reservada("retorno"))         # False
