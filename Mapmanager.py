from direct.showbase.ShowBase import ShowBase
import json

class Mapmanager():
    def __init__(self):
        self.model = 'mymodel/untitled.gltf'  # модель куба у файлі block.egg
        self.texture = 'block.png'  # текстура куба
        self.color = (150/255, 32/255, 10/255, 1)  # rgba
        self.startNew()


    def addBlock(self,position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)
    def addPanda(self, position, size):
        self.panda = loader.loadModel('mymodel/untitled.gltf')
        self.panda.setPos(position)
        self.panda.setScale(size)
        self.panda.reparentTo(self.land)

    def startNew(self):
        self.land = render.attachNewNode("Land")


    def loadLand(self):
        with open("map1.json", "r") as file:
            data = json.load(file)
            for elem in data:
                if elem["name"] == "block":
                    self.addBlock(tuple(elem["pos"]))
