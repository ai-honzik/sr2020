import random

import numpy as np
from lxml import etree


class Robot(object):
    """
    An example robot object. Please override me!
    """

    def __init__(self, morphology=None):
        if morphology is not None:
            self.morphology = morphology
        else:
            self.morphology = np.ones(shape=(2, 2, 5), dtype=np.int8)
            self.mutate()

    def get_body_xlim(self):
        return self.morphology.shape[0]

    def get_body_ylim(self):
        return self.morphology.shape[1]

    def get_body_zlim(self):
        return self.morphology.shape[2]

    def mutate(self):
        """
        very simple mutation.
        :return:
        """
        # mutate one voxel: flip it's bit
        x = random.randint(0, self.morphology.shape[0] - 1)
        y = random.randint(0, self.morphology.shape[1] - 1)
        z = random.randint(0, self.morphology.shape[2] - 1)
        if self.morphology[x, y, z]:
            self.morphology[x, y, z] = 0
        else:
            self.morphology[x, y, z] = 1

    def write_to_xml(self, root, **kwargs):
        structure = etree.SubElement(root, "Structure")
        structure.set('replace', 'VXA.VXC.Structure')
        structure.set('Compression', 'ASCII_READABLE')

        etree.SubElement(structure, "X_Voxels").text = str(self.morphology.shape[0])
        etree.SubElement(structure, "Y_Voxels").text = str(self.morphology.shape[1])
        etree.SubElement(structure, "Z_Voxels").text = str(self.morphology.shape[2])
        #etree.SubElement(structure, "numRegenerationModelSynapses").text = "0"
        #etree.SubElement(structure, "numForwardModelSynapses").text = "0"
        #etree.SubElement(structure, "numControllerSynapses").text = "0"

        data = etree.SubElement(structure, "Data")
        for layer in range(self.morphology.shape[2]):
            etree.SubElement(data, "Layer").text = etree.CDATA(''.join([str(d) for d in self.morphology[:, :, layer].flatten()]))

        return structure
