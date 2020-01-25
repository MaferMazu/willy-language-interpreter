"""
    Analizador Lexicografico del Lenguaje GuardedUSB
    Primera fase del proyecto
    Traductores e Interpretadores (CI-3725)
    Maria Fernanda Magallanes (13-10787)
    Jesus Marcano (12-10359)
    E-M 2020
"""
from ply import lex
from LexerModels import TokenConstants
from LexerModels import LexerFunctions
from sys import argv

# AQUI SOLO SE HARA EL AREA DE INPUT PARA EL LEXER, LO QUE TENGA QUE VER CON EL READ ARCHIVO O UN MENU PARA EL USUARIO #
print("Hola mundo")
TokenConstants.outHello()
print(LexerFunctions.tk)
# Functions working

if len(argv) > 2:
    print("Uso del programa: python3 lexer.py <Nombre del archivo>")
    print("o utiizando: python3 lexer.py ")
    sys.exit()
elif len(argv) == 2:
    filepath = argv[1]
else:
    filepath = input('Archivo a Interpretar: ')

try:
    f = open(filepath,'r')
    data =f.readline()
    token_prev= 'Unknown'
    lexer = lex.lex()
    while data:
        #pasamos la linea como data al lexer
        #Esto es con el fin de calcular bien la columna de los tokens
        lexer.input(data)


        #Iteramos sobre el la entrada para extraer los tokens
        #for tok in lexer:
        #    print(tok.type, tok.value, tok.lineno)
        tok = lexer.token()

        while tok:
            if (tok.type == 'TkNum'):
                token_info = str(tok.type) + ' ("' + str(tok.value) + '") '\
                + str(tok.lineno) + ' ' + str(tok.lexpos+1)
            elif (tok.type == 'TkId'):
                token_info = str(tok.type) + ' ("' + str(tok.value) + '" , ' + token_prev + ') '\
                + str(tok.lineno) + ' ' + str(tok.lexpos+1)
            else:
                token_info = str(tok.type) + ' ' + str(tok.lineno) + ' ' + str(tok.lexpos+1)
                token_prev = str(tok.type)

            ValidTokens.append(token_info)
            tok = lexer.token()


        #leemos otra linea
        data = f.readline()

    # Cuando hay un error se imprime solo el error
    # Cuando no hay error se imprimen los tokens validos
    if (len(TokenConstants.InvalidTokens)>0):
        for x in TokenConstants.InvalidTokens:
            print(x)
    else:
        for x in TokenConstants.ValidTokens:
            print(x)
    f.close()
except FileNotFoundError:
    print('Imposible abrir el archivo '+filepath)
    sys.exit()