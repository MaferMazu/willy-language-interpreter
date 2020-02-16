import lexer
DEBUG_MODE = False

# import some required globals from tokenizer
tokens = lexer.tokens

def p_intanceWorld(p):
    '''instanceWorld : TkBeginWorld Tkid instructions TkEndWorld instanceWorld |
                       empty'''
    pass

def p_worldSet(p):
    'worldSet : TkWorld TkInt TkInt | empty'
    pass

def p_instructions(p):
    '''instructions : wallSet instructions |
                      objectTypeSet instructions | 
                      placeInBasketSet instructions |
                      placeInWorldSet instructions |
                      
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