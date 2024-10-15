def validar_numero_entero(cadena: str) -> bool:
    # Tabla de estados
    tabla_estados = [
        #   -   d   otro
        [1, 2, 3],  # estado 0 (inicial)
        [3, 2, 3],  # estado 1 (reconoce '-')
        [3, 2, 3],  # estado 2 (reconoce dígitos)
        [3, 3, 3]   # estado 3 (estado de error)
    ]

    estado = 0

    for caracter in cadena:
        if caracter == '-':
            estado = tabla_estados[estado][0]
        elif caracter.isdigit():
            estado = tabla_estados[estado][1]
        else:
            estado = tabla_estados[estado][2]
    
    # El estado de aceptación es el 2 (reconoce números válidos)
    return estado == 2

# Ejemplo de uso

# Ejemplo de uso
# cadena = "-12"
# if validar_numero_entero(cadena):
#     print("La cadena es valida.")
# else:
#     print("La cadena no es valida.")

# print(validar_numero_entero("123"))    # True
# print(validar_numero_entero("-456"))   # True
# print(validar_numero_entero("0"))      # True
# print(validar_numero_entero("-"))      # False
# print(validar_numero_entero("12a"))    # False
# print(validar_numero_entero("-12a"))   # False
