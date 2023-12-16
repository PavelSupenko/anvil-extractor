class Material:
    def __init__(self, name, missing_no=False, diffuse=None, normal=None, specular=None, height=None, transmission=None, mask1=None, mask2=None):
        self.name = name
        self.missing_no = missing_no
        self.diffuse = diffuse
        self.normal = normal
        self.specular = specular
        self.height = height
        self.transmission = transmission
        self.mask1 = mask1
        self.mask2 = mask2
