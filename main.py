from math import *

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import *

import Mapmanager
import simplepbr

def degToRad(degrees):
    return degrees * (pi / 180.0)


class Game(ShowBase):
    def __init__(self):
        super().__init__(self)

        self.land = Mapmanager.Mapmanager()
        self.land.loadLand()

        self.captureMouse()
        self.setupCamera()
        self.setupControls()

        self.taskMgr.add(self.update, 'update')
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


game = Game()
game.run()
