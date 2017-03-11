from STATE import STATE

archivo = open("Input.txt")
linea = archivo.read()
archivo.close()

estado = STATE.BEGGIN  #TOKEN en el que se encuentra
cont_inicial = 0 #Contará las posiciones desde la última
contador = 0 #Puntero que recorrerá el texto
band = True #Estado de error
lineaActual = 1 #Linea del archivo en la que se encuentra
arreglo = ["CATEGORIA \t##\t COMPONENTE LÉXICO   ## Fila"]

while contador < len(linea):
    caracter = linea[contador]
    if ((caracter == '\n') | (caracter == ' ') | (caracter == '\t')) & (estado == STATE.BEGGIN):
        if caracter == '\n':
            lineaActual += 1
        cont_inicial = contador+1
        contador += 1
        continue

    #INICIO DE AUTÓMATA
    if (estado == STATE.BEGGIN):
        if caracter == '/':
            estado = STATE.DIFFERENCE
        elif (caracter == ' ') | (caracter == '\t') | (caracter == '\n'):
            estado = STATE.BEGGIN #División
        else:
            estado = STATE.ERROR #Estado de Error
    elif estado == STATE.DIFFERENCE:
        if caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT
        elif caracter == '/':
            estado = STATE.BEGGIN #Forma de terminar
            while (contador < len(linea)) & (linea[contador] != '\n'):
                contador += 1
            # cont_inicial += 1
            while linea[cont_inicial] == '\n':
                cont_inicial += 1
            # print("Comment inline detected: " + linea[cont_inicial:contador])
            arreglo.append("Comment inline ## " + linea[cont_inicial:contador] + "##" + str(lineaActual))
            cont_inicial = (contador+1)
            lineaActual += 1
        else:
            estado = STATE.ERROR
    elif estado == STATE.IN_MULTIPLE_COMMENT:
        if caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT_END
    elif estado == STATE.IN_MULTIPLE_COMMENT_END:
        if caracter == '/':
            estado = STATE.BEGGIN #Terminó, volvemos al estado inicial
            arreglo.append("Multiple comment ## " + linea[cont_inicial:contador + 1] + "##" + str(lineaActual))
            cont_inicial = (contador+1)
            if linea[contador+1] == '\n':
                cont_inicial += 1
        elif caracter == '*':
            estado = STATE.IN_MULTIPLE_COMMENT_END
        else:
            estado = STATE.IN_MULTIPLE_COMMENT

    if estado == STATE.ERROR:
       band = False
       break
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