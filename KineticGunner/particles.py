# Particles ------------------------------------------------------------------ #

from vector import Vector3
import utils
import math
import ent
import ogre.renderer.OGRE as ogre

class Particles:
    def __init__(self, ent):
        self.ent = ent
        self.thruster = None
        # Create Smoke and Explosion Particles
        self.smoke = self.ent.engine.gfxMgr.sceneManager.createParticleSystem("Smoke" + self.ent.uiname, "Angst/Smoke")
        self.ent.renderer.oNode.attachObject(self.smoke)
        self.smoke.setEmitting(False)

        self.explosion = self.ent.engine.gfxMgr.sceneManager.createParticleSystem("Explosion" + self.ent.uiname, "Angst/Explosion")
        self.ent.renderer.oNode.attachObject(self.explosion)
        self.explosion.setEmitting(False)
        
        # Create Thrusters
        if ent.flag == "Player":
            self.thruster = self.ent.engine.gfxMgr.sceneManager.createParticleSystem("Thrust" + self.ent.uiname, "Angst/PlayerThruster")
            self.ent.renderer.oNode.attachObject(self.thruster)
            pass
            
        elif ent.flag == "Enemy":
            self.thruster = self.ent.engine.gfxMgr.sceneManager.createParticleSystem("Thrust" + self.ent.uiname, "Angst/EnemyThruster")
            self.ent.renderer.oNode.attachObject(self.thruster)
            pass
            
        elif ent.flag == "Missile":
            self.thruster = self.ent.engine.gfxMgr.sceneManager.createParticleSystem("Thrust" + self.ent.uiname, "Angst/MissileThruster")
            self.ent.renderer.oNode.attachObject(self.thruster)
            pass
        
    def tick(self, dtime):
        # Particles
        if self.ent.flag == "Dead":
            self.smoke.setEmitting(False)
            if self.thruster:
                self.thruster.setEmitting(False)
            self.explosion.setEmitting(True)
            pass
        elif self.ent.flag == "Damaged":
            self.smoke.setEmitting(True)
            pass
        
    def delete(self):
        self.smoke.setEmitting(False)
        self.ent.renderer.oNode.detachObject(self.smoke)
        self.explosion.setEmitting(False)
        self.ent.renderer.oNode.detachObject(self.explosion)
        if self.thruster:
            self.thruster.setEmitting(False)
            self.ent.renderer.oNode.detachObject(self.thruster)
        self.ent = None
        
# Particles ------------------------------------------------------------------ #
