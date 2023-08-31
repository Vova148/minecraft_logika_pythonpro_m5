from direct.showbase.ShowBase import ShowBase
class Mapmanager():
    def __init__(self):
        self.model = 'block.egg'  # модель куба у файлі block.egg
        self.texture = 'block.png'  # текстура куба
        self.color = (150/255, 32/255, 10/255, 1)  # rgba
        self.startNew()
        self.addBlock((0, 10, 0))
        self.addBlock((0, 9, 0))
        self.addBlock((1, 10, 0))


    def addBlock(self,position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)

    def startNew(self):
        self.land = render.attachNewNode("Land")