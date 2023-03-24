import taichi as ti
from self_render.programmable_procedure import SimpleProgramProcessor

@ti.data_oriented
class SimpleVertexProcessor(SimpleProgramProcessor):
    def __init__(self) -> None:
        super().__init__()
        #
        #self._uniform_vars={'uViewportMatrix':ti.math.mat4.field(shape=())}
        self._buffers={'input':None,'output':None}
        #
        self._keys={'input':None,'output':None}
        #
    def set_programmableProcedure(self,programmable_procedure):
        #super().set_programmableProcedure(programmable_procedure)
        self._programmable_procedure=programmable_procedure
        #
        var_dict=vars(programmable_procedure.Input)
        self._keys['input']=list(var_dict['members'].keys())
        var_dict=vars(programmable_procedure.Output)
        self._keys['output']=list(var_dict['members'].keys())
        #
    #TODO: program:ti.template()
    def process(self,end):
        self.vertex_process(end)
    #
    @ti.kernel
    def vertex_process(self, end:int):
        for vertex_index in range(end):
            rasterization_position,output_data=self.vertexProgram_process(vertex_index)
            if( ti.static(len(self._keys['output'])>0) ):
                self._buffers['output'][vertex_index]=output_data
            #Homogeneous division
            # w = -
            # OpenGL keep the z=+, w=+ => z/w=+,w=+ for depth-testing & Perspective-Correction: Very Convenient
            #print('Before Homogeneous division',rasterization_position)
            # For Perspective-Correction
            #rasterization_position/=rasterization_position.w
            rasterization_position.xyz/=rasterization_position.w
            #print('After Homogeneous division',rasterization_position)
            #ViewPort
            #rasterization_position=self._uniform_vars['uViewportMatrix'][None]@rasterization_position
            #   easy for int() or floor() [-1,1] -> [0,width or height]
            rasterization_position.x=0.5*self._buffers['width'][None]*(rasterization_position.x+1.0)    # 0.5*width *x + 0.5*width
            rasterization_position.y=0.5*self._buffers['height'][None]*(rasterization_position.y+1.0)   # 0.5*height *y + 0.5*height
            #   Special for Games101: because z<0, so we need map it to + for intuition {but the map-configuration be defined by programer or customer?}
            #rasterization_position.z=rasterization_position.z*(self._buffers['far'][None]-self._buffers['near'][None])*0.5 + (self._buffers['far'][None]+self._buffers['near'][None])*0.5
            #rasterization_position.z=-rasterization_position.z
            #print('vertex_index:',vertex_index,rasterization_position)
            self._buffers['vertex_pixelPosition'][vertex_index]=rasterization_position
            #print(input_data.aVertexPosition,output_data.position)

    #
    @ti.func
    def vertexProgram_process(self,vertex_index):
        if( ti.static(len(self._keys['input'])>0) ):
            input_data=self._buffers['input'][vertex_index]
            rasterization_position,output_data=self._programmable_procedure.program(input_data)
            return rasterization_position,output_data
        else:
            input_data=0
            rasterization_position,output_data=self._programmable_procedure.program(input_data)
            return rasterization_position,output_data

        




