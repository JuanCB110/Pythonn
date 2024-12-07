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
        # Convertimos las tuplas a objetos Token
        self.tokens = [Token(t[0], t[1]) for t in tokens]
        self.posicion = 0
    
    def analizar(self):
        arboles = []
        while self.posicion < len(self.tokens):
            token_actual = self.tokens[self.posicion]
            
            if token_actual.tipo == "Palabra Reservada" and token_actual.valor == "int":
                arboles.append(self.crear_arbol_declaracion())
            elif token_actual.tipo == "Variable":
                arboles.append(self.crear_arbol_asignacion())
            
            self.posicion += 1
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
        if self.posicion + 1 < len(self.tokens):
            raiz.agregar_hijo(Nodo("operador", self.tokens[self.posicion + 1].valor))
        
        # Valor asignado
        if self.posicion + 2 < len(self.tokens):
            raiz.agregar_hijo(Nodo("valor", self.tokens[self.posicion + 2].valor))
        
        self.posicion += 2  # Avanzamos para saltar el operador y el valor
        return raiz

