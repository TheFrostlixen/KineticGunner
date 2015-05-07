from expression import Expression
import math

class Pathing:    
    def __init__(self, ent, speed = [], yaw = [], pitch = []):
        self.paths = {}
        self.indices = {}
        self.ent = ent
        # Speed
        self.paths['speed'] = speed
        self.indices['speed'] = 0
        # Yaw
        self.paths['yaw'] = yaw
        self.indices['yaw'] = 0
        # Pitch
        self.paths['pitch'] = pitch
        self.indices['pitch'] = 0
    
    def tick(self, dt):
        # Yaw ---------------------------------------------
        if len(self.paths['yaw']) > 0:
            rate = self.paths['yaw'][self.indices['yaw']].tick(dt)
            self.ent.yawRate = math.fabs(rate)
            self.ent.desiredYaw = self.ent.yaw + rate
            if self.paths['yaw'][self.indices['yaw']].complete():
                self.indices['yaw'] = (self.indices['yaw'] + 1) % len(self.paths['yaw'])
                
        # Pitch -------------------------------------------
        if len(self.paths['pitch']) > 0:
            rate = self.paths['pitch'][self.indices['pitch']].tick(dt)
            self.ent.pitchRate = math.fabs(rate)
            self.ent.desiredPitch = self.ent.pitch + rate
            if self.paths['pitch'][self.indices['pitch']].complete():
                self.indices['pitch'] = (self.indices['pitch'] + 1) % len(self.paths['pitch'])
                
        # Speed -------------------------------------------
        if len(self.paths['speed']) > 0:
            rate = self.paths['speed'][self.indices['speed']].tick(dt)
            self.ent.acceleration = math.fabs(rate)
            self.ent.desiredSpeed = self.ent.speed + rate
            if self.paths['speed'][self.indices['speed']].complete():
                self.indices['speed'] = (self.indices['speed'] + 1) % len(self.paths['speed'])


    def setMultiple(self, speed = [], yaw = [], pitch = []):
        self.paths['speed'] = speed
        self.paths['yaw'] = yaw
        self.paths['pitch'] = pitch
            
#---------------------------------------------------------------------------------------------------
