from math import radians
import numpy as np
import taichi as ti
import self_render as sr
#from self_render.rasterizer import simple_rasterizer
from self_programmableProcedure import *

screen_width,screen_height=700,700
screen_aspect=1.0
near,far=0.1,50.0
simple_rasterizer=sr.SimpleRasterizer(screen_width=screen_width,screen_height=screen_height,camera_near=near,camera_far=far)
#
'''
simple_mesh1=sr.SimpleMesh()
# Vertex
coordinate_data=[ [2.0, 0.0, -2.0],[0.0, 2.0, -2.0],[-2.0, 0.0, -2.0]
                  ,[3.5, -1.0, -5.0],[2.5, 1.5, -5.0],[-1.0, 0.5, -5.0] 
                ]
coordinate_data=np.array(object=coordinate_data,dtype=np.float32)
simple_mesh1.set_data(data_key='coordinate',data=coordinate_data)
#
color_data=[ [217.0/255, 238.0/255, 185.0/255],[217.0/255, 238.0/255, 185.0/255],[217.0/255, 238.0/255, 185.0/255]
            ,[185.0/255, 217.0/255, 238.0/255],[185.0/255, 217.0/255, 238.0/255],[185.0/255, 217.0/255, 238.0/255]
            ]
color_data=np.array(object=color_data,dtype=np.float32)
simple_mesh1.set_data(data_key='color',data=color_data)
#
#print(coordinate_data.shape)
simple_mesh1.set_count('vertex',coordinate_data.shape[0])
# Element
element_data=[[0,1,2], [3,4,5]]
element_data=np.array(object=element_data,dtype=np.int32)
#print(element_data.shape)
simple_mesh1.set_data(data_key='element_vertexIndex',data=element_data)
simple_mesh1.set_count('element',element_data.shape[0])
#
#
simple_rasterizer.add_mesh(mesh=simple_mesh1)
'''
#
simple_mesh2=sr.SimpleMesh.constructMesh_fromFile('../Self_Render/assets/spot/spot_triangulated_good.obj',file_type='.obj')
simple_rasterizer.add_mesh(mesh=simple_mesh2)

#raise RuntimeError
#
#simple_rasterizer.set_var('model_matrix',ti.math.mat4([[1.0 if i==j else 0.0 for j in range(4)] for i in range(4)]))
'''
'''
radian=140.0/180.0*ti.math.pi
simple_rasterizer.set_var('model_matrix',ti.math.mat4([[ti.math.cos(radian),0,ti.math.sin(radian),0]
                                                        ,[0,1,0,0]
                                                        ,[-ti.math.sin(radian),0,ti.math.cos(radian),0]
                                                        ,[0,0,0,1]]))
eye_pos,view_direction,up_direction=ti.math.vec3([0,0,5]),ti.math.vec3([0,0,-1]),ti.math.vec3([0,1,0])
simple_rasterizer.look_at(eye_pos,view_direction,up_direction)
simple_rasterizer.projection(45,screen_aspect,near,far,'perspective')   # perspective,orthogonal
model_matrix=simple_rasterizer.get_var('model_matrix')
view_matrix=simple_rasterizer.get_var('view_matrix')
projection_matrix=simple_rasterizer.get_var('projection_matrix')
'''
'''
#
self_vertexProgram=MicrofacetVertexProgram()    # SelfVertexProgram,ColorVertexProgram,TextureVertexProgram
#self_vertexProgram.set_uniformVar('uModelViewMatrix',view_matrix@model_matrix)
self_vertexProgram.set_uniformVar('uModelMatrix',model_matrix)
self_vertexProgram.set_uniformVar('uViewMatrix',view_matrix)
print('model_matrix',model_matrix)
print('view_matrix',view_matrix)
print('view_matrix@model_matrix:',view_matrix@model_matrix)
project_matrix=ti.math.mat4([[1/(screen_aspect*ti.math.tan(45/180*ti.math.pi*0.5)),0.0,0.0,0.0]
                             ,[0.0,1/(ti.math.tan(45/180*ti.math.pi*0.5)),0.0,0.0]
                             ,[0.0,0.0,-(far+near)/(far-near),2*far*near/(near-far)]
                             ,[0.0,0.0,-1.0,0.0]])  # set w=-abs(z)
self_vertexProgram.set_uniformVar('uProjectionMatrix',projection_matrix)
print('projection_matrix:',projection_matrix)
print('project_matrix:',project_matrix)
#
simple_rasterizer.set_program('vertex',self_vertexProgram)
simple_rasterizer._processors['vertex'].write2buffer('near',near)
simple_rasterizer._processors['vertex'].write2buffer('far',far)
#simple_rasterizer.register_bufferMap(buffer_key='vertex',buffer_map={'aVertexPosition':'coordinate','aVertexColor':'color'})
simple_rasterizer.register_bufferMap(buffer_key='vertex',buffer_map={'aVertexPosition':'coordinate','aVertexTextureCoordinate':'texture_coordinate'
                                                                     ,'aVertexNormalVector':'normal'})
#
self_fragmentProgram=MicrofacetFragmentProgram()     # SelfFragmentProgram,ColorFragmentProgram,TextureFragmentProgram
self_fragmentProgram.set_uniformVar('uSurfaceColor',ti.math.vec3([185.0/255, 217.0/255, 238.0/255]))
self_fragmentProgram.set_uniformVar('uLightColor',ti.math.vec3(500))
light_pos=ti.math.vec3([0, 1, 5])
self_fragmentProgram.set_uniformVar('uLightPos',light_pos)
self_fragmentProgram.set_uniformVar('uCameraPos',eye_pos)
# Microfacet: https://learnopengl-cn.github.io/07%20PBR/01%20Theory/
roughness=0.3   # 0.1.0.3.0.5,0.8,1.0
self_fragmentProgram.set_uniformVar('uRoughness',roughness)
remapping_ofRoughness=(roughness+1)**2 *0.125  # direct,IBL{alpha**2*0.5}
self_fragmentProgram.set_uniformVar('uRemapping',remapping_ofRoughness)
reflectivity=ti.math.vec3(0.04) # 0.02, 0.95, [0.95, 0.93, 0.88]
self_fragmentProgram.set_uniformVar('uReflectivity',reflectivity)
metalness=0.7
self_fragmentProgram.set_uniformVar('uMetalness',metalness)
#
color_map=ti.tools.imread('../Self_Render/assets/spot/spot_texture.png')
print('type(color_map):',type(color_map),'color_map.shape:',color_map.shape)
if color_map.shape[2]==4:
    colorMap_buffer=ti.math.vec4.field(shape=list(color_map.shape[:2]))
else:   # 3
    colorMap_buffer=ti.math.vec3.field(shape=list(color_map.shape[:2]))
colorMap_buffer.from_numpy(color_map)
self_fragmentProgram.set_uniformBuffer('uColorMap', colorMap_buffer) 
print('colorMap_buffer:',colorMap_buffer.shape)
#
simple_rasterizer.set_program('fragment',self_fragmentProgram)
simple_rasterizer.register_bufferMap(buffer_key='element',buffer_map={})
print('Finish initialization')
'''
'''
#

#raise RuntimeError

if __name__=='__main__':
    #pass
    #while simple_rasterizer.ti_gui.running:
    simple_rasterizer.render()
    while True:
        pass
