
def validar_variable(variable:str):

    tabla_estados = [
    #   @   l  n  _
        [1, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 2, 2, 2]
    ]

    estado = 0

    for caracter in variable:
        match caracter:
            case '@':
                estado = tabla_estados[estado][0]
            case _ if 'a' <= caracter <= 'z' or 'A' <= caracter <= 'Z':
                estado = tabla_estados[estado][1]
            case _ if '0' <= caracter <= '9':
                estado = tabla_estados[estado][2]
            case '_':
                estado = tabla_estados[estado][3]
            case _ :
                estado = 0
                break

    if estado == 2:
        return True

    return False

# if validar_variable("@z"):
#     print("variable valida")
# else:
#     print("variable no valida")