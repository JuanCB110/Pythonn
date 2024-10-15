def validar_cadena_digitos(cadena: str) -> bool:
    # Tabla de estados
    tabla_estados = [
        #  dígito  otro
        [0, 1],  # estado 0 (inicial, de aceptación si solo hay dígitos)
        [1, 1]   # estado 1 (de rechazo)
    ]

    estado = 0

    for caracter in cadena:
        if '0' <= caracter <= '9':  # Si es un dígito
            estado = tabla_estados[estado][0]
        else:  # Cualquier otro carácter
            estado = tabla_estados[estado][1]

    return estado == 0  # Acepta si está en el estado 0 al finalizar

# Ejemplo de uso
# cadena = "6688826658"
# if validar_cadena_digitos(cadena):
#     print("La cadena es valida y solo contiene digitos.")
# else:
#     print("La cadena no es valida, tiene otros caracteres.")
