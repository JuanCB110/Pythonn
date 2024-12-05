#Tarea 1-Desarrollo de Funciones
#Funcion para eliminar  Espacios en Blanco, Líneas Vacías, Comentarios, Tabuladores
def PreprocesarArchivo(ruta1,ruta2):
    try:
        #Abrir el archivo intacto para leerlo
        with open(ruta1, 'r') as archivo_inicial:
            lineas_procesadas = []
            #recorrer el archivo
            for linea in archivo_inicial:
                #Eliminar espacios en blanco
                linea = linea.strip()

                #Saltar lineas vacias o comentarios
                if not linea or linea.startswith('/'):
                    continue

                #eliminar tab
                linea = linea.replace('\t', '')

                # Eliminar espacios alrededor de operadores "="
                if '=' in linea:
                    partes = linea.split('=')
                    linea = '='.join(parte.strip() for parte in partes)

                # Eliminar espacios alrededor de operadores "+"
                if '+' in linea:
                    partes = linea.split('+')
                    linea = '+'.join(parte.strip() for parte in partes)

                # Eliminar espacios alrededor de operadores "-"
                if '-' in linea:
                    partes = linea.split('-')
                    linea = '-'.join(parte.strip() for parte in partes)

                # Eliminar espacios alrededor de operadores "*"
                if '*' in linea:
                    partes = linea.split('*')
                    linea = '*'.join(parte.strip() for parte in partes)

                # Eliminar espacios alrededor de operadores "/"
                if '/' in linea:
                    partes = linea.split('/')
                    linea = '/'.join(parte.strip() for parte in partes)

                # Eliminar espacios alrededor de paréntesis "("
                if '(' in linea:
                    partes = linea.split('(')
                    linea = '('.join(parte.strip() for parte in partes)

                # Eliminar espacios alrededor de paréntesis ")"
                if ')' in linea:
                    partes = linea.split(')')
                    linea = ')'.join(parte.strip() for parte in partes)

                # Eliminar espacios alrededor de ";"
                if ';' in linea:
                    partes = linea.split(';')
                    linea = ';'.join(parte.strip() for parte in partes)

                #Agregar la linea procesada a la lista
                lineas_procesadas.append(linea)
                print(linea)

        #Abrir el archivo de salida para escritura
        with open(ruta2, 'w') as archivo_salida:
                for linea in lineas_procesadas:
                    archivo_salida.write(linea + '\n')
    except FileNotFoundError:
        print(f"Error: El archivo {ruta1} no existe.")

    except Exception as e:
        print(f"Valio burger {e}")


#Funcion de Recorrer el Archivo .txt
def RecorrerArchivo(ruta):
    try:
        with open(ruta, 'r') as archivomodificado:
            while True:
                #Lee el archivo caracter por caracter
                caracter = archivomodificado.read(1)
                #Si llega al final del archivo, se sale del bucle
                if not caracter:
                    break
                #Imprimir el caracter
                # print(caracter, end ='')
    except FileNotFoundError:
        print(f"El archivo {ruta} no fue encontrado.")
    except IOError:
        print("Ocurrio un error al intentar leer el archivo.")

#Main padrino
# PreprocesarArchivo('C:\\Pythonn\\miprograma.txt', 'C:\\Pythonn\\nuevotexto.txt')
# ruta = 'C:\\Pythonn\\miprograma.txt'
# RecorrerArchivo(ruta)