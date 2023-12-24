from games.ac2.files import AC2FileReadersFactory
from games.acu.acu_game_data import ACUGameData
from games.acu.files import ACUFileReadersFactory
from model.compression.compressor import Compressor
from model.export import ExportPluginsFactory
from model.export.export_plugin_base import ExportPluginBase
from model.settings.export_settings_loader import ExportSettingsLoader
from model.settings.game_settings import GameSettings
from model.settings.game_settings_loader import GameSettingsLoader
from model.tree.file_data_base import FileDataBase
from model.tree.system_directory_data import SystemDirectoryData
from model.tree.system_file_data import SystemFileData
from model.forge.forge_container_file_data import ForgeFileData, ForgeContainerFileData
from model.forge.forge_files_finder import ForgeFilesFinder
from model.forge.forge_reader import ForgeReader
from view.context_menu.export_context_menu_factory import ExportContextMenuFactory
from view.view import View


class Controller:
    def __init__(self):
        # TODO: Get from view
        self.game_data = None
        self.compressor = Compressor()
        self.forge_readers: dict[str, ForgeReader] = {}

        self.export_settings_loader = ExportSettingsLoader('settings')
        self.game_settings_loader = GameSettingsLoader(settings_directory_path='settings', change_callback=self.handle_game_settings_changed)
        game_settings = self.game_settings_loader.load()

        self.view = View(item_clicked_callback=self.handle_item_clicked,
                         plugin_clicked_callback=self.handle_export_plugin_clicked,
                         game_settings_changed_callback=self.handle_game_settings_changed,
                         export_settings_loader=self.export_settings_loader,
                         game_settings_loader=self.game_settings_loader)

        self.view.show()
        self.handle_game_settings_changed(game_settings)
        self.view.wait()

    def reset_tree(self):
        self.view.reset_tree()

    def handle_game_settings_changed(self, game_settings: GameSettings):
        if game_settings is None or not game_settings.is_valid:
            return

        if game_settings.preset == 'ACU':
            self.view.export_context_menu_factory = ExportContextMenuFactory(
                             export_plugins_factory=ExportPluginsFactory('output', ACUFileReadersFactory()))
        elif game_settings.preset == 'AC2':
            self.view.export_context_menu_factory = ExportContextMenuFactory(
                             export_plugins_factory=ExportPluginsFactory('output', AC2FileReadersFactory()))
        else:
            raise Exception(f'Unknown preset: {game_settings.preset}')

        game_path = game_settings.path
        self.game_data = ACUGameData(path=game_path)
        game_directory_data = SystemDirectoryData(game_path)

        forge_finder = ForgeFilesFinder(game_directory_data)
        forge_files = forge_finder.find_files()

        self.reset_tree()
        self.view.add_item(node_data=game_directory_data)

        print(f'Found {len(forge_files)} forge files: {forge_files}')

        forge_files_sorted_by_size = sorted(forge_files, key=lambda x: x.size_mb, reverse=True)
        for forge_file_data in forge_files_sorted_by_size:
            self.view.add_item(forge_file_data)
            self.parse_forge(forge_file_data)

    def handle_export_plugin_clicked(self, file_data: FileDataBase, plugin: ExportPluginBase):
        if type(file_data) is not ForgeFileData:
            print(f'Export can be applied only to forge item files')
            return

        file_data: ForgeFileData = file_data

        name = file_data.name
        print(f'Export plugin {plugin.plugin_name} on item: {file_data.full_path}')

        parent_forge_file_data: SystemFileData = file_data.get_parent_forge_file_data()

        if parent_forge_file_data is None:
            print(f'Forge file not found for {name}')
            return None

        file_forge_reader = self.forge_readers[parent_forge_file_data.path]
        plugin.execute(file_forge_reader, list(self.forge_readers.values()), file_data, self.game_data)

    def handle_item_clicked(self, item: FileDataBase):
        item_name = item.name

        if type(item) is not ForgeContainerFileData:
            print(f'File {item_name} is not a forge container file')
            return

        forge_item: ForgeContainerFileData = item

        if forge_item.children:
            print(f'File {item_name} is already decompressed')
            return

        self.parse_forge_item(forge_item)

    def parse_forge(self, file_data: SystemFileData):
        path = file_data.path
        print(f'Forge file path: {path}')

        if path in self.forge_readers:
            print(f'Forge file {path} is already parsed')
            return

        forge_reader = ForgeReader(path, self.game_data, self.compressor)
        self.forge_readers[path] = forge_reader

        parsed_files = forge_reader.parse_forge_data()

        for parsed_file in parsed_files:
            parsed_file.add_parent(file_data)
            file_data.add_child(parsed_file)
            self.view.add_item(parsed_file)

    def parse_forge_item(self, file_data: ForgeContainerFileData):
        name = file_data.name
        print(f'Forge item file name: {name}')

        parent_forge_file_data: SystemFileData = file_data.get_parent_forge_file_data()

        if parent_forge_file_data is None:
            print(f'Forge file not found for {name}')
            return None

        forge_reader = self.forge_readers[parent_forge_file_data.path]
        forge_reader.parse_file_data(file_data)

        for child in file_data.children:
            self.view.add_item(node_data=child)
