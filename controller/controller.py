from model.files.files_tree import FileTree
from model.forge.forge_files_finder import ForgeFilesFinder
from view.view import View


class Controller:
    def __init__(self):
        # TODO: Get from view
        self.game_path = "/Users/pavelsupenko/Library/Application Support/CrossOver/Bottles/Windows-10-64/drive_c/Games/Assassin's Creed Unity"
        self.game_name = "Assassin's Creed Unity"

        self.view = View(FileTree(self.game_name, 0))
        self.view.show()

        self.handle_game_path_changed(self.game_path)

        self.view.wait()

    def handle_game_path_changed(self, game_path: str):
        self.game_path = game_path
        self.game_name = game_path.split('/')[-1]

        forge_finder = ForgeFilesFinder(self.game_path)
        forge_files = forge_finder.find()

        new_tree = FileTree(self.game_name, 0)

        for forge_file in forge_files:
            new_tree.add_child(self.game_name, forge_file, 0)

        self.view.update_tree(new_tree)
