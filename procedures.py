from parser import Procedure, ProductionRule

START = 'Program'
TERMINALS = {'$', 'ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'else', 'while',
             'return', 'for', '=', '<', '==', '+', '-', '*', 'ε'}

PROCEDURES = {
    "Program": Procedure("Program",
                         [ProductionRule(['int', 'void', '$'], ['Declaration-list', '$'])
                          ],
                         ['$'],
                         False),
    "Declaration-list": Procedure("Declaration-list",
                                  [ProductionRule(['int', 'void'], ['Declaration', 'Declaration-list'])
                                   ],
                                  ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'while', 'return', 'for', '+',
                                   '-'],
                                  True),
    "Declaration": Procedure("Declaration",
                             [ProductionRule(['int', 'void'], ['Declaration-initial', 'Declaration-prime'])
                              ],
                             ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while', 'return',
                              'for', '+', '-'],
                             False),
    "Declaration-initial": Procedure("Declaration-initial",
                                     [ProductionRule(['int', 'void'], ['Type-specifier', 'ID'])
                                      ],
                                     [';', '[', '(', ')', ','],
                                     False),
    "Declaration-prime": Procedure("Declaration-prime",
                                   [ProductionRule([';', '['], ['Var-declaration-prime']),
                                    ProductionRule(['('], ['Fun-declaration-prime'])
                                    ],
                                   ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while',
                                    'return', 'for', '+', '-'],
                                   False),
    "Var-declaration-prime": Procedure("Var-declaration-prime",
                                       [ProductionRule([';'], [';']),
                                        ProductionRule(['['], ['[', 'NUM', ']', ';'])
                                        ],
                                       ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while',
                                        'return', 'for', '+', '-'],
                                       False),
    "Fun-declaration-prime": Procedure("Fun-declaration-prime",
                                       [ProductionRule(['('], ['(', 'Params', ')', 'Compound-stmt'])
                                        ],
                                       ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while',
                                        'return', 'for', '+', '-'],
                                       False),

}
