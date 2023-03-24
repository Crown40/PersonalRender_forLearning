import taichi as ti

class TextureSampling(object):
    #
    @staticmethod
    @ti.func
    def nearest_sampling(texture_map,texture_coordinate):
        texel_Index=ti.cast(texture_coordinate*texture_map.shape+0.5, ti.i32)
        return texture_map[texel_Index]
    #
    @staticmethod
    @ti.func
    def bilerp2D_sampling(texture_map,texture_coordinate):
        uv_Index=texture_coordinate*texture_map.shape
        texel_Index=ti.cast(uv_Index-0.5, ti.i32)
        delta_Index=uv_Index-texel_Index+0.5
        # +0,+0
        result=(1.0-delta_Index[0])*(1.0-delta_Index[1])*texture_map[texel_Index]
        # +0,+1
        result+=(1.0-delta_Index[0])*(delta_Index[1])*texture_map[texel_Index+[0,1]]
        # +1,+0
        result+=(delta_Index[0])*(1.0-delta_Index[1])*texture_map[texel_Index+[1,0]]
        # +1,+1
        result+=(delta_Index[0])*(delta_Index[1])*texture_map[texel_Index+[1,1]]
        #
        return result





