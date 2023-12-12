from model.export.export_plugin_base import ExportPluginBase


class TextureExportPlugin(ExportPluginBase):
    def __init__(self, output_directory_path: str):
        super().__init__('A2B7E917', 'Export DDS', output_directory_path)
