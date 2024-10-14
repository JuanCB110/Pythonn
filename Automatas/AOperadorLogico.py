def validar_operador_logico(cadena: str) -> bool:
    # Tabla de estados
    tabla_estados = [
        #  &   |   !   otro
        [1, 3, 5, 6],  # estado 0 (inicial)
        [2, 6, 6, 6],  # estado 1 (reconoce primer '&')
        [6, 6, 6, 6],  # estado 2 (reconoce '&&')
        [6, 4, 6, 6],  # estado 3 (reconoce primer '|')
        [6, 6, 6, 6],  # estado 4 (reconoce '||')
        [6, 6, 6, 6],  # estado 5 (reconoce '!')
        [6, 6, 6, 6]   # estado 6 (estado de error)
    ]

    estado = 0

    for caracter in cadena:
        match caracter:
            case '&':
                estado = tabla_estados[estado][0]
            case '|':
                estado = tabla_estados[estado][1]
            case '!':
                estado = tabla_estados[estado][2]
            case _:
                estado = tabla_estados[estado][3]

    return estado in {2, 4, 5}  # Acepta si termina en un estado de aceptación (&&, ||, !)

# Ejemplo de uso
cadena = "||"
if validar_operador_logico(cadena):
    print("La cadena es valida.")
else:
    print("La cadena no es valida.")