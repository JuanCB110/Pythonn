def validar_operador_aritmetico(operador):
    operadores_aritmeticos = ['+', '-', '*', '/', '%']
    
    if operador in operadores_aritmeticos:
        return True
    return False

# Ejemplos de prueba
# print(validar_operador_aritmetico("+"))  # True
# print(validar_operador_aritmetico("/"))  # True
# print(validar_operador_aritmetico("**")) # False
