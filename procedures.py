from parser import Procedure, ProductionRule

START = 'Program'
TERMINALS = {'$', 'ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'else', 'while',
             'return', 'for', '=', '<', '==', '+', '-', '*', 'ε'}

PROCEDURES = {
    "Program": Procedure("Program",
                         [ProductionRule(['int', 'void', '$'],
                                         ['Declaration-list' '$'])
                          ],
                         ['$'],
                         False),
    "Declaration-list": Procedure("Declaration-list",
                                  [ProductionRule(['int', 'void'],
                                                  ['Declaration' 'Declaration-list'])
                                   ],
                                  ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'while', 'return', 'for', '+',
                                   '-'],
                                  True),
    "Declaration": Procedure("Declaration",
                             [ProductionRule(['int', 'void'],
                                             ['Declaration-initial' 'Declaration-prime'])
                              ],
                             ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while', 'return',
                              'for', '+', '-'],
                             False),

}
