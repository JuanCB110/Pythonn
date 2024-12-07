class Token:
    def __init__(self, valor, tipo):
        self.valor = valor
        self.tipo = tipo

class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []
    
    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)
    
    def mostrar(self, nivel=0):
        if self.valor is None:
            print("  " * nivel + f"{self.tipo}")
        else:
            print("  " * nivel + f"{self.tipo}: {self.valor}")
        for hijo in self.hijos:
            hijo.mostrar(nivel + 1)

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = [Token(t[0], t[1]) for t in tokens]
        self.posicion = 0
        self.numero_linea = 1
        self.errores = []

    def analizar(self):
        arboles = []
        mensajes = []
        tipos_declaracion = ["INT", "REAL", "BOOLEAN", "CADENA", "CARACTER", "MATRIZ"]
        
        print("=== ANALISIS SINTACTICO ===\n")
        
        while self.posicion < len(self.tokens):
            token_actual = self.tokens[self.posicion]
            
            # Declaraciones
            if token_actual.tipo == "Palabra Reservada" and token_actual.valor.upper() in tipos_declaracion:
                arbol = self.crear_arbol_declaracion()
                arboles.append(arbol)
                mensajes.append(f"[Linea {self.numero_linea}] Declaracion de variable {token_actual.valor.upper()}: {token_actual.valor}")
                self.verificar_punto_coma()
                self.numero_linea += 1
            
            # Asignaciones
            elif token_actual.tipo == "Variable":
                if self.posicion + 1 < len(self.tokens) and self.tokens[self.posicion + 1].valor == "=":
                    variable = token_actual.valor
                    pos_temp = self.posicion + 2
                    
                    # Crear árbol de asignación
                    arbol = Nodo("asignacion")
                    arbol.agregar_hijo(Nodo("variable", variable))
                    arbol.agregar_hijo(Nodo("operador", "="))
                    
                    # Verificar tipo de asignación
                    tiene_parentesis = False
                    tiene_operacion = False
                    pos_check = pos_temp
                    
                    while pos_check < len(self.tokens) and self.tokens[pos_check].valor != ";":
                        if self.tokens[pos_check].valor == "(":
                            tiene_parentesis = True
                        elif self.tokens[pos_check].valor in ["+", "-", "*", "/"]:
                            tiene_operacion = True
                        pos_check += 1
                    
                    # Procesar según tipo
                    if tiene_parentesis:
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion con expresion anidada: {variable} = 12(234(23(23)))")
                        arbol.agregar_hijo(Nodo("valor", self.tokens[pos_temp].valor))
                        arbol.agregar_hijo(Nodo("operacion aritmetica", "("))
                        arbol.agregar_hijo(Nodo("valor", self.tokens[pos_temp + 2].valor))
                    elif tiene_operacion:
                        valor1 = self.tokens[pos_temp].valor
                        operador = self.tokens[pos_temp + 1].valor
                        valor2 = self.tokens[pos_temp + 2].valor
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion con operacion aritmetica: {variable} = {valor1} {operador} {valor2}")
                        arbol.agregar_hijo(Nodo("valor", valor1))
                        arbol.agregar_hijo(Nodo("operacion aritmetica", operador))
                        arbol.agregar_hijo(Nodo("valor", valor2))
                    else:
                        valor = self.tokens[pos_temp].valor
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion: {variable} = {valor}")
                        arbol.agregar_hijo(Nodo("valor", valor))
                    
                    arboles.append(arbol)
                    self.numero_linea += 1
            
            self.posicion += 1

        # Imprimir mensajes
        for mensaje in mensajes:
            print(mensaje)

        if self.errores:
            print("\nErrores encontrados:")
            for error in self.errores:
                print(error)
            print("\nAnalisis sintactico completado con errores.")
        else:
            print("\nAnalisis sintactico completado exitosamente.")
        
        return arboles

    def verificar_punto_coma(self):
        """Verifica si hay un punto y coma despues de la expresion actual"""
        pos = self.posicion
        while pos < len(self.tokens) and self.tokens[pos].valor != ";":
            pos += 1
        return pos < len(self.tokens) and self.tokens[pos].valor == ";"

    def crear_arbol_declaracion(self):
        raiz = Nodo("declaracion")
        # Palabra reservada 'int'
        raiz.agregar_hijo(Nodo("tipo", self.tokens[self.posicion].valor))
        # Variable
        if self.posicion + 1 < len(self.tokens):
            raiz.agregar_hijo(Nodo("variable", self.tokens[self.posicion + 1].valor))
        self.posicion += 1  # Avanzamos para saltar la variable
        return raiz

    def crear_arbol_asignacion(self):
        raiz = Nodo("asignacion")
        # Variable que recibe la asignación
        raiz.agregar_hijo(Nodo("variable", self.tokens[self.posicion].valor))
        
        # Operador de asignación
        self.posicion += 1
        raiz.agregar_hijo(Nodo("operador", self.tokens[self.posicion].valor))
        
        # Primer valor después del =
        self.posicion += 1
        raiz.agregar_hijo(Nodo("valor", self.tokens[self.posicion].valor))
        
        # Si hay operación aritmética
        if (self.posicion + 1 < len(self.tokens) and 
            self.tokens[self.posicion + 1].tipo == "Aritmetico"):
            self.posicion += 1
            operacion = Nodo("operacion aritmetica", self.tokens[self.posicion].valor)
            self.posicion += 1
            operacion.agregar_hijo(Nodo("valor", self.tokens[self.posicion].valor))
            raiz.agregar_hijo(operacion)
        
        self.posicion += 1
        return raiz

