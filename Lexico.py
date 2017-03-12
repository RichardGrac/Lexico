from STATE import STATE

archivo = open("Input.txt")
linea = archivo.read()
linea += "\n"
archivo.close()

pReservadas = ["main","if","then","else end","do","while","repeat","until","cin","cout","real","int","boolean"]
estado = STATE.BEGGIN  #TOKEN en el que se encuentra
cont_inicial = 0 #Contará las posiciones desde la última
contador = 0 #Puntero que recorrerá el texto
band = True #Estado de error
lineaActual = 1 #Linea del archivo en la que se encuentra
lineasExtras = 0 #Contará los \n de un bloque de comentarios
arreglo = ["CATEGORIA##COMPONENTE LÉXICO##Fila"]
errores = []

while contador < len(linea):
    caracter = linea[contador]
    #INICIO DE AUTÓMATA
    if (estado == STATE.BEGGIN):
        if ((caracter >= 'A') & (caracter <= 'Z')) | ((caracter >= 'a') & (caracter <= 'z')) | (caracter == '_'):
            estado = STATE.IN_STRING
        elif (caracter >= '0') & (caracter <= '9'):
            estado = STATE.IN_NUMERAL
        elif caracter == '/':
            estado = STATE.DIFFERENCE
        elif (caracter == ' ') | (caracter == '\t') | (caracter == '\n'):
            if caracter == '\n':
                lineaActual += 1
            cont_inicial = (contador + 1)
            contador += 1
            continue
        else:
            estado = STATE.ERROR #Estado de Error
    elif estado == STATE.IN_STRING:
        if ((caracter < 'A') | (caracter > 'Z')) & ((caracter < 'a') | (caracter > 'z')) & ((caracter < '0') | (caracter > '9')) & ((caracter != '_')):
            estado = STATE.END
            if linea[cont_inicial:contador] in pReservadas:
                arreglo.append("Palabra reservada##" + linea[cont_inicial:contador] + "##" + str(lineaActual))
            else:
                arreglo.append("Identificador##" + linea[cont_inicial:contador] + "##" + str(lineaActual))
            contador -= 1
    elif estado == STATE.IN_NUMERAL:
        if caracter == '.':
            if (linea[contador+1] >= '0') & (linea[contador+1] <= '9'):
                estado = STATE.IN_FLOAT
            else:
                estado = STATE.ERROR
        elif (caracter < '0') | (caracter > '9'):
            estado = STATE.END
            arreglo.append("Cte. numérica##" + linea[cont_inicial:contador] + "##" + str(lineaActual))
            contador -= 1
    elif estado == STATE.IN_FLOAT:
        if (caracter < '0') | (caracter > '9'):
            estado = STATE.END
            arreglo.append("Flotante##" + linea[cont_inicial:contador] + "##" + str(lineaActual))
            contador -= 1
    elif estado == STATE.DIFFERENCE:
        if caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT
        elif caracter == '/':
            estado = STATE.END #Forma de terminar
            while (contador < len(linea)) & (linea[contador] != '\n'):
                contador += 1
            while linea[cont_inicial] == '\n':
                cont_inicial += 1
            # print("Comment inline detected: " + linea[cont_inicial:contador])
            arreglo.append("Comment inline ## " + linea[cont_inicial:contador] + "##" + str(lineaActual))
            lineaActual += 1
        else:
            estado = STATE.ERROR
    elif estado == STATE.IN_MULTIPLE_COMMENT:
        if caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT_END
        elif caracter == "\n":
            lineasExtras += 1
    elif estado == STATE.IN_MULTIPLE_COMMENT_END:
        if caracter == '/':
            estado = STATE.END #Terminó, volvemos al estado inicial
            arreglo.append("Multiple comment ## " + linea[cont_inicial:contador + 1] + "##" + str(lineaActual))
            if linea[contador+1] == '\n':
                cont_inicial += 1
            lineaActual += lineasExtras
            lineasExtras = 0
        elif caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT_END
        else:
            estado = STATE.IN_MULTIPLE_COMMENT

    if estado == STATE.END:
        cont_inicial = (contador+1)
        estado = STATE.BEGGIN
    if estado == STATE.ERROR:
        errores.append("Error en linea: " + str(lineaActual))
        while (contador < len(linea)) & (linea[contador] != '\n'):
            contador += 1
        cont_inicial = (contador + 1)
        lineaActual += 1
        estado = STATE.BEGGIN
    contador += 1
    #FIN DE AUTÓMATA (while)

#Si está en estado de error 0 ó si quedó en un estado NO TERMINANTE:
if (estado == STATE.ERROR) | ((estado != STATE.END) & (estado != STATE.BEGGIN)):
    print("Error en linea", lineaActual)
    band = False
# Si todo salió bien:
if band:
    print("Without problems.")

for tokens in arreglo:
    print(tokens)

for error in errores:
    print(error)