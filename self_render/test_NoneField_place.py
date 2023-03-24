import taichi as ti
import time

ti.init(arch=ti.cpu)

vec4s=ti.Vector.field(n=4,dtype=ti.f32,shape=(64,64))
#un-allowed
#a=ti.field(ti.math.mat4, ())
#allowed
#a=ti.math.mat4.field(shape=())
#a=ti.Matrix.field(n=4,m=4,dtype=ti.f32,shape=())
#a=ti.math.mat4(0.0)
#a=ti.Matrix([[0.0 for j in range(4)] for i in range(4)])
#un-allowed in Python-scope
#a=ti.Matrix.zero(n=4,m=4,dt=ti.f32)

#
#b=ti.Vector.field(n=4,dtype=ti.f32,shape=())
#b=ti.math.vec4.field(shape=())

@ti.kernel
def kernel_func():
    #a[None]=ti.math.mat4(0.0)
    #a[None]=ti.Matrix.zero(n=4,m=4,dt=ti.f32)
    #print(a)
    #print(a[None])
    for I in ti.grouped(ti.ndrange(*[64,64])):
        #vec4_instance=ti.Vector.zero(n=4,dt=ti.f32)
        #out=a[None]@vec4_instance
        out=a@vec4s[I]
    '''
    temp=b[None]
    print(temp.xyz)
    '''


start=time.time()
kernel_func()
end=time.time()
print('\n',end-start)
