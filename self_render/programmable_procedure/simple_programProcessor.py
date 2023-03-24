from .program_processor import ProgramProcessor

class SimpleProgramProcessor(ProgramProcessor):
    #
    def __init__(self) -> None:
        super().__init__()
        #
        self._programmable_procedure=0
        #
        self._buffers={'input':None,'output':None}
        #
        self._keys={'input':None,'output':None}
        #
    #
    def set_programmableProcedure(self,programmable_procedure):
        #del  self._programmable_procedure
        self._programmable_procedure=programmable_procedure
        #
        var_dict=vars(programmable_procedure.Input)
        self._keys['input']=list(var_dict['members'].keys())
        var_dict=vars(programmable_procedure.Output)
        self._keys['output']=list(var_dict['members'].keys())
        #
    def set_key(self, key,key_value):
        self._keys[key]=key_value
    def get_key(self, key):
        return self._keys[key];
    #
    def set_buffer(self, buffer_key,data_buffers):
        self._buffers[buffer_key]=data_buffers
    def get_buffer(self, buffer_key):
        return self._buffers[buffer_key]
    def get_allBuffers(self):
        return self._buffers
    def write2buffer(self, buffer_key,buffer_data):
        self._buffers[buffer_key][None]=buffer_data
    def load2buffer(self, buffer_key,buffer_datas):
        self._buffers[buffer_key]._from_external_arr(buffer_datas)
    #def readFromBuffer(self, buffer_key)   
    #






