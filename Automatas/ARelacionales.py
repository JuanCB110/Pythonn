def validar_operador_relacional(operador):
    operadores_relacionales = ['<', '>', '<=', '>=', '==', '!=']
    
    if operador in operadores_relacionales:
        return True
    return False

# Ejemplos de prueba
# print(validar_operador_relacional(">="))  # True
# print(validar_operador_relacional("<"))  # True
# print(validar_operador_relacional("!=")) # False
