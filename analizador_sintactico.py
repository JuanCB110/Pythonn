class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []
    
    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)
    
    def mostrar(self, nivel=0):
        print("  " * nivel + f"{self.tipo}: {self.valor}")
        for hijo in self.hijos:
            hijo.mostrar(nivel + 1)

class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0
    
    def analizar(self):
        resultados = []
        while self.posicion < len(self.tokens):
            if self.tokens[self.posicion].valor == "int":
                resultados.append(self.crear_arbol_declaracion())
            elif self.tokens[self.posicion].valor.startswith("@"):
                resultados.append(self.crear_arbol_asignacion())
            self.posicion += 1
        return resultados
    
    def crear_arbol_declaracion(self):
        raiz = Nodo("declaracion")
        # int
        raiz.agregar_hijo(Nodo("tipo", self.tokens[self.posicion].valor))
        # @variable
        if self.posicion + 1 < len(self.tokens):
            raiz.agregar_hijo(Nodo("variable", self.tokens[self.posicion + 1].valor))
        return raiz

# En tu archivo principal (main.py o como lo tengas llamado)
#if __name__ == "__main__":
    # Aquí recibirías los tokens de tu analizador léxico
    #analizador = AnalizadorSintactico(tokens)
    #arboles = analizador.analizar()
    
    # Mostrar los árboles generados
    #for arbol in arboles:
    #    arbol.mostrar()

    
