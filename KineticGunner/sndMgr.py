# Sound Manager -------------------------------------------------------------- #

import math
from vector import Vector3
import ogre.renderer.OGRE as ogre
#import ogre.io.OIS as OIS
import ogre.sound.OgreAL as OgreAL


class SndMgr:

    def __init__(self, engine):
        self.engine = engine
        self.manager = OgreAL.SoundManager()
        self.soundCount = 0
        self.bgm = None
        self.missileExplode = "Grenade.wav"
        self.laser = "laser.wav"
        self.hit = "Hit.wav"
        self.jetExplode = "Bomb.wav"
        print "Sound Manager Constructed "
        
    def init(self):
        print "Initializing Sound manager"
        pass

    def playSound(self, snd, pos = None):
        sound = self.manager.createSound("Snd" + str(self.soundCount), snd)
        self.soundCount += 1
        if pos:
            sound.setPosition( pos )
        sound.setGain(0.25)
        sound.play()

    def playMusic(self, msc):
        if self.bgm:
            self.bgm.pause()
            self.manager.destroySound( self.bgm )
        self.bgm = self.manager.createSound("bgm", msc) #, True) #Looping Causes Crashes
        self.bgm.setGain(0.1)
        self.bgm.play()
        
    def stop(self):
        self.bgm.pause()
        self.manager.destroyAllSounds()
        
    def tick(self, dtime):
        pass

# Sound Manager -------------------------------------------------------------- #
