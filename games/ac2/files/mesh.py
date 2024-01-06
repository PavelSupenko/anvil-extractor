import numpy
import logging

from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from model.files.mesh import BaseMesh

#           vertex coords           scale factor            normals                   ?            vertex texture coords            ?               bone numbers            bone weights                  ?
VertTableTypes = {
    20: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16),    ('vt', numpy.int16, 2)],
    24: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16, 3), ('vt', numpy.int16, 2)],
    32: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16, 3), ('vt', numpy.int16, 2),                       ('bn', numpy.uint8, 4), ('bw', numpy.uint8, 4)],
}


class Reader(BaseMesh, BaseFile):
    ResourceType = 0x415D9568

    def read(self, file_id: int, model_file: FileDataWrapper):
        # There is two types of export in Archive_next: mdl and mdl_s. As I can see, ACExplorer uses only mdl.

        self.type = model_file.read_bytes(4)
        model_file.read_bytes(1)  # skip an empty byte
        a_count = model_file.read_uint_32()

        # This loop is kind of magic. Keeping it for now
        # for a in range(a_count * 2):
        #     check = model_file.read_uint_8()
        #     while check == 3:
        #         check = model_file.read_uint_8()
        #     model_file.read_bytes(1)
        #     model_file.read_file()
        # if a_count > 0:
        #     model_file.read_bytes(1)

        if a_count > 0:
            model_file.read_bytes(1)

            for i in range(2):
                model_file.read_bytes(13)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 4)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 4)
                num7 = model_file.read_int_32()

                if num7 > 0:
                    logging.warning("Undetermined block of model information.")
                    return

                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 4)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 12)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 12)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 12)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 12)
                num7 = model_file.read_int_32()

                if num7 > 0:
                    logging.warning("Undetermined block of model information.")
                    return

                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 4)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 4)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 16)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7)
                num7 = model_file.read_int_32()

                if num7 > 0:
                    logging.warning("Undetermined block of model information.")
                    return

                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 13)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 8)
                num7 = model_file.read_int_32()
                model_file.read_bytes(num7 * 4)
                model_file.read_bytes(8)

        bones_count = model_file.read_uint_32()

        if bones_count > 0:
            for i in range(bones_count):
                model_file.read_bytes(40)

        model_file.read_bytes(5)

        resource_type = model_file.read_resource_type()

        # TODO: this part should get moved to a different file technically
        if resource_type == int("FC9E1595", 16):
            model_file.read_bytes(14)
            model_file.out_file_write('Vert table width\n')
            vert_table_width = int.from_bytes(model_file.read_bytes(1), byteorder='big')

            mesh_count = model_file.read_uint_32()
            self._meshes = model_file.read_numpy([
                ('file_id', numpy.uint32),
                ('file_type', numpy.uint32),
                ('verts_used', numpy.uint32),  # this is not always perfect # meshTable.X
                ('', numpy.uint32),  # 4L
                ('vert_count', numpy.uint32),  # meshTable.Y
                ('faces_used_x3', numpy.uint32),  # meshTable.Z
                ('face_count', numpy.uint32),  # meshTable.W
                ('', numpy.uint32)  # 4L
            ], 32 * mesh_count)

            model_file.out_file_write('Shadow Table\n')
            shadow_count = model_file.read_uint_32()
            shadow_table = model_file.read_numpy([
                ('file_id', numpy.uint32),
                ('file_type', numpy.uint32),
                ('X', numpy.uint32),
                ('', numpy.uint32),
                ('Y', numpy.uint32),
                ('Z', numpy.uint32),
                ('W', numpy.uint32),
                ('', numpy.uint32),
            ], 32 * shadow_count)

            model_file.out_file_write(f'{shadow_table}\n')

            model_file.out_file_write('\nVert table\n')
            vert_table_length = model_file.read_uint_32()
            self.vert_count = vert_table_length / vert_table_width

            if vert_table_width in VertTableTypes:
                vert_table = model_file.read_numpy(VertTableTypes[vert_table_width], vert_table_length)
            else:
                logging.warning(f'Not yet implemented!\n\nvertTableWidth = {vert_table_width}')
                raise Exception()

            # Scaling according to read data
            # self._vertices = vert_table['v'].astype(numpy.float64) * numpy.sign(vert_table['sc'].reshape(-1, 1)) / 2 ** 15
            self._vertices = vert_table['v'].astype(numpy.float64) / 2 ** 15
            # self._vertices *= numpy.sum(bounding_box2, 0) / numpy.amax(self.vertices, 0)

            self._texture_vertices = vert_table['vt'].astype(numpy.float64) / 2048.0
            self._texture_vertices[:, 1] *= -1
            if 'n' in vert_table.dtype.names:
                self._normals = vert_table['n'].astype(numpy.float64)
            if 'bn' in vert_table.dtype.names:
                self.bone_numbers = vert_table['bn']
                self.bone_weights = vert_table['bw']
            else:
                self.bone_number = None
            self.vert_table = vert_table

            model_file.out_file_write('Face table\n')
            face_table_length = model_file.read_uint_32()
            face_table = model_file.read_numpy(numpy.uint16, face_table_length).reshape(-1, 3)

            if face_table is not None:
                # if use_blocks == 1:
                if False:
                    # self._faces = numpy.split(face_table, numpy.cumsum(mesh_face_blocks * 64)[:-1])
                    # for index in range(len(self._faces)):
                    #     self._faces[index] = self._faces[index][:self.meshes['face_count'][index]]  # strip the end of the block
                    #     if index >= 1:
                    #         self._faces[index] += numpy.max(self._faces[index - 1]) + 1  # add the vertex offset (each block starts from 0)
                    pass
                else:
                    faces = face_table
                    self._faces = []
                    for faces_used_x3, face_count, verts_used in zip(self.meshes['faces_used_x3'], self.meshes['face_count'], self.meshes['verts_used']):
                        self._faces.append(faces[int(faces_used_x3 / 3):int(faces_used_x3 / 3) + face_count] + verts_used)

            for index in range(5):
                skin_count_temp = model_file.read_uint_32()
                if skin_count_temp <= 0:
                    continue

                if index != 4:
                    print('Unknown block of information')
                    model_file.read_rest()
                    return

                skin_count = skin_count_temp
                skin_table = model_file.read_numpy([
                    ('file_id', numpy.uint32),
                    ('file_type', numpy.uint32),
                    ('', numpy.uint8),
                    ('bone_count', numpy.uint8),
                    ('', numpy.uint8, 9),
                    ('bones', numpy.uint8, 42)
                ], 61 * skin_count)

                model_file.out_file_write(f'{skin_table}\n')

            model_file.read_bytes(8)
            model_file.out_file_write('Material Table\n')
            material_count = model_file.read_uint_32()
            material_table = model_file.read_numpy([
                ('', numpy.uint16),
                ('file_id', numpy.uint32)
            ], 6 * material_count)

            model_file.out_file_write(f'{material_table}\n')
            self._materials = material_table['file_id']

            model_file.read_rest()  # doesn't seem to contain anything useful
        else:
            raise Exception("Error reading model file!")