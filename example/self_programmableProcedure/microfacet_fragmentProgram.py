import taichi as ti
from self_render import SimpleProgrammableProcedure
from self_render.interpolation import TextureSampling,mix

@ti.data_oriented
class MicrofacetFragmentProgram(SimpleProgrammableProcedure):
    #
    @ti.dataclass
    class Input:
        #pass
        #vColor:ti.math.vec3
        vTextureCoordinate:ti.math.vec2
        vFragPos:ti.math.vec3
        vNormalVector:ti.math.vec3
    #
    @ti.dataclass
    class Output:
        pass
    #
    def __init__(self) -> None:
        super().__init__()
        #
        self._uniform_vars={'uSurfaceColor':ti.math.vec3.field(shape=())
                            ,'uLightColor':ti.math.vec3.field(shape=())
                            ,'uLightPos':ti.math.vec3.field(shape=())
                            ,'uCameraPos':ti.math.vec3.field(shape=())
                            ,'uRoughness':ti.field(dtype=float,shape=())
                            ,'uRemapping':ti.field(dtype=float,shape=())
                            ,'uReflectivity':ti.math.vec3.field(shape=())
                            ,'uMetalness':ti.field(dtype=float,shape=())
                            ,'uColorMap':None}
        #
    #
    @ti.func
    def program(self,input_data):
        #fragment_color=self._uniform_vars['uSurfaceColor'][None]
        #I=ti.cast(input_data.vTextureCoordinate*self._uniform_vars['uColorMap'].shape, ti.i32)
        #fragment_color=self._uniform_vars['uColorMap'][I]/256
        fragment_color=TextureSampling.bilerp2D_sampling(self._uniform_vars['uColorMap'],input_data.vTextureCoordinate) * (1/(256))
        fragment_color=mix(self._uniform_vars['uReflectivity'][None],fragment_color, self._uniform_vars['uMetalness'][None])
        #
        light_direction=ti.math.normalize(self._uniform_vars['uLightPos'][None]-input_data.vFragPos)
        view_direction=ti.math.normalize(self._uniform_vars['uCameraPos'][None]-input_data.vFragPos)
        half_vector=ti.math.normalize(light_direction+view_direction)
        normal_vector=input_data.vNormalVector
        # specular
        fragment_color = (self.D(normal_vector,half_vector) * self.G_Smith(normal_vector,view_direction,light_direction) * self.F(view_direction,half_vector,fragment_color)) \
                        / (4*ti.math.dot(light_direction,normal_vector)*ti.math.dot(view_direction,normal_vector)+0.001)
        # radiance
        fragment_color*= self._uniform_vars['uLightColor'][None]/((self._uniform_vars['uLightPos'][None]-input_data.vFragPos).norm()**2)
        #
        return fragment_color,0;
    #
    # Normal distribution function: GGXTR
    @ti.func
    def D(self, normal_vector,half_vector):
        roughness=self._uniform_vars['uRoughness'][None]
        roughness_square=roughness*roughness
        #
        result=ti.math.max(ti.math.dot(normal_vector,half_vector) ,0.0)
        result=result*result*(roughness_square-1.0) + 1.0
        result=ti.math.pi * result*result
        result=roughness_square/result
        #
        return result
    # Geometry function: Smith
    @ti.func
    def G_Smith(self,normal_vector,view_direction,light_direction):
        normalDotView=ti.math.max(ti.math.dot(normal_vector,view_direction) ,0.0)
        normalDotLight=ti.math.max(ti.math.dot(normal_vector,light_direction) ,0.0)
        #
        return self.G_SchlickGGX(normalDotView)*self.G_SchlickGGX(normalDotLight)
        #
    #
    # Geometry function:    combination of the GGX and Schlick-Beckmann approximation
    @ti.func
    def G_SchlickGGX(self, normalDot_):
        remapping=self._uniform_vars['uRemapping'][None]
        #
        #result=ti.math.max(ti.math.dot(normal_vector,view_direction) ,0.0)
        result=normalDot_/(normalDot_*(1.0-remapping) + remapping)
        #
        return result
    #
    @ti.func
    def G(self, normal_vector,view_direction):
        remapping=self._uniform_vars['uRemapping'][None]
        #
        result=ti.math.max(ti.math.dot(normal_vector,view_direction) ,0.0)
        result=result/(result*(1.0-remapping) + remapping)
        #
        return result
    #
    # Fresnel equation: Fresnel-Schlick approximation
    @ti.func
    def F(self, view_direction,half_vector,reflectivity):
        #reflectivity=self._uniform_vars['uReflectivity'][None]
        #
        temp=1.0-ti.math.max(ti.math.dot(view_direction,half_vector) ,0.0)
        temp=temp*(temp*temp)**2
        result=reflectivity+(1.0-reflectivity) * temp
        #
        return result
    #
    

#
