import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from treelib import Node, Tree
from treelib.exceptions import DuplicatedNodeIdError


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("300x100")
        self.pack()
        self.create_widgets()
        self.init_tree()

    def create_widgets(self):
        self.initial_label = tk.Label(self)
        self.initial_label["text"] = "Pense em um prato que gosta"
        self.initial_label.pack(side="top")

        self.start_button = tk.Button(self)
        self.start_button["text"] = "Ok"
        self.start_button["command"] = self.run_game
        self.start_button.pack(side="top")

    def init_tree(self):
        tree = Tree()
        tree.create_node("Root", "root")
        tree.create_node(
            "Massa",
            "massa",
            parent="root",
        )
        tree.create_node(
            "Bolo",
            "bolo",
            parent="root",
        )
        tree.create_node(
            "Bolo de Chocolate",
            "bolo_chocolate",
            parent="bolo",
        )
        tree.create_node(
            "Macarrão",
            "macarrao",
            parent="massa",
        )
        tree.show()
        self.tree = tree

    def run_through_tree(self, tree, last_node="root"):
        right_answer = False
        last_leaf = None
        for identifier in tree[last_node].fpointer:
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

            food_type_identifier = "_".join(
                list(map(lambda x: x.lower(), food_type.split(" ")))
            )
            food_name_identifier = "_".join(
                list(map(lambda x: x.lower(), food_name.split(" ")))
            )

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
