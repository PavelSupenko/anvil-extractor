from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.api.files.texture import Material
import logging


@register_file_reader('D70E6670')
class Reader(BaseFile, Material):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):

        BaseFile.__init__(self, file_id, file)
        Material.__init__(self, None)

        texture_table = file.read_numpy([('', '<u2'), ('texture_id', '<u8')], 120)
        self.diffuse, self.normal, self.specular, \
            self.height, tex5, self.transmission, tex7, \
            self.mask1, self.mask2, tex10, tex11, tex12 \
            = [texture_id if texture_id != 0 else None for texture_id in texture_table['texture_id']]

        for var, pos in [[tex5, 5], [tex7, 7], [tex10, 10], [tex11, 11], [tex12, 12]]:
            if var is not None:
                logging.info(f'found a texture set with an id in position {pos}')
