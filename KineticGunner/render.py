# Renderer ------------------------------------------------------------------- #

from vector import Vector3
import utils
import math
import ent
import ogre.renderer.OGRE as ogre

class Renderer:
    def __init__(self, ent):
        ''' Creates ogre SceneNode and Entity and attaches them. '''
        self.ent = ent
        print "Rendering setting up for: ", str(self.ent)
        self.oEnt =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + "_ogreEnt", self.ent.mesh)
        self.oNode =  self.ent.engine.gfxMgr.getNode()
        self.oNode.attachObject(self.oEnt)
        self.oNode.setPosition(self.ent.pos)
        #self.yawNode =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + 'yNode', ent.pos)
        #self.pitchNode = self.yawNode.createChildSceneNode(self.ent.uiname + 'pNode')
        #self.rollNode = self.pitchNode.createChildSceneNode(self.ent.uiname + 'rNode')
        #self.pitchNode.yaw( ogre.Degree(90) )
        #self.rollNode.attachObject(self.oEnt)
        
    def tick(self, dtime):
        ''' Updates SceneNode Position, Orientation and Visibility. '''
        self.oNode.setPosition(self.ent.pos)
        self.oNode.resetOrientation()
        self.oNode.yaw( ogre.Degree(self.ent.yaw+90) )
        # Pitch and Roll reversed due to Model facing
        self.oNode.pitch( ogre.Degree(-self.ent.pitch) )
        self.oNode.roll( ogre.Degree(self.ent.roll) )
        # Check for Explosion
        if self.ent.flag == "Dead":
            self.oEnt.setVisible(False)
        
    def delete(self):
        ''' Detaches ogre Entity and releases references. '''
        self.oNode.detachObject(self.oEnt)
        #self.oEnt.detachFromParent()
        self.oEnt = None
        node = self.oNode
        self.oNode = None
        self.ent = None
        return node
        
# Renderer ------------------------------------------------------------------- #
