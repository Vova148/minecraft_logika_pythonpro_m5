from direct.showbase.ShowBase import ShowBase
import Mapmanager
import simplepbr
class Game(ShowBase):
  def __init__(self):
      super().__init__(self)

      simplepbr.init()
      land = Mapmanager.Mapmanager()
      land.loadLand()



game = Game()
game.run()
