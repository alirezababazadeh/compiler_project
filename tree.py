# from anytree import Node


def toleave(branch):
    if branch[1:] == []:
        return [branch[0]]
    else:
        return [toleave(branch[1:])]


# fold the flattened tree
def fold(flattened_tree):
    if flattened_tree == []:
        return []
    else:
        return toleave(flattened_tree[0]) + fold(flattened_tree[1:])


# decorator for rendering
def render(f):
    render.level = -2
    indent = '   '

    def _f(*args):
        render.level += 1
        try:
            result = f(*args)
            if not isinstance(result, list):
                print(render.level * indent, result)
        finally:
            render.level = -2
        return result

    return _f


# go over a tree and render it
@render
def tree_render(tree):
    if not isinstance(tree, list):
        return tree
    elif tree == []:
        return []
    else:
        return [tree_render(tree[0])] + [tree_render(tree[1:])]


def main():
    flattened_tree = [[1], [1, 2], [1, 2, 5], [1, 2, 8], [1, 2, 5, 3], [1, 2, 6], [1, 2, 6, 7], [1, 2, 4]]
    tree_render(fold(flattened_tree))


# def main():
#     udo = Node("Udo")
#     marc = Node("Marc")
#     lian = Node("Lian", parent=marc)
#     print(RenderTree(udo))
#     Node('/Udo')
#     print(RenderTree(marc))
#     Node('/Marc')


if __name__ == '__main__':
    main()
