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
            
            if token_actual.tipo == "Palabra Reservada" and token_actual.valor.upper() in tipos_declaracion:
                arbol = self.crear_arbol_declaracion()
                arboles.append(arbol)
                mensajes.append(f"[Linea {self.numero_linea}] Declaracion de variable {token_actual.valor.upper()}: {self.tokens[self.posicion-1].valor}")
            
            elif token_actual.tipo == "Variable":
                if self.posicion + 1 < len(self.tokens) and self.tokens[self.posicion + 1].valor == "=":
                    arbol = self.crear_arbol_asignacion()
                    arboles.append(arbol)
                    
                    # Obtener los siguientes tokens de manera segura
                    siguientes_tokens = self.tokens[self.posicion:self.posicion+4]
                    valores_siguientes = [t.valor for t in siguientes_tokens]
                    
                    # Determinar tipo de asignación
                    if "+" in valores_siguientes:
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion con operacion aritmetica: {token_actual.valor} = ...")
                    elif "(" in valores_siguientes:
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion con expresion anidada: {token_actual.valor} = ...")
                    else:
                        # Verificar que existe el valor después del =
                        if self.posicion + 2 < len(self.tokens):
                            valor = self.tokens[self.posicion + 2].valor
                            mensajes.append(f"[Linea {self.numero_linea}] Asignacion: {token_actual.valor} = {valor}")
                        else:
                            mensajes.append(f"[Linea {self.numero_linea}] Asignacion incompleta: {token_actual.valor} =")
                            self.errores.append(f"[Linea {self.numero_linea}] Error: Asignacion incompleta")
            
            if token_actual.valor == ";":
                self.numero_linea += 1
            
            self.posicion += 1

        # Imprimir mensajes de análisis
        for mensaje in mensajes:
            print(mensaje)

        if self.errores:
            print("\nErrores encontrados:")
            for error in self.errores:
                print(error)
        else:
            print("\nAnalisis sintactico completado exitosamente.")
        
        return arboles
    
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

