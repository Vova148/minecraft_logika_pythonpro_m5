from direct.showbase.ShowBase import ShowBase

class Game(ShowBase):
  def __init__(self):
      super().__init__(self)

      self.model = self.loader.loadModel('models/environment')
      self.model.reparentTo(self.render)

      self.panda = self.loader.loadModel('models/panda')
      self.panda.reparentTo(self.render)
      self.panda.setPos(0, 15, 0)
      self.panda.setScale(5, 5, 5)




game = Game()
game.run()