import numpy as np

from .threedFile_loader import ThreeDFileLoader


class MeshFileLoader(ThreeDFileLoader):
    #
    @staticmethod
    def readFile_obj(file_path,usemtl=False):
        #
        #assert file is not None
        #
        v,vt,vn=[],[],[]
        faces=[]
        usemtls=[]
        mtllib=None
        #
        with open(file_path, 'rb') as file:
        #file=open(file_path, 'rb')
            lines = file.readlines()
        #print('vetex')
        # vertex
        for line in lines:
            line=line.strip()
            #assert isinstance(line, bytes), f'BytesIO expected! (got {type(line)})'
            try:
                _type,fields=line.split(maxsplit=1)
                #if(_type==b'#'):
                #    print(_type,fields)
                if _type in [b'v',b'vt',b'vn']:
                    fields=[float(_) for _ in fields.split()]
                else:
                    fields=fields.split()
                #fields=fields.spilt()
            except ValueError:
                continue
            #v|vt|vn ?/?/? ?/?/? ?/?/?
            if _type==b'v':
                v.append(fields)
            elif _type==b'vt':
                vt.append(fields)
            elif _type==b'vn':
                vn.append(fields)
            #
            if _type==b'mtllib':
                mtlllib=fields[0]
                continue
            elif _type==b'usemtl':
                usemtls.append([len(faces), fields[0]])
                continue
            #
            # line looks like 'f 5/1/1 1/2/1 4/3/1'
            # or 'f 314/380/494 382/400/494 388/550/494 506/551/494' for quads
            if _type!=b'f':
                continue
            indices = [[int(_) - 1 if _ else 0 for _ in field.split(b'/')] for field in fields]
            #
            if len(indices)>2:
                for n in range(1, len(indices) - 1):
                    # disorder
                    faces.append([indices[0], indices[n], indices[n + 1]])
        #print('face')
        # face
        '''
        for line in lines:
            line=line.strip()
            #assert isinstance(line, bytes), f'BytesIO expected! (got {type(line)})'
            try:
                _type,fields=line.split(maxsplit=1)
                #print(_type,type(fields),fields)
                #fields=[float(_) for _ in fields.split()]
                fields=fields.split()
            except ValueError:
                continue
            #
            if _type==b'mtllib':
                mtlllib=fields[0]
                continue
            if _type==b'usemtl':
                usemtls.append([len(faces), fields[0]])
                continue
            # line looks like 'f 5/1/1 1/2/1 4/3/1'
            # or 'f 314/380/494 382/400/494 388/550/494 506/551/494' for quads
            if _type!=b'f':
                continue
            indices = [[int(_) - 1 if _ else 0 for _ in field.split(b'/')] for field in fields]
            #
            if len(indices)>2:
                for n in range(1, len(indices) - 1):
                    # disorder
                    faces.append([indices[0], indices[n], indices[n + 1]])
        '''
        #
        result=dict()
        result['v']=np.array([[0, 0, 0]], dtype=np.float32) if len(v) == 0 else np.array(v, dtype=np.float32)
        result['f']=np.zeros((1, 3, 3), dtype=np.int32) if len(faces) == 0 else np.array(faces, dtype=np.int32)
        if len(vt)>0 and len(vt)==len(v):
            result['vt']=np.array(vt, dtype=np.float32)
        if len(vn)>0 and len(vn)==len(v):
            result['vn']=np.array(vn, dtype=np.float32)
        #
        if usemtl:
            result['usemtl'] = usemtls
            result['mtllib'] = mtllib
        #
        return result
    #
    @classmethod
    def loadMesh_fromFile(cls, file_path: str,file_type: str,usemtl=False):
        #
        if file_type=='.obj':
            #with open(file=file_path,mode='rb') as file
            return cls.readFile_obj(file_path=file_path,usemtl=usemtl)
        else:
            raise ValueError(f'still not support to open {file_type} type of file.\n')
    #
    
             




