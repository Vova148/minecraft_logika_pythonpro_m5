from direct.showbase.ShowBase import ShowBase
import json

from panda3d.core import CollisionBox, CollisionNode


class Mapmanager():
    def __init__(self):
        self.model = 'blocks/dirt-block.glb'  # модель куба у файлі block.egg
        self.color = (150/255, 32/255, 10/255, 1)  # rgba
        self.startNew()

    def addBlock(self,position):
        self.block = loader.loadModel(self.model)
        self.block.setPos(position)
        self.block.reparentTo(self.land)


        blockSolid = CollisionBox((-1,-1,-1), (1,1,1))

        blockNode = CollisionNode('block-collision-node')
        blockNode.addSolid(blockSolid)
        collider = self.block.attachNewNode(blockNode)

        collider.setPythonTag('owner', self.block)

    def startNew(self):
        self.land = render.attachNewNode("Land")


    def loadLand(self):
        with open("map1.json", "r") as file:
            data = json.load(file)
            for elem in data:
                if elem["name"] == "block":
                    self.addBlock(tuple(elem["pos"]))


