# Intro
Gourmet Game

# Instruções
Executar em ordem:
    `pip install -r requirements.txt`
    `python main.py`

###### Para não haver necessidade de dar pip install, remover partes referentes a treelib do codigo 
    application.py:
        from treelib import Node, Tree
        from treelib.exceptions import DuplicatedNodeIdErrorrror
        def run_through_tree()
        def run_game()
        def init_tree()

###### Da função create_widgets:
    self.start_button = tk.Button(self)
    self.start_button["text"] = "Ok (treelib)"
    self.start_button["command"] = self.run_game
    self.start_button.pack(side="bottom")
