from model.export.export_plugin_base import ExportPluginBase
from model.forge.forge_reader import ForgeReader


class ExportBinaryPlugin(ExportPluginBase):
    def __init__(self, output_directory_path: str):
        super().__init__('*', 'Export Binary', output_directory_path)
