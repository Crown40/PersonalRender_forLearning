import taichi as ti
from self_render.programmable_procedure import SimpleProgramProcessor
from self_render.interpolation import barycentricInterpolation2D_triangle

@ti.data_oriented
class SimpleFragmentProcessor(SimpleProgramProcessor):
    #
    def __init__(self) -> None:
        super().__init__()
        #
        self._buffers={'input':None,'output':None}
        #
        self._keys={'input':None,'output':None}   # 'output':None
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
        self.fragment_process(end)
        #if self._keys['input']!=None:
        #    self.fragmentProcess_withInput(fragment_end)
        #else:
        #    self.fragmentProcess_withoutInput(fragment_end)
    #
    @ti.kernel
    def fragment_process(self, end:int):
        for element_index in range(end):
            element_vertexIndex=self._buffers['element_vertexIndex'][element_index]
            pos0,pos1,pos2=self._buffers['vertex_pixelPosition'][element_vertexIndex[0]],self._buffers['vertex_pixelPosition'][element_vertexIndex[1]],self._buffers['vertex_pixelPosition'][element_vertexIndex[2]]
            
            # Rasterization
            #   one: BoundBox
            #   TODO:another: basic-unit: quad{2x2 pixels} <- 4x4 <- 16x16
            min_bound=ti.Vector.zero(dt=ti.i32,n=2)
            max_bound=ti.Vector.zero(dt=ti.i32,n=2)
            for d in ti.static(range(2)):
                min_bound[d]=ti.cast(ti.floor(ti.min(pos0[d],pos1[d],pos2[d])), ti.i32)
                min_bound[d]=ti.max(min_bound[d],0)
                max_bound[d]=ti.cast(ti.ceil(ti.max(pos0[d],pos1[d],pos2[d])), ti.i32)
            max_bound[0]=ti.min(max_bound[0],self._buffers['width'][None])
            max_bound[1]=ti.min(max_bound[1],self._buffers['height'][None])
            #print('min_bound:',min_bound,'max_bound:',max_bound)
            # Edge-bound: 01,12,20  {-delta_x,delta_y} dot P0,P1,P2 >0
            normalOf_edge0,normalOf_edge1,normalOf_edge2=ti.Vector([pos0.y-pos1.y,pos1.x-pos0.x]),ti.Vector([pos1.y-pos2.y,pos2.x-pos1.x]),ti.Vector([pos2.y-pos0.y,pos0.x-pos2.x])
            #for i in range(min_bound[0],max_bound[0]+1):
            #    for j in range(min_bound[1],max_bound[1]+1):
            for I in ti.grouped(ti.ndrange((min_bound[0],max_bound[0])
                                           ,(min_bound[1],max_bound[1]) )):
                pos=I+0.5;
                #print(I)
                # Inside or not
                #   Edge-func
                #   TODO:Increment d_Edge-func
                if(ti.math.dot(normalOf_edge0,pos-pos0.xy)>=0.0 and ti.math.dot(normalOf_edge1,pos-pos1.xy)>=0.0 and ti.math.dot(normalOf_edge2,pos-pos2.xy)>=0.0):
                    #print(I)
                    # Inpterpolation
                    #   Barycentric-Interpolation
                    #   TODO:Increment: ddx,ddy  {dF/dx,dF/dy}
                    # Actually, recover the world-space-position of pixel maybe more intuitive for interpolation {need inverse-transformation}
                    weights=barycentricInterpolation2D_triangle(pos,pos0,pos1,pos2)
                    #TODO: Perspective-Correction for Weights
                    #https://www.zhihu.com/question/332096916
                    #https://zhuanlan.zhihu.com/p/403259571
                    if( ti.static(self._keys['projection_type']=='perspective') ):
                        weights[0],weights[1],weights[2]=weights[0]/pos0.w,weights[1]/pos1.w,weights[2]/pos2.w
                        weightSum_inverse=1/(weights[0]+ weights[1] + weights[2])
                        weights[0],weights[1],weights[2]=weights[0]*weightSum_inverse,weights[1]*weightSum_inverse,weights[2]*weightSum_inverse
                    #   
                    if( ti.static('depth' in self._keys['output']) ):
                        fragment_color,output_data=self.fragmentProgram_process(element_vertexIndex=element_vertexIndex,weights=weights)
                        # Post-Z: Merge {Testing}
                        #depth=weights[0]*pos0.z+weights[1]*pos1.z+weights[2]*pos2.z
                        depth=output_data.depth
                        ti.atomic_min(self._buffers['depth'][I],depth)
                        ti.sync()
                        #
                        if(depth<=self._buffers['depth'][I]):
                            if( ti.static(len(self._keys['output'])>0) ):
                                self._buffers['output'][I]=output_data
                            #
                            self._buffers['color'][I]=fragment_color
                    else:
                        # Early-Z: Merge {Testing}
                        depth=weights[0]*pos0.z+weights[1]*pos1.z+weights[2]*pos2.z
                        ti.atomic_min(self._buffers['depth'][I],depth)
                        ti.sync()
                        #
                        #print(I,depth,self._buffers['depth'][I])
                        if(depth<=self._buffers['depth'][I]):
                            fragment_color,output_data=self.fragmentProgram_process(element_vertexIndex=element_vertexIndex,weights=weights)
                            #
                            if( ti.static(len(self._keys['output'])>0) ):
                                self._buffers['output'][I]=output_data
                            #
                            self._buffers['color'][I]=fragment_color
            '''
            '''
        #
    #
    #
    @ti.func
    def fragmentProgram_process(self,element_vertexIndex,weights):
        if( ti.static(len(self._keys['input'])>0) ):
            input0,input1,input2=self._buffers['input'][element_vertexIndex[0]],self._buffers['input'][element_vertexIndex[1]],self._buffers['input'][element_vertexIndex[2]]
            #
            input_data=self._programmable_procedure.Input()
            for key_index in ti.static(range(len(self._keys['input']))):
                input_data[self._keys['input'][key_index]]=weights[0]*input0[self._keys['input'][key_index]] + weights[1]*input1[self._keys['input'][key_index]] + weights[2]*input2[self._keys['input'][key_index]]
            #
            fragment_color,output_data=self._programmable_procedure.program(input_data)
            #self._buffers['output'][I]=output_data
            return fragment_color,output_data
        else: # No input_data
            fragment_color,output_data=self._programmable_procedure.program(0)   
            return fragment_color,output_data
        #

    #
    '''
    @ti.kernel
    def fragmentProcess_withoutInput(self, fragment_end:int):
        for i in range(fragment_end):
            element_vertexIndex=self._buffers['element_vertexIndex'][i]
            #
    #
    def fragmentProcess_withInput(self, fragment_end:int):
        for i in range(fragment_end):
            element_vertexIndex=self._buffers['element_vertexIndex'][i]
            input0,input1,input2=self._buffers['input'][element_vertexIndex[0]],self._buffers['input'][element_vertexIndex[1]],self._buffers['input'][element_vertexIndex[2]]
            #
    ''' 



