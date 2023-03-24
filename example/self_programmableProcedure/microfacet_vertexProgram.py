import taichi as ti
from self_render import SimpleProgrammableProcedure

@ti.data_oriented
class MicrofacetVertexProgram(SimpleProgrammableProcedure):
    #
    @ti.dataclass
    class Input:
        #pass
        #aVertexColor:ti.math.vec3
        aVertexPosition:ti.math.vec3
        aVertexTextureCoordinate:ti.math.vec2
        aVertexNormalVector:ti.math.vec3
    #
    @ti.dataclass
    class Output:
        #pass
        #position:ti.math.vec3
        #vColor:ti.math.vec3
        vTextureCoordinate:ti.math.vec2
        vFragPos:ti.math.vec3
        vNormalVector:ti.math.vec3
    #
    def __init__(self) -> None:
        super().__init__()
        #
        self._uniform_vars={'uModelMatrix':ti.math.mat4.field(shape=())
                           ,'uViewMatrix':ti.math.mat4.field(shape=())
                           ,'uProjectionMatrix':ti.math.mat4.field(shape=())}
        #
    #
    @ti.func
    def program(self, input_data):
        #
        rasterization_position=ti.math.vec4(input_data.aVertexPosition,1.0)
        rasterization_position=self._uniform_vars['uModelMatrix'][None] @ rasterization_position
        vFragPos=rasterization_position.xyz
        vNormalVector=(self._uniform_vars['uModelMatrix'][None] @ ti.math.vec4(input_data.aVertexNormalVector,0.0)).xyz
        #print('After ModelView',rasterization_position)
        rasterization_position=self._uniform_vars['uProjectionMatrix'][None]@ self._uniform_vars['uViewMatrix'][None] @ rasterization_position
        #print('After Projection',rasterization_position)
        #
        #output_data=self.Output(vColor=input_data.aVertexColor)
        output_data=self.Output(vTextureCoordinate=input_data.aVertexTextureCoordinate,vFragPos=vFragPos,vNormalVector=vNormalVector)
        return rasterization_position,output_data
    #
#
