START = 'Program'
TERMINALS = {'$', 'ID', ';', '[', 'NUM', ']', '(', ')', 'int', 'void', ',', '{', '}', 'break', 'if', 'else', 'while',
             'return', 'for', '=', '<', '==', '+', '-', '*', 'ε'}


class Procedure:
    def __init__(self, name, production_rules, follow, has_epsilon_in_first, has_epsilon_rule=False):
        self.has_epsilon_in_first = has_epsilon_in_first
        self.name = name
        self.production_rules = production_rules
        self.follow = follow
        self.has_epsilon_rule = has_epsilon_rule


class ProductionRule:
    def __init__(self, first, sentence):
        self.first = first
        self.sentence = sentence


PROCEDURES = {
    "Program": Procedure("Program",
                         [ProductionRule(['int', 'void', '$'], ['Declaration-list', '#EOP' '$'])
                          ],
                         ['$'],
                         False, False),
    "Declaration-list": Procedure("Declaration-list",
                                  [ProductionRule(['int', 'void'], ['Declaration', 'Declaration-list'])
                                   ],
                                  ['$', 'ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'while', 'return', 'for', '+',
                                   '-'],
                                  True, True),
    "Declaration": Procedure("Declaration",
                             [ProductionRule(['int', 'void'], ['Declaration-initial', 'Declaration-prime'])
                              ],
                             ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while', 'return',
                              'for', '+', '-'],
                             False, False),
    "Declaration-initial": Procedure("Declaration-initial",
                                     [ProductionRule(['int', 'void'], ['#ptype', 'Type-specifier', '#pid', 'ID'])
                                      ],
                                     [';', '[', '(', ')', ','],
                                     False, False),
    "Declaration-prime": Procedure("Declaration-prime",
                                   [ProductionRule([';', '['], ['Var-declaration-prime']),
                                    ProductionRule(['('], ['#func_start', 'Fun-declaration-prime'])
                                    ],
                                   ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while',
                                    'return', 'for', '+', '-'],
                                   False, False),
    "Var-declaration-prime": Procedure("Var-declaration-prime",
                                       [ProductionRule([';'], ['#declare', ';']),
                                        ProductionRule(['['], ['[', '#pnum', 'NUM', ']', '#declare_array', ';'])
                                        ],
                                       ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while',
                                        'return', 'for', '+', '-'],
                                       False, False),
    "Fun-declaration-prime": Procedure("Fun-declaration-prime",
                                       [ProductionRule(['('],
                                                       ['(', 'Params', ')', '#func_def', 'Compound-stmt', '#func_end'])
                                        ],
                                       ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'while',
                                        'return', 'for', '+', '-'],
                                       False, False),
    "Type-specifier": Procedure("Type-specifier",
                                [ProductionRule(['int'], ['int']),
                                 ProductionRule(['void'], ['void'])
                                 ],
                                ['ID'],
                                False, False),
    "Params": Procedure("Params",
                        [ProductionRule(['int'],
                                        ['#ptype', 'int', '#pid', 'ID', 'Param-prime', '#declare_param', 'Param-list']),
                         ProductionRule(['void'], ['void', 'Param-list-void-abtar'])
                         ],
                        [')'],
                        False, False),
    "Param-list-void-abtar": Procedure("Param-list-void-abtar",
                                       [ProductionRule(['ID'], ['ID', 'Param-prime', 'Param-list'])
                                        ],
                                       [')'],
                                       True, True),
    "Param-list": Procedure("Param-list",
                            [ProductionRule([','], [',', 'Param', 'Param-list'])
                             ],
                            [')'],
                            True, True),
    "Param": Procedure("Param",
                       [ProductionRule(['int', 'void'], ['Declaration-initial', 'Param-prime', '#declare_param'])
                        ],
                       [')', ','],
                       False, False),
    "Param-prime": Procedure("Param-prime",
                             [ProductionRule(['['], ['[', ']', '#param_array']),
                              ProductionRule(['epsilon'], ['#param'])
                              ],
                             [')', ','],
                             True, True),
    "Compound-stmt": Procedure("Compound-stmt",
                               [ProductionRule(['{'], ['{', 'Declaration-list', 'Statement-list', '}'])
                                ],
                               ['$', 'ID', ';', 'NUM', '(', 'int', 'void', '{', '}', 'break', 'if', 'else', 'while',
                                'return', 'for', '+', '-'],
                               False),
    "Statement-list": Procedure("Statement-list",
                                [ProductionRule(
                                    ['ID', ';', 'NUM', '(', '{', 'break', 'if', 'while', 'return', 'for', '+', '-'],
                                    ['Statement', 'Statement-list'])
                                ],
                                ['}'],
                                True, True),
    "Statement": Procedure("Statement",
                           [ProductionRule(['ID', ';', 'NUM', '(', 'break', '+', '-'], ['Expression-stmt']),
                            ProductionRule(['{'], ['Compound-stmt']),
                            ProductionRule(['if'], ['Selection-stmt']),
                            ProductionRule(['while'], ['Iteration-stmt']),
                            ProductionRule(['return'], ['Return-stmt']),
                            ProductionRule(['for'], ['For-stmt']),
                            ],
                           ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+', '-'],
                           False),
    "Expression-stmt": Procedure("Expression-stmt",
                                 [ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Expression', ';', '#pop']),
                                  ProductionRule(['break'], ['#break', 'break', ';']),
                                  ProductionRule([';'], [';']),
                                  ],
                                 ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+',
                                  '-'],
                                 False),
    "Selection-stmt": Procedure("Selection-stmt",
                                [ProductionRule(['if'],
                                                ['if', '(', 'Expression', ')', '#save', 'Statement',
                                                 'else', '#jpf_save', 'Statement', '#jp']),
                                 ],
                                ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+',
                                 '-'],
                                False),
    "Iteration-stmt": Procedure("Iteration-stmt",
                                [ProductionRule(['while'],
                                                ['#iteration_break', 'while', '#label', '(', 'Expression', ')', '#save',
                                                 'Statement',
                                                 '#while']),
                                 ],
                                ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+',
                                 '-'],
                                False),
    "Return-stmt": Procedure("Return-stmt",
                             [ProductionRule(['return'], ['return', 'Return-stmt-prime', '#return']),
                              ],
                             ['ID', ';', 'NUM', '(', '{', '}', 'break', 'if', 'else', 'while', 'return', 'for', '+',
                              '-'],
                             False),
    "Return-stmt-prime": Procedure("Return-stmt-prime",
                                   [ProductionRule([';'], ['#pnum', ';']),
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
                            True, True),
    "Var": Procedure("Var",
                     [ProductionRule(['ID'], ['ID', 'Var-prime']),
                      ],
                     ['ID', ';', 'NUM', '(', ',', '{', 'break', 'if', 'while', 'return', 'for', '+', '-'],
                     False),
    "Expression": Procedure("Expression",
                            [ProductionRule(['NUM', '(', '+', '-'], ['Simple-expression-zegond']),
                             ProductionRule(['ID'], ['#pid', 'ID', 'B']),
                             ],
                            [';', ']', ')', ','],
                            False),
    "B": Procedure("B",
                   [ProductionRule(['='], ['=', 'Expression', '#assign']),
                    ProductionRule(['['], ['[', 'Expression', ']', '#array_usage', 'H']),
                    ProductionRule(['(', '<', '==', '+', '-', '*'], ['Simple-expression-prime']),
                    ],
                   [';', ']', ')', ','],
                   True),
    "H": Procedure("H",
                   [ProductionRule(['='], ['=', 'Expression', '#assign']),
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
                                         [ProductionRule(['(', '<', '==', '+', '-', '*'],
                                                         ['Additive-expression-prime', 'C']),
                                          ],
                                         [';', ']', ')', ','],
                                         True),
    "C": Procedure("C",
                   [ProductionRule(['<', '=='], ['#push_op', 'Relop', 'Additive-expression', '#relop']),
                    ],
                   [';', ']', ')', ','],
                   True, True),
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
                   [ProductionRule(['+', '-'], ['#push_op', 'Addop', 'Term', '#add_or_sub', 'D']),
                    ],
                   [';', ']', ')', ',', '<', '=='],
                   True, True),
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
                   [ProductionRule(['*'], ['*', 'Signed-factor', '#mult', 'G']),
                    ],
                   [';', ']', ')', ',', '<', '==', '+', '-'],
                   True, True),
    "Signed-factor": Procedure("Signed-factor",
                               [ProductionRule(['+'], ['+', 'Factor']),
                                ProductionRule(['-'], ['-', 'Factor', '#neg_fac']),
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
                         ProductionRule(['ID'], ['#pid', 'ID', 'Var-call-prime']),
                         ProductionRule(['NUM'], ['#pnum', 'NUM']),
                         ],
                        [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                        False),
    "Factor-prime": Procedure("Factor-prime",
                              [ProductionRule(['('], ['#start_func_call', '(', 'Args', ')', '#end_func_call']),
                               ],
                              [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                              True, True),
    "Factor-zegond": Procedure("Factor-zegond",
                               [ProductionRule(['('], ['(', 'Expression', ')']),
                                ProductionRule(['NUM'], ['#pnum', 'NUM']),
                                ],
                               [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                               False),
    "Var-call-prime": Procedure("Var-call-prime",
                                [ProductionRule(['('], ['#start_func_call''(', 'Args', ')', '#end_func_call']),
                                 ProductionRule(['['], ['Var-prime']),
                                 ],
                                [';', ']', ')', ',', '<', '==', '+', '-', '*'],
                                True),
    "Var-prime": Procedure("Var-prime",
                           [ProductionRule(['['], ['[', 'Expression', ']', '#array_usage']),
                            ],
                           ['ID', ';', 'NUM', ']', '(', ')', ',', '{', 'break', 'if', 'while', 'return', 'for', '<',
                            '==', '+', '-', '*'],
                           True, True),
    "Args": Procedure("Args",
                      [ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Arg-list']),
                       ],
                      [')'],
                      True, True),
    "Arg-list": Procedure("Arg-list",
                          [ProductionRule(['ID', 'NUM', '(', '+', '-'], ['Expression', 'Arg-list-prime']),
                           ],
                          [')'],
                          False),
    "Arg-list-prime": Procedure("Arg-list-prime",
                                [ProductionRule([','], [',', 'Expression', 'Arg-list-prime']),
                                 ],
                                [')'],
                                True, True),

}
