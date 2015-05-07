# Entity Manager ------------------------------------------------------------- #

from vector import Vector3
import command

class EntityMgr:
    def __init__(self, engine):
        import time
        print "starting ent mgr"
        self.engine = engine
                
    def init(self):
        # Player --------
        self.player = None
        ##self.projectiles = {}
        ##self.nProjs = 0
        # Hostiles ------
        self.enemies = {}
        self.nEnems = 0
        self.missiles = {}
        self.nMissiles = 0
        # Other ---------
        self.dead = []
        import random ##--##
        self.randomizer = random
        self.randomizer.seed(None)
        import ent ##--##
        self.entTypes = [ent.PlayerJet, ent.EnemyJet]

    def createPlayer(self, playerType, pos, yaw, speed):
        self.player = playerType(self.engine, 0, pos, yaw, speed)
        self.player.init()
        self.player.renderer.oEnt.setMaterialName ('Angst/Player')
        return self.player
    
    def createEnemy(self, enemyType, pos = None, speed = None):
        if pos == None:
            x = self.randomizer.randint(-5000, 5000)
            y = self.randomizer.randint(-500, 2500)
            z = self.randomizer.randint(-5000, 5000)
            pos = self.player.pos + Vector3(x,y,z)
        if speed == None:
            speed = self.player.speed + 10
            
        ent = enemyType(self.engine, self.nEnems, pos, 0, speed)
        ent.init()
        ent.unitai.addCommand( command.OffsetFollow(ent, self.player, self.createRandomOffset()) )
        self.enemies[ent.uiname] = ent;
        self.nEnems = self.nEnems + 1
        ent.renderer.oEnt.setMaterialName ('Angst/Enemy')
        return ent
        
    def createMissile(self, missileType, source):
        ent = missileType(self.engine, self.nMissiles, source)
        ent.init()
        ent.unitai.addCommand( command.Ram(ent, self.player) )
        self.missiles[ent.uiname] = ent;
        self.nMissiles = self.nMissiles + 1
        ent.renderer.oEnt.setMaterialName ('Angst/Missile')
        return ent
        
    def Cleanup(self):
        for ent in self.dead:
            # Get ID
            index = ent.uiname
            # Remove from List
            if index in self.enemies:
                self.enemies.pop(index)
            elif index in self.missiles:
                self.missiles.pop(index)
            # Delete Ent and ogre ent
            node = ent.delete()
            # Recycle Node
            self.engine.gfxMgr.recycleNode(node)
            print 'Enemy Count: ' + str(len(self.enemies))
            print 'Missile Count: ' + str(len(self.missiles))
        # Clear List
        self.dead = []
        
    def clear(self):
        # Player --------
        self.player = None
        ##self.projectiles = {}
        ##self.nProjs = 0
        # Hostiles ------
        self.enemies = {}
        self.nEnems = 0
        self.missiles = {}
        self.nMissiles = 0
        # Other ---------
        self.dead = []

    def createRandomOffset(self):
        x = self.randomizer.randint(-250, -175)
        y = self.randomizer.randint(75,125)
        i = self.randomizer.randint(1,2)
        z = self.randomizer.randint(175, 250) * (-1)**i
        return Vector3(x,y,z)

    def tick(self, dt):
        # for eid, ent in self.ents.iteritems():
            # ent.tick(dt)
        if self.player:
            self.player.tick(dt)
        for eid, ent in self.enemies.iteritems():
            ent.tick(dt)
        for eid, ent in self.missiles.iteritems():
            ent.tick(dt)
        # Cleanup
        self.Cleanup()
        
# Entity Manager ------------------------------------------------------------- #
