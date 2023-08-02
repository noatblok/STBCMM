import pygame
from pygame.locals import *

from ui.utils import sound


class UserInterface:
    def __init__(self, screen, resolution=(800,480),
                 ui_placement_mode=False, fps=60, dev_mode=False, audio=True, fullscreen=False,
                 audio_params=(22050, -8, 1, 1024)):
        # init system
        pygame.display.init()
        pygame.font.init()
        sound.init(audio_params)
        self.resolution = resolution
        
        if fullscreen == True:
            self.buttonSurface = pygame.Surface(resolution, RESIZABLE)
            self.screenSurface = pygame.Surface((800, 480), RESIZABLE)#pygame.display.set_mode((800, 480))
            self.surface = pygame.display.set_mode(resolution, FULLSCREEN)
        else:
            self.buttonSurface = pygame.Surface(resolution, RESIZABLE)
            self.screenSurface = pygame.Surface((800, 480), RESIZABLE)#pygame.display.set_mode((800, 480))
            self.surface = pygame.display.set_mode(resolution)#, FULLSCREEN)
        self.fpsClock = pygame.time.Clock()
        self.fps = fps
        pygame.display.set_caption("LCARS")
        if not dev_mode: 
            # see https://github.com/tobykurien/rpi_lcars/issues/9
            #pygame.mouse.set_visible(False)
            pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        pygame.mouse.set_visible(True)
        # set up screen elements
        self.all_sprites = pygame.sprite.LayeredDirty()
        self.all_sprites.UI_PLACEMENT_MODE = ui_placement_mode
        self.unscaled_sprites = pygame.sprite.LayeredDirty()
        self.unscaled_sprites.UI_PLACEMENT_MODE = ui_placement_mode
        self.screen = screen
        self.screen.setup(self.all_sprites, self.unscaled_sprites)
        self.running = True

    def update(self):
        pygame.mouse.set_visible(True)
        self.buttonSurface = pygame.Surface((1366, 768), pygame.SRCALPHA, 32)
        self.screenSurface = pygame.Surface((800, 480), pygame.SRCALPHA, 32)
        self.screen.pre_update(self.screenSurface, self.fpsClock)
        self.all_sprites.update(self.screenSurface)
        self.screen.update(self.screenSurface, self.fpsClock)
        self.surface.blit(pygame.transform.smoothscale(self.screenSurface, (1366, 768)), (0,0))
        self.unscaled_sprites.update(self.buttonSurface)
        self.surface.blit(self.buttonSurface, (0,0))
        pygame.display.flip()
        pygame.display.update()
    
    def handleEvents(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or \
                (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                self.running = False
                return
    
            for sprite in self.all_sprites.sprites():
                if hasattr(event, "pos"):
                    focussed = sprite.rect.collidepoint(event.pos)
                    if (focussed or sprite.focussed) and sprite.handleEvent(event, self.fpsClock):
                        break
            for sprite in self.unscaled_sprites.sprites():
                if hasattr(event, "pos"):
                    focussed = sprite.rect.collidepoint(event.pos)
                    if (focussed or sprite.focussed) and sprite.handleEvent(event, self.fpsClock):
                        break
                
            self.screen.handleEvents(event, self.fpsClock)
    
            newScreen = self.screen.getNextScreen()
            if (newScreen):
                self.all_sprites.empty()
                self.unscaled_sprites.empty()
                pygame.display.flip()
                newScreen.setup(self.all_sprites, self.unscaled_sprites)
                self.screen = newScreen
                break
    
    def isRunning(self):
        pygame.display.get_init()
    
    def tick(self):
        self.update()
        self.handleEvents()
        self.fpsClock.tick(self.fps)
