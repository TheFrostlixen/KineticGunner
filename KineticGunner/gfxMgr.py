# Graphics manager
from vector import Vector3
import ogre.renderer.OGRE as ogre
#import ogre.renderer.ogreterrain as ogreterrain

# Manages graphics. Creates graphics, scene, scene nodes, renders scene
class GfxMgr:
    def __init__(self, engine):
        self.engine = engine
        self.freeNodes = []
        self.usedNodes = []
        self.totalNodes = 0

    def init(self):
        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.createScene()
        self.laserTimer = 0
        self.laserDuration = 0.20
        self.rayDuration = 0.25

    def showLaser(self, main = True):
        if main:
            self.laserTimer = self.laserDuration
            self.laser.setVisible(True)
        else:
            self.laserTimer = self.rayDuration
            self.ray.setVisible(True)
        pass

    def tick(self, dtime):
        if self.laser and self.laserTimer > 0:
            self.laserTimer -= dtime
            if self.laserTimer <= 0:
                self.laser.setVisible(False)
                self.ray.setVisible(False)
        self.root.renderOneFrame()

    # The Root constructor for the ogre
    def createRoot(self):
        self.root = ogre.Root()
 
    # Here the resources are read from the resources.cfg
    def defineResources(self):
        cf = ogre.ConfigFile()
        cf.load("resources.cfg")
 
        seci = cf.getSectionIterator()
        while seci.hasMoreElements():
            secName = seci.peekNextKey()
            settings = seci.getNext()
 
            for item in settings:
                typeName = item.key
                archName = item.value
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)
 
    # Create and configure the rendering system (either DirectX or OpenGL) here
    def setupRenderSystem(self):
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled the config dialog -> Application.setupRenderSystem()")
 
    # Create the render window
    def createRenderWindow(self):
        self.root.initialise(True, "(CS 381 Spring 2014 Final Project)")
 
    # Initialize the resources here (which were read from resources.cfg in defineResources()
    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
        self.materialManager = ogre.MaterialManager.getSingleton()
        self.materialManager.setDefaultTextureFiltering(ogre.TFO_ANISOTROPIC)
        self.materialManager.setDefaultAnisotropy(7)
 
    # Now, create a scene here. Three things that MUST BE done are sceneManager, camera and
    # viewport initializations
    def createScene(self):
        self.sceneManager = self.root.createSceneManager(ogre.ST_EXTERIOR_CLOSE, "Default SceneManager")
        #self.sceneManager.shadowTechnique = ogre.SHADOWTYPE_STENCIL_MODULATIVE
        self.sceneManager.setShadowFarDistance( 10000 )
        self.meshManager = ogre.MeshManager.getSingleton ()

        self.camera = self.sceneManager.createCamera("Camera")
        self.camera.nearClipDistance = 1

        self.viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)
        self.particleManager = ogre.ParticleSystemManager.getSingleton()
        

    def setupCamera(self):
        self.debugYawNode = self.sceneManager.getRootSceneNode().createChildSceneNode('CamNodeD',(12500, 10000, 12500))
        self.debugPitchNode = self.debugYawNode.createChildSceneNode('PitchNodeD')
        
        self.camYawNode = self.engine.entityMgr.player.renderer.oNode.createChildSceneNode('CamNode1',(0, 30, 0))
        self.camPitchNode = self.camYawNode.createChildSceneNode('PitchNode1')
        self.camPitchNode.attachObject(self.camera)
        
        self.laser = self.sceneManager.createParticleSystem( "Laser", "Angst/Laser" )
        self.laserNode = self.camPitchNode.createChildSceneNode('LaserNode', (0,-6,0))
        self.laserNode.attachObject(self.laser)
        self.laser.setVisible(False)

        self.ray = self.sceneManager.createParticleSystem( "Ray", "Angst/Ray" )
        self.rayNode = self.camPitchNode.createChildSceneNode('RayNode', (0,-6,0))
        self.rayNode.attachObject(self.ray)
        self.ray.setVisible(False)

        self.turret = self.sceneManager.createEntity("LAZER", "laser.mesh")
        self.turretNode = self.camPitchNode.createChildSceneNode('turretNode', (0,-10,-5))
        #self.turretNode.setInheritOrientation(False)
        self.turretNode.yaw(ogre.Degree(90))
        self.turretNode.roll(ogre.Degree(10))
        self.turretNode.attachObject(self.turret)
        
        #Currently Debug Trail
        sunParticle = self.sceneManager.createParticleSystem("Sun", "Angst/Sun")
        sunNode = self.camYawNode.createChildSceneNode("SunNode", (0,-50,0))
        sunNode.setInheritOrientation(False)
        sunNode.attachObject(sunParticle)
        
        self.engine.camMgr.crosslink()
        
    def setupScene1(self):
        # Everything after this can be level specific and is deleted by clearScene() #
        self.sceneManager.ambientLight = 0.1, 0.1, 0.05
        self.light = self.sceneManager.createLight ('Sun')
        self.light.type = ogre.Light.LT_DIRECTIONAL
        self.light.direction = Vector3(0, -1, 1).normalisedCopy()
        self.light.diffuseColour = (0.8, 0.8, 0.6)
        self.light.specularColour = (0.8, 0.8, 0.6)
 
        # sunParticle = self.sceneManager.createParticleSystem("Sun", "Angst/Sun")
        # sunNode = self.camPitchNode.createChildSceneNode("Particle", (0,5,5))
        # sunNode.attachObject(sunParticle)
 
        # Setup a ground plane
        worldSize = 25000
        height = 160
        self.sceneManager.setWorldGeometry("terrain.cfg")
        self.groundPlane = ogre.Plane ((0, 1, 0), height)
        self.meshManager.createPlane ('Ground', 'General', self.groundPlane,
                                    worldSize, worldSize, 20, 20, True, 1, 5, 5, (0, 0, 1))
        ent = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode('Water', (worldSize/2,0,worldSize/2)).attachObject(ent)
        ent.setMaterialName ('Angst/Ocean2_Cg')
        ent.castShadows = False
        # Sky Box/Plane --------------------------------------------------------
        self.sceneManager.setSkyDome (True, "Angst/Sky1", 10, 6)
        #plane = ogre.Plane ((0, -1, 0), -10)
        #self.sceneManager.setSkyPlane (True, plane, "Examples/SpaceSkyPlane", 100, 45, True, 0.5, 150, 150)
        # Fog ------------------------------------------------------------------
        #fadeColour = (0.1, 0.1, 0.1)
        #self.viewPort.backgroundColour = fadeColour
        #self.sceneManager.setFog (ogre.FOG_LINEAR, fadeColour, 0.0, 3000, 7500)
        
        #ent = self.sceneManager.createEntity('MountainEnt', 'Mountain.mesh')
        #node = self.sceneManager.getRootSceneNode().createChildSceneNode('Mountain', (0,325,0))
        #node.attachObject(ent)
        #node.setScale(500,1500,1000)
        
        self.setupCamera()

    def setupScene2(self):
        # Everything after this can be level specific ##############################################
        self.sceneManager.ambientLight = 0.05, 0.05, 0.075
        self.light = self.sceneManager.createLight ('Moon')
        self.light.type = ogre.Light.LT_DIRECTIONAL
        self.light.direction = Vector3(1, -1, 1).normalisedCopy()
        self.light.diffuseColour = (0.4, 0.4, 0.6)
        self.light.specularColour = (0.4, 0.4, 0.6)
 
        # Setup a ground plane.
        worldSize = 25000
        height = 160
        self.sceneManager.setWorldGeometry("terrain2.cfg")
        self.groundPlane = ogre.Plane ((0, 1, 0), height)
        #meshManager = ogre.MeshManager.getSingleton ()
        self.meshManager.createPlane ('Ground', 'General', self.groundPlane,
                                    35000, 35000, 20, 20, True, 1, 5, 5, (0, 0, 1))
        water = self.sceneManager.createEntity('GroundEntity', 'Ground')
        self.sceneManager.getRootSceneNode().createChildSceneNode('Water', (worldSize/2,0,worldSize/2)).attachObject(water)
        water.setMaterialName ('OceanCg')
        water.castShadows = False
        # Sky Box/Plane --------------------------------------------------------
        self.sceneManager.setSkyDome (True, "Angst/Nebula2", 10, 4)
        #plane = ogre.Plane ((0, -1, 0), -10)
        #self.sceneManager.setSkyPlane (True, plane, "Examples/SpaceSkyPlane", 100, 45, True, 0.5, 150, 150)
        # Fog ------------------------------------------------------------------
        #fadeColour = (0.1, 0.1, 0.1)
        #self.viewPort.backgroundColour = fadeColour
        #self.sceneManager.setFog (ogre.FOG_LINEAR, fadeColour, 0.0, 3000, 7500)
        self.setupCamera()

    def clearScene(self):
        self.camera.parentSceneNode.detachObject(self.camera)
        self.laser.parentSceneNode.detachObject(self.laser)
        self.laser = None
        self.freeNodes = []
        self.usedNodes = []
        self.totalNodes = 0
        self.sceneManager.clearScene()

    def crosslink(self):
        self.setupCamera()
 
    # In the end, clean everything up (delete)
    def stop(self):
        del self.root

    # Creating and Recycling of Scene Nodes
    def getNode(self):
        if len(self.freeNodes) > 0:
            node = self.freeNodes.pop()#len(self.freeNodes) )
            # Show?
        else:
            node = self.sceneManager.getRootSceneNode().createChildSceneNode(str(self.totalNodes))
            self.totalNodes += 1
        self.usedNodes.append( node )
        return node
        
    def recycleNode(self, node):
        i = self.usedNodes.index(node)
        self.usedNodes.pop(i)
        # hide?
        self.freeNodes.append(node)
        return node
        
# ---------------------------------------------------------------------------- #
