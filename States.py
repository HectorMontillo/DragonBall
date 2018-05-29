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
    def reboot(self):
        pass
    def boot(self):
        pass
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

    def boot(self):
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
                self.estado_siguiente = "Tutorial"
                self.quit()
            elif self.n == 1:
                self.estado_siguiente = "QUIT"
                self.quit()
            else:
                self.estado_siguiente = "Creditos"
                self.quit()

#------------ESTADO: Prologo--------------------------------------------------
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

#------------ESTADO: CLASE PADRE PARA CADA NIVEL--------------------------------
class Level(State):
    def __init__(self,caption,estado_siguiente,tamano_mundo,mapeado,titulo):
        State.__init__(self,caption,estado_siguiente)
        self.tamano_mundo = tamano_mundo
        self.fuente = pg.font.Font(None, 16)
        self.fuente2 = pg.font.Font(None, 14)
        self.fuenteTitulo = pg.font.Font(None,72)
        self.timewait = 150
        self.target = [None]
        with open(mapeado) as archivo:
            self.datos = json.load(archivo)

        self.x = -1000
        self.y = 512
        self.pow = 100

        self.xm = -1000
        self.ym = 512
        self.powm = 100

        self.ftitle = True
        self.titulo = titulo
        self.texttitle = self.fuenteTitulo.render("{}...".format(self.titulo),True,c.BLANCO)
        self.texttitlesombra = self.fuenteTitulo.render("{}...".format(self.titulo),True,c.NEGRO)
        self.completado = False

        #self.boot()

    def reboot(self):
        c.limpiargrupos()

    def boot(self):
        self.timewait = 150
        self.completado = False

        comp.Global_posicion_x = 0
        comp.Global_posicion_y = -335
        self.x = -1000
        self.y = 512
        self.pow = 100
        self.ftitle = True
        self.xm = -1000
        self.ym = 512
        self.powm = 100
        self.makeboot()

    def makeboot(self):
        pass


    def buscarcapa(self,capa):
        index = -1
        f = False
        for i in self.datos["layers"]:
            index += 1
            if i["name"]== capa:
                f = True
                break
        if f:
            return index
        else:
            return -1

    def generarmuros(self,listname = None):
        index = self.buscarcapa("Muros")
        print index
        if index > -1:
            for i in self.datos["layers"][index]["objects"]:
                possize = (i["x"],i["y"],i["width"],i["height"])
                m = comp.Muro(possize)
                c.Grupos["muros"].add(m)
                c.Grupos["todos"].add(m)
            if listname != None:
                j = 0
                for i in self.datos["layers"][index+1]["objects"]:
                    possize = (i["x"],i["y"],i["width"],i["height"])
                    m = comp.CollisionChecker(possize)
                    m.name = listname[j]
                    j+=1
                    c.Grupos["collisions"].add(m)
                    c.Grupos["todos"].add(m)

        else:
            print "No se generaron muros"

    def generarorbes(self):
        index = self.buscarcapa("Orbeski")
        if index > -1:
            for i in self.datos["layers"][index]["objects"]:
                pos = (i["x"],i["y"])
                orb = comp.Orbes("Ki",pos)
                c.Grupos["orbes"].add(orb)
                c.Grupos["todos"].add(orb)
            for i in self.datos["layers"][index+1]["objects"]:
                pos = (i["x"],i["y"])
                orb = comp.Orbes("Vida",pos)
                c.Grupos["orbes"].add(orb)
                c.Grupos["todos"].add(orb)
            for i in self.datos["layers"][index+2]["objects"]:
                pos = (i["x"],i["y"])
                orb = comp.Orbes("Trampa",pos)
                c.Grupos["orbes"].add(orb)
                c.Grupos["todos"].add(orb)
            for i in self.datos["layers"][index+3]["objects"]:
                pos = (i["x"],i["y"])
                orb = comp.Orbes("Exp",pos)
                c.Grupos["orbes"].add(orb)
                c.Grupos["todos"].add(orb)
        else:
            print "No se generaron orbes"

    def generarenemigos(self, listaenemigos):
        index = self.buscarcapa("Triceratops")
        if index > -1:
            if listaenemigos["Triceratops"]:
                for i in self.datos["layers"][index]["objects"]:
                    pos = (i["x"],i["y"])
                    en = comp.Triceratops(pos,self.target)
                    c.Grupos["enemigos"].add(en)
                    c.Grupos["todos"].add(en)
            if listaenemigos["Generador"]:
                for i in self.datos["layers"][index+1]["objects"]:
                    pos = (i["x"],i["y"])
                    en = comp.GeneradorMinions(pos,self.target)
                    #c.Grupos["enemigos"].add(en)
                    c.Grupos["todos"].add(en)
        else:
            print "No se generaron enemigos"

    def generarforeground(self):
        index = self.buscarcapa("Palmeras")
        if index > -1:
            for i in self.datos["layers"][index]["objects"]:
                pos = (i["x"],i["y"]-i["height"])
                m = comp.Palmera(pos)
                c.Grupos["todos"].add(m)

            for i in self.datos["layers"][index+1]["objects"]:
                pos = (i["x"],i["y"]-i["height"])
                m = comp.Edificio(pos)
                c.Grupos["todos"].add(m)
        else:
            print "No se genero foreground"

    def update2(self):
        pass

    def update(self):

        self.ventana.fill(c.NEGRO)
        c.Grupos["todos"].update()
        c.Grupos["todos"].draw(self.ventana)
        pg.draw.rect(self.ventana,(100,100,100),(80,46,self.goku.vidamax, 18))
        pg.draw.rect(self.ventana,(0,255,0),(80,46,self.goku.vida, 18))
        pg.draw.rect(self.ventana,(100,100,100),(80,64,self.goku.kimax, 12))
        pg.draw.rect(self.ventana,(0,0,255),(80,64,self.goku.ki, 12))
        self.ventana.blit(c.ItemSheets["BarLifePro"],(16,16))
        nivelexp = self.fuente.render("Exp {}/{}, Nivel {}".format(self.goku.exp,self.goku.expsiguientenivel,self.goku.nivel),True,c.NEGRO)
        fuerza =  self.fuente2.render("{}".format(self.goku.dano),True,c.BLANCO)
        poder =  self.fuente2.render("{}".format(self.goku.poder),True,c.BLANCO)
        resistencia =  self.fuente2.render("{}%".format(self.goku.resistencia),True,c.BLANCO)
        self.ventana.blit(nivelexp,(150,48))
        self.ventana.blit(fuerza,(116,86))
        self.ventana.blit(poder,(116,96))
        self.ventana.blit(resistencia,(116,106))


        if self.target[0] != None:
            if self.target[0].name == "Cell":
                pg.draw.rect(self.ventana,(100,100,100),(80,190,self.target[0].vidamax, 18))
                pg.draw.rect(self.ventana,(255,0,0),(80,190,self.target[0].vida, 18))
                self.ventana.blit(c.ItemSheets["CellBarLife"],(16,160))
            elif self.target[0].name == "Rino":
                pg.draw.rect(self.ventana,(100,100,100),(58,178,self.target[0].vidamax, 15))
                pg.draw.rect(self.ventana,(255,0,0),(58,178,self.target[0].vida, 15))
                self.ventana.blit(c.ItemSheets["RinoBarLife"],(16,160))
            else:
                pg.draw.rect(self.ventana,(100,100,100),(58,178,self.target[0].vidamax, 15))
                pg.draw.rect(self.ventana,(255,0,0),(58,178,self.target[0].vida, 15))
                self.ventana.blit(c.ItemSheets["MinionBarLife"],(16,160))


        if self.ftitle:
            self.ventana.blit(self.texttitlesombra,(self.x-3,self.y-3))
            self.ventana.blit(self.texttitle,(self.x,self.y))

            self.x += self.pow
            if self.x < 99:
                self.pow = self.pow/1.1
            else:
                self.pow = self.pow*1.1

            if self.x > c.TAMANO_VENTANA[0]:
                self.ftitle = False

        if self.completado:
            text = self.fuenteTitulo.render("Nivel Completado...",True,c.BLANCO)
            textsombra = self.fuenteTitulo.render("Nivel Completado...",True,c.NEGRO)
            self.ventana.blit(textsombra,(self.xm-3,self.ym-3))
            self.ventana.blit(text,(self.xm,self.ym))

            self.xm += self.powm
            if self.xm < 99:
                self.powm = self.powm/1.1
            else:
                self.powm = self.powm*1.1

            self.timewait -= 1

        if not self.goku.live:
            text = self.fuenteTitulo.render("Juego Terminado",True,c.BLANCO)
            textsombra = self.fuenteTitulo.render("Juego Terminado",True,c.NEGRO)
            self.ventana.blit(textsombra,(self.xm-3,self.ym-3))
            self.ventana.blit(text,(self.xm,self.ym))

            self.xm += self.powm
            if self.xm < 99:
                self.powm = self.powm/1.1
            else:
                self.powm = self.powm*1.1
            self.timewait -= 1

        if self.timewait <= 0:
            if not self.goku.live:
                self.estado_siguiente = "Menu"
            self.quit()


        self.update2()
#------------ESTADO: Level tutorial-------------------------------------------------

class LevelTutorial(Level):
    def __init__(self,caption,estado_siguiente):
        Level.__init__(self,caption,estado_siguiente,(2692,1790),"Recursos/Datos/mapeado_tutorial.json","Casa de Goku")

    def makeboot(self):

        c.LevelTutorial["TeclasMovimiento"].convert_alpha()

        self.tuto = {
        "Teclas":True,
        "Espacio":False,
        "Orbes":False,
        "Busca":False,
        "Pelea":False
        }

        self.listaenemigos = {
        "Triceratops":False,
        "Generador":True

        }

        self.listname = ["Espacio","Orbes","Busca","Pelea"]

        self.bg = comp.Background(self.tamano_mundo,c.LevelTutorial["Background"])
        self.goku = comp.Goku(self.tamano_mundo,self.target)
        self.goku.rect.x = 320
        self.goku.rect.y = 512
        c.Grupos["usuarios"].add(self.goku)
        #Anadir objetos GRUPO TODOS
        self.generarmuros(self.listname)
        c.Grupos["todos"].add(self.bg)
        self.generarorbes()
        self.generarenemigos(self.listaenemigos)
        c.Grupos["todos"].add(self.goku)
        self.generarforeground()

    def update2(self):
        if self.goku.nivel >= 5:
            self.completado = True
        collisions = pg.sprite.spritecollide(self.goku,c.Grupos["collisions"],False)
        for col in collisions:

            for i in self.listname:
                if (col.name == i):
                    for j in self.tuto:
                        self.tuto[j] = False
                    #print self.tuto
                    self.tuto[i] = True
                    break
            #print self.tuto

        if self.tuto["Teclas"]:
            self.ventana.blit(c.LevelTutorial["TeclasMovimiento"],(720,32))
        elif self.tuto["Espacio"]:
            self.ventana.blit(c.LevelTutorial["Espacio"],(720,32))
        elif self.tuto["Orbes"]:
            self.ventana.blit(c.LevelTutorial["Orbes"],(720,32))
        elif self.tuto["Busca"]:
            self.ventana.blit(c.LevelTutorial["Generador"],(720,32))
        elif self.tuto["Pelea"]:
            self.ventana.blit(c.LevelTutorial["Pelea"],(720,32))
            self.ventana.blit(c.LevelTutorial["Mision"],(720,300))



#------------ESTADO: Level 1-------------------------------------------------
class Level1(Level):
    def __init__(self,caption,estado_siguiente):
        Level.__init__(self,caption,estado_siguiente,(3904,4720),"Recursos/Datos/mapeado.json","Nivel 1")

    def makeboot(self):

        self.listaenemigos = {
        "Triceratops":True,
        "Generador":True
        }

        self.bg = comp.Background(self.tamano_mundo,c.Level1Graficos["Background"])
        self.goku = comp.Goku(self.tamano_mundo,self.target)
        self.goku.rect.x = 100
        self.goku.rect.y = 512
        c.Grupos["usuarios"].add(self.goku)
        #Anadir objetos GRUPO TODOS
        self.generarmuros()
        c.Grupos["todos"].add(self.bg)
        self.generarorbes()
        self.generarenemigos(self.listaenemigos)
        c.Grupos["todos"].add(self.goku)
        self.generarforeground()
