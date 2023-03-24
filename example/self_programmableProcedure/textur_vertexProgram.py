import taichi as ti
from self_render import SimpleProgrammableProcedure

@ti.data_oriented
class TextureVertexProgram(SimpleProgrammableProcedure):
    #
    @ti.dataclass
    class Input:
        #pass
        aVertexPosition:ti.math.vec3
        aVertexTextureCoordinate:ti.math.vec2
        #aVertexColor:ti.math.vec3
    #
    @ti.dataclass
    class Output:
        #pass
        #position:ti.math.vec3
        #vColor:ti.math.vec3
        vTextureCoordinate:ti.math.vec2
    #
    def __init__(self) -> None:
        super().__init__()
        #
        self._uniform_vars={'uModelViewMatrix':ti.math.mat4.field(shape=())
                           ,'uProjectionMatrix':ti.math.mat4.field(shape=())}
        #
    #
    @ti.func
    def program(self, input_data):
        #
        rasterization_position=ti.math.vec4(input_data.aVertexPosition,1.0)
        rasterization_position=self._uniform_vars['uModelViewMatrix'][None] @ rasterization_position
        #print('After ModelView',rasterization_position)
        rasterization_position=self._uniform_vars['uProjectionMatrix'][None]@rasterization_position
        #print('After Projection',rasterization_position)
        #
        #output_data=self.Output(vColor=input_data.aVertexColor)
        output_data=self.Output(vTextureCoordinate=input_data.aVertexTextureCoordinate)
        return rasterization_position,output_data
    #
#
