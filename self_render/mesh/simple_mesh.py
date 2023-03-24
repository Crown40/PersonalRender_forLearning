from .mesh import Mesh
from self_render.threeFile_loader import MeshFileLoader

class SimpleMesh(Mesh):
    #
    @staticmethod
    def constructMesh_fromFile(file_path:str,file_type:str):
        raw_result=MeshFileLoader.loadMesh_fromFile(file_path=file_path,file_type=file_type)
        #
        result=SimpleMesh()
        assert raw_result['v'] is not None
        assert raw_result['f'] is not None
        result.set_data(data_key='coordinate',data=raw_result['v'])
        #result.set_verticesCount(raw_result['v'].shape[0])
        result.set_count('vertex',raw_result['v'].shape[0])
        print('vertex_count:',raw_result['v'].shape[0])
        result.set_data(data_key='element_vertexIndex',data=raw_result['f'])
        #result.set_elementsCount(raw_result['f'].shape[0])
        result.set_count('element',raw_result['f'].shape[0])
        print('element:',raw_result['f'].shape[0])
        #
        print('raw_result.keys()',raw_result.keys())
        if 'vt' in raw_result.keys():
            result.set_data(data_key='texture_coordinate',data=raw_result['vt'])
        if 'vn' in raw_result.keys():
            result.set_data(data_key='normal',data=raw_result['vn'])
        if 'usemtl' in raw_result.keys():
            result.set_data(data_key='usemtl',data=raw_result['usemtl'])
            result.set_data(data_key='mtllib',data=raw_result['mtllib'])
        #
        return result
    #
    def __init__(self) -> None:
        super().__init__()
        #
        #self.vertices_datas=dict()
        #self.elements_datas=dict()
        self._datas=dict()
        #
        #self._vertex_count=0
        #self._element_count=0
        self._counts={'vertex':0,'element':0}
        # Read File
        #result=MeshFileLoader.load_mesh(file_path,file_type)
        #
    #
    '''
    def set_vertexCount(self,vertex_count):
        self._vertex_count=vertex_count
    def set_elementCount(self,element_count):
        self._element_count=element_count
    def get_vertexCount(self):
        return self._vertex_count
    def get_elementCount(self):
        return self._element_count
    '''
    def set_count(self, count_key,count):
        self._counts[count_key]=count
    def get_count(self, count_key):
        return self._counts[count_key]
    #
    def get_datasDict(self):
        return self._datas
    def set_data(self, data_key, data):
        self._datas[data_key]=data
        #self._counts[data_key]=data_count
    def get_data(self, data_key):
        assert self._datas[data_key]
        return self._datas[data_key]
    #
    def clear(self):
        for value in self._datas.values():
            del value
        del self._datas
        self._datas=dict()
        #
        del self._counts
        self._counts={'vertex':0,'element':0}
    #
#
    
#




