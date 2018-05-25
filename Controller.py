import pygame as pg

#Control central del JUEGO
class Control():
    def __init__(self):
        self.ventana = pg.display.get_surface()
        self.fin = False
        self.reloj = pg.time.Clock()
        self.fps = 60
        self.keys = pg.key.get_pressed()
        self.estados = None
        self.estado = None

    def update(self):
        if not self.estado.fin:
            self.estado.update()
        else:
            if self.estado.estado_siguiente == "QUIT":
                self.fin = True
            else:
                self.estado.fin = False
                self.estado = self.estados[self.estado.estado_siguiente]

    def preparar_estados(self, estados, estadoinicial):
        if estadoinicial != None:
            self.estado = estadoinicial
        else:
            print "Estado inicial debe ser diferente de NONE"
            self.fin = True
        self.estados = estados

    def eventos(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.fin = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()

    def main(self):
        while not self.fin:
            self.eventos()
            self.update()
            pg.display.update()
            self.reloj.tick(self.fps)
