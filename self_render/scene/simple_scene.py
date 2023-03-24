import numpy as np
from .scene import Scene

class SimpleScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        #
        self._meshes=list()
        #self.volumes=list()
        #
        self._counts={'vertex':0,'element':0}
        #self._elements_count=0   # not primitive
        #
        self._datas={'mesh':dict()}
        #
    #
    def add_mesh(self, mesh):
        self._meshes.append(mesh)
        self._counts['vertex']+=mesh.get_count('vertex')
        self._counts['element']+=mesh.get_count('element')
        #
        keys=self._datas['mesh'].keys()
        for key,value in (mesh.get_datasDict()).items():
            if key in keys:
                self._datas['mesh'][key]=np.concatenate([self._datas['meshes'][key],value],axis=0)
            else:
                self._datas['mesh'][key]=value
    #
    def clear_mesh(self):
        #
        '''
        keys=self._meshes.keys()
        for value in self._datas['mesh'].values():
            del value
        '''
        del self._datas['mesh']
        self._datas['mesh']=dict()
        #
        for mesh in self._meshes:
            mesh.clear()
        self._meshes.clear()
        #
        self._counts['vertex']=0
        self._counts['element']=0
    #def add_volume(self, volume):
    #    self.volumes.append(volume)
    #
    def get_count(self, count_key):
        return self._counts[count_key]
    #
    def get_meshData(self,data_key):
        return self._datas['mesh'][data_key]
#
