from parser import Procedure, ProductionRule

START = 'Program'
TERMINALS = {'$', 'ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'else', 'while',
             'return', 'for', '=', '<', '==', '+', '-', '*', 'ε'}

PROCEDURES = {
    "Program": Procedure("Program",
                         [ProductionRule(['int', 'void', '$'],
                                         ['Declaration-list' '$'])],
                         '$'),


}
