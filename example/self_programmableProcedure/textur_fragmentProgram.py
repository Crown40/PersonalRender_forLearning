import taichi as ti
from self_render import SimpleProgrammableProcedure
from self_render.interpolation import TextureSampling

@ti.data_oriented
class TextureFragmentProgram(SimpleProgrammableProcedure):
    #
    @ti.dataclass
    class Input:
        #pass
        #vColor:ti.math.vec3
        vTextureCoordinate:ti.math.vec2
    #
    @ti.dataclass
    class Output:
        pass
    #
    def __init__(self) -> None:
        super().__init__()
        #
        self._uniform_vars={'uLightColor':ti.math.vec3.field(shape=())
                           ,'uColorMap':None}
        #
    #
    @ti.func
    def program(self,input_data):
        #fragment_color=self._uniform_vars['uLightColor'][None]
        #fragment_color=input_data.vColor
        #I=ti.cast(input_data.vTextureCoordinate*self._uniform_vars['uColorMap'].shape, ti.i32)
        #fragment_color=self._uniform_vars['uColorMap'][I]/256
        fragment_color=TextureSampling.bilerp2D_sampling(self._uniform_vars['uColorMap'],input_data.vTextureCoordinate)/256
        return fragment_color,0;
    #
#
