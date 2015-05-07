# Commands ------------------------------------------------------------------- #

from vector        import Vector3
import utils
import math
import ent

#------------------------------------------------------------------------------#

class Command:
    def __init__(self, ent):
        self.ent = ent
        pass

    def getDesiredHeadingToTargetPosition(self, targetPos):
        diff = targetPos - self.ent.pos
        return math.degrees(math.atan2(-diff.z, diff.x))
    
    def tick(self, dtime):
        pass

#------------------------------------------------------------------------------#

class Move( Command ):
    def __init__(self, ent, targ):
        Command.__init__(self, ent)
        self.target = targ
        
    def tick(self, dt):
        return True

#------------------------------------------------------------------------------#

class Crash( Command ):
    def __init__(self, ent):
        Command.__init__(self, ent)
        self.ent.desiredPitch = -40
        self.ent.desiredSpeed = self.ent.speed
        self.ent.desiredYaw = self.ent.yaw
        self.ent.desiredRoll = self.ent.roll
        self.timer = 3.0
        
    def tick(self, dt):
        ## Check for Ground
            ## Raytrace forward
            ## Check Distance to closest
            ## If Ent and not terrain
                ## Kill it as well
                ## Die
            ## If Ground
                ## Die
                
        # raySceneQuery = self.engine.gfxMgr.sceneManager.createRayQuery(ogre.Ray( self.ent.pos, self.ent.vel ))
        # raySceneQuery.setSortByDistance( True )

        # result = raySceneQuery.execute()
        # if len(result) > 0:
            # if result[0].first < 50:
                # if item.movable:
                    # print item.movable.getName()
                # elif item.worldFragment:
                    # print item.worldFragment
                # #self.ent.die()
        # self.engine.gfxMgr.sceneManager.destroyQuery(raySceneQuery)
        
        ## vs Height
            ## if < ground
                ## Die
                ## Return True
            ## else:
                ## Return False
                
        ## vs Timer
        ## Update Timer
        self.timer -= dt
            ## Check for Done
        if self.timer < 0:
            ## Return True/False
            self.ent.unitai.addCommand( Explode(self.ent) )
            return True
            ## Die
        return False
        
#------------------------------------------------------------------------------#

class Explode( Command ):
    def __init__(self, ent):
        Command.__init__(self, ent)
        self.ent.desiredPitch = self.ent.pitch
        self.ent.desiredSpeed = self.ent.speed
        self.ent.desiredYaw = self.ent.yaw
        self.ent.desiredRoll = self.ent.roll
        self.ent.desiredSpeed = 0
        self.ent.speed = 0
        self.timer = 2.0
        self.ent.flag = "Dead"
        
    def tick(self, dt):
        self.ent.desiredSpeed = 0
        self.timer -= dt
        if self.timer < 0:
            self.ent.engine.entityMgr.dead.append(self.ent)
            return True
        return False
        
#------------------------------------------------------------------------------#

class Ram( Command ):
    def __init__(self, ent, targ):
        Command.__init__(self, ent)
        self.target = targ

    def tick(self, dtime):
        # Check Planar Distance
        self.ent.distance = math.sqrt((self.target.pos.x - self.ent.pos.x)**2 + (self.target.pos.z - self.ent.pos.z)**2)
        # Check Distance
        if self.ent.distance < 75:
            # Explode
            self.target.damage(self.ent.explodeDmg)
            self.ent.damage(self.ent.explodeDmg)
            self.ent.unitai.addCommand( Explode(self.ent) )
            return True
        # Set Planar Orientation (Yaw)
        self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(self.target.pos)
        
        # Check Relative Position
        angle = utils.diffAngle(self.ent.yaw, self.ent.desiredYaw)
        if math.fabs( angle) > 90:
            self.ent.desiredSpeed = self.ent.maxSpeed - math.fabs(self.ent.speed - self.ent.maxSpeed)
            self.ent.desiredYaw = self.target.yaw
        else:
            self.ent.desiredSpeed = self.ent.maxSpeed
        # Height Difference (Pitch)
        difference = self.target.pos.y - self.ent.pos.y
        self.ent.desiredPitch = math.degrees(math.atan2(difference, self.ent.distance))
        #return False
        
        # print "Self: %s, Target Name: %s, Distance2: %f, Angle: %f" % (self.ent.uiname, self.target.uiname, self.ent.distance, angle)
        # print "CURRENT:: yaw: %f, speed: %f, pitch: %f" % (self.ent.yaw, self.ent.speed, self.ent.pitch)
        # print "DESIRED:: yaw: %f, speed: %f, pitch: %f" % (self.ent.desiredYaw, self.ent.desiredSpeed, self.ent.desiredPitch)
        # print "Target:: " + self.target.uiname
        # print "Target Vel: " + str(self.target.vel)
        # print "Self Vel: " + str(self.ent.vel) +'\n'
        
#------------------------------------------------------------------------------#

class Follow( Command ):
    def __init__(self, ent, targ):
        Command.__init__(self, ent)
        self.target = targ

    def tick(self, dtime):
        # Check Planar Distance
        self.ent.distance = math.sqrt((self.target.pos.x - self.ent.pos.x)**2 + (self.target.pos.z - self.ent.pos.z)**2)
        # Set Planar Orientation (Yaw)
        self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(self.target.pos)
        # Check Distance
        if self.ent.distance < 100:
            if math.fabs(utils.diffAngle(self.ent.yaw, self.ent.desiredYaw)) < 90:
                self.ent.desiredSpeed = self.target.speed
            else:
                self.ent.desiredSpeed = self.ent.maxSpeed - math.fabs(self.ent.speed - self.ent.maxSpeed)
                self.ent.desiredYaw = self.target.yaw
        else:
            self.ent.desiredSpeed = self.ent.maxSpeed
        # Height Difference (Pitch)
        difference = self.target.pos.y - self.ent.pos.y
        self.ent.desiredPitch = math.degrees(math.atan2(difference, self.ent.distance))
        
        # print "CURRENT:: yaw: %f, speed: %f, pitch: %f" % (self.ent.yaw, self.ent.speed, self.ent.pitch)
        # print "DESIRED:: yaw: %f, speed: %f, pitch: %f" % (self.ent.desiredYaw, self.ent.desiredSpeed, self.ent.desiredPitch)
        # print "Target:: " + self.target.uiname
        # print "VEL:: Target: " + str(self.target.vel)
        # print "VEL:: Self: " + str(self.ent.vel) +'\n'
        
#------------------------------------------------------------------------------#

class OffsetFollow( Command ):
    def __init__(self, ent, targ, offset = Vector3(0,0,0)):
        Command.__init__(self, ent)
        self.target = targ
        self.offset = math.sqrt((offset.x)**2 + (offset.z)**2)
        self.angle = math.degrees(math.atan2(-offset.z, offset.x))
        self.height = offset.y

    def tick(self, dtime):
        # Set Target Point
        point = Vector3(0, self.target.pos.y + self.height, 0)
        angleRad = math.radians(utils.diffAngle(self.target.yaw, -self.angle))
        point.x = self.target.pos.x + self.offset * math.cos(angleRad)
        point.z = self.target.pos.z + self.offset * -math.sin(angleRad)
        # Check Planar Distance
        self.ent.distance = math.sqrt((point.x - self.ent.pos.x)**2 + (point.z - self.ent.pos.z)**2)
        # Set Planar Orientation (Yaw)
        self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(point)
        # Check Distance
        if self.ent.distance < 100:
            if math.fabs(utils.diffAngle(self.ent.yaw, self.ent.desiredYaw)) < 90:
                self.ent.desiredSpeed = self.target.speed
            else:
                self.ent.desiredSpeed = self.ent.maxSpeed - math.fabs(self.ent.speed - self.ent.maxSpeed)
                self.ent.desiredYaw = self.target.yaw
        else:
            self.ent.desiredSpeed = self.ent.maxSpeed
        # Height Difference (Pitch)
        self.ent.difference = self.ent.pos.y - point.y
        self.ent.desiredPitch = math.degrees(math.atan2(-self.ent.difference, self.ent.distance))

        # print "Self: %s, Target Name: %s" % (self.ent.uiname, self.target.uiname)
        # print "CURRENT:: yaw: %f, speed: %f, pitch: %f" % (self.ent.yaw, self.ent.speed, self.ent.pitch)
        # print "DESIRED:: yaw: %f, speed: %f, pitch: %f" % (self.ent.desiredYaw, self.ent.desiredSpeed, self.ent.desiredPitch)
        # print "Target:: " + self.target.uiname
        # print "Target Vel: " + str(self.target.vel)
        # print "Self Vel: " + str(self.ent.vel) +'\n'
        
#------------------------------------------------------------------------------#

class Intercept( Command ):
    def __init__(self, ent, targ):
        Command.__init__(self, ent)
        self.target = targ

    def tick(self, dtime):
        # Calculate Intercept Point
        sqrDist = self.ent.pos.squaredDistance(self.target.pos)
        
        # Set Planar Orientation (Yaw)
        self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(self.target.pos)
        # Check Distance
        if sqrDist < 250:
            # Explode
            self.target.damage(25)
            self.ent.unitai.setCommand( Explode(self.ent) )

        else:
            # Set Course
            distance = math.sqrt(sqrDist)
            speed = math.fabs(self.ent.speed - self.target.speed)
            if speed:
                time = distance / speed
            else:
                time = 10
            point = self.target.pos + self.target.vel * time
            self.ent.desiredYaw = self.getDesiredHeadingToTargetPosition(point)
            self.ent.desiredSpeed = self.ent.maxSpeed
            difference = point.y - self.ent.pos.y
            self.ent.desiredPitch = math.degrees(math.atan2(difference, distance))

            print "Self:: " + self.ent.uiname
            print "Target:: Name: %s, Point: %s, Speed: %f" % (self.target.uiname, str(point), self.target.speed)
            print "Distance: %f, yDiff: %f, Time: %f, Speed: %f" % (distance, difference, time, speed )
            print "CURRENT:: yaw: %f, speed: %f, pitch: %f" % (self.ent.yaw, self.ent.speed, self.ent.pitch)
            print "DESIRED:: yaw: %f, speed: %f, pitch: %f" % (self.ent.desiredYaw, self.ent.desiredSpeed, self.ent.desiredPitch)
            print "VEL:: Target: " + str(self.target.vel)
            print "VEL:: Self: " + str(self.ent.vel) + '\n'

    # def __init__(self, ent, targetEnt):
        # Command.__init__(self, ent, targetEnt)
        # self.targetEntity = targetEnt
        # self.entity.desiredHeading = self.getDesiredHeadingToTargetPosition(self.targetEntity.pos, self.entity.pos)
        # self.entity.desiredSpeed = self.entity.maxSpeed
        # self.done = False
        # self.isEntityTarget = True
        # print "Intercepting: ", str(self.targetEntity)

    # def tick(self, dt):
        # if not self.done:
            # if self.entity.pos.squaredDistance(self.targetEntity.pos) < 100:
                # self.done = True
                # self.entity.desiredSpeed = 0
            # else:
                # self.entity.desiredHeading = self.getDesiredHeadingToTargetPosition(self.targetEntity.pos, self.entity.pos)
                
    # def tick(self, dtime):
        # # Set Speed
        # self.ent.desiredSpeed = self.ent.maxSpeed

        # # Calculate Intercept Point
        # distance = math.sqrt((self.target.pos.x - self.ent.pos.x)**2 + (self.target.pos.z - self.ent.pos.z)**2)
        # speed = self.ent.speed
        # if( speed < 0.01 ):
            # time = 0
        # else:
            # time = distance / speed
        # print time
        # point = self.target.pos + self.target.vel * time
        
        # # Set Heading
        # self.ent.desiredHeading = math.atan2( -( point.z - self.ent.pos.z ),
                                                  # point.x - self.ent.pos.x )
        # self.ent.desiredHeading = utils.fixAngle(self.ent.desiredHeading)
        
# Commands ------------------------------------------------------------------- #