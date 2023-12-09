from model.files.tree.file_data import FileData
from model.files.tree.files_tree import FileTree
from model.forge.forge_files_finder import ForgeFilesFinder
from model.forge.forge_reader import ForgeReader
from view.view import View


class Controller:
    def __init__(self):
        # TODO: Get from view
        self.game_path = "/Users/pavelsupenko/Library/Application Support/CrossOver/Bottles/Windows-10-64/drive_c/Games/Assassin's Creed Unity"
        self.game_name = "Assassin's Creed Unity"

        self.current_tree: FileTree = None
        self.view = View(item_clicked_callback=self.handle_item_clicked)
        self.view.show()

        self.handle_game_path_changed(self.game_path)

        self.view.wait()

    def reset_tree(self, tree: FileTree):
        self.current_tree = tree
        self.view.reset_tree(tree)

    def update_tree(self, parent_name: str, node_data: FileData):
        self.view.update_tree(parent_name, node_data)

    def handle_game_path_changed(self, game_path: str):
        self.game_path = game_path
        self.game_name = game_path.split('/')[-1]

        forge_finder = ForgeFilesFinder(self.game_path)
        forge_files = forge_finder.find()

        print(f'Found {len(forge_files)} forge files: {forge_files}')

        new_tree = FileTree(self.game_name, 0)

        for forge_file in forge_files.values():
            new_tree.add_child(self.game_name, forge_file, 0)

        self.reset_tree(new_tree)

    def handle_item_clicked(self, item_name: str):
        print(f'File: {item_name} double clicked')

        clicked_file_data: FileData = self.current_tree.find_file_by_name(item_name)

        if clicked_file_data is None:
            print(f'File data not found for {item_name}')
            return

        if clicked_file_data.children:
            print(f'File {item_name} is already decompressed')
            return

        if clicked_file_data.type == 'forge':
            self.update_tree_by_parsing_forge(clicked_file_data)

    def update_tree_by_parsing_forge(self, file_data: FileData):
        path = file_data.path
        print(f'File path: {path}')

        forge_reader = ForgeReader(path, data_file_format=3)
        parsed_files = forge_reader.parse()

        for parsed_file in parsed_files:
            file_data.children.append(parsed_file)
            self.update_tree(file_data.name, parsed_file)
