import ply.lex as lex
import ply.yacc as yacc 
import lexer, parser
from sys import argv
import os,sys


ValidTokens = []  # Coleccion de tokens validos
InvalidTokens = []  # Coleccion de tokens invalidos

# Construimos lexer
lexer = lex.lex(module=lexer)
# Construimos parser
parser = yacc.yacc(parser)


#Verificamos la ejecucion del programa y sus entradas
if len(argv) > 2:
    print("Uso del programa: python lexer.py <Nombre del archivo>")
    print("o utiizando: python3 lexer.py ")
    sys.exit()
elif len(argv) == 2:
    filepath = argv[1]
else:
    filepath = input('Archivo a Interpretar: ')


#Probamos abrir el archivo
try:
    f = open(filepath, 'r')
    data = f.readline()
    output=""
    
    while data:
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
        result = parser.parse(datacopy)
        print(result)
        
        # Leemos otra linea
        data = f.readline()

    # Cuando hay un error se imprime solo el error
    # Cuando no hay error se imprimen los tokens validos
    if (len(InvalidTokens) > 0):
        print(InvalidTokens[0])
    else:
        print(output)

except FileNotFoundError:
    print('Imposible abrir el archivo ' + filepath)
    sys.exit()