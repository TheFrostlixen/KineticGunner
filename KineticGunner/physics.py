# Physics -------------------------------------------------------------------- #

from vector import Vector3
import utils
import math

class Physics:
    def __init__(self, ent):
        self.ent = ent
        
    def tick(self, dtime):
        #----------position-----------------------------------
        timeScaledAcceleration = self.ent.acceleration * dtime
        self.ent.speed += utils.clamp( self.ent.desiredSpeed - self.ent.speed, -timeScaledAcceleration, timeScaledAcceleration)
        self.ent.vel.y = self.ent.speed * math.sin( math.radians( self.ent.pitch ) )
        #xz = self.ent.speed * math.cos( math.radians( self.ent.pitch ) )
        self.ent.vel.x = self.ent.speed * math.cos( math.radians( self.ent.yaw ) )
        self.ent.vel.z = self.ent.speed * -math.sin( math.radians( self.ent.yaw ) )
        self.ent.pos = self.ent.pos + ( self.ent.vel * dtime )

        # Yaw -----------------------------------
        timeScaledYaw = self.ent.yawRate * dtime
        angleDiff = utils.diffAngle(self.ent.desiredYaw, self.ent.yaw)
        self.ent.deltaYaw = utils.clamp(angleDiff, -timeScaledYaw, timeScaledYaw)
        # print '---' + self.ent.uiname + '---'
        # print "angleDiff: %f, timeScaledYaw: %f,  deltaYaw: %f " % (angleDiff, timeScaledYaw, self.ent.deltaYaw )
        # print "yaw: %f, desiredYaw: %f, yawRate: %f" % (self.ent.yaw, self.ent.desiredYaw, self.ent.yawRate)
        self.ent.yaw = utils.fixAngle( self.ent.yaw + self.ent.deltaYaw)
        # Pitch ---------------------------------
        timeScaledPitch = self.ent.pitchRate * dtime
        angleDiff = utils.diffAngle(self.ent.desiredPitch, self.ent.pitch)
        self.ent.deltaPitch = utils.clamp(angleDiff, -timeScaledPitch, timeScaledPitch)
        # print "angleDiff: %f, timeScaledPitch: %f,  deltaPitch: %f " % (angleDiff, timeScaledPitch, self.ent.deltaPitch )
        # print "pitch: %f, desiredPitch: %f, pitchRate: %f" % (self.ent.pitch, self.ent.desiredPitch, self.ent.pitchRate)
        self.ent.pitch = utils.fixAngle( self.ent.pitch + self.ent.deltaPitch)
        # Roll ----------------------------------
        if dtime > 0.001:
            self.ent.desiredRoll = -self.ent.deltaYaw / dtime * 0.75
        timeScaledRoll = self.ent.rollRate * dtime
        angleDiff = utils.diffAngle(self.ent.desiredRoll, self.ent.roll)
        self.ent.deltaRoll = utils.clamp(angleDiff, -timeScaledRoll, timeScaledRoll)
        # print "angleDiff: %f, timeScaledRoll: %f,  dRoll: %f " % (angleDiff, timeScaledRoll, self.ent.deltaRoll )
        # print "roll: %f, desiredRoll: %f, rollRate: %f" % (self.ent.roll, self.ent.desiredRoll, self.ent.rollRate)
        # print "---"
        self.ent.roll = utils.fixAngle( self.ent.roll + self.ent.deltaRoll)
        
# Physics -------------------------------------------------------------------- #