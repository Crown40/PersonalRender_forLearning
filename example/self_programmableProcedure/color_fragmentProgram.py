import taichi as ti
from self_render import SimpleProgrammableProcedure

@ti.data_oriented
class ColorFragmentProgram(SimpleProgrammableProcedure):
    #
    @ti.dataclass
    class Input:
        #pass
        vColor:ti.math.vec3
    #
    @ti.dataclass
    class Output:
        pass
    #
    def __init__(self) -> None:
        super().__init__()
        #
        self._uniform_vars={'uLightColor':ti.math.vec3.field(shape=())
                           }
        #
    #
    @ti.func
    def program(self,input_data):
        #fragment_color=self._uniform_vars['uLightColor'][None]
        fragment_color=input_data.vColor
        return fragment_color,0;
    #
#




