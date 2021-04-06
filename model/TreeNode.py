class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
        self.is_leaf = True

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        self.is_leaf = False
        return child

    def get_level(self):
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level

    def print_tree(self):
        spaces = " " * self.get_level() * 3
        prefix = f'{spaces}{"|__ " if self.parent else ""}'
        print(f"{prefix}{self.data}")
        if len(self.children) > 0:
            for child in self.children:
                child.print_tree()