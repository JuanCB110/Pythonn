def validar_operador_asignacion(operador):
    operadores_asignacion = ['=', '+=', '-=', '*=', '/=', '%=']
    
    if operador in operadores_asignacion:
        return True
    return False

# Ejemplos de prueba
# print(validar_operador_asignacion("+="))  # True
# print(validar_operador_asignacion("="))   # True
# print(validar_operador_asignacion("-"))   # False
