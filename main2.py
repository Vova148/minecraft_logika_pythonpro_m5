from math import sin, cos

from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import  ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionRay, CollisionNode, CollisionHandlerQueue, CollisionTraverser, DirectionalLight, \
    AmbientLight, TransparencyAttrib

from Map import Map

def degToRad(degrees):
    return degrees * (3.14 / 180.0)

class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)
        self.map = Map()
        self.setupLight()
        self.setupCamera()
        self.setupSkyBox()
        self.setupControls()
        self.map.load_map()
        self.setupCrosshairs()
        self.taskMgr.add(self.update, 'update')

    def setupCrosshairs(self):
        crosshairs = OnscreenImage(
            image='crosshairs.png',
            pos=(0,0,0),
            scale=0.05
        )
        crosshairs.setTransparency(TransparencyAttrib.MAlpha)

    def setupSkyBox(self):
        skybox = loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(render)
    def setupLight(self):
        main_light = DirectionalLight('main light')
        main_light_node = render.attachNewNode(main_light)
        main_light_node.setHpr(30, -60, 0)
        render.setLight(main_light_node)

        ambient_light = AmbientLight('ambient_light')
        ambient_light_node = render.attachNewNode(ambient_light)
        ambient_light.setColor((0.3, 0.3, 0.3, 1))
        render.setLight(ambient_light_node)
    def delete_block(self):
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            ray_hit = self.ray_queue.get_entry(0)

            hit_node = ray_hit.getIntoNodePath()
            hit_object = hit_node.getPythonTag('owner')

            hit_object.clearPythonTag('owner')
            hit_object.removeNode()
    def create_block(self):
        if self.ray_queue.getNumEntries() > 0:
            self.ray_queue.sortEntries()
            ray_hit = self.ray_queue.get_entry(0)

            hit_node = ray_hit.getIntoNodePath()
            hit_object = hit_node.getPythonTag('owner')

            pos = hit_object.getPos()
            normal = ray_hit.getSurfaceNormal(hit_node)

            new_pos = pos + normal*2
            self.map.create_block(new_pos)


    def update(self, task):
        dt = globalClock.getDt()

        speed = 10
        x = y = z = 0
        if self.key_map["forward"]:
            x -= dt * speed * sin(degToRad(self.camera.getH()))
            y += dt * speed * cos(degToRad(self.camera.getH()))
        if self.key_map['backward']:
            x += dt * speed * sin(degToRad(self.camera.getH()))
            y -= dt * speed * cos(degToRad(self.camera.getH()))
        # if self.key_map['left']:
        #     x -= dt * speed * cos(degToRad(self.camera.getH()))
        #     y -= dt * speed * sin(degToRad(self.camera.getH()))
        # if self.key_map['right']:
        #     x += dt * speed * cos(degToRad(self.camera.getH()))
        #     y += dt * speed * sin(degToRad(self.camera.getH()))
        # if self.key_map['up']:
        #     z += dt * speed
        # if self.key_map['down']:
        #     z -= dt * speed


        self.camera.setPos(
            self.camera.getX() + x,
            self.camera.getY() + y,
            self.camera.getZ() + z,
        )

        cursor = self.win.getPointer(0)
        cursor_x = cursor.getX()
        cursor_y = cursor.getY()

        cursor_dx = cursor_x - (self.win.getXSize() // 2)
        cursor_dy = cursor_y - (self.win.getYSize() // 2)
        self.camera.setHpr(
            self.camera.getH() - cursor_dx * dt *2,
            self.camera.getP() - cursor_dy * dt * 2,
            0
        )
        self.win.movePointer(0, self.win.getXSize() // 2, self.win.getYSize() // 2)
        return task.cont
    def update_move(self, key, value):
        self.key_map[key] = value

    def setupControls(self):
        self.key_map = {
            "forward": False,
            "backward": False,


        }

        self.accept('w', self.update_move, ['forward', True])
        self.accept('w-up', self.update_move, ['forward', False])
        self.accept('mouse3', self.create_block)
        self.accept('mouse1', self.delete_block)
        self.accept('v', self.map.save_map)

        self.accept('1', self.setGrassBlock)

    def setGrassBlock(self):
        self.map.model = "blocks/grass-block.glb"
    def setupCamera(self):
        self.disableMouse()
        self.camera.setPos(0, -10, 0)
        self.camLens.setFov(80)

        ray = CollisionRay()
        ray.setFromLens(self.cam.node(), 0, 0)

        rayNode = CollisionNode('ray')
        rayNode.addSolid(ray)

        rayNodePath = self.camera.attachNewNode(rayNode)

        self.ray_queue = CollisionHandlerQueue()
        self.cTrav = CollisionTraverser()
        self.cTrav.addCollider(rayNodePath, self.ray_queue)
game = Game()
game.run()