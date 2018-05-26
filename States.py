import Components as comp
import Constans as c
import pygame as pg
import random
import json


#-------------CLASE PADRE PARA CADA ESTADO DEL JUEGO---------------------------
class State():
    def __init__(self, caption, estado_siguiente):
        self.caption = caption
        self.fin = False
        self.estado_siguiente = estado_siguiente
        self.ventana = pg.display.get_surface()
    def update(self):
        pass
    def setup(self):
        pg.display.set_caption(self.caption)
    def __str__(self):
        return "Caption: %s, Estado Siguiente: %s" % (self.caption,self.estado_siguiente)
    def quit(self):
        self.fin = True
#-------------ESTADO: PANTALLA DE INICIO--------------------------------------
class PantallaInicio(State):
    def __init__(self,caption,estado_siguiente):
        State.__init__(self,caption,estado_siguiente)
        self.x = -1000
        self.y = 32
        self.pow = 100
        self.ntran = 3
        self.tran = 1
        self.fuente = pg.font.Font(None,22)
        self.text = self.fuente.render("Presione A para ir al menu principal", True, c.NEGRO)

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.quit()
        self.ventana.fill(c.BLANCO)
        if self.tran == 1:
            self.ventana.blit(c.GraficosPantallaPrincipal["LogoUTP"],(self.x,self.y))
        elif self.tran == 2:
            self.ventana.blit(c.GraficosPantallaPrincipal["LogoISC"],(self.x,self.y))
        else:
            self.ventana.blit(c.GraficosPantallaPrincipal["Presentacion"],(self.x,self.y))

        self.ventana.blit(self.text,(c.TAMANO_VENTANA[0]-268,c.TAMANO_VENTANA[1]-32))

        self.x += self.pow
        if self.x < 99:
            self.pow = self.pow/1.1
        else:
            self.pow = self.pow*1.1

        if self.x > c.TAMANO_VENTANA[0]:
            if self.tran < self.ntran:
                self.tran += 1
            else:
                self.quit()
            self.x = -1000
            self.pow = 100

#------------ESTADO: MENU PRINCIPAL--------------------------------------------
class MenuPrincipal(State):
    def __init__(self,caption,estado_siguiente):
        State.__init__(self,caption,estado_siguiente)
        self.surfacetran = pg.Surface(c.TAMANO_VENTANA)
        self.alpha = 255
        self.alpha2 = 0
        self.title1_x = -1024
        self.title1_y = 16
        self.aumento = 100
        self.title2_x = -1024
        self.title2_y = 16
        self.aumento2 = 35
        self.bg_x = 0
        self.bg_y = 0
        self.dir = 0
        self.n = 0
        self.fbtn = False

    def update(self):

        self.ventana.fill((0,0,255))
        self.ventana.blit(c.GraficosMenuPrincipal["MenuBackground"],(self.bg_x,self.bg_y))
        self.ventana.blit(c.GraficosMenuPrincipal["TitleDBZ"],(self.title1_x,self.title1_y))
        self.ventana.blit(c.GraficosMenuPrincipal["TitleBMAll"],(self.title2_x,self.title2_y))
        self.ventana.blit(c.GraficosMenuPrincipal["BotonPlay"],(448,300))
        self.ventana.blit(c.GraficosMenuPrincipal["BotonQuit"],(448,364))
        self.ventana.blit(c.GraficosMenuPrincipal["BotonCredits"],(416,428))

        if self.n == 0:
            self.ventana.blit(c.GraficosMenuPrincipal["Puntero"],(400,296))
        elif self.n == 1:
            self.ventana.blit(c.GraficosMenuPrincipal["Puntero"],(400,360))
        else:
            self.ventana.blit(c.GraficosMenuPrincipal["Puntero"],(368,424))


        if self.title1_x < 187:
            self.title1_x += self.aumento
            self.aumento = self.aumento/1.09

        if self.title2_x < 177:
            self.title2_x += self.aumento2
            self.aumento2 = self.aumento2/1.03

        if self.alpha > 0:
            self.ventana.blit(self.surfacetran,(0,0))
            self.surfacetran.set_alpha(self.alpha)
            self.alpha -= 2

        key = pg.key.get_pressed()
        if (key[pg.K_DOWN] or key[pg.K_RIGHT]) and not self.fbtn:
            self.fbtn = True
            if self.n < 2:
                self.n+=1
            else:
                self.n = 0
        if (key[pg.K_UP] or key[pg.K_LEFT]) and not self.fbtn:
            self.fbtn = True
            if self.n > 0:
                self.n-=1
            else:
                self.n = 2
        if (not key[pg.K_UP]) and (not key[pg.K_RIGHT]) and (not key[pg.K_DOWN]) and (not key[pg.K_LEFT]):
            self.fbtn = False

        if key[pg.K_SPACE] or key[pg.K_RETURN] or key[pg.K_KP_ENTER]:
            if self.n == 0:
                self.estado_siguiente = "Level1"
                self.quit()
            elif self.n == 1:
                self.estado_siguiente = "QUIT"
                self.quit()
            else:
                self.estado_siguiente = "Creditos"
                self.quit()

#------------ESTADO: Prologo--------------------------------------------
class Prologo(State):
    def __init__(self,caption,estado_siguiente):
        State.__init__(self,caption,estado_siguiente)
        self.fuente = pg.font.Font(None,32)
        self.texto = self.fuente.render("Prologo",True, c.BLANCO)

    def update(self):
        key = pg.key.get_pressed()

        if key[pg.K_SPACE]:
            self.fin = True

        self.ventana.fill(c.NEGRO)
        self.ventana.blit(self.texto,(100,100))

#------------ESTADO: Level 1--------------------------------------------
class Level1(State):
    def __init__(self,caption,estado_siguiente):
        State.__init__(self,caption,estado_siguiente)
        self.tamano_mundo = (3904,4720)
        with open("Recursos/Datos/mapeado.json") as archivo:
            self.datos = json.load(archivo)
        self.fuente = pg.font.Font(None, 18)
        self.objetivo = self.fuente.render("Objetivo: Encuentra el Orbe ROJO, SPACE: Velociad, A: Golpe, S: Golpe Mejorado, D: Bola de energia", 0, (0, 0, 0))
        self.timewait = 50
        #Grupos
        '''
        self.todos = pg.sprite.LayeredUpdates()
        self.usuarios = pg.sprite.Group()
        self.muros = pg.sprite.Group()
        self.shoots = pg.sprite.Group()
        self.shootsenemigos = pg.sprite.Group()
        self.orbes = pg.sprite.Group()
        self.enemigos = pg.sprite.Group()
        '''
        comp.Global_posicion_x = -512
        comp.Global_posicion_y = -512

        #Objetos
        self.target = [None]
        self.bg = comp.Background(self.tamano_mundo)
        self.goku = comp.Goku(self.tamano_mundo,self.muros,self.shoots,self.shootsenemigos,self.orbes,self.enemigos,self.todos,self.target)
        self.goku.rect.x = 512
        self.goku.rect.y = 512

        #Anadir objetos GRUPO USUARIOS
        self.usuarios.add(self.goku)

        #Anadir objetos GRUPO TODOS
        self.generarjsonmuros()
        self.todos.add(self.bg)
        #self.generarjsonorbes()
        self.generarjsonenemigos()
        self.todos.add(self.goku)
        self.generarjsonforeground()

    def generarjsonmuros(self):
        for i in self.datos["layers"][1]["objects"]:
            possize = (i["x"],i["y"],i["width"],i["height"])
            m = comp.Muro(possize)
            self.muros.add(m)
            self.todos.add(m)

    def generarjsonforeground(self):
        for i in self.datos["layers"][3]["objects"]:
            pos = (i["x"],i["y"]-i["height"])
            m = comp.Edificio(pos)
            self.todos.add(m)
        for i in self.datos["layers"][2]["objects"]:
            pos = (i["x"],i["y"]-i["height"])
            m = comp.Palmera(pos)
            self.todos.add(m)

    def generarjsonorbes(self):
        for i in self.datos["layers"][2]["objects"]:
            pos = (i["x"],i["y"])
            orb = comp.Orbes(self.aniorbes["OrbKi"],pos)
            orb.tipo = "Ki"
            self.orbes.add(orb)
            self.todos.add(orb)
        for i in self.datos["layers"][3]["objects"]:
            pos = (i["x"],i["y"])
            orb = comp.Orbes(self.aniorbes["OrbVida"],pos)
            orb.tipo = "Vida"
            self.orbes.add(orb)
            self.todos.add(orb)
        for i in self.datos["layers"][4]["objects"]:
            pos = (i["x"],i["y"])
            orb = comp.Orbes(self.aniorbes["OrbFuerza"],pos)
            orb.tipo = "Fuerza"
            self.orbes.add(orb)
            self.todos.add(orb)
        for i in self.datos["layers"][5]["objects"]:
            pos = (i["x"],i["y"])
            orb = comp.Orbes(self.aniorbes["OrbTrampa"],pos)
            orb.tipo = "Trampa"
            self.orbes.add(orb)
            self.todos.add(orb)

    def generarjsonenemigos(self):
        '''
        for i in self.datos["layers"][6]["objects"]:
            pos = (i["x"],i["y"])
            en = comp.EnemigoDinamico(self.aniCell,pos,self.muros,self.shoots,self.shootsenemigos,self.todos,self.target)
            self.enemigosdinamicos.add(en)
            self.todos.add(en)
        '''
        for i in self.datos["layers"][4]["objects"]:
            pos = (i["x"],i["y"])
            en = comp.Triceratops(pos,self.shoots,self.shootsenemigos,self.todos,self.target)
            self.enemigos.add(en)
            self.todos.add(en)


    def update(self):
        if not self.goku.live:
            self.timewait -= 1

        if self.timewait <= 0:
            self.siguiente_estado = "GameOver"
            self.quit()

        self.ventana.fill(c.NEGRO)
        self.todos.update()
        self.todos.draw(self.ventana)
        pg.draw.rect(self.ventana,(100,100,100),(80,46,self.goku.vidamax, 18))
        pg.draw.rect(self.ventana,(0,255,0),(80,46,self.goku.vida, 18))
        pg.draw.rect(self.ventana,(100,100,100),(80,64,self.goku.kimax, 12))
        pg.draw.rect(self.ventana,(0,0,255),(80,64,self.goku.ki, 12))
        self.ventana.blit(c.ItemSheets["BarLife"],(16,16))

        if self.target[0] != None:
            pg.draw.rect(self.ventana,(100,100,100),(80,126,self.target[0].vidamax, 18))
            pg.draw.rect(self.ventana,(255,0,0),(80,126,self.target[0].vida, 18))
            if self.target[0].name == "Cell":
                self.ventana.blit(c.ItemSheets["CellBarLife"],(16,96))
            else:
                self.ventana.blit(c.ItemSheets["RinoBarLife"],(16,96))

        self.ventana.blit(self.objetivo,(230,16))
