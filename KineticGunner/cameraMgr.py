import ogre.renderer.OGRE as ogre
from vector import Vector3
import utils

class CamMgr:
    def __init__(self, engine):
        self.engine = engine
        self.camYaw = 180.0
        self.yawSpeed = -0.1
        self.camPitch = 0.0
        self.pitchSpeed = -0.1
        self.pitchMax = 80.0
        self.pitchMin = -10.0
        self.debugCam = False
        self.toggle = 0.1
        self.toggleMax = 0.1
        self.transVector = Vector3(0,0,0)
        self.yawRot = 0.0
        self.pitchRot = 0.0
        self.rollRot = 0.0
        print "-- Starting Camera Manager --"

    def init(self):
        self.camYawNode = None
        self.camPitchNode = None
        pass        

    def crosslink(self):
        ''' Links Camera Nodes from Graphics Manager '''
        self.camera = self.engine.gfxMgr.camera
        self.camYawNode = self.engine.gfxMgr.camYawNode
        self.camPitchNode = self.engine.gfxMgr.camPitchNode
        self.camYawNode.yaw(ogre.Degree(self.camYaw).valueRadians())
        self.camPitchNode.pitch(ogre.Degree(self.camPitch).valueRadians())

    def tick(self, dt):
        ''' Update Camera Toggle Timer, Yaw, Pitch, and Roll '''
        if self.toggle > 0.0:
            self.toggle -= dt
        if self.camYawNode:
            self.camYawNode.translate(self.camYawNode.orientation * self.transVector * dt)
            self.transVector = Vector3(0,0,0)
            self.Yaw(self.yawRot)
            self.yawRot = 0.0
        if self.camPitchNode:
            self.Pitch(self.pitchRot)
            self.pitchRot = 0.0
            self.camPitchNode.roll(ogre.Degree(self.rollRot))
            self.rollRot = 0.0

    def Yaw(self, amount):
        ''' Yaws the Camera Yaw Node clamped by Min and Max '''
        self.camYaw = utils.fixAngle( self.camYaw + self.yawSpeed * amount )
        self.camYawNode.resetOrientation()
        self.camYawNode.yaw(ogre.Degree(self.camYaw).valueRadians())

    def Pitch(self, amount):
        ''' Pitches the Camera Pitch Node clamped by Min and Max '''
        self.camPitch = utils.fixAngle( self.camPitch + self.pitchSpeed * amount )
        self.camPitch = utils.clamp( self.camPitch, self.pitchMin, self.pitchMax )
        self.camPitchNode.resetOrientation()
        self.camPitchNode.pitch(ogre.Degree(self.camPitch).valueRadians())

    def swap(self):
        ''' Swaps between 1st person and 3rd person (debug) cameras '''
        if self.toggle <= 0.0:
            self.toggle = self.toggleMax
            self.debugCam = not self.debugCam
            if( self.debugCam ):
                self.camYawNode = self.engine.gfxMgr.debugYawNode
                self.camPitchNode = self.engine.gfxMgr.debugPitchNode
                self.pitchMin = -90.0
            else:
                self.camYawNode = self.engine.gfxMgr.camYawNode
                self.camPitchNode = self.engine.gfxMgr.camPitchNode
                self.pitchMin = 0.0
            self.camera.parentSceneNode.detachObject(self.camera)
            self.camPitchNode.attachObject(self.camera)
    
    def clear(self):
        self.camYawNode = None
        self.camPitchNode = None
        self.camYaw = 180.0
        self.camPitch = 0.0
        
    def stop(self):
        self.camera = None
        self.camYawNode = None
        self.camPitchNode = None
        pass

