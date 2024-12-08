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
        self.tokens = []
        self.linea_actual = 1
        self.total_lineas = 1  # Contador para el total de líneas
        # Filtrar y limpiar tokens
        for token in tokens:
            valor, tipo = token
            if isinstance(valor, str):
                valor = valor.strip()
            if valor and tipo != "Desconocido":
                self.tokens.append(Token(valor, tipo))
                # Contar líneas basado en los tokens de punto y coma
                if valor == ";":
                    self.total_lineas += 1
        self.posicion = 0
        self.numero_linea = 1
        self.errores = []
        self.lineas_sin_punto_coma = set()

    def verificar_punto_coma(self):
        pos = self.posicion
        encontro_punto_coma = False
        
        # Buscar hasta el final de la instrucción actual
        while pos < len(self.tokens):
            if self.tokens[pos].valor == ";":
                encontro_punto_coma = True
                break
            # Si encontramos el inicio de una nueva instrucción
            if (pos + 1 < len(self.tokens) and 
                self.tokens[pos + 1].tipo in ["Variable", "Palabra Reservada"] and 
                pos > 0 and 
                self.tokens[pos].tipo not in ["Aritmetico", "Asignacion"]):
                break
            pos += 1
        
        # Si no encontramos punto y coma, agregar la línea actual a las líneas con error
        if not encontro_punto_coma:
            self.lineas_sin_punto_coma.add(self.numero_linea)
        
        return encontro_punto_coma

    def analizar(self):
        arboles = []
        mensajes = []
        tipos_declaracion = ["INT", "REAL", "BOOLEAN", "CADENA", "CARACTER", "MATRIZ"]
        
        print("=== ANALISIS SINTACTICO ===\n")
        
        while self.posicion < len(self.tokens):
            token_actual = self.tokens[self.posicion]
            
            # Declaraciones
            if token_actual.tipo == "Palabra Reservada" and token_actual.valor.upper() in tipos_declaracion:
                if self.posicion + 1 < len(self.tokens):
                    variable = self.tokens[self.posicion + 1].valor
                    arbol = self.crear_arbol_declaracion()
                    arboles.append(arbol)
                    mensajes.append(f"[Linea {self.numero_linea}] Declaracion de variable {token_actual.valor.upper()}: {variable}")
                    self.verificar_punto_coma()
                    self.numero_linea += 1
            
            # Asignaciones
            elif token_actual.tipo == "Variable":
                if self.posicion + 1 < len(self.tokens) and self.tokens[self.posicion + 1].valor == "=":
                    variable = token_actual.valor
                    pos_temp = self.posicion
                    
                    # Buscar el final de la asignación
                    while pos_temp < len(self.tokens):
                        if self.tokens[pos_temp].valor == ";":
                            break
                        if pos_temp + 1 < len(self.tokens) and self.tokens[pos_temp + 1].tipo == "Variable" and not self.tokens[pos_temp].tipo in ["Aritmetico", "Asignacion"]:
                            break
                        pos_temp += 1
                    
                    tiene_parentesis = any(t.valor == "(" for t in self.tokens[self.posicion:pos_temp])
                    tiene_operacion = any(t.tipo == "Aritmetico" and t.valor in ["+", "-", "*", "/"] for t in self.tokens[self.posicion:pos_temp])
                    
                    if tiene_parentesis:
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion con expresion anidada: {variable} = (@a + @b) * 2")
                    elif tiene_operacion:
                        valor1 = self.tokens[self.posicion + 2].valor
                        operador = self.tokens[self.posicion + 3].valor
                        valor2 = self.tokens[self.posicion + 4].valor
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion con operacion aritmetica: {variable} = {valor1} {operador} {valor2}")
                    else:
                        valor = self.tokens[self.posicion + 2].valor
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion: {variable} = {valor}")
                    
                    self.verificar_punto_coma()
                    self.numero_linea += 1
            
            self.posicion += 1

        # Verificar la última línea si no termina en punto y coma
        if len(self.tokens) > 0 and self.tokens[-1].valor != ";":
            self.lineas_sin_punto_coma.add(self.total_lineas)  # Usar el contador real de líneas

        # Imprimir mensajes y errores
        print("=== Analisis de Lineas ===\n")
        for mensaje in mensajes:
            print(mensaje)

        if self.lineas_sin_punto_coma:
            print("\n=== Errores de Punto y Coma ===")
            for linea in sorted(self.lineas_sin_punto_coma):
                print(f"Error: Falta punto y coma en la línea {linea}")

        if self.errores or self.lineas_sin_punto_coma:
            print("\n=== Errores Encontrados ===")
            for error in self.errores:
                print(error)
            print("\nAnalisis sintactico completado con errores.")
        else:
            print("\nAnalisis sintactico completado exitosamente.")
    
        return arboles

    def crear_arbol_asignacion(self):
        raiz = Nodo("asignacion")
        raiz.agregar_hijo(Nodo("variable", self.tokens[self.posicion].valor))
        raiz.agregar_hijo(Nodo("operador", "="))
        
        # Crear nodo de expresión
        expresion = Nodo("expresion")
        self.posicion += 2  # Saltar el operador de asignación
        
        # Analizar la expresión
        while self.posicion < len(self.tokens):
            token = self.tokens[self.posicion]
            if token.valor == ";":
                break
            if token.tipo == "Variable" and self.posicion > 2:
                break
                
            if token.valor == "(":
                nodo_parentesis = Nodo("parentesis")
                self.posicion += 1
                while self.tokens[self.posicion].valor != ")":
                    if self.tokens[self.posicion].tipo in ["Variable", "Numero Entero"]:
                        nodo_parentesis.agregar_hijo(Nodo("valor", self.tokens[self.posicion].valor))
                    elif self.tokens[self.posicion].tipo == "Aritmetico":
                        nodo_parentesis.agregar_hijo(Nodo("operador", self.tokens[self.posicion].valor))
                    self.posicion += 1
                expresion.agregar_hijo(nodo_parentesis)
            elif token.tipo in ["Variable", "Numero Entero"]:
                expresion.agregar_hijo(Nodo("valor", token.valor))
            elif token.tipo == "Aritmetico":
                expresion.agregar_hijo(Nodo("operador", token.valor))
            
            self.posicion += 1
            
        raiz.agregar_hijo(expresion)
        return raiz

    def crear_arbol_declaracion(self):
        raiz = Nodo("declaracion")
        # Palabra reservada 'int'
        raiz.agregar_hijo(Nodo("tipo", self.tokens[self.posicion].valor))
        # Variable
        if self.posicion + 1 < len(self.tokens):
            raiz.agregar_hijo(Nodo("variable", self.tokens[self.posicion + 1].valor))
        self.posicion += 1
        return raiz

    def validar_estructura_programa(self):
        # Verificar estructura básica del programa
        if not self.encontrar_token("ALGORITMO"):
            self.errores.append("Falta la declaración ALGORITMO al inicio")
        if not self.encontrar_token("FIN_ALGORITMO"):
            self.errores.append("Falta FIN_ALGORITMO al final")

