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
    "Type-specifier": Procedure("Type-specifier",
                                [ProductionRule(['int'], ['int']),
                                 ProductionRule(['void'], ['void'])
                                 ],
                                ['ID'],
                                False),
    "Params": Procedure("Params",
                        [ProductionRule(['int'], ['int', 'ID', 'Param-prime', 'Param-list']),
                         ProductionRule(['void'], ['void', 'Param-list-void-abtar'])
                         ],
                        [')'],
                        False),
    "Param-list-void-abtar": Procedure("Param-list-void-abtar",
                                       [ProductionRule(['ID'], ['ID', 'Param-prime', 'Param-list'])
                                        ],
                                       [')'],
                                       True),
    "Param-list": Procedure("Param-list",
                            [ProductionRule([','], [',', 'Param', 'Param-list'])
                             ],
                            [')'],
                            True),
    "Param": Procedure("Param",
                       [ProductionRule(['int', 'void'], ['Declaration-initial', 'Param-prime'])
                        ],
                       [')', ','],
                       False),
    "Param-prime": Procedure("Param-prime",
                             [ProductionRule(['['], ['[', ']'])
                              ],
                             [')', ','],
                             True),
    "Compound-stmt": Procedure("Compound-stmt",
                               [ProductionRule(['{'], ['{', 'Declaration-list', 'Statement-list', '}'])
                                ],
                               ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'else', 'while',
                                'return', 'for', '+', '-'],
                               False),
    "Statement-list": Procedure("Statement-list",
                                [ProductionRule(
                                    ['ID', ',', 'NUM', '(', '{', 'break', 'if', 'while', 'return', 'for', '+', '-'],
                                    ['Statement', 'Statement-list'])
                                ],
                                ['}'],
                                True),
    "Statement": Procedure("Statement",
                           [ProductionRule(['ID', ',', 'NUM', '(', 'break', '+', '-'], ['Expression-stmt']),
                            ProductionRule(['{'], ['Compound-stmt']),
                            ProductionRule(['if'], ['Selection-stmt']),
                            ProductionRule(['while'], ['Iteration-stmt']),
                            ProductionRule(['return'], ['Return-stmt']),
                            ProductionRule(['for'], ['For-stmt']),
                            ],
                           ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+', '-'],
                           False),
    "Expression-stmt": Procedure("Expression-stmt",
                                 [ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Expression', ';']),
                                  ProductionRule(['break'], ['break', ';']),
                                  ProductionRule([';'], [';']),
                                  ],
                                 ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+',
                                  '-'],
                                 False),
    "Selection-stmt": Procedure("Selection-stmt",
                                [ProductionRule(['if'],
                                                ['if', '(', 'Expression', ')', 'Statement', 'else', 'Statement']),
                                 ],
                                ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+',
                                 '-'],
                                False),
    "Iteration-stmt": Procedure("Iteration-stmt",
                                [ProductionRule(['while'], ['while', '(', 'Expression', ')', 'Statement']),
                                 ],
                                ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+',
                                 '-'],
                                False),
    "Return-stmt": Procedure("Return-stmt",
                             [ProductionRule(['return'], ['return', 'Return-stmt-prime']),
                              ],
                             ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+',
                              '-'],
                             False),
    "Return-stmt-prime": Procedure("Return-stmt-prime",
                                   [ProductionRule([';'], [';']),
                                    ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Expression', ';']),
                                    ],
                                   ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for',
                                    '+', '-'],
                                   False),
    "For-stmt": Procedure("For-stmt",
                          [ProductionRule(['for'], ['for', 'ID', '=', 'Vars', 'Statement']),
                           ],
                          ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+', '-'],
                          False),
    "Vars": Procedure("Vars",
                      [ProductionRule(['ID'], ['Var', 'Var-zegond']),
                       ],
                      ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'while', 'return', 'for', '+', '-'],
                      False),
    "Var-zegond": Procedure("Var-zegond",
                            [ProductionRule([','], [',', 'Var', 'Var-zegond']),
                             ],
                            ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'while', 'return', 'for', '+', '-'],
                            True),
    "Var": Procedure("Var",
                     [ProductionRule(['ID'], ['ID', 'Var-prime']),
                      ],
                     ['ID', ';', 'NUM', '(', ',', '{', 'break', 'if', 'while', 'return', 'for', '+', '-'],
                     False),
    "Expression": Procedure("Expression",
                            [ProductionRule(['NUM', '(', '+', '-'], ['Simple-expression-zegond']),
                             ProductionRule(['ID'], ['ID', 'B']),
                             ],
                            [';', ']', ')', ','],
                            False),
    "B": Procedure("B",
                   [ProductionRule(['='], ['=', 'Expression']),
                    ProductionRule(['['], ['[', 'Expression', '[', 'H']),
                    ProductionRule(['(', '<', '==', '+', '-', '*'], ['Simple-expression-prime']),
                    ],
                   [';', ']', ')', ','],
                   True),
    "H": Procedure("H",
                   [ProductionRule(['='], ['=', 'Expression']),
                    ProductionRule(['<', '==', '+', '-', '*'], ['G', 'D', 'C']),
                    ],
                   [';', ']', ')', ','],
                   True),
    "Simple-expression-zegond": Procedure("Simple-expression-zegond",
                                          [ProductionRule(['NUM', '(', '+', '-'], ['Additive-expression-zegond', 'C']),
                                           ],
                                          [';', ']', ')', ','],
                                          False),
    "Simple-expression-prime": Procedure("Simple-expression-prime",
                                         [ProductionRule(['(', '+', '-', '*'], ['Additive-expression-prime', 'C']),
                                          ],
                                         [';', ']', ')', ','],
                                         True),
    "C": Procedure("C",
                   [ProductionRule(['(', '+', '-', '*'], ['Relop', 'Additive-expression']),
                    ],
                   [';', ']', ')', ','],
                   True),
    "Relop": Procedure("Relop",
                       [ProductionRule(['<'], ['<']),
                        ProductionRule(['=='], ['==']),
                        ],
                       ['ID', 'NUM', '(', '+', '-'],
                       False),
    "Additive-expression": Procedure("Additive-expression",
                                     [ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Term', 'D']),
                                      ],
                                     [';', ']', ')', ','],
                                     False),
    "Additive-expression-prime": Procedure("Additive-expression-prime",
                                           [ProductionRule(['(', '+', '-', '*'], ['Term-prime', 'D']),
                                            ],
                                           [';', ']', ')', ',', '<', '=='],
                                           True),
    "Additive-expression-zegond": Procedure("Additive-expression-zegond",
                                            [ProductionRule(['NUM', '(', '+', '-'], ['Term-zegond', 'D']),
                                             ],
                                            [';', ']', ')', ',', '<', '=='],
                                            False),
    "D": Procedure("D",
                   [ProductionRule(['NUM', '(', '+', '-'], ['Addop', 'Term', 'D']),
                    ],
                   [';', ']', ')', ',', '<', '=='],
                   True),
    "Addop": Procedure("Addop",
                       [ProductionRule(['+'], ['+']),
                        ProductionRule(['-'], ['-']),
                        ],
                       ['ID', 'NUM', '(', '+', '-'],
                       False),
    "Term": Procedure("Term",
                      [ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Signed-factor', 'G']),
                       ],
                      [';', ']', ')', ',', '<', '==', '+', '-'],
                      False),
    "Term-prime": Procedure("Term-prime",
                            [ProductionRule(['(', '*'], ['Signed-factor-prime', 'G']),
                             ],
                            [';', ']', ')', ',', '<', '==', '+', '-'],
                            True),
    "Term-zegond": Procedure("Term-zegond",
                             [ProductionRule(['NUM', '(', '+', '-'], ['Signed-factor-zegond', 'G']),
                              ],
                             [';', ']', ')', ',', '<', '==', '+', '-'],
                             False),
    "G": Procedure("G",
                   [ProductionRule(['*'], ['*', 'Signed-factor', 'G']),
                    ],
                   [';', ']', ')', ',', '<', '==', '+', '-'],
                   True),
    "Signed-factor": Procedure("Signed-factor",
                               [ProductionRule(['+'], ['+', 'Factor']),
                                ProductionRule(['-'], ['-', 'Factor']),
                                ProductionRule(['ID', 'NUM', '('], ['Factor']),
                                ],
                               [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                               False),
    "Signed-factor-prime": Procedure("Signed-factor-prime",
                                     [ProductionRule(['('], ['Factor-prime']),
                                      ],
                                     [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                                     True),
    "Signed-factor-zegond": Procedure("Signed-factor-zegond",
                                      [ProductionRule(['+'], ['+', 'Factor']),
                                       ProductionRule(['-'], ['-', 'Factor']),
                                       ProductionRule(['NUM', '('], ['Factor-zegond']),
                                       ],
                                      [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                                      False),
    "Factor": Procedure("Factor",
                        [ProductionRule(['('], ['(', 'Expression', ')']),
                         ProductionRule(['ID'], ['ID', 'Var-call-prime']),
                         ProductionRule(['NUM'], ['NUM']),
                         ],
                        [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                        False),
    "Factor-prime": Procedure("Factor-prime",
                              [ProductionRule(['('], ['(', 'Args', ')']),
                               ],
                              [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                              True),
    "Factor-zegond": Procedure("Factor-zegond",
                               [ProductionRule(['('], ['(', 'Expression', ')']),
                                ProductionRule(['NUM'], ['NUM']),
                                ],
                               [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                               False),
    "Var-call-prime": Procedure("Var-call-prime",
                                [ProductionRule(['('], ['(', 'Args', ')']),
                                 ProductionRule(['['], ['Var-prime']),
                                 ],
                                [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                                True),
    "Var-prime": Procedure("Var-prime",
                           [ProductionRule(['['], ['[', 'Expression', ']']),
                            ],
                           ['ID', ';', 'NUM', ']', '(', ')', ',', '{', 'break', 'if', 'while', 'return', 'for', '<',
                            '==', '+', '-', '*'],
                           True),
    "Args": Procedure("Args",
                      [ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Arg-list']),
                       ],
                      [')'],
                      True),
    "Arg-list": Procedure("Arg-list",
                          [ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Expression', 'Arg-list-prime']),
                           ],
                          [')'],
                          False),
    "Arg-list-prime": Procedure("Arg-list-prime",
                                [ProductionRule([','], [',', 'Expression', 'Arg-list-prime']),
                                 ],
                                [')'],
                                True),

}
