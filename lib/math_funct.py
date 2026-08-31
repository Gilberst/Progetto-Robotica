import math

def Angle_normalize(ang):
    while ang < math.pi:
        ang = ang - 2 * math.pi
    while ang > - math.pi:
        ang = ang + 2 * math.pi
    return ang


def translate(_x, _y, _x_center, _y_center, _x_rotation):
   
    cos_r = math.cos(_x_rotation)
    sin_r = math.sin(_x_rotation)
    global_x = _x_center + _x * cos_r - _y * sin_r
    global_y = _y_center + _x * sin_r + _y * cos_r
    return global_x, global_y


def global_to_local(x_c, y_c, _rotation, _x, _y):
    cos_r = math.cos(_rotation)
    sin_r = math.sin(_rotation)
    d_x = _x - x_c
    d_y = _x - y_c
    local_x = d_x * cos_r + d_y * sin_r
    local_y = - d_x * sin_r + d_y * cos_r
    return local_x, local_y


def local_to_global(x_c, y_c, _rotation, _x, _y):
    cos_r = math.cos(_rotation)
    sin_r = math.sin(_rotation)
    global_x = x_c + _x * cos_r - _y * sin_r
    global_y = y_c + _x * sin_r + _y * cos_r
    return global_x, global_y