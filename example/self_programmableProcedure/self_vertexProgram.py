import taichi as ti
from self_render import SimpleProgrammableProcedure

@ti.data_oriented
class SelfVertexProgram(SimpleProgrammableProcedure):
    #
    @ti.dataclass
    class Input:
        aVertexPosition:ti.math.vec3
    #
    @ti.dataclass
    class Output:
        None
        #position:ti.math.vec3
    #
    def __init__(self) -> None:
        super().__init__()
        #
        #self._buffer_count=buffer_count
        #
        self._uniform_vars={'uModelViewMatrix':ti.math.mat4.field(shape=())
                           ,'uProjectionMatrix':ti.math.mat4.field(shape=())}
        #
    #
    #def get_bufferCount(self):
    #    return self._buffer_count
    #
    
    #
    @ti.func
    def program(self, input_data):
        #
        '''
        position=ti.math.vec4(0.0)
        for d in ti.static(range(3)):
            position[d]=input_data.aVertexPosition[d]
        position[3]=1.0
        '''
        rasterization_position=ti.math.vec4(input_data.aVertexPosition,1.0)
        rasterization_position=self._uniform_vars['uModelViewMatrix'][None] @ rasterization_position
        #print('After ModelView',rasterization_position)
        rasterization_position=self._uniform_vars['uProjectionMatrix'][None]@rasterization_position
        #print('After Projection',rasterization_position)
        #
        #output_data=self.Output(position=input_data.aVertexPosition)
        return rasterization_position,0
    #
#





