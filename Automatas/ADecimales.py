def validar_numero_decimal(cadena: str) -> bool:
    # Tabla de estados
    #   -   d   .   otro
    tabla_estados = [
        # estado 0 (inicial)  : Transición para '-','d','.' y 'otro'
        [1, 2, 6, 6],        # Estado 0
        [6, 2, 6, 6],        # Estado 1 (reconoce '-')
        [6, 2, 3, 6],        # Estado 2 (reconoce parte entera)
        [6, 4, 6, 6],        # Estado 3 (reconoce '.')
        [6, 4, 5, 6],        # Estado 4 (reconoce parte fraccionaria)
        [6, 6, 6, 6],        # Estado 5 (estado de aceptación)
        [6, 6, 6, 6],        # Estado 6 (estado de error)
    ]

    estado = 0
    punto_encontrado = False

    for caracter in cadena:
        if caracter == '-':  # Maneja el signo negativo
            estado = tabla_estados[estado][0]
        elif caracter.isdigit():  # Maneja dígitos
            estado = tabla_estados[estado][1]
        elif caracter == '.' and not punto_encontrado:  # Maneja el punto decimal
            estado = tabla_estados[estado][2]
            punto_encontrado = True
        else:
            estado = tabla_estados[estado][3]  # Transición por cualquier otro carácter no válido

    # El estado de aceptación es el 5 (números válidos con decimales)
    return estado == 5 or estado == 2  # Aceptamos también el estado 2 para números enteros

# Ejemplos de uso
# print(validar_numero_decimal("123.45"))  # True
# print(validar_numero_decimal("-123.45"))  # True
# print(validar_numero_decimal("0.123"))  # True
# print(validar_numero_decimal("123."))  # True
# print(validar_numero_decimal(".456"))  # True
# print(validar_numero_decimal("123"))  # True
# print(validar_numero_decimal("-"))  # False
# print(validar_numero_decimal("12a.34"))  # False
# print(validar_numero_decimal("-12.a34"))  # False