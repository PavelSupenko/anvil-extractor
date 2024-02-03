from model.export.export_entity_plugin import ExportEntityPlugin


class ExportEntityGroupPlugin(ExportEntityPlugin):
    target_type = '3F742D26'
    file_type_int = 0x3F742D26

    texture_type_int = 0xA2B7E917
    entity_type_int = 0x0984415E
    mesh_data_type_int = 0x415D9568

    plugin_name = 'Export Entity Group'
