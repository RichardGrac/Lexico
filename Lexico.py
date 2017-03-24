from STATE import STATE

archivo = open("Input.txt")
linea = archivo.read()
linea += "\n"
archivo.close()

pReservadas = ["main", "if", "then", "else end", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real",
               "int", "boolean"]
estado = STATE.BEGGIN        # TOKEN en el que se encuentra
cont_inicial = 0             # Contará las posiciones desde la última
contador = 0                 # Puntero que recorrerá el texto
lineaActual = 1              # Linea del archivo en la que se encuentra
lineasExtras = 0             # Contará los \n de un bloque de comentarios
colActual = 1                # Contador de columna en que se encuentra
arreglo = []
errores = []

# Cuando hago contador -= 1 es porque vamos a repetir la lectura de ese caracter que rompió con la secuencia del
# token anterior encontrado. colActual -= 1 para seguir con el correcto conteo.

while contador < len(linea):
    caracter = linea[contador]
    # INICIO DE AUTÓMATA
    if estado == STATE.BEGGIN:
        if ((caracter >= 'A') & (caracter <= 'Z')) | ((caracter >= 'a') & (caracter <= 'z')) | (caracter == '_'):
            estado = STATE.IN_STRING
        elif (caracter >= '0') & (caracter <= '9'):
            estado = STATE.IN_NUMERAL
        elif (caracter == ' ') | (caracter == '\t') | (caracter == '\n'):
            colActual += 1
            if caracter == '\n':
                lineaActual += 1
                colActual = 1
            cont_inicial = (contador + 1)
            contador += 1
            continue
        elif caracter == '/':
            estado = STATE.DIFFERENCE
        elif caracter == '+':
            estado = STATE.ADDITION
        elif caracter == '-':
            estado = STATE.SUBSTRACTION
        elif caracter == '<':
            estado = STATE.IN_LESS
        elif caracter == '>':
            estado = STATE.IN_GREATER
        elif caracter == ':':
            estado = STATE.IN_ASSIGNMENT
        elif caracter == '!':
            estado = STATE.IN_NEGATION
        elif caracter == '=':
            estado = STATE.IN_EQUAL
        elif (caracter == '*') | (caracter == '%'):
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Operador          \t#" + linea[cont_inicial:contador + 1])
            estado = STATE.END
        elif (caracter == '(') | (caracter == ')') | (caracter == '{') | (caracter == '}') | (caracter == ';') | \
                (caracter == ','):
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Simbolo especial \t#" + linea[cont_inicial:contador + 1])
            estado = STATE.END
        else:
            estado = STATE.ERROR  # Estado de Error
    elif estado == STATE.IN_STRING:
        if ((caracter < 'A') | (caracter > 'Z')) & ((caracter < 'a') | (caracter > 'z')) & \
                ((caracter < '0') | (caracter > '9')) & (caracter != '_'):
            estado = STATE.END
            if linea[cont_inicial:contador] in pReservadas:
                arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Palabra reservada\t#" + linea[cont_inicial:contador])
            else:
                arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Identificador    \t#" + linea[cont_inicial:contador])
            contador -= 1
            colActual -= 1
    elif estado == STATE.IN_NUMERAL:
        if caracter == '.':
            if (linea[contador + 1] >= '0') & (linea[contador + 1] <= '9'):
                estado = STATE.IN_FLOAT
            else:
                estado = STATE.ERROR
        elif (caracter < '0') | (caracter > '9'):
            estado = STATE.END
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Cte. numerica    \t#" + linea[cont_inicial:contador])
            contador -= 1
            colActual -= 1
    elif estado == STATE.IN_FLOAT:
        if (caracter < '0') | (caracter > '9'):
            estado = STATE.END
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Flotante         \t#" + linea[cont_inicial:contador])
            contador -= 1
            colActual -= 1
    elif estado == STATE.DIFFERENCE:
        if caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT
        elif caracter == '/':
            estado = STATE.END  # Forma de terminar
            while (contador < len(linea)) & (linea[contador] != '\n'):
                contador += 1
            while linea[cont_inicial] == '\n':
                cont_inicial += 1
            # print("Comment inline detected: " + linea[cont_inicial:contador])
            # arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Comment inline    \t " + linea[cont_inicial:contador])
            lineaActual += 1
            colActual = 1
        else:
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Operador          \t#" + linea[cont_inicial:contador])
            contador -= 1
            colActual -= 1
            estado = STATE.END
    elif estado == STATE.IN_MULTIPLE_COMMENT:
        if caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT_END
        elif caracter == "\n":
            lineasExtras += 1
    elif estado == STATE.IN_MULTIPLE_COMMENT_END:
        if caracter == "\n":
            lineasExtras += 1
        if caracter == '/':
            estado = STATE.END  # Terminó, volvemos al estado inicial
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Multiple comment   \t#" + linea[cont_inicial:contador + 1])
            if linea[contador + 1] == '\n':
                cont_inicial += 1
            lineaActual += lineasExtras
            lineasExtras = 0
        elif caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT_END
        else:
            estado = STATE.IN_MULTIPLE_COMMENT
    elif estado == STATE.ADDITION:
        if caracter == '+':
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. Incremento    \t#" + linea[cont_inicial:contador + 1])
            estado = STATE.END
        elif (caracter >= '0') & (caracter <= '9'):
            estado = STATE.IN_NUMERAL
            contador -= 1
            colActual -= 1
        else:
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Operador          \t#" + linea[cont_inicial:contador])
            contador -= 1
            colActual -= 1
            estado = STATE.END
    elif estado == STATE.SUBSTRACTION:
        if caracter == '-':
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. Decremento    \t#" + linea[cont_inicial:contador + 1])
            estado = STATE.END
        elif (caracter >= '0') & (caracter <= '9'):
            estado = STATE.IN_NUMERAL
            contador -= 1
            colActual -= 1
        else:
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Operador          \t#" + linea[cont_inicial:contador])
            contador -= 1
            colActual -= 1
            estado = STATE.END
    elif estado == STATE.IN_LESS:
        if caracter == '=':
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. relacional     \t#" + linea[cont_inicial:contador + 1])
        else:
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. relacional     \t#" + linea[cont_inicial:contador])
            contador -= 1
            colActual -= 1
        estado = STATE.END
    elif estado == STATE.IN_GREATER:
        if caracter == '=':
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. relacional     \t#" + linea[cont_inicial:contador + 1])
        else:
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. relacional     \t#" + linea[cont_inicial:contador])
            contador -= 1
            colActual -= 1
        estado = STATE.END
    elif estado == STATE.IN_ASSIGNMENT:
        if caracter == '=':
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. Asignacion    \t#" + linea[cont_inicial:contador + 1])
            estado = STATE.END
        else:
            contador -= 1
            colActual -= 1
            estado = STATE.ERROR
    elif estado == STATE.IN_NEGATION:
        if caracter == '=':
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. comparacion   \t#" + linea[cont_inicial:contador + 1])
            estado = STATE.END
        else:
            contador -= 1
            colActual -= 1
            estado = STATE.ERROR
    elif estado == STATE.IN_EQUAL:
        if caracter == '=':
            arreglo.append(str(lineaActual) + "#" + str(colActual-(contador-cont_inicial)) + "#" + "Op. comparacion   \t#" + linea[cont_inicial:contador + 1])
            estado = STATE.END
        else:
            contador -= 1
            colActual -= 1
            estado = STATE.ERROR
    if estado == STATE.END:
        cont_inicial = (contador + 1)
        estado = STATE.BEGGIN
    if estado == STATE.ERROR:
        errores.append("Error en (" + str(lineaActual) + "," + str(colActual) + "): " + linea[cont_inicial:contador + 1])
        cont_inicial = (contador + 1)
        estado = STATE.BEGGIN
    contador += 1
    colActual += 1
    # FIN DE AUTÓMATA (while)

# Si está en estado de error 0 ó si quedó en un estado NO TERMINANTE (Comentario multiple sin cerrar):
if (estado == STATE.ERROR) | ((estado != STATE.END) & (estado != STATE.BEGGIN)):
    contador -= 1
    colActual -= 1
    if (estado == STATE.IN_MULTIPLE_COMMENT) | (estado == STATE.IN_MULTIPLE_COMMENT_END):
        errores.append("Error en (" + str(lineaActual) + "," + str(colActual) + "): [Comentario]")
    else:
        errores.append("Error en (" + str(lineaActual) + "," + str(colActual) + "): " + linea[cont_inicial:contador + 1])

for tokens in arreglo:
    print(tokens)

# print("ERRORES:")
for error in errores:
    print(error)

output = open("Output.txt", "w")
for tokens in arreglo:
    output.write(tokens + "\n")
output.close()

faults = open("Errores.txt", "w")
for error in errores:
    faults.write(error + "\n")
faults.close()
