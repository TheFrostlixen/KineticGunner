import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class OverlayMgr():
    def __init__(self, engine):
        self.engine = engine

    def init(self):
        # vars
        self.showingSplash = False
        self.maxAngst = 510
        self.score = 0
        self.progLeftBound = 270
        self.uiHeight = 50

        # set up fonts & overlay manager
        self.overlayManager = ogre.OverlayManager.getSingleton()
        self.fontManager = ogre.FontManager.getSingleton()
        self.font = self.fontManager.create( "BlueHighway", "General" )
        self.font.setType(ogre.FT_TRUETYPE)
        self.font.setSource("fonts/bluehigh.ttf")
        self.fontManager.load( "BlueHighway", "General" )
        
        # Splash Screen
        self.splashScreen = self.overlayManager.createOverlayElement('Panel', 'SplashScreenPanel')
        self.splashScreen.metricsMode = ogre.GMM_PIXELS
        self.splashScreen.setPosition( 0, 0 )
        self.splashScreen.setDimensions( self.engine.gfxMgr.viewPort.actualWidth, self.engine.gfxMgr.viewPort.actualHeight )

        # Crosshairs
        self.targetPanel = self.overlayManager.createOverlayElement('Panel', 'TargetPanel')
        self.targetPanel.metricsMode = ogre.GMM_PIXELS
        self.targetPanel.setPosition(self.engine.gfxMgr.viewPort.actualWidth/2-64, self.engine.gfxMgr.viewPort.actualHeight/2-52)
        self.targetPanel.setDimensions(128, 128)
        self.targetPanel.materialName="Angst/Crosshair"

        # UI Panel
        self.uiPanel = self.overlayManager.createOverlayElement('Panel', 'UIPanel')
        self.uiPanel.metricsMode = ogre.GMM_PIXELS
        self.uiPanel.setPosition(0, self.engine.gfxMgr.viewPort.actualHeight-(self.uiHeight+50))
        self.uiPanel.setDimensions(self.engine.gfxMgr.viewPort.actualWidth, self.uiHeight+50)
        self.uiPanel.materialName="Angst/UI"

        # Score
        self.scoreText = self.overlayManager.createOverlayElement("TextArea", "ScoreTextArea")
        self.scoreText.setMetricsMode(ogre.GMM_PIXELS)
        self.scoreText.setCaption("Score: " + str(self.score))
        self.scoreText.setPosition(50, 10)
        self.scoreText.setFontName("BlueHighway")
        self.scoreText.setCharHeight(self.uiHeight - 5)
        self.scoreText.setColour( (1.0,1.0,0.7) ) #color of angst: (0.54,0.4,0.97)

        self.scorePanel = self.overlayManager.createOverlayElement("Panel", "ScorePanel")
        self.scorePanel.metricsMode = ogre.GMM_PIXELS
        self.scorePanel.setPosition(0, self.engine.gfxMgr.viewPort.actualHeight-self.uiHeight)
        self.scorePanel.setDimensions(self.uiHeight*3.75, self.uiHeight)
        self.scorePanel.addChild( self.scoreText )

        # Angst Meter Background
        self.angstBar = self.overlayManager.createOverlayElement('Panel', 'AngstPanel')
        self.angstBar.metricsMode = ogre.GMM_PIXELS
        self.angstBar.setPosition(self.engine.gfxMgr.viewPort.actualWidth-585, self.engine.gfxMgr.viewPort.actualHeight-self.uiHeight)
        self.angstBar.setDimensions(self.maxAngst, self.uiHeight)
        self.angstBar.materialName="Angst/BarBG"
        # Angst Meter
        self.angstMeter = self.overlayManager.createOverlayElement('Panel', 'AngstBarPanel')
        self.angstMeter.metricsMode = ogre.GMM_PIXELS
        self.angstMeter.setPosition(self.engine.gfxMgr.viewPort.actualWidth-584, self.engine.gfxMgr.viewPort.actualHeight-(self.uiHeight/2))
        self.angstMeter.setDimensions(0, (self.uiHeight/2))
        self.angstMeter.materialName="Angst/Bar"
        # Angst Meter 2
        self.angstMeter2 = self.overlayManager.createOverlayElement('Panel', 'AngstBarPanel2')
        self.angstMeter2.metricsMode = ogre.GMM_PIXELS
        self.angstMeter2.setPosition(self.engine.gfxMgr.viewPort.actualWidth-584, self.engine.gfxMgr.viewPort.actualHeight-(self.uiHeight))
        self.angstMeter2.setDimensions(0, (self.uiHeight/2))
        self.angstMeter2.materialName="Angst/Bar2"

        # Progress Bar
        self.progBar = self.overlayManager.createOverlayElement('Panel', 'ProgressBar')
        self.progBar.metricsMode = ogre.GMM_PIXELS
        self.progBar.setPosition(self.progLeftBound, self.engine.gfxMgr.viewPort.actualHeight-self.uiHeight)
        self.progBar.setDimensions(312, self.uiHeight)
        self.progBar.materialName="Angst/ProgressBar"
        # Progress Arrow
        self.progArrow = self.overlayManager.createOverlayElement('Panel', 'ProgressArrow')
        self.progArrow.metricsMode = ogre.GMM_PIXELS
        self.progArrow.setPosition(self.progLeftBound, self.engine.gfxMgr.viewPort.actualHeight-self.uiHeight)
        self.progArrow.setDimensions(30, (self.uiHeight*0.8))
        self.progArrow.materialName="Angst/ProgressArrow"


        # Add Panels to Overlay
        self.overlay = self.overlayManager.create('UIOverlay')
        self.overlay.add2D(self.uiPanel)
        self.overlay.add2D(self.targetPanel)
        self.overlay.add2D(self.scorePanel)
        self.overlay.add2D(self.angstBar)
        self.overlay.add2D(self.angstMeter)
        self.overlay.add2D(self.angstMeter2)
        self.overlay.add2D(self.progBar)
        self.overlay.add2D(self.progArrow)
        self.overlay.add2D(self.splashScreen) # this has to be last to render over everything else
        self.overlay.show()

    def showSplash(self):
        self.splashScreen.materialName = "Angst/SplashScreen"
        self.splashScreen.show()
        self.showingSplash = True

    def showVictorySplash(self):
        self.splashScreen.materialName = "Angst/Victory"
        self.splashScreen.show()
        self.showingSplash = True

    def showDefeatSplash(self):
        self.splashScreen.materialName = "Angst/Defeat"
        self.splashScreen.show()
        self.showingSplash = True
    
    def hideSplash(self):
        self.splashScreen.hide()
        self.showingSplash = False

    def destroy(self, name):
        self.overlayManager.destroyOverlayElement( name )

    def tick(self, dt):
        if not self.showingSplash:
            # update angstmeter
            angstRatio = 1.0 - (float(self.engine.entityMgr.player.health) / float(self.engine.entityMgr.player.maxHealth))
            self.angstMeter.setDimensions(angstRatio * self.maxAngst, (self.uiHeight/2))

            # update overheat meter
            heatValue = (float(self.engine.gameMgr.weaponHeat) / float(self.engine.gameMgr.weaponMaxHeat)) * self.maxAngst
            if heatValue > self.maxAngst:
                heatValue = self.maxAngst
            self.angstMeter2.setDimensions( heatValue, (self.uiHeight/2))

            # update score
            self.score = str(self.engine.gameMgr.score)
            self.scoreText.setCaption("Score: " + self.score)
            self.scorePanel.setDimensions((self.uiHeight*3.4) + (len(self.score)*(self.uiHeight/2)-2), self.uiHeight)

            # update progress bar
            self.progArrow.setPosition( self.progLeftBound + ((self.engine.gameMgr.levelDuration-self.engine.gameMgr.levelTimer)/self.engine.gameMgr.levelDuration * 384), self.engine.gfxMgr.viewPort.actualHeight-self.uiHeight )
        
    def stop(self):
        self.overlayManager.destroyAll()

