def validar_numero_decimal(cadena: str) -> bool:
    # Tabla de estados
    tabla_estados = [
        #   -   d   .   otro
        [1, 2, 6, 6],  # estado 0 (inicial)
        [6, 2, 6, 6],  # estado 1 (reconoce '-')
        [6, 2, 3, 6],  # estado 2 (reconoce parte entera)
        [6, 4, 6, 6],  # estado 3 (reconoce '.')
        [6, 4, 6, 6],  # estado 4 (reconoce parte fraccionaria)
        [6, 6, 6, 6],  # estado 5 (estado de aceptación)
        [6, 6, 6, 6],  # estado 6 (estado de error)
    ]

    estado = 0
    punto_encontrado = False

    for caracter in cadena:
        if caracter == '-':
            estado = tabla_estados[estado][0]
        elif caracter.isdigit():
            estado = tabla_estados[estado][1]
        elif caracter == '.' and not punto_encontrado:
            estado = tabla_estados[estado][2]
            punto_encontrado = True
        else:
            estado = tabla_estados[estado][3]
    
    # El estado de aceptación es el 4 (números válidos con decimales)
    return estado == 2 or estado == 4

# Ejemplo de uso

# Ejemplo de uso
# cadena = "falso"
# if validar_numero_decimal(cadena):
#     print("La cadena es valida.")
# else:
#     print("La cadena no es valida.")

# print(validar_numero_decimal("123.45"))    # True
# print(validar_numero_decimal("-123.45"))   # True
# print(validar_numero_decimal("0.123"))     # True
# print(validar_numero_decimal("123."))      # True
# print(validar_numero_decimal(".456"))      # True
# print(validar_numero_decimal("123"))       # True
# print(validar_numero_decimal("-"))         # False
# print(validar_numero_decimal("12a.34"))    # False
# print(validar_numero_decimal("-12.a34"))   # False
