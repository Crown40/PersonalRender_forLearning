import taichi as ti
import time

#taichi_version: 1.14.1
# there're no ti.vector and ti.matrix but ti.Vector and ti.Matrix
#https://docs.taichi-lang.cn/docs/math_module
#ti.init(arch=ti.cpu)


'''
@ti.dataclass
class Sphere:
    center:ti.math.vec3
    radius:ti.f32
'''
#Sphere = ti.types.struct(center=ti.math.vec3, radius=ti.f32)
#, order='ji' un-allowed?
#test_field=Sphere.field(shape=[64,64],layout=ti.Layout.AOS)
#,layout=ti.Layout.AOS un-allowed?; Struct-type un-allowed!
#test_field=ti.field(dtype=Sphere,shape=[64,64],order='ji')
#test_field=ti.Vector.field(n=3,dtype=ti.f32,shape= [64,64],order='ji', layout=ti.Layout.AOS)
#test_field=ti.types.vector(n=3,dtype=ti.f32).field(shape= [64,64],order='ji', layout=ti.Layout.AOS)
#test_field=ti.math.vec3.field(shape= [64,64],order='ji', layout=ti.Layout.AOS)
vec3_type=ti.types.vector(n=3,dtype=ti.f32)
#, dtype= un-allowed?
#test_field=ti.field(dtype=vec3_type,shape= [64,64],order='ji')
#test_field=ti.field(dtype=ti.math.vec3,shape= [64,64],order='ji')
#print(a)

@ti.kernel
def kernel_func():
    for I in ti.grouped(test_field):
        print(test_field[I])
        #print(test_field[I].center)

#un-allowed
#a=ti.field(ti.math.mat4, ())
#allowed
#a=ti.math.mat4.field(shape=())
#a=ti.Matrix.field(n=4,m=4,dtype=ti.f32,shape=())
#
#b=ti.Vector.field(n=4,dtype=ti.f32,shape=())
#b=ti.math.vec4.field(shape=())

@ti.kernel
def kernel_func():
    #a[None]=ti.math.mat4(0.0)
    #a[None]=ti.Matrix.zero(n=4,m=4,dt=ti.f32)
    print(a[None])
    '''
    temp=b[None]
    print(temp.xyz)
    '''

start=time.time()
kernel_func()
end=time.time()
print('\n',end-start)

