import numpy
import logging

from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from model.files.mesh import BaseMesh

#           vertex coords           scale factor            normals                   ?            vertex texture coords            ?               bone numbers            bone weights                  ?
VertTableTypes = {
    16: [('v', numpy.int16, 3), ('sc', numpy.int16),                        ('', numpy.int16, 2), ('vt', numpy.int16, 2)],
    20: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16),    ('vt', numpy.int16, 2)],
    24: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16, 3), ('vt', numpy.int16, 2)],
    28: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16, 3), ('vt', numpy.int16, 2), ('', numpy.int16, 2), ],
    32: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16, 3), ('vt', numpy.int16, 2),                       ('bn', numpy.uint8, 4), ('bw', numpy.uint8, 4)],
    36: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16, 3), ('vt', numpy.int16, 2), ('', numpy.int16, 2), ('bn', numpy.uint8, 4), ('bw', numpy.uint8, 4)],
    40: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16, 3), ('vt', numpy.int16, 2),                       ('bn', numpy.uint8, 8), ('bw', numpy.uint8, 8)],
    48: [('v', numpy.int16, 3), ('sc', numpy.int16), ('n', numpy.int16, 3), ('', numpy.int16, 3), ('vt', numpy.int16, 2), ('', numpy.int16, 2), ('bn', numpy.uint8, 8), ('bw', numpy.uint8, 8), ('', numpy.int16, 2)]
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
        #self._bones = [model_file.read_file() for _ in range(bones_count)]

        if bones_count > 0:
            for i in range(bones_count):
                model_file.read_bytes(40)

        model_file.read_bytes(5)

        # self.bounding_box = model_file.read_numpy(numpy.float32, 32).reshape(2, 4)
        # model_file.out_file_write(f'{self.bounding_box}\n')

        # model_file.read_bytes(1)

        # model_file.read_file_id()

        resource_type = model_file.read_resource_type()

        # TODO: this part should get moved to a different file technically
        if resource_type == int("FC9E1595", 16):
            model_file.read_bytes(14)
            model_file.out_file_write('Vert table width\n')
            vert_table_width = model_file.read_bytes(1)

            mesh_count = model_file.read_uint_32()
            self._meshes = model_file.read_numpy([
                ('file_id', numpy.uint32),
                ('file_type', numpy.uint32),
                ('verts_used', numpy.uint32),  # this is not always perfect # meshTable.X
                ('', numpy.uint32),  # 4L
                ('vert_count', numpy.uint32),  # meshTable.Y
                ('faces_used_x3', numpy.uint32),  # meshTable.Z
                ('face_count', numpy.uint32),  # meshTable.W
                ('', numpy.uint32)
            ], 32 * mesh_count)



        # TODO: this part should get moved to a different file technically
        if False and resource_type == int("FC9E1595", 16):
            model_file.read_bytes(4)
            model_file.out_file_write('Typeswitch\n')
            type_switch = model_file.read_uint_8()
            use_blocks = 0
            face_table = None
            mesh_face_blocks = None
            if type_switch == 0:
                model_file.read_file_id()
                model_file.read_resource_type()  # C351EE43
                model_file.read_bytes(5)
                model_file.out_file_write('Vert table width\n')
                vert_table_width = model_file.read_uint_32()
                mesh_face_block_sum = model_file.read_uint_32()  # = sum(mesh_face_blocks)
                bounding_box2 = model_file.read_numpy(numpy.float32, 24).reshape(2, 3)
                mesh_face_block_count = model_file.read_uint_32()
                shadow_face_block_count = model_file.read_uint_32()
                model_file.out_file_write('Mesh Face Blocks\n')
                mesh_face_blocks = model_file.read_numpy(numpy.uint32, 4 * mesh_face_block_count)
                shadow_face_blocks = model_file.read_numpy(numpy.uint32, 4 * shadow_face_block_count)
                model_file.read_uint_32()
                use_blocks = model_file.read_uint_8()  # use blocks?
                model_file.out_file_write('\nVert table\n')
                vert_table_length = model_file.read_uint_32()
                self.vert_count = vert_table_length / vert_table_width

                if vert_table_width in VertTableTypes:
                    vert_table = model_file.read_numpy(VertTableTypes[vert_table_width], vert_table_length)

                else:
                    logging.warning(f'Not yet implemented!\n\nvertTableWidth = {vert_table_width}')
                    raise Exception()

                self._vertices = vert_table['v'].astype(numpy.float64) * numpy.sign(vert_table['sc'].reshape(-1, 1)) / 2 ** 15
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
                # self._faces = numpy.split(face_table, numpy.cumsum(mesh_face_blocks * 64)[:-1])
                #
                #
                # mesh_face_blocks_x64 = numpy.cumsum(mesh_face_blocks * 64)
                # mesh_face_blocks_x64[-1] =
                # mesh_face_blocks[-1] =* 64 * 6 == face_table_length:
                # 	self._faces = [face_table[64*mesh_face_blocks[index-1]:64*block_count] for index, block_count in enumerate(mesh_face_blocks)]
                # self._faces = [face_table[:64 * block_count] if index==0 else face_table[64*mesh_face_blocks[index-1]:64*block_count] for index, block_count in enumerate(mesh_face_blocks)]

                for _ in range(3):
                    count = model_file.read_uint_32()
                    model_file.read_bytes(count)

            model_file.read_file_id()
            model_file.read_resource_type()  # 0645ABB5
            model_file.read_bytes(3)
            model_file.out_file_write('Mesh Table\n')
            mesh_count = model_file.read_uint_32()
            self._meshes = model_file.read_numpy([
                ('file_id', numpy.uint64),
                ('file_type', numpy.uint32),
                ('verts_used', numpy.uint32),  # this is not always perfect
                ('', numpy.uint32),
                ('vert_count', numpy.uint32),
                ('faces_used_x3', numpy.uint32),
                ('face_count', numpy.uint32),
                ('', numpy.uint32)
            ], 36 * mesh_count)

            if face_table is not None:
                if use_blocks == 1:
                    self._faces = numpy.split(face_table, numpy.cumsum(mesh_face_blocks * 64)[:-1])
                    for index in range(len(self._faces)):
                        self._faces[index] = self._faces[index][:self.meshes['face_count'][index]]  # strip the end of the block
                        if index >= 1:
                            self._faces[index] += numpy.max(self._faces[index - 1]) + 1  # add the vertex offset (each block starts from 0)
                else:
                    faces = face_table
                    self._faces = []
                    for faces_used_x3, face_count, verts_used in zip(self.meshes['faces_used_x3'], self.meshes['face_count'], self.meshes['verts_used']):
                        self._faces.append(faces[int(faces_used_x3 / 3):int(faces_used_x3 / 3) + face_count] + verts_used)

            model_file.out_file_write('Shadow Table\n')
            shadow_count = model_file.read_uint_32()
            shadow_table = model_file.read_numpy([
                ('file_id', numpy.uint64),
                ('file_type', numpy.uint32),
                ('X', numpy.uint32),
                ('', numpy.uint32),
                ('Y', numpy.uint32),
                ('Z', numpy.uint32),
                ('W', numpy.uint32),
                ('', numpy.uint32),
            ], 36 * shadow_count)

            model_file.out_file_write(f'{shadow_table}\n')

            for index in range(2):
                count = model_file.read_uint_32()
                with model_file.indent:
                    model_file.read_bytes(count)

            model_file.out_file_write('Skin Data Table\n')
            skin_count = model_file.read_uint_32()
            skin_table = model_file.read_numpy([
                ('file_id', numpy.uint64),
                ('file_type', numpy.uint32),
                ('', numpy.int8),
                ('', numpy.uint32),
                ('bone_count', numpy.uint16),
                ('', numpy.int8, 11),
                ('bones', numpy.uint16, 128)
            ], 286 * skin_count)

            model_file.out_file_write(f'{skin_table}\n')

            model_file.read_bytes(8)
            model_file.out_file_write('Model Scale\n')
            model_scale = model_file.read_float_32()  # model scale? (looks to be the magnitude of sc in the vert table)
            self._vertices *= model_scale
            model_file.out_file_write('Material Table\n')
            material_count = model_file.read_uint_32()
            material_table = model_file.read_numpy([
                ('', numpy.uint16),
                ('file_id', numpy.uint64)
            ], 10 * material_count)

            model_file.out_file_write(f'{material_table}\n')
            self._materials = material_table['file_id']

            model_file.read_rest()  # doesn't seem to contain anything useful

        else:
            raise Exception("Error reading model file!")
