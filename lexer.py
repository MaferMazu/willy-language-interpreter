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

# AQUI SOLO SE HARA EL AREA DE INPUT PARA EL LEXER, LO QUE TENGA QUE VER CON EL READ ARCHIVO O UN MENU PARA EL USUARIO #
print("Hola mundo")
TokenConstants.outHello()
print(LexerFunctions.tk)
# Functions working
