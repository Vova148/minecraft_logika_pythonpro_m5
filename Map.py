import json
from panda3d.core import CollisionBox, CollisionNode


class Map:
    def __init__(self):
        self.model = 'blocks/dirt-block.glb'
        self.land = render.attachNewNode("Land")


    def create_block(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setPos(position)
        self.block.setPythonTag('type', self.model)
        self.block.reparentTo(self.land)

        hitbox = CollisionBox((-1,-1,-1), (1, 1, 1))
        blockNode =CollisionNode("block-collision-node")
        blockNode.addSolid(hitbox)
        collider = self.block.attachNewNode(blockNode)
        collider.setPythonTag('owner', self.block)


    def save_map(self):
        blocks = self.land.getChildren()
        with open("map.json", "w", encoding="utf-8") as file:
            data = []
            for block in blocks:
                elem = {
                    "name": "block",
                    "pos": list(block.getPos()),
                    "type": block.getPythonTag("type")
                }
                data.append(elem)
            json.dump(data, file, indent=4)

    def load_map(self):
        with open("map.json", "r", encoding="utf-8") as file:
            blocks = json.load(file)
            for block in blocks:
                if block["name"] == "block":
                    self.model = block["type"]
                    self.create_block(tuple(block["pos"]))