from datetime import datetime

from ui.widgets.background import LcarsBackgroundImage, LcarsImage
from ui.widgets.gifimage import LcarsGifImage
from ui.widgets.lcars_widgets import *
from ui.widgets.screen import LcarsScreen
from pygame_widgets.slider import Slider

from datasources.network import get_ip_address_string


class ScreenHome(LcarsScreen):
    def setup(self, all_sprites, unscaled_sprites):
        all_sprites.add(LcarsBackgroundImage("assets/lcars_screen_1b.png"), layer=0)

        # panel text
        all_sprites.add(LcarsText(colours.BLACK, (15, 44), "LCARS 105"),
                        layer=1)
        #all_sprites.add(LcarsText(colours.ORANGE, (0, 135), "HOME AUTOMATION", 2),
        #                layer=1)
        #all_sprites.add(LcarsBlockMedium(colours.RED_BROWN, (145, 16), "LIGHTS"),
        #                layer=1)
        #all_sprites.add(LcarsBlockSmall(colours.ORANGE, (211, 16), "CAMERAS"),
        #                layer=1)
        #all_sprites.add(LcarsBlockLarge(colours.BEIGE, (400, 24), "ENERGY"),
        #                layer=1)

        self.ip_address = LcarsText(colours.BLACK, (444, 520),
                                    get_ip_address_string())
        unscaled_sprites.add(self.ip_address, layer=1)

        self.info_text = all_sprites.get_sprites_from_layer(3)

        # date display
        self.stardate = LcarsText(colours.BLUE, (12, 380), "STAR DATE 2311.05 17:54:32", 1.5)
        self.lastClockUpdate = 0
        all_sprites.add(self.stardate, layer=1)

        # gadgets
        # 494 424

        self.dashboard = LcarsImage("assets/gadgets/dashboard.png", (300, 232))
        self.dashboard.visible = False
        unscaled_sprites.add(self.dashboard, layer=2)

        self.unscaled_sprites = unscaled_sprites
        self.all_sprites = all_sprites
        #unscaled_sprites.add(LcarsMoveToMouse(colours.WHITE), layer=1)
        self.beep1 = Sound("assets/audio/panel/201.wav")
        Sound("assets/audio/panel/220.wav").play()

    def update(self, screenSurface, fpsClock):
        if pygame.time.get_ticks() - self.lastClockUpdate > 1000:
            self.stardate.setText("STAR DATE {}".format(datetime.now().strftime("20%y.%m/%d %I:%M:%S %p")))
            self.lastClockUpdate = pygame.time.get_ticks()
        LcarsScreen.update(self, screenSurface, fpsClock)


