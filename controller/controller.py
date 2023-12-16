from games.acu.acu_game_data import ACUGameData
from model.export import get_export_plugins
from model.export.export_plugin_base import ExportPluginBase
from model.tree.file_data_base import FileDataBase
from model.tree.system_directory_data import SystemDirectoryData
from model.tree.system_file_data import SystemFileData
from model.forge.forge_file_data import ForgeFileData
from model.forge.forge_files_finder import ForgeFilesFinder
from model.forge.forge_reader import ForgeReader
from view.context_menu.export_context_menu_factory import ExportContextMenuFactory
from view.view import View


class Controller:
    def __init__(self):
        # TODO: Get from view
        self.game_data = None
        self.forge_readers: dict[str, ForgeReader] = {}

        # a = get_default_type_readers()

        self.view = View(item_clicked_callback=self.handle_item_clicked,
                         plugin_clicked_callback=self.handle_export_plugin_clicked,
                         export_context_menu_factory=ExportContextMenuFactory(
                             export_plugins=get_export_plugins('output')))
        self.view.show()
        self.handle_game_path_changed("/Users/pavelsupenko/Library/Application Support/CrossOver/Bottles/Windows-10-64/drive_c/Games/Assassin's Creed Unity")
        self.view.wait()

    def reset_tree(self):
        self.view.reset_tree()

    def handle_game_path_changed(self, game_path: str):
        self.game_data = ACUGameData(path=game_path)
        game_directory_data = SystemDirectoryData(game_path)

        forge_finder = ForgeFilesFinder(game_directory_data)
        forge_files = forge_finder.find_files()

        self.reset_tree()
        self.view.add_item(parent_data=None, node_data=game_directory_data)

        print(f'Found {len(forge_files)} forge files: {forge_files}')

        for forge_file_data in forge_files:
            self.view.add_item(game_directory_data, forge_file_data)

    def handle_export_plugin_clicked(self, file_data: FileDataBase, plugin: ExportPluginBase):
        if type(file_data) is not ForgeFileData:
            print(f'Export can be applied only to forge item files')
            return

        file_data: ForgeFileData = file_data

        name = file_data.name
        print(f'Export plugin {plugin.plugin_name} on item: {file_data.get_name_data()}')

        parent_forge_file_data: SystemFileData = file_data.get_parent_forge_file_data()

        if parent_forge_file_data is None:
            print(f'Forge file not found for {name}')
            return None

        forge_reader = self.forge_readers[parent_forge_file_data.path]
        plugin.execute(forge_reader, file_data, self.game_data)

    def handle_item_clicked(self, item: FileDataBase):
        item_name = item.get_name_data()
        item_type = item.get_type_data()

        if item.children or not item.parent:
            print(f'File {item_name} is already decompressed or root')
            return

        # TODO: Add normal check to not parse already parsed forge item internal files
        if item.get_name_data() == item.parent.get_name_data():
            print(f'File {item_name} is already parsed')
            return

        if item_type == 'forge':
            self.parse_forge(item)
        else:
            self.parse_forge_item(item)

    def parse_forge(self, file_data: SystemFileData):
        path = file_data.path
        print(f'Forge file path: {path}')

        if path in self.forge_readers:
            print(f'Forge file {path} is already parsed')
            return

        forge_reader = ForgeReader(path, self.game_data)
        self.forge_readers[path] = forge_reader

        parsed_files = forge_reader.parse_forge_data()

        for parsed_file in parsed_files:
            parsed_file.add_parent(file_data)
            file_data.add_child(parsed_file)
            self.view.add_item(file_data, parsed_file)

    def parse_forge_item(self, file_data: ForgeFileData):
        name = file_data.name
        print(f'Forge item file name: {name}')

        parent_forge_file_data: SystemFileData = file_data.get_parent_forge_file_data()

        if parent_forge_file_data is None:
            print(f'Forge file not found for {name}')
            return None

        forge_reader = self.forge_readers[parent_forge_file_data.path]
        forge_reader.parse_file_data(file_data)

        for child in file_data.children:
            self.view.add_item(parent_data=file_data, node_data=child)
