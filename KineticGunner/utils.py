import math

def clamp(val, min, max):
    if val <= min:
        return min
    elif val >= max:
        return max

    return val

def fixAngle(angle):
    while angle > 180.0:
        angle -= 360.0
    while angle < -180.0:
        angle += 360.0

    return angle

def diffAngle(angle1, angle2):
    return fixAngle(angle1 - angle2)

