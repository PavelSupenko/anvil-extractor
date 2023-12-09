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
        self.forge_readers: dict[str, ForgeReader] = {}

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
            self.parse_forge(clicked_file_data)
        else:
            self.parse_forge_item(clicked_file_data)

    def parse_forge(self, file_data: FileData):
        path = file_data.path
        print(f'Forge file path: {path}')

        if path in self.forge_readers:
            print(f'Forge file {path} is already parsed')
            return

        forge_reader = ForgeReader(path, data_file_format=3)
        self.forge_readers[path] = forge_reader

        parsed_files = forge_reader.parse_forge_data()

        for parsed_file in parsed_files:
            parsed_file.parent = file_data
            file_data.children.append(parsed_file)
            self.update_tree(file_data.name, parsed_file)

    def parse_forge_item(self, file_data: FileData):
        name = file_data.name
        print(f'Forge item file name: {name}')

        parent_forge_file_data: FileData = None
        iterative_parent: FileData = file_data

        while iterative_parent.parent is not None:
            iterative_parent = iterative_parent.parent
            if iterative_parent.type == 'forge':
                parent_forge_file_data = iterative_parent
                break

        if parent_forge_file_data is None:
            print(f'Forge file not found for {name}')
            return

        forge_reader = self.forge_readers[parent_forge_file_data.path]
        forge_reader.parse_file_data(file_data)

        for child in file_data.children:
            self.update_tree(name, child)
