import lexer
DEBUG_MODE = False

# import some required globals from tokenizer
tokens = lexer.tokens


def p_correctProgram(p):
    "correctProgram: program"
    p[0] = p[1]

def p_program(p):
    """
    progam: worldBlock |
            taskBlock |
            worldBlock program|
            taskBlock program
    """
    if(p.len < 1):
        p[0] = p[1]
    else:
        P[0] = p[1] + p[2]

    
def p_worldBlock(p):
    '''worldBlock : TkBeginWorld Tkid instructions TkEndWorld worldBlock |
                    TkBeginWorld Tkid TkEndWorld worldBlock |
                        TkBeginWorld Tkid instructions TkEndWorld taskBlock '''
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

def p_worldSet(p):
    'worldSet : TkWorld TkInt TkInt | empty'
    pass

def p_instructions(p):
    '''instructions : wallSet tkSemiColon instructions |
                      objectTypeSet tkSemiColon instructions | 
                      placeInBasketSet tkSemiColon instructions |
                      placeInWorldSet tkSemiColon instructions |
                      wallSet tkSemiColon |
                      objectTypeSet tkSemiColon | 
                      placeInBasketSet tkSemiColon |
                      placeInWorldSet tkSemiColon |
                      
    '''
    pass

def p_wallSet(p):
    'wallSet : TkWall directions TkFrom TkInt TkInt TkTo TkInt TkInt'
    pass

def p_directions(p):
    'directions : TkNorth | TkEast | TkSouth | TkWest'
    pass
def p_empty(p):
    'empty :'
    pass