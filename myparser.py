import lexer
import Node
import ply.yacc as yacc
import parser

DEBUG_MODE = False

# import some required globals from tokenizer
tokens = lexer.tokens

def p_correctProgram(p):
    "correctProgram : program"
    p[0] = p[1]
    pass

def p_program(p):
    """
    program : worldBlock 
            | taskBlock 
            | worldBlock program
            | taskBlock program
    """
    if(len(p) < 1):
        p[0] = p[1]
    else:
        P[0] = p[1] + p[2]

def p_wallSet(p):
    'wallSet : TkWall directions TkFrom TkNum TkNum TkTo TkNum TkNum'
    pass

def p_worldBlock(p):
    '''worldBlock : TkBeginWorld TkId instructions TkEndWorld worldBlock 
                    | TkBeginWorld TkId TkEndWorld worldBlock 
                    | TkBeginWorld TkId instructions TkEndWorld '''
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

def p_worldSet(p):
    '''worldSet : TkWorld TkNum TkNum 
                | empty'''


def p_instructions(p):
    "instructions : TkId"
    pass

def p_taskBlock(p):
    "taskBlock : TkId"
    pass

def p_directions(p):
    '''directions : TkNorth 
                | TkEast 
                | TkSouth 
                | TkWest'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at token", p.type)
        # Just discard the token and tell the parser it's okay.
        parser.errok()
    else:
        print("Syntax error at EOF")

#parser = yacc.yacc()