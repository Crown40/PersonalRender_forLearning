import taichi as ti
import math
from self_render.render import Render
from self_render.scene import SimpleScene
from self_render.camera import SimpleRasterizerCamera
from .simple_vertexProcessor import SimpleVertexProcessor
from .simple_fragmentProcessor import SimpleFragmentProcessor



class SimpleRasterizer(Render):
    def __init__(self, screen_width=512,screen_height=512,screen_format='rgb',camera_near=0.1,camera_far=50.0) -> None:
        super().__init__()
        #
        self._scene=SimpleScene()
        #
        self._programs={'vertex':0,'fragment':0}
        self._processors={'vertex':None
                          ,'fragment':None}
        self._buffer_counts={'vertex':4096,'element':8192}
        #
        self._regsiter_bufferMaps={'vertex':dict()
                                    ,'element':dict()}
        self._run_buffers={'vertex':None
                           ,'element':None
                           ,'element_vertexIndex':ti.math.ivec3.field(shape=[self._buffer_counts['element']])
                           #,'vertex_pixelPosition':ti.math.vec3.field(shape=[self._buffer_counts['vertex']])
                           ,'vertex_pixelPosition':ti.math.vec4.field(shape=[self._buffer_counts['vertex']])
                           ,'frame':None    # nick-name: G-Buffer{Geometry Buffer}
                           ,'depth':None
                           ,'frame_buffer':None}
        #
        self._camera=SimpleRasterizerCamera()
        #
        self._vars={'model_matrix':ti.math.mat4([[1.0 if i==j else 0.0 for j in range(4)] for i in range(4)])
                   ,'view_matrix':ti.math.mat4(0.0)
                   ,'projection_matrix':ti.math.mat4(0.0)}
        #
        self._screen_properties={'width':screen_width,'height':screen_height,'format':screen_format,'projection_type':'perspective'
                                 ,'near':camera_near,'far':camera_far}
        
        #
        self._run_buffers['frame_buffer']=ti.math.vec4.field(shape=[self._screen_properties['width'],self._screen_properties['height']]) if screen_format=='rgba' \
                                            else ti.math.vec3.field(shape=[self._screen_properties['width'],self._screen_properties['height']])
        self._run_buffers['depth']=ti.field(dtype=float,shape=[self._screen_properties['width'],self._screen_properties['height']])
        #
        self.ti_gui=ti.GUI('Self_Render',(self._screen_properties['width'],self._screen_properties['height']))
    #
    def set_var(self,var_key,var):
        self._vars[var_key]=var
    def get_var(self,var_key):
        return self._vars[var_key]
    #
    def add_mesh(self, mesh):
        self._scene.add_mesh(mesh)
    #
    def set_program(self, program_key,program):
        #if program_key in self._programs.keys():
        #    del self._programs[program_key]
        #self._programs[program_key]=program
        #self._processors[program_key].set_programmableProcedure(program)
        #
        if program_key == 'vertex':
            self._processors['vertex']=SimpleVertexProcessor()
            self._processors['vertex'].set_programmableProcedure(program)
            #
            if len(self._processors['vertex'].get_key('input'))>0:
                self._processors['vertex'].set_buffer('input',program.Input.field(shape=[self._buffer_counts['vertex']]))
            if len(self._processors['vertex'].get_key('output'))>0:
                self._processors['vertex'].set_buffer('output',program.Output.field(shape=[self._buffer_counts['vertex']]) )
            #
            self._processors['vertex'].set_buffer('vertex_pixelPosition', self._run_buffers['vertex_pixelPosition'])
            #
            self._processors['vertex'].set_buffer('width',ti.field(dtype=int,shape=()) )
            self._processors['vertex'].write2buffer('width',self._screen_properties['width'])
            self._processors['vertex'].set_buffer('height',ti.field(dtype=int,shape=()) )
            self._processors['vertex'].write2buffer('height',self._screen_properties['height'])
            self._processors['vertex'].set_buffer('near',ti.field(dtype=float,shape=()) )
            self._processors['vertex'].write2buffer('near',self._screen_properties['near'])
            self._processors['vertex'].set_buffer('far',ti.field(dtype=float,shape=()) )
            self._processors['vertex'].write2buffer('far',self._screen_properties['far'])
            #
            self._run_buffers['vertex']=self._processors['vertex'].get_buffer('input')
            #print('hera',self._run_buffers['vertex'],self._processors['vertex']._buffers['input'])
        elif program_key == 'fragment':
            self._processors['fragment']=SimpleFragmentProcessor()
            self._processors['fragment'].set_programmableProcedure(program)
            #
            if len(self._processors['fragment'].get_key('input'))>0:
                self._processors['fragment'].set_buffer('input',self._processors['vertex'].get_buffer('output'))
            if len(self._processors['fragment'].get_key('output'))>0:
                self._processors['fragment'].set_buffer('output',program.Output.field(shape=[self._screen_properties['width'],self._screen_properties['height']]) )
            self._processors['fragment'].set_key('projection_type',self._screen_properties['projection_type'])
            #
            self._processors['fragment'].set_buffer('element_vertexIndex',self._run_buffers['element_vertexIndex'])
            self._processors['fragment'].set_buffer('vertex_pixelPosition',self._run_buffers['vertex_pixelPosition'])
            self._processors['fragment'].set_buffer('color',self._run_buffers['frame_buffer'])
            self._processors['fragment'].set_buffer('depth',self._run_buffers['depth'])
            #
            self._processors['fragment'].set_buffer('width',ti.field(dtype=int,shape=()) )
            self._processors['fragment'].write2buffer('width',self._screen_properties['width'])
            self._processors['fragment'].set_buffer('height',ti.field(dtype=int,shape=()) )
            self._processors['fragment'].write2buffer('height',self._screen_properties['height'])
        #
        self._programs[program_key]=program
        
    #
    def register_bufferMap(self, buffer_key,buffer_map):
        #
        if buffer_key in self._regsiter_bufferMaps.keys():
            #for value in self._regsiter_buffers[buffer_key].values():
            #    del value
            del self._regsiter_bufferMaps[buffer_key]
        #
        self._regsiter_bufferMaps[buffer_key]=buffer_map
    #
    def look_at(self, eye_pos,view_direction,up_direction):
        view_matrix=self._camera.look_at(eye_pos,view_direction,up_direction)
        #self._camera.look_at(eye_pos,view_direction,up_direction)
        self.set_var('view_matrix',view_matrix)
    def projection(self,eye_fov,aspect_ratio,near,far,projection_type='perspective'):
        self._screen_properties['projection_type']=projection_type
        self._screen_properties['near']=abs(near)
        self._screen_properties['far']=abs(far)
        #
        projection_matrix=self._camera.projection(eye_fov,aspect_ratio,near,far,projection_type=projection_type)
        #
        self.set_var('projection_matrix',projection_matrix)
        #
        #self._processors['vertex'].write2buffer('near',abs(near))
        #self._processors['vertex'].write2buffer('far',abs(far))
    #
    def set_screenProperty(self, screenProperty_key,screen_property):
        self._screen_properties[screenProperty_key]=screen_property
        #
        if screenProperty_key in ['width','height','format','near','far']:
            if screenProperty_key in ['near','far']:
                self._processors['vertex'].write2buffer(screenProperty_key,screen_property)
            if screenProperty_key in ['format']:
                del self._run_buffers['frame_buffer']
                self._run_buffers['frame_buffer']=ti.math.vec4.field(shape=[self._screen_properties['width'],self._screen_properties['height']]) if self._screen_properties['format']=='rgba' \
                                                    else ti.math.vec3.field(shape=[self._screen_properties['width'],self._screen_properties['height']])
            if screenProperty_key in ['width','height']:
                self._processors['vertex'].write2buffer(screenProperty_key,screen_property)
                self._processors['fragment'].write2buffer(screenProperty_key,screen_property)
                #
                del self.ti_gui
                self.ti_gui=ti.GUI('Self_Render',[self._screen_properties['width'],self._screen_properties['height']])
                del self._run_buffers['frame_buffer']
                self._run_buffers['frame_buffer']=ti.math.vec4.field(shape=[self._screen_properties['width'],self._screen_properties['height']]) if self._screen_properties['format']=='rgba' \
                                                    else ti.math.vec3.field(shape=[self._screen_properties['width'],self._screen_properties['height']])
                del self._run_buffers['depth']
                self._run_buffers['depth']=ti.field(dtype=ti.f32,shape=[self._screen_properties['width'],self._screen_properties['height']])
                del self._processors['fragment'].buffers['output']
                self._processors['fragment'].set_buffer('output',self._processors['fragment']._programmable_procedure.Output.field(shape=[self._screen_properties['width'],self._screen_properties['height']]) )
        #
    def get_screenProperty(self, screenProperty_key):
        return self._screen_properties[screenProperty_key]
    #
    def render_loop(self,vertex_end,vertex_globalStart, element_end,element_globalStart):
        #
        self._run_buffers['depth'].fill(self._screen_properties['far'])
        #Vertex
        #self._processors['vertex'].vertex_process(vertex_end)
        self._processors['vertex'].process(vertex_end)
        #Fragment
        self._processors['fragment'].process(element_end)
        #
        self.ti_gui.set_image(self._run_buffers['frame_buffer'])
        self.ti_gui.show()
    #
    def render(self):
        vertex_globalStart=0
        vertex_end=self._scene.get_count('vertex')
        print('vertex_end:',vertex_end)
        element_globalStart=0
        element_end=self._scene.get_count('element')
        print('element_end:',element_end)
        #Load2Buffer
        data_dict={'vertex':dict(),'element':dict()}
        buffer_map=self._regsiter_bufferMaps['vertex']
        if len(buffer_map.keys())>0:
            for key,value in buffer_map.items():
                data_dict['vertex'][key]=self._scene.get_meshData(value)
            
            self._run_buffers['vertex'].from_numpy(data_dict['vertex'])
        #
        buffer_map=self._regsiter_bufferMaps['element']
        #if self._run_buffers['element'] is not None:
        if len(buffer_map.keys())>0:
            for key,value in buffer_map.items():
                data_dict['element'][key]=self._scene.get_meshData(value)
            self._run_buffers['element'].from_numpy(data_dict['element'])
        #
        self._run_buffers['element_vertexIndex'].from_numpy(self._scene.get_meshData('element_vertexIndex'))
        #self._run_buffers['vertex']._from_external_arr(data_dict['vertex'])
        #self._run_buffers['element']._from_external_arr(data_dict['element'])
        #Loop
        self.render_loop(vertex_end,vertex_globalStart, element_end,element_globalStart)
    #
    def patch_render(self):
        scene_vertexCount=self._scene.get_count('vertex')
        buffer_vertexLoadSize=self._buffer_counts['vertex']-1
        buffer_elementLoadSize=buffer_vertexLoadSize//3
        for path in range(int(math.ceil(scene_vertexCount/buffer_vertexLoadSize)) ):
            vertex_globalStart=path*buffer_vertexLoadSize
            vertex_end=min(buffer_vertexLoadSize, scene_vertexCount-vertex_globalStart)
            element_globalStart=path*buffer_elementLoadSize
            element_end=min(buffer_elementLoadSize, vertex_end//3)
            #Load2Buffer
            data_dict={'vertex':dict(),'element':dict()}
            buffer_map=self._regsiter_bufferMaps['vertex']
            for key,value in buffer_map.items():
                data_dict['vertex'][key]=self._scene.get_data(value)[vertex_globalStart:vertex_end+vertex_globalStart]
            buffer_map=self._regsiter_bufferMaps['element']
            for key,value in buffer_map.items():
                data_dict['element'][key]=self._scene.get_data(value)[element_globalStart:element_end+element_globalStart]
            #
            self._run_buffers['vertex']._from_external_arr(data_dict['vertex'])
            self._run_buffers['element']._from_external_arr(data_dict['element'])
            #self._processors['vertex'].load2buffer('input',data_dict['vertex'])
            #Loop
            self.render_loop(vertex_end,vertex_globalStart, element_end,element_globalStart)
    #
#

