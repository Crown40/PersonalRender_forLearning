import taichi as ti

@ti.func
def barycentricInterpolation2D_triangle(pos,pos0,pos1,pos2):
    # counterclockwise
    # edge-func only represent +,0,- not actual-distance 
    # and area-ratio don't need computing the correct-triangle-area but its rectangle's area 
    alpha=((pos1.x-pos.x)*(pos2.y-pos1.y) + (pos.y-pos1.y)*(pos2.x-pos1.x)) \
            /((pos1.x-pos0.x)*(pos2.y-pos1.y) + (pos0.y-pos1.y)*(pos2.x-pos1.x))
    beta=((pos2.x-pos.x)*(pos0.y-pos2.y) + (pos.y-pos2.y)*(pos0.x-pos2.x)) \
            /((pos2.x-pos1.x)*(pos0.y-pos2.y) + (pos1.y-pos2.y)*(pos0.x-pos2.x))
    gamma=1.0-alpha-beta
    #
    return ti.math.vec3([alpha,beta,gamma])
    #return alpha,beta,gamma

@ti.func
def mix(x,y, t):
    return (1-t)*x + t*y
