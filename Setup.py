import pygame as pg
import os
import Constans as c


def Setup():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
    pg.display.set_caption(c.CAPTION)
    ventana = pg.display.set_mode(c.TAMANO_VENTANA)
    ventana_rect = ventana.get_rect()
