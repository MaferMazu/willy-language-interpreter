import lexer
import Node
import ply.yacc as yacc

DEBUG_MODE = False

# import some required globals from tokenizer
tokens = lexer.tokens


def p_correctProgram(p):
    "correctProgram : program"
    p[0] = p[1]

def p_program(p):
    """
    progam : worldBlock 
            | taskBlock 
            | worldBlock program
            | taskBlock program
    """
    if(len(p) < 1):
        p[0] = p[1]
    else:
        P[0] = p[1] + p[2]

    
def p_worldBlock(p):
    '''worldBlock : TkBeginWorld TkId instructions TkEndWorld worldBlock 
                    | TkBeginWorld TkId TkEndWorld worldBlock 
                    | TkBeginWorld TkId instructions TkEndWorld taskBlock '''
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

def p_worldSet(p):
    '''worldSet : TkWorld TkInt TkInt 
                | empty'''
    pass

def p_instructions(p):
    '''instructions : wallSet TkSemicolon instructions 
                     | objectTypeSet TkSemicolon instructions 
                     | placeInBasketSet TkSemicolon instructions 
                     | placeInWorldSet TkSemicolon instructions 
                     | wallSet TkSemicolon 
                     | objectTypeSet TkSemicolon 
                     | placeInBasketSet TkSemicolon 
                     | placeInWorldSet TkSemicolon      '''
    pass

def p_wallSet(p):
    'wallSet : TkWall directions TkFrom TkInt TkInt TkTo TkInt TkInt'
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
    print("Syntax error at '%s'" % p.value)

parser = yacc.yacc()