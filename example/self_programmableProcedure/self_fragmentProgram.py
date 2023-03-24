import taichi as ti
from self_render import SimpleProgrammableProcedure

@ti.data_oriented
class SelfFragmentProgram(SimpleProgrammableProcedure):
    #
    @ti.dataclass
    class Input:
        pass
    #
    @ti.dataclass
    class Output:
        pass
    #
    def __init__(self) -> None:
        super().__init__()
        #
        #self._buffer_count=buffer_count
        #
        self._uniform_vars={'uLightColor':ti.math.vec3.field(shape=())
                           }
        #
    #
    @ti.func
    def program(self,input_data):
        fragment_color=self._uniform_vars['uLightColor'][None]
        return fragment_color,0;

