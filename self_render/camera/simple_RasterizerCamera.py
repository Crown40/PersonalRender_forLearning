import taichi as ti
from .camera import Camera

class SimpleRasterizerCamera(Camera):
    #
    def __init__(self) -> None:
        super().__init__()
        #
        '''
        self._vars={'model_matrix':ti.math.mat4(0.0)
                   ,'view_matrix':ti.math.mat4(0.0)
                   ,'projection_matrix':ti.math.mat4(0.0)}
        '''
        #
    #
    '''
    def set_var(self, var_key, var):
        self._vars[var_key]=var
    def get_var(self, var_key):
        return self._vars[var_key]
    '''
    #
    def look_at(self, eye_pos,view_direction,up_direction):
        #Translation
        translation_matrix=ti.math.mat4(0.0)
        for d in range(3):
            translation_matrix[d,d]=1.0
            translation_matrix[d,3]=-eye_pos[d]
        translation_matrix[3,3]=1.0
        #Rotation
        result_matrix=ti.math.mat4(0.0)
        right_direction=view_direction.cross(up_direction)
        for d in range(3):
            result_matrix[0,d]=right_direction[d]
            result_matrix[1,d]=up_direction[d]
            result_matrix[2,d]=-view_direction[d]
        result_matrix[3,3]=1.0
        #Multiplication
        result_matrix@=translation_matrix
        #
        #self._vars['view_matrix']=result_matrix
        return result_matrix
    #
    # 由于Camera看向-Z,所以所以view space中，在Frustum内的顶点的Z_{view}应该是一个负数,所以需要near,far取反来得到+w值
    # https://blog.csdn.net/n5/article/details/122535066
    # https://zhuanlan.zhihu.com/p/65969162
    def projection(self, eye_fov,aspect_ratio,near,far,projection_type='perspective'):
        result_matrix=ti.math.mat4(0.0)
        temp_matrix=ti.math.mat4([[1.0 if i==j else 0.0 for j in range(4)] for i in range(4)])
        eye_fov=eye_fov/180*ti.math.pi
        top=ti.math.tan(eye_fov*0.5)*abs(near)    # bottom=-top
        right=top*aspect_ratio  # left=-right
        near,far=-abs(near),-abs(far)
        # Follow OpenGL
        #near,far=abs(near),abs(far)
        #
        # orthogonal: [l,r] x [b.t] x [f,n]   {f<n<0} -> map -> [-1,+1]**3
        #   Translation
        temp_matrix[0,3]=(right-right)*-0.5
        temp_matrix[1,3]=(top-top)*-0.5
        temp_matrix[2,3]=(near+far)*-0.5
        #   Scale
        result_matrix[0,0]=2/(right+right)
        result_matrix[1,1]=2/(top+top)
        result_matrix[2,2]=2/(near-far)
        result_matrix[3,3]=1.0
        #
        result_matrix@=temp_matrix
        # Follow OpenGL
        result_matrix[2,2]=-result_matrix[2,2]
        result_matrix[2,3]=-result_matrix[2,3]
        # perspective
        if projection_type=='perspective':
            for d in range(2):
                temp_matrix[d,3]=0.0
            #
            temp_matrix[0,0]=near
            temp_matrix[1,1]=near
            temp_matrix[3,2]=1.0
            temp_matrix[3,3]=0.0
            temp_matrix[2,2]=(near+far)
            temp_matrix[2,3]=(-near*far)
            print(result_matrix)
            print(temp_matrix)
            #
            result_matrix@=temp_matrix
            # Follow OpenGL
            result_matrix=ti.math.mat4([[-1.0 if i==j else 0.0 for j in range(4)] for i in range(4)]) @ result_matrix
        #
        return result_matrix;
#









