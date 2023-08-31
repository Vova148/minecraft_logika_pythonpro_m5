from direct.showbase.ShowBase import ShowBase
import simplepbr

class Game(ShowBase):
  def __init__(self):
      super().__init__(self)
      simplepbr.init()
      self.model = self.loader.loadModel('ussrBuild/scene.gltf')
      self.model.reparentTo(self.render)


game = Game()

game.run()
