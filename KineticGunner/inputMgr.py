# Input Manager -------------------------------------------------------------- #
# Initialize and manage keyboard and mouse. Buffered and unbuffered input      #

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
from vector import Vector3
import os
import command
import time

class InputMgr(OIS.KeyListener, OIS.MouseListener, OIS.JoyStickListener):
    def __init__(self, engine):
        self.engine = engine
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.JoyStickListener.__init__(self)
        self.move = 1000
        self.rotate = 25
        self.selectionRadius = 100
        self.MB_Left_Down = False
        self.MB_Right_Down = False

    def init(self):
        windowHandle = 0
        renderWindow = self.engine.gfxMgr.root.getAutoCreatedWindow()
        windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        paramList = [("WINDOW", str(windowHandle))]

        if os.name == "nt":
            #t = [("w32_mouse","DISCL_FOREGROUND"), ("w32_mouse", "DISCL_NONEXCLUSIVE")]
            t = [("w32_mouse","DISCL_FOREGROUND"), ("w32_mouse", "DISCL_EXCLUSIVE")]
        else:
            t = [("x11_mouse_grab", "true"), ("x11_mouse_hide", "true")]
            #t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "true")]

        paramList.extend(t)

        self.inputManager = OIS.createPythonInputSystem(paramList)
 
        # Now InputManager is initialized for use. Keyboard and Mouse objects
        # must still be initialized separately
        self.keyboard = None
        self.mouse    = None
        try:
            self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
            self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)
            #Joystick
        except Exception, e:
            print "No Keyboard or mouse!!!!"
            raise e
        if self.keyboard:
            self.keyboard.setEventCallback(self)
        if self.mouse:
            self.mouse.setEventCallback(self)
            self.windowResized( renderWindow )
 
        # import random
        # self.randomizer = random
        # self.randomizer.seed(None)
        print "Initialized Input Manager"

    def crosslink(self):
        pass

    def stop(self):
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None
        
    def tick(self, dtime):
        self.keyboard.capture()
        self.mouse.capture()
        self.handleCamera(dtime)
        self.handleModifiers(dtime)
        # Quit
        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.engine.keepRunning = False
        pass
        
    # Keyboard Listener ----------------------------------------------------- #
    def keyPressed(self, evt):
        '''Handles Toggleable Key Presses'''
        # Swap Cameras (Between First-Person and Debug Views)
        if self.keyboard.isKeyDown(OIS.KC_G):
            self.engine.camMgr.swap()
        # Pause ------------------------DEBUG-----------------------------------
        if self.keyboard.isKeyDown(OIS.KC_SPACE):
            time.sleep(10)
        return True

    def keyReleased(self, evt):
        return True
    
    def handleModifiers(self, dtime):
        self.leftShiftDown = self.keyboard.isKeyDown(OIS.KC_LSHIFT)
        self.leftCtrlDown = self.keyboard.isKeyDown(OIS.KC_LCONTROL)
        pass
        
    def handleCamera(self, dtime):
        '''Move the camera using keyboard input.'''
        # Forward
        if self.keyboard.isKeyDown(OIS.KC_W):
            self.engine.camMgr.transVector.z -= self.move
        # Backward
        if self.keyboard.isKeyDown(OIS.KC_S):
            self.engine.camMgr.transVector.z += self.move
        # Left
        if self.keyboard.isKeyDown(OIS.KC_A):
            self.engine.camMgr.transVector.x -= self.move
        # Right
        if  self.keyboard.isKeyDown(OIS.KC_D):
            self.engine.camMgr.transVector.x += self.move
        # Up     
        if self.keyboard.isKeyDown(OIS.KC_3):
            self.engine.camMgr.transVector.y += self.move
        # Down
        if self.keyboard.isKeyDown(OIS.KC_4):
            self.engine.camMgr.transVector.y -= self.move          
        # Yaw
        if self.keyboard.isKeyDown(OIS.KC_Q):
            self.engine.camMgr.yawRot = -self.rotate
        # Yaw
        if self.keyboard.isKeyDown(OIS.KC_E):
            self.engine.camMgr.yawRot = self.rotate
        # Pitch
        if self.keyboard.isKeyDown(OIS.KC_Z):
            self.engine.camMgr.pitchRot = -self.rotate
        # Pitch
        if self.keyboard.isKeyDown(OIS.KC_X):
            self.engine.camMgr.pitchRot = self.rotate
        # Roll
        if self.keyboard.isKeyDown(OIS.KC_R):
            self.engine.camMgr.rollRot = self.rotate
        # Roll
        if self.keyboard.isKeyDown(OIS.KC_V):
            self.engine.camMgr.rollRot = -self.rotate
        pass
        
    # MouseListener --------------------------------------------------------- #
    def mouseMoved(self, evt):
        currMouse = self.mouse.getMouseState()
        self.engine.camMgr.yawRot += currMouse.X.rel
        self.engine.camMgr.pitchRot += currMouse.Y.rel
        return True

    def mousePressed(self, evt, id):
        #self.mouse.capture()
        #self.ms = self.mouse.getMouseState()

        #self.ms.width = self.engine.gfxMgr.viewPort.actualWidth 
        #self.ms.height = self.engine.gfxMgr.viewPort.actualHeight
        #self.mousePos = (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))
        
        if id == OIS.MB_Left:
            self.MB_Left_Down = True

        elif id == OIS.MB_Right:
            self.MB_Right_Down = True
        return True
                
    def mouseReleased(self, evt, id):
        if id == OIS.MB_Left:
            self.MB_Left_Down = False

        elif id == OIS.MB_Right:
            self.MB_Right_Down = False
        return True
    
    # JoystickListener ------------------------------------------------------ #
    def buttonPressed(self, evt, button):
        return True
    def buttonReleased(self, evt, button):
        return True
    def axisMoved(self, evt, axis):
        return True

    def windowResized (self, rw):
        temp = 0
        width, height, depth, left, top= rw.getMetrics(temp,temp,temp, temp, temp)  # Note the wrapped function as default needs unsigned int's
        ms = self.mouse.getMouseState()
        ms.width = width
        ms.height = height
         
# Input Manager -------------------------------------------------------------- #
