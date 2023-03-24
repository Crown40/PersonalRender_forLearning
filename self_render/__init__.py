import taichi as ti

from .mesh import *
from .threeFile_loader import *
from .rasterizer import *
from .programmable_procedure import SimpleProgrammableProcedure

ti.init(arch=ti.cpu)

