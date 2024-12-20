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
            token_actual = self.tokens[self.posicion]
            # Excluir palabras clave que no requieren punto y coma
            if token_actual.valor != "FIN_ALGORITMO" and token_actual.valor != "FIN_SI":
                self.lineas_sin_punto_coma.add(self.numero_linea)
        
        return encontro_punto_coma

    def analizar(self):
        arboles = []  # Aquí almacenaremos los árboles sintácticos
        mensajes = []
        tipos_declaracion = ["ENTERO", "REAL", "BOOLEAN", "CADENA", "CARACTER", "MATRIZ"]

        print("=== ANALISIS SINTACTICO ===\n")

        while self.posicion < len(self.tokens):
            token_actual = self.tokens[self.posicion]

            # Declaraciones de variables
            if token_actual.tipo == "Palabra Reservada" and token_actual.valor.upper() in tipos_declaracion:
                if self.posicion + 1 < len(self.tokens):
                    variable = self.tokens[self.posicion + 1].valor
                    arbol = self.crear_arbol_declaracion()  # Crear el árbol de declaración
                    arboles.append(arbol)
                    mensajes.append(f"[Linea {self.numero_linea}] Declaracion de variable {token_actual.valor.upper()}: {variable}")
                    self.verificar_punto_coma()  # Verificar si termina en punto y coma
                    self.numero_linea += 1

            # Asignaciones
            elif token_actual.tipo == "Variable":
                if self.posicion + 1 < len(self.tokens) and self.tokens[self.posicion + 1].valor == "=":
                    # Verificar si hay suficientes tokens para la asignación
                    if self.posicion + 2 < len(self.tokens):
                        # Aquí estamos en una asignación, y tenemos los tokens suficientes para acceder
                        mensajes.append(f"[Linea {self.numero_linea}] Asignacion: {self.tokens[self.posicion].valor} = {self.tokens[self.posicion + 2].valor}")
                        arbol = self.crear_arbol_asignacion()  # Crear el árbol para esta asignación
                        arboles.append(arbol)
                    else:
                        # Si no hay suficientes tokens para completar la asignación, registrar un error
                        self.errores.append(f"[Linea {self.numero_linea}] Error en asignación: faltan tokens para completar la expresión.")
                    
                    self.verificar_punto_coma()  # Verificar si termina en punto y coma
                    self.numero_linea += 1

            # Relacionales
            elif token_actual.tipo == "Palabra Reservada" and token_actual.valor == "SI":
                arbol = Nodo("condicional")
                condicion = Nodo("condicion")
                bloque_verdadero = Nodo("bloque_verdadero")
                bloque_falso = Nodo("bloque_falso")
                
                # Procesar la condición
                self.posicion += 1  # Saltar "SI"
                while self.tokens[self.posicion].valor != "ENTONCES":
                    # Agregar los tokens de la condición al nodo
                    condicion.agregar_hijo(Nodo(self.tokens[self.posicion].tipo, self.tokens[self.posicion].valor))
                    self.posicion += 1
                arbol.agregar_hijo(condicion)

                # Procesar el bloque verdadero
                self.posicion += 1  # Saltar "ENTONCES"
                while self.tokens[self.posicion].valor != "SINO" and self.tokens[self.posicion].valor != "FIN_SI":
                    bloque_verdadero.agregar_hijo(self.crear_arbol_asignacion())  # Por ejemplo, si hay asignaciones
                    self.posicion += 1
                arbol.agregar_hijo(bloque_verdadero)

                # Procesar el bloque falso
                if self.tokens[self.posicion].valor == "SINO":
                    self.posicion += 1  # Saltar "SINO"
                    while self.tokens[self.posicion].valor != "FIN_SI":
                        bloque_falso.agregar_hijo(self.crear_arbol_asignacion())
                        self.posicion += 1
                    arbol.agregar_hijo(bloque_falso)

                self.posicion += 1  # Saltar "FIN_SI"
                arboles.append(arbol)


            self.posicion += 1  # Avanzamos al siguiente token

        # Verificar si la última línea termina en punto y coma
        if len(self.tokens) > 0 and self.tokens[-1].valor != ";":
            ultimo_token = self.tokens[-1]
            # Excluir palabras claves que no requieren punto y coma
            if ultimo_token.valor not in ["FIN_ALGORITMO", "FIN_SI"]:
                self.lineas_sin_punto_coma.add(self.total_lineas)  # Usamos el contador real de líneas


        # Imprimir los mensajes y errores
        print("=== Analisis de Lineas ===\n")
        for mensaje in mensajes:
            print(mensaje)

        if self.lineas_sin_punto_coma:
            print("\n=== Errores de Punto y Coma ===")
            for linea in sorted(self.lineas_sin_punto_coma):
                print(f"Error: Falta punto y coma en la linea {linea}")

        if self.errores or self.lineas_sin_punto_coma:
            print("\n=== Errores Encontrados ===")
            for error in self.errores:
                print(error)
            print("\nAnalisis sintactico completado con errores.")
        else:
            print("\nAnalisis sintactico completado exitosamente.")

        return arboles  # Devolvemos la lista de árboles sintácticos generados


    def crear_arbol_asignacion(self):
        raiz = Nodo("asignacion")
        raiz.agregar_hijo(Nodo("variable", self.tokens[self.posicion].valor))  # Agregar la variable

        # Agregar el operador de asignación
        raiz.agregar_hijo(Nodo("operador", "="))

        # Crear el nodo de expresión
        expresion = Nodo("expresion")
        self.posicion += 2  # Saltar el operador de asignación

        # Analizar la expresión (izquierda y derecha de la asignación)
        while self.posicion < len(self.tokens):
            token = self.tokens[self.posicion]
            
            # Si encontramos un punto y coma, terminamos la expresión
            if token.valor == ";":
                break
            
            # Si encontramos un operador aritmético, lo agregamos a la expresión
            if token.tipo == "Aritmetico":
                expresion.agregar_hijo(Nodo("operador", token.valor))
            
            # Si encontramos una variable o número, lo agregamos a la expresión
            elif token.tipo in ["Variable", "Numero Entero"]:
                expresion.agregar_hijo(Nodo("valor", token.valor))
            
            # Si encontramos un paréntesis, creamos un subárbol para esa expresión
            elif token.valor == "(":
                nodo_parentesis = Nodo("parentesis")
                self.posicion += 1
                while self.tokens[self.posicion].valor != ")":
                    if self.tokens[self.posicion].tipo in ["Variable", "Numero Entero"]:
                        nodo_parentesis.agregar_hijo(Nodo("valor", self.tokens[self.posicion].valor))
                    elif self.tokens[self.posicion].tipo == "Aritmetico":
                        nodo_parentesis.agregar_hijo(Nodo("operador", self.tokens[self.posicion].valor))
                    self.posicion += 1
                expresion.agregar_hijo(nodo_parentesis)
            
            # Aseguramos que hemos procesado el operador o el valor
            if token.valor != "(" and token.tipo not in ["Aritmetico", "Variable", "Numero Entero"]:
                break

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

