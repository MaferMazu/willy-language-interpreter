#!/usr/bin/env python3
import ply.lex as lex
import ply.yacc as yacc 
import lexer, myparser
from sys import argv
import os,sys
import logging
from Task import *

ValidTokens = []  # Coleccion de tokens validos
InvalidTokens = []  # Coleccion de tokens invalidos
ParserErrors = [] #Errores en el parser

#Verificamos la ejecucion del programa y sus entradas
if len(argv) ==3:
    filepath = argv[1]
    if argv[2] == "-m" or argv[2] == "--manual":
        Task.add_element("man")
    elif argv[2] == "-a" or argv[2] == "--auto":
        Task.add_element(0)
    else:
        print("Uso del programa: willy <Nombre del archivo> <--manual|-m>")
        print("Uso del programa: willy <Nombre del archivo> <--auto|-a> <un float que representa los seg>\n")
        print("Los elementos entre < > son opcionales. Y '|' significa que se puede utilizar uno u otro.")
        sys.exit()

elif len(argv) == 2:
    filepath = argv[1]
    Task.add_element(0)
elif len(argv) == 4:
    filepath = argv[1]
    if argv[2] == "-a" or argv[2] == "--auto":
        if float(argv[3]) > 0:
            Task.add_element(float(argv[3]))
        else:
            print("La cantidad en segundos puede ser un entero o decimal mayor a 0")
            sys.exit()
    else:
        print("Uso del programa: python lexer.py <Nombre del archivo> <--auto> <segundos>")
        print("Uso del programa: python lexer.py <Nombre del archivo> <-a> <segundos>")
        sys.exit()


elif len(argv) == 1 :
    filepath = input('Archivo a Interpretar: ')

else:
    print("Uso del programa: python lexer.py <Nombre del archivo> <--manual>")
    print("Uso del programa: python lexer.py <Nombre del archivo> <-m>")
    print("Uso del programa: python lexer.py <Nombre del archivo> <--auto>")
    print("Uso del programa: python lexer.py <Nombre del archivo> <-a>")
    print("o utiizando: willy ")
    sys.exit()



#Probamos abrir el archivo
try:
    f = str(open(str(filepath),'r').read()) #open(filepath, 'r')
    string = str(open(str(filepath),'r').read())
    
    data = f #.readline()
    output=""
    log = logging.getLogger()
    # Construimos lexer
    lexer = lex.lex(module=lexer)
    # Construimos parser
    # myparser = myparser()
    parser = yacc.yacc(module=myparser, debug=True, debuglog=log)


    result = parser.parse(string,lex,debug=log)

    datacopy = data
    # pasamos la linea como data al lexer
    # Esto es con el fin de calcular bien la columna de los tokens
    lexer.input(data)
    column=0
    controlSpaceSemaphore=True
    # Iteramos sobre el la entrada para extraer los tokens
    tok = lexer.token()
    while tok:
        if column==0:
            while column < (tok.lexpos):
                output+=" "
                column+=1
        if controlSpaceSemaphore==False:
            while column < (tok.lexpos):
                output+=" "
                column+=1
            column += len(str(tok.value))
        else:
            column += len(str(tok.value))
            controlSpaceSemaphore=False
        if (tok.type == 'TkId' or tok.type == 'TkNum'):
            token_info = str(tok.type) + '(valor="' + str(tok.value)+'", linea='  + str(tok.lineno)+', columna='  + str(tok.lexpos + 1)+')'
        else:
            token_info = str(tok.type) + '(linea=' +str(tok.lineno)+', columna='  + str(tok.lexpos + 1)+')'
            
        ValidTokens.append(token_info)
        output+= token_info
        # Agarro el siguiente token
        tok = lexer.token()
    output+="\n"



    #while data:
        
    # Cuando hay un error se imprime solo el error
    # Cuando no hay error se imprimen los tokens validos
    if (len(InvalidTokens) > 0):
        print(InvalidTokens[0])
    else:
        print("tokens")
       #print(output)
    
    if len(ParserErrors)>=1:
        print(ParserErrors[0])

except FileNotFoundError:
    print('Imposible abrir el archivo ' + filepath)
    sys.exit()