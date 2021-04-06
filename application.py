import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from treelib import Node, Tree
from treelib.exceptions import DuplicatedNodeIdError
from model.TreeNode import TreeNode


def sanitize_id(id):
    return "_".join(list(map(lambda x: x.lower(), id.split(" "))))


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("300x100")
        self.pack()
        self.create_widgets()
        self.init_tree()
        self.init_custom_tree()

    def create_widgets(self):
        self.initial_label = tk.Label(self)
        self.initial_label["text"] = "Pense em um prato que gosta"
        self.initial_label.pack(side="top")

        self.start_button = tk.Button(self)
        self.start_button["text"] = "Ok (treelib)"
        self.start_button["command"] = self.run_game
        self.start_button.pack(side="bottom")

        self.start_button2 = tk.Button(self)
        self.start_button2["text"] = "Ok (custom)"
        self.start_button2["command"] = self.run_game2
        self.start_button2.pack(side="bottom")

    def init_tree(self):
        tree = Tree()
        tree.create_node("Root", "root")
        tree.create_node(
            "Massa",
            "massa",
            parent="root",
        )
        tree.create_node(
            "Bolo de Chocolate",
            "bolo_chocolate",
            parent="root",
        )
        tree.create_node(
            "Macarrão",
            "macarrao",
            parent="massa",
        )
        tree.show()
        self.tree = tree

    def init_custom_tree(self):
        root = TreeNode("root")

        massa = root.add_child(TreeNode("Massa"))
        massa.add_child(TreeNode("Macarrão"))

        root.add_child(TreeNode("Bolo de Chocolate"))
        root.print_tree()
        self.custom_tree = root

    def run_through_tree(self, tree, last_node="root"):
        right_answer = False
        last_leaf = None
        for identifier in sorted(
            tree[last_node].fpointer, key=lambda x: self.tree[x].is_leaf()
        ):
            node = self.tree[identifier]

            if node.is_leaf():
                last_leaf = identifier
            else:
                last_node = identifier

            if messagebox.askyesno(
                "Question", f"O prato que voce pensou é {node.tag}?"
            ):
                last_leaf = None
                if node.is_leaf():
                    right_answer = True
                else:
                    sub_tree = self.tree.subtree(identifier)

                    right_answer, last_node, last_leaf = self.run_through_tree(
                        sub_tree, identifier
                    )
                break
            elif node.is_leaf():
                last_node = self.tree[last_leaf].bpointer

        return right_answer, last_node, last_leaf

    def run_game(self):
        right_answer, last_node, last_leaf = self.run_through_tree(self.tree)
        if right_answer:
            messagebox.showinfo(message="Acertei de novo!")
        else:
            food_name = askstring("Desisto", "Qual prato você pensou?")

            if not food_name:
                return

            food_type = askstring(
                "Complete",
                f"{food_name} é ______ mas {self.tree[last_leaf or last_node].tag} não.",
            )

            if not food_type:
                return

            food_type_identifier = sanitize_id(food_type)
            food_name_identifier = sanitize_id(food_name)

            try:
                self.tree.create_node(
                    food_type,
                    food_type_identifier,
                    parent=last_node,
                )
                self.tree.create_node(
                    food_name,
                    food_name_identifier,
                    parent=food_type_identifier,
                )
                self.tree.show()
            except DuplicatedNodeIdError:
                messagebox.showerror(
                    message=f"Comida não cadastrada, {food_type} ou {food_name} já existem"
                )

    def run_through_tree2(self, tree, last_node=None):
        right_answer = False
        last_leaf = None

        for node in sorted(tree.children, key=lambda x: x.is_leaf):
            if node.is_leaf:
                last_leaf = node
            else:
                last_node = node

            if messagebox.askyesno(
                "Question", f"O prato que voce pensou é {node.data}?"
            ):
                if node.is_leaf:
                    right_answer = True
                else:
                    sub_tree = node
                    right_answer, last_node, last_leaf = self.run_through_tree2(
                        sub_tree, last_node
                    )
                break
            else:
                last_node = (
                    last_leaf.parent if node.is_leaf else last_node.parent
                )

        return right_answer, last_node, last_leaf

    def run_game2(self):
        right_answer, last_node, last_leaf = self.run_through_tree2(
            self.custom_tree, self.custom_tree
        )
        if right_answer:
            messagebox.showinfo(message="Acertei de novo!")
        else:
            food_name = askstring("Desisto", "Qual prato você pensou?")

            if not food_name:
                return

            last_visited = last_leaf or last_node
            food_type = askstring(
                "Complete",
                f"{food_name} é ______ mas {last_visited.data} não.",
            )

            if not food_type:
                return

            food = last_node.add_child(TreeNode(food_type))
            food.add_child(TreeNode(food_name))
            self.custom_tree.print_tree()