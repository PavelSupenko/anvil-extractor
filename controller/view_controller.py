from model.forge.forge_files_finder import ForgeFilesFinder
from view.view import View


class ViewController:
    def __init__(self):
        self.game_path = None

        self.view = View()

        # TODO: Get from view
        self.handle_game_path_changed(
            "/Users/pavelsupenko/Library/Application Support/CrossOver/Bottles/Windows-10-64/drive_c/Games/Assassin's Creed Unity"
        )

        forge_finder = ForgeFilesFinder(self.game_path)
        forge_files = forge_finder.find()
        print(forge_files)

    def handle_game_path_changed(self, game_path: str):
        self.game_path = game_path

        forge_finder = ForgeFilesFinder(self.game_path)
        forge_files = forge_finder.find()
        print(forge_files)
