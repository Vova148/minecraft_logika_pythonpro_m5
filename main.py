from math import *

from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *

import Mapmanager


def degToRad(degrees):
    return degrees * (pi / 180.0)


class Game(ShowBase):
    def __init__(self):
        super().__init__(self)

        self.land = Mapmanager.Mapmanager()
        self.land.loadLand()
        self.setupLights()
        self.captureMouse()
        self.setupCamera()
        self.setupSkybox()
        self.setupControls()

        self.setup_crosshair()
        self.taskMgr.add(self.update, 'update')
    def setup_crosshair(self):
        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0, 0, 0),
            scale=0.05,
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)
    def setupLights(self):
        mainLight = DirectionalLight('main light')
        mainLightNodePath = render.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)
        render.setLight(mainLightNodePath)

        ambientLight = AmbientLight('ambient light')
        ambientLight.setColor((0.3, 0.3, 0.3, 1))
        ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNodePath)
    def setupControls(self):
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }
        self.accept('w', self.updateKeyMap, ['forward', True])
        self.accept('w-up', self.updateKeyMap, ['forward', False])
        self.accept('a', self.updateKeyMap, ['left', True])
        self.accept('a-up', self.updateKeyMap, ['left', False])
        self.accept('s', self.updateKeyMap, ['backward', True])
        self.accept('s-up', self.updateKeyMap, ['backward', False])
        self.accept('d', self.updateKeyMap, ['right', True])
        self.accept('d-up', self.updateKeyMap, ['right', False])
        self.accept('space', self.updateKeyMap, ['up', True])
        self.accept('space-up', self.updateKeyMap, ['up', False])
        self.accept('lshift', self.updateKeyMap, ['down', True])
        self.accept('lshift-up', self.updateKeyMap, ['down', False])
        self.accept('mouse1', self.deleteBlock)
        self.accept('mouse3', self.placeBlock)

        self.accept('h', self.land.saveMap)
        self.accept('1', self.setGrassBlock)
        self.accept('2', self.setLab)
        self.accept('3', self.rotate)
        self.accept('4', self.rotateStandart)

    def setGrassBlock(self):
        self.land.model = "blocks/grass-block.glb"

    def rotateStandart(self):
        self.land.block.setHpr(0,0,0)
    def rotate(self):
        self.land.block.setHpr(90, 50,10)
    def setLab(self):
        self.land.model = "лабораторія/scene.gltf"

    def deleteBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()

            rayHit = self.rayQueue.get_entry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')

            hitNodePath.clearPythonTag('owner')
            hitObject.removeNode()

    def placeBlock(self):
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.get_entry(0)

            hitNodePath = rayHit.getIntoNodePath()
            hitObject = hitNodePath.getPythonTag('owner')

            hitBoxPos = hitObject.getPos()
            normal = rayHit.getSurfaceNormal(hitNodePath)
            newBlockPos = hitBoxPos + normal*2
            self.land.addBlock(newBlockPos)

    def updateKeyMap(self, key, value):
        self.keyMap[key] = value

    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, -3, 3)
        self.camLens.setFov(80)

        ray = CollisionRay()
        ray.setFromLens(self.camNode, (0, 0))

        rayNode = CollisionNode('line-of-sight')
        rayNode.addSolid(ray)

        rayNodePath = self.camera.attachNewNode(rayNode)

        self.rayQueue = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(rayNodePath, self.rayQueue)

    def update(self, task):
        dt = globalClock.getDt()

        playerMoveSpeed = 10

        x_movement = 0
        y_movement = 0
        z_movement = 0
        if self.keyMap['forward']:
            x_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['backward']:
            x_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
        if self.keyMap['left']:
            x_movement -= dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement -= dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['right']:
            x_movement += dt * playerMoveSpeed * cos(degToRad(self.camera.getH()))
            y_movement += dt * playerMoveSpeed * sin(degToRad(self.camera.getH()))
        if self.keyMap['up']:
            z_movement += dt * playerMoveSpeed
        if self.keyMap['down']:
            z_movement -= dt * playerMoveSpeed


        self.camera.setPos(
            self.camera.getX() + x_movement,
            self.camera.getY() + y_movement,
            self.camera.getZ() + z_movement,
        )


        md = self.win.getPointer(0)
        mouseX = md.getX()
        mouseY = md.getY()

        mouseChangeX = mouseX - (self.win.getXSize() // 2)
        mouseChangeY = mouseY - self.win.getYSize() // 2

        self.cameraSwingFactor = 10  # чутливість

        currentH = self.camera.getH()
        currentP = self.camera.getP()

        self.camera.setHpr(
            currentH - mouseChangeX * dt * self.cameraSwingFactor,
            currentP - mouseChangeY * dt * self.cameraSwingFactor,
            0
        )

        self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)

        return task.cont
    def captureMouse(self):
        properties = WindowProperties()
        properties.setCursorHidden(True)
        self.win.requestProperties(properties)

    def setupSkybox(self):
        skybox = loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(render)


game = Game()
game.run()
