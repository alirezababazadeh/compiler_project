# from anytree import Node
from anytree import Node, RenderTree


class InternalNode:
    def __init__(self, name, father):
        self.father = father
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)


class Tree:
    def __init__(self):
        self.root = None

    def set_root(self, node):
        self.root = node


class TreeGenerator:
    def __init__(self):
        self.current_node = None
        self.tree = Tree()

    def add_node(self, node_name):
        if self.current_node is None:
            root = InternalNode(node_name, None)
            self.tree.set_root(root)
            self.current_node = root
        else:
            node = InternalNode(node_name, self.current_node)
            self.current_node.add_child(node)
            self.current_node = node

    def level_up(self):
        # if self.current_node.father is None:
        #     raise Exception("root node doesn't have any father")
        self.current_node = self.current_node.father


class TreeRenderer:
    def __init__(self, tree):
        self.tree = tree
        self.root = Node(self.tree.root.name)

    def render(self):
        current_node = self.root
        internal_current_node = self.tree.root
        self.recursive_renderer(internal_current_node, current_node)

        tree_string = ''
        for pre, _, node in RenderTree(self.root):
            tree_string += f"{pre}{node.name}\n"
        return tree_string

    def recursive_renderer(self, internal_current_node, any_tree_current_node):
        for child in internal_current_node.children:
            new_node = Node(child.name, parent=any_tree_current_node)
            self.recursive_renderer(child, new_node)

    def write_to_file(self, path):
        open(path, 'w', encoding='utf-8').write(self.render())
