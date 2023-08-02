from screens.home import ScreenHome
from ui.ui import UserInterface
import config

if __name__ == "__main__":
    firstScreen = ScreenHome()
    ui = UserInterface(firstScreen, config.RESOLUTION, config.UI_PLACEMENT_MODE, config.FPS, config.DEV_MODE,
                       config.SOUND, config.FULLSCREEN)

    while (True):
        ui.tick()
