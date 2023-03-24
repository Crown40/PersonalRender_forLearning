import taichi as ti
from render import Render
from self_render.scene import SimpleScene

class SimpleRasterizer(Render):
    def __init__(self) -> None:
        super().__init__()
        #
        self._scene=SimpleScene()
        #
        self._programs=dict()
        self._program_buffers=dict()
        #
    #
    def add_mesh(self, mesh):
        self._scene.add_mesh(mesh)
    #
    def set_program(self, program_key,program):
        #
        if program_key in self._programs.keys():
            program_buffer=self._program_buffers[program_key]
            #
            data_buffer=program_buffer['input']
            for key,value in data_buffer.items():
                del value
            data_buffer=program_buffer['output']
            for key,value in data_buffer.items():
                del value
            #
            del program_buffer
            self._program_buffers[program_key]=None
        #
        buffer_count=program.get_bufferCount()
        program_buffer={'input':dict(),'output':dict()}
        #
        snode=ti.root.dense(ti.i,buffer_count)
        dataType_dict=(vars(program.Input))['members']
        for key,Value in dataType_dict.items():
            data_field=Value.field()
            snode.place(data_field)
            program_buffer['input'][key]=data_field
        program_buffer['input']['snode']=snode
        #
        snode=ti.root.dense(ti.i,buffer_count)
        dataType_dict=(vars(program.Output))['members']
        for key,Value in dataType_dict.items():
            data_field=Value.field()
            snode.place(data_field)
            program_buffer['output'][key]=data_field
        program_buffer['output']['snode']=snode
        #
        self._program_buffers[program_key]=program_buffer
    #
    def render_loop():
        pass
    #
    def render():
        pass
    #
#

