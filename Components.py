#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame as pg
import Constans as c
import random

Global_posicion_x = -512
Global_posicion_y = -512

Global_speed_x = 0
Global_speed_y = 0

def recortarAnimacion(img,size,scale):
    img_rect = img.get_rect()[2:]

    matriz = []

    filas = img_rect[1]/size[1]
    columnas = img_rect[0]/size[0]


    for i in range(filas):
        matriz.append([])
        for j in range(columnas):
            frame = img.subsurface((j*size[0],i*size[1],size[0],size[1]))
            if scale > 1:
                frame = pg.transform.scale(frame, (scale*size[0],scale*size[1]))
            matriz[i].append(frame)
    return matriz

class Goku(pg.sprite.Sprite):
    def __init__(self,tm,tar):
        pg.sprite.Sprite.__init__(self)
        self.dicAnimacion = c.GokuSheets;
        self.image = self.dicAnimacion["Idle"][0][0]
        self.rect = self.image.get_rect()
        self.rect.x = 512
        self.rect.y = 512
        self.xspeed = 0
        self.yspeed = 0
        self.speed = 3
        self.pxlimit = 256
        self.tm = tm
        self.layer = 2
        self.target = tar
        self.orbevictoria = False
        self.vidamax = 180
        self.vida = 180
        self.kimax = 96
        self.ki = 96
        self.puno = False
        self.fpuno = False
        self.puno2 = False
        self.fpuno2 = False
        self.shoot = False
        self.fshoot = False
        self.punorang = 48
        self.anim = "Idle"
        self.prevanim = ""
        self.dir = 0
        self.indexanim = 0
        self.speedanim = 5
        self.tickcount = 0
        self.f = False
        self.fdano = True
        self.danotick = True

        self.factordenivel = 2
        self.aumentobasenivel = 50
        self.factorderesistencia = 2
        self.danobase = 5
        self.poderbase = 5


        self.exp = 0
        self.nivel = 20
        self.expsiguientenivel = (self.factordenivel**self.nivel)*self.factordenivel+100

        self.dano = self.danobase*self.nivel/2
        self.poder = self.poderbase*self.nivel/2
        self.resistencia = self.nivel*self.factorderesistencia

        self.live = True



    def disparar(self):
        b = Shoot(self.rect.center, self.dir,0,self.dano+self.poder+20)
        c.Grupos["shoots"].add(b)
        c.Grupos["todos"].add(b)

    def punometod(self):
        pospuno = [0,0]
        if self.dir == 0:
            pospuno = [self.rect.centerx,self.rect.bottom + self.punorang]
        elif self.dir == 1:
            pospuno = [self.rect.right + self.punorang,self.rect.centery]
        elif self.dir == 2:
            pospuno = [self.rect.centerx ,self.rect.top - self.punorang]
        elif self.dir == 3:
            pospuno = [self.rect.left - self.punorang,self.rect.centery]

        if self.puno:
            i = Impacto(pospuno,1)
            d = self.dano
        elif self.puno2:
            i = Impacto(pospuno,0)
            d = self.dano+self.poder
        else:
            i = Impacto(pospuno,0)
            d = 0

        c.Grupos["todos"].add(i)
        for en in c.Grupos["enemigos"]:
            if en.live:
                collide = pg.sprite.collide_circle(i,en)
                if collide:
                    if self.puno or self.puno2:
                        text = TextoFlotante((en.rect.x,en.rect.y),"-{} golpe".format(d),c.ROJO)
                        c.Grupos["todos"].add(text)
                    self.target[0] = en
                    en.vida -= d

    def subirnivel(self):
        self.exp = 0
        self.nivel += 1
        self.expsiguientenivel = (self.factordenivel**self.nivel)*self.factordenivel

        self.dano = self.danobase*self.nivel/3
        self.poder = self.poderbase*self.nivel/2
        self.resistencia = self.nivel*self.factorderesistencia
        self.vida = self.vidamax
        self.ki = self.kimax

    def update(self):
        global Global_posicion_x
        global Global_posicion_y
        global Global_speed_x
        global Global_speed_y
        self.xspeed = 0
        self.yspeed = 0
        #Vive?
        if self.vida > 0:
            #Teclas
            keystate = pg.key.get_pressed()
            if keystate[pg.K_SPACE]:
                if (not self.puno) and (not self.puno2) and (not self.shoot):
                    if self.ki >= 1:
                        self.speed = 5
                        self.ki -= 0.1
                    else:
                        self.speed = 3
                else:
                    self.speed = 0
            else:
                if (not self.puno) and (not self.puno2) and (not self.shoot):
                    self.speed = 3
                else:
                    self.speed = 0

            if keystate[pg.K_LEFT]:
                self.xspeed = -self.speed
                self.dir = 3
                self.yspeed = 0

            if keystate[pg.K_RIGHT]:
                self.xspeed = self.speed
                self.dir = 1
                self.yspeed = 0

            if keystate[pg.K_UP]:
                self.yspeed = -self.speed
                self.dir = 2
                self.xspeed = 0

            if keystate[pg.K_DOWN]:
                self.yspeed = self.speed
                self.dir = 0
                self.xspeed = 0

            if keystate[pg.K_a] and (not self.fpuno) and (not self.fpuno2) and (not self.fshoot) and (not self.puno):
                self.puno = True
                self.fpuno = True
                #self.subirnivel()
                self.indexanim = 0
                self.punometod()

            if keystate[pg.K_s] and (not self.fpuno) and (not self.fpuno2) and (not self.fshoot) and (not self.puno2) and (self.ki >= 3):
                self.puno2 = True
                self.ki -= 2
                text = TextoFlotante((self.rect.x,self.rect.y),"-2 ki",c.AZUL)
                c.Grupos["todos"].add(text)
                self.fpuno2 = True
                self.indexanim = 0
                self.punometod()

            if keystate[pg.K_d] and (not self.fpuno) and (not self.fpuno2) and (not self.fshoot) and (not self.shoot) and (self.ki >= 10):
                self.shoot = True
                self.ki -= 5
                self.fshoot = True
                self.indexanim = 0

            if (not keystate[pg.K_a]):
                self.fpuno = False
            if (not keystate[pg.K_s]):
                self.fpuno2 = False
            if (not keystate[pg.K_d]):
                self.fshoot = False

            #Establecer Animacion
            if self.shoot:
                self.anim = "Shoot"
            elif self.puno:
                self.anim = "Puno"
            elif self.puno2:
                self.anim = "Puno2"
            elif (not keystate[pg.K_LEFT]) and (not keystate[pg.K_RIGHT]) and (not keystate[pg.K_DOWN])and (not keystate[pg.K_UP]):
                self.anim = "Idle"

            elif (keystate[pg.K_SPACE]) and (self.ki >= 1):
                self.prevanim = self.anim
                self.anim = "Run"
            else:
                self.prevanim = self.anim
                self.anim = "Walk"

            #Colisiones con los muros

            self.rect.x += self.xspeed
            self.rect.y += self.yspeed

            collisions = pg.sprite.spritecollide(self,c.Grupos["muros"],False)

            for wall in collisions:
                if self.xspeed > 0 and self.yspeed == 0:
                    self.rect.right = wall.rect.left
                elif self.xspeed < 0 and self.yspeed == 0:
                    self.rect.left = wall.rect.right

                if self.yspeed > 0 and self.xspeed == 0:
                    self.rect.bottom = wall.rect.top
                elif self.yspeed < 0 and self.xspeed == 0:
                    self.rect.top = wall.rect.bottom

            #Orb collisions
            collisions = pg.sprite.spritecollide(self,c.Grupos["orbes"],False)

            for orb in collisions:
                if orb.tipo == "Ki":
                    if self.ki + 20 > self.kimax:
                        self.ki = self.kimax
                        text = TextoFlotante((self.rect.x,self.rect.y),"+full ki",c.AZUL)
                        c.Grupos["todos"].add(text)
                    else:
                        text = TextoFlotante((self.rect.x,self.rect.y),"+20 ki",c.AZUL)
                        c.Grupos["todos"].add(text)
                        self.ki += 20
                elif orb.tipo == "Vida":
                    if self.vida + 50 > self.vidamax:
                        self.vida = self.vidamax
                        text = TextoFlotante((self.rect.x,self.rect.y),"+full vida",c.VERDE)
                        c.Grupos["todos"].add(text)
                    else:
                        self.vida += 50
                        text = TextoFlotante((self.rect.x,self.rect.y),"+50 vida",c.VERDE)
                        c.Grupos["todos"].add(text)
                elif orb.tipo == "Trampa":
                    self.vida -= 10
                    text = TextoFlotante((self.rect.x,self.rect.y),"-10 vida",c.ROJO)
                    c.Grupos["todos"].add(text)

                elif orb.tipo == "Exp":
                    self.exp += 10
                    if self.exp >= (self.expsiguientenivel):
                        self.subirnivel()

                    text = TextoFlotante((self.rect.x,self.rect.y),"+10 exp",c.AMARILLO)
                    c.Grupos["todos"].add(text)

                im = Impacto(self.rect.center, 0)
                c.Grupos["todos"].add(im)
                orb.kill()

            #Colisiones con el enemigo
            for en in c.Grupos["enemigos"]:

                collide = pg.sprite.collide_circle(self,en)
                if collide:
                    if self.fdano:
                        print en.name
                        danototal = (en.cdano-(self.resistencia*en.cdano/100))
                        self.vida -= danototal
                        im = Impacto(self.rect.center, 0)
                        text = TextoFlotante((self.rect.x,self.rect.y),"-{} vida".format(danototal),c.ROJO)
                        c.Grupos["todos"].add(text)
                        c.Grupos["todos"].add(im)


            self.danotick +=1
            if self.danotick == 30:
                self.danotick = 0
                self.fdano = True
            else:

                self.fdano = False



            #Coliciones con los proyectiles enemigos
            collisions = pg.sprite.spritecollide(self,c.Grupos["shootsenemigos"],False)

            for b in collisions:
                danototal = (b.dano-(self.resistencia*b.dano/100))
                self.vida -= (b.dano-(self.resistencia*b.dano/100))
                im = Impacto(self.rect.center, 0)
                text = TextoFlotante((self.rect.x,self.rect.y),"-{} vida".format(danototal),c.ROJO)
                c.Grupos["todos"].add(text)
                c.Grupos["todos"].add(im)
                b.kill()


            #Gestion de la Animacion
            if (self.tickcount < self.speedanim):
                self.tickcount+=1
            else:
                self.tickcount = 0

                if self.anim == "Shoot":
                    if self.indexanim < 4:
                        self.indexanim += 1
                    else:
                        self.indexanim = 0
                        self.shoot = False
                        self.disparar()
                        self.punometod()
                        text = TextoFlotante((self.rect.x,self.rect.y),"-5 ki",c.AZUL)
                        c.Grupos["todos"].add(text)


                elif self.anim == "Puno2":
                    if self.indexanim < 7:
                        self.indexanim += 1
                    else:
                        self.indexanim = 0
                        self.puno2 = False

                elif self.anim == "Puno":
                    if self.indexanim < 2:
                        self.indexanim += 1
                    else:
                        self.indexanim = 0
                        self.puno = False

                elif self.anim == "Idle":
                    if self.indexanim < 1:
                        self.indexanim += 1
                    else:
                        self.indexanim = 0
                elif self.anim == "Walk":
                    if self.indexanim < 3:
                        self.indexanim += 1
                    else:
                        self.indexanim = 0
                elif self.anim == "Run":
                    if self.indexanim < 3:
                        self.indexanim += 1
                    else:
                        self.indexanim = 0



            try:
                self.image = self.dicAnimacion[self.anim][self.dir][self.indexanim]
            except IndexError:
                self.indexanim = 0
                self.image = self.dicAnimacion[self.anim][self.dir][self.indexanim]

            #Limites Globales
            if abs(Global_posicion_x - c.TAMANO_VENTANA[0]) < self.tm[0]:
                if self.rect.right > c.TAMANO_VENTANA[0] - self.pxlimit:
                    self.rect.right = c.TAMANO_VENTANA[0] - self.pxlimit
                    Global_posicion_x -= self.speed
                    Global_speed_x = -self.speed
                else:
                    Global_speed_x = 0
            else:
                if self.rect.right > c.TAMANO_VENTANA[0] - 32:
                    self.rect.right = c.TAMANO_VENTANA[0] - 32
                Global_speed_x = 0


            if Global_posicion_x <= 0:
                if self.rect.left < self.pxlimit:
                    self.rect.left = self.pxlimit
                    Global_posicion_x += self.speed
                    Global_speed_x = self.speed

            else:
                if self.rect.left < 32:
                    self.rect.left = 32
                Global_speed_x = 0


            if abs(Global_posicion_y - c.TAMANO_VENTANA[1]) < self.tm[1]:
                if self.rect.bottom > c.TAMANO_VENTANA[1] - self.pxlimit:
                    self.rect.bottom = c.TAMANO_VENTANA[1] - self.pxlimit
                    Global_posicion_y -= self.speed
                    Global_speed_y = -self.speed
                else:
                    Global_speed_y = 0

            else:
                if self.rect.bottom > c.TAMANO_VENTANA[1] - 128:
                    self.rect.bottom = c.TAMANO_VENTANA[1] -128
                Global_speed_y = 0

            if Global_posicion_y <= 0:
                if self.rect.top < self.pxlimit:
                    self.rect.top = self.pxlimit
                    Global_posicion_y += self.speed
                    Global_speed_y = self.speed
            else:
                if self.rect.top < 32:
                    self.rect.top = 32
                Global_speed_y = 0

            if self.vida <= 0:
                self.indexanim = 0

        else:
            if (self.tickcount < self.speedanim):
                self.tickcount+=1
            else:
                self.tickcount = 0
                if self.indexanim < 3:
                    self.indexanim += 1
                else:
                    self.indexanim = 0
                    self.live = False

            if  self.live:
                self.image = self.dicAnimacion["Die"][0][self.indexanim]
            else:
                self.image = self.dicAnimacion["Die"][0][3]

class Triceratops(pg.sprite.Sprite):
    def __init__(self,pos,tar):
        pg.sprite.Sprite.__init__(self)
        self.name = "Rino"
        self.MatrizAnimations = c.TriceratopsSheets;
        self.image = self.MatrizAnimations["Idle"][0][0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.init_x = self.rect.x
        self.init_y = self.rect.y
        self.live = True
        self.target = tar
        self.layer = 1
        self.vidamax = 388
        self.vida = 388

        self.shoot = False
        self.anim = "Idle"
        self.dir = random.randrange(0,4)
        self.indexanim = 0
        self.speedanim = 5
        self.n = 0
        self.time = random.randrange(100,200)
        self.timeidle = self.time
        self.wait = 10
        self.radius = 50

        self.dano = 50
        self.cdano = 10

        self.flagdie = False

    def disparar(self):
        b = Shoot(self.rect.center, self.dir, 1,self.dano)
        c.Grupos["shootsenemigos"].add(b)
        c.Grupos["todos"].add(b)

    def generarrecompensa(self):
        n = random.randrange(9,20)
        for i in range(3):
            x = random.randrange(-128,128)
            y = random.randrange(-128,128)
            orb = Orbes("Exp",(self.rect.centerx+x-Global_posicion_x,self.rect.centery+y-Global_posicion_y))
            #orb = Orbes(tipo,(512+x,512+y))
            c.Grupos["orbes"].add(orb)
            c.Grupos["todos"].add(orb)
        for i in range(n):
            x = random.randrange(-128,128)
            y = random.randrange(-128,128)
            t = random.randrange(0,3)
            if t == 0:
                tipo = "Ki"
            elif t==1:
                tipo = "Vida"
            elif t==2:
                tipo = "Exp"
            orb = Orbes(tipo,(self.rect.centerx+x-Global_posicion_x,self.rect.centery+y-Global_posicion_y))
            #orb = Orbes(tipo,(512+x,512+y))
            c.Grupos["orbes"].add(orb)
            c.Grupos["todos"].add(orb)


    def update(self):
        self.rect.x = self.init_x + Global_posicion_x
        self.rect.y = self.init_y + Global_posicion_y

        if self.timeidle > 1 and not self.shoot and self.live:
            self.timeidle -= 1
        elif self.timeidle == 1:
            for us in c.Grupos["usuarios"]:
                if (us.rect.bottom>self.rect.top) and (us.rect.right<self.rect.left):
                    self.dir = 3
                elif (us.rect.bottom>self.rect.top) and (us.rect.left>self.rect.right):
                    self.dir = 1
                elif (us.rect.bottom<self.rect.top):
                    self.dir = 2
                elif (us.rect.top>self.rect.bottom):
                    self.dir = 0
                else:
                    self.dir = random.randrange(0,4)
            self.timeidle -= 1
        else:
            self.shoot = True
            self.timeidle = self.time

        if self.shoot and self.live:
            if self.n < self.speedanim:
                self.n += 1
            else:
                self.n = 0
                if self.indexanim < 2:
                    self.indexanim += 1
                else:
                    self.indexanim = 0
                    self.disparar()
                    self.shoot = False

            self.image = self.MatrizAnimations["Attack"][self.dir][self.indexanim]

        elif not self.shoot and self.live:

            if self.n < self.speedanim:
                self.n += 1
            else:
                self.n = 0
                if self.indexanim < 1:
                    self.indexanim += 1
                else:
                    self.indexanim = 0

            self.image = self.MatrizAnimations["Idle"][self.dir][self.indexanim]

        else:
            if self.n < self.speedanim:
                self.n += 1
            else:
                self.n = 0
                if self.indexanim < 3:
                    self.indexanim += 1
                else:
                    self.indexanim = 0

            self.image = self.MatrizAnimations["Die"][0][self.indexanim]


        if self.live:
            collisions = pg.sprite.spritecollide(self,c.Grupos["shoots"],False)
            for b in collisions:
                self.target[0] = self
                text = TextoFlotante((self.rect.x,self.rect.y),"-{} bola de energia".format(b.dano),c.ROJO)
                c.Grupos["todos"].add(text)
                im = Impacto(self.rect.center,1)
                c.Grupos["todos"].add(im)
                b.kill()
                self.vida -= b.dano

        if self.vida <= 0:

            if not self.flagdie :
                self.generarrecompensa()
                self.flagdie = True
            #self.target[0] = None
            self.live = False
            #self.kill()

class GeneradorMinions(pg.sprite.Sprite):
    def __init__(self,pos,tar):
        pg.sprite.Sprite.__init__(self)
        self.image = c.ItemSheets["Spawn"][0][0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.init_x = self.rect.x
        self.init_y = self.rect.y
        self.target = tar


        self.timespawn = 500
        self.n = 0
        self.cont = 0
        self.indexanim = 0
        self.speedanim = 3


    def update(self):
        self.rect.x = self.init_x + Global_posicion_x
        self.rect.y = self.init_y + Global_posicion_y

        if (self.rect.top < c.TAMANO_VENTANA[1] and self.rect.left < c.TAMANO_VENTANA[0] and self.rect.right > 0 and self.rect.bottom > 0):
            if self.n < self.timespawn:
                self.n+=1
                self.image = c.ItemSheets["Spawn"][0][0]
                self.indexanim = 0
            else:

                if self.cont < self.speedanim:
                    self.cont += 1
                else:
                    self.cont = 0
                    if self.indexanim < 12:
                        self.indexanim += 1
                    else:
                        self.indexanim= 0
                        self.n = 0
                        cant = random.randrange(1,4)
                        for i in range(cant):
                            x = random.randrange(-128,128)
                            y = random.randrange(-128,128)
                            pos = (self.rect.centerx+x,self.rect.centery+y)
                            minion = Minion(pos,self.target)
                            im = Impacto(pos,0)
                            c.Grupos["todos"].add(im)
                            c.Grupos["enemigos"].add(minion)
                            c.Grupos["todos"].add(minion)

                self.image = c.ItemSheets["Spawn"][0][self.indexanim]

class Minion(pg.sprite.Sprite):
    def __init__(self,pos,tar):
        pg.sprite.Sprite.__init__(self)
        self.name = "Minion"
        self.MatrizAnimations = c.MinionSheets
        self.image = self.MatrizAnimations["Idle"][0][0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.xspeed = 0
        self.yspeed = 0
        self.speed = 2
        self.target = tar
        self.cdano = 5
        self.dano = 10
        self.flagdie = True
        self.live = True
        self.radius = 50

        #self.ventana = pg.display.get_surface()
        self.vidamax = 113
        self.vida = 113

        self.anim = "Idle"
        self.dir = 0
        self.indexanim = 0
        self.speedanim = 5
        self.n = 0
        self.timevisible = 50
        self.parpadeo = True

        self.timeidle = random.randrange(100,200)
        self.timerun = random.randrange(100,200)

        self.contrun = 0
        self.contidle = 0

    def generarrecompensa(self):
        n = random.randrange(3,6)
        for i in range(1):
            x = random.randrange(-128,128)
            y = random.randrange(-128,128)
            orb = Orbes("Exp",(self.rect.centerx+x-Global_posicion_x,self.rect.centery+y-Global_posicion_y))
            #orb = Orbes(tipo,(512+x,512+y))
            c.Grupos["orbes"].add(orb)
            c.Grupos["todos"].add(orb)
        for i in range(n):
            x = random.randrange(-128,128)
            y = random.randrange(-128,128)
            t = random.randrange(0,3)
            if t == 0:
                tipo = "Ki"
            elif t==1:
                tipo = "Vida"
            elif t==2:
                tipo = "Exp"
            orb = Orbes(tipo,(self.rect.centerx+x-Global_posicion_x,self.rect.centery+y-Global_posicion_y))
            #orb = Orbes(tipo,(512+x,512+y))
            c.Grupos["orbes"].add(orb)
            c.Grupos["todos"].add(orb)

    def disparar(self):
        b = Shoot(self.rect.center, self.dir, 2,self.dano)
        c.Grupos["shootsenemigos"].add(b)
        c.Grupos["todos"].add(b)

    def update(self):
        self.yspeed = Global_speed_y
        self.xspeed = Global_speed_x

        if self.live:
            if self.anim == "Walk":
                self.speed = 2
            else:
                self.speed = 0

            for us in c.Grupos["usuarios"]:
                '''
                if (us.rect.right<self.rect.left) and (us.rect.bottom<self.rect.top):
                    self.dir = 3

                elif (us.rect.left <= self.rect.right) and (us.rect.right >= self.rect.left) and (us.rect.bottom<self.rect.top):
                    self.dir = 2

                elif (us.rect.left>self.rect.right) and (us.rect.bottom<self.rect.top):
                    self.dir = 1

                elif (us.rect.right<self.rect.left) and (us.rect.top>self.rect.bottom):
                    self.dir = 3

                elif (us.rect.left <= self.rect.right) and (us.rect.right >= self.rect.left) and (us.rect.top>self.rect.bottom):
                    self.dir = 0

                elif (us.rect.left>self.rect.right) and (us.rect.top>self.rect.bottom):
                    self.dir = 1

                elif (us.rect.top<=self.rect.bottom) and (us.rect.top>=self.rect.top) and (us.rect.right<=self.rect.left):
                    self.dir = 3

                elif (us.rect.top<=self.rect.bottom) and (us.rect.top>=self.rect.top) and (us.rect.left>=self.rect.right):
                    self.dir = 1

                else:
                    self.dir = 1
                '''

                if (us.rect.centerx<self.rect.centerx) and (us.rect.centery<self.rect.centery):
                    self.dir = 3
                elif (us.rect.centerx>self.rect.centerx) and (us.rect.centery<self.rect.centery):
                    self.dir = 1
                elif (us.rect.centerx<self.rect.centerx) and (us.rect.centery>self.rect.centery):
                    self.dir = 1
                elif (us.rect.centerx>self.rect.centerx) and (us.rect.centery>self.rect.centery):
                    self.dir = 1


                if (us.rect.bottom>self.rect.top) and (us.rect.right<self.rect.left):
                    self.dir = 3
                elif (us.rect.bottom>self.rect.top) and (us.rect.left>self.rect.right):
                    self.dir = 1
                elif (us.rect.bottom<self.rect.top):
                    self.dir = 2
                elif (us.rect.top>self.rect.bottom):
                    self.dir = 0
                else:
                    pass
                    #self.dir = random.randrange(0,4)

            if self.dir == 0:
                self.yspeed = Global_speed_y + self.speed
            elif self.dir == 1:
                self.xspeed = Global_speed_x + self.speed
            elif self.dir == 2:
                self.yspeed = Global_speed_y - self.speed
            elif self.dir == 3:
                self.xspeed = Global_speed_x - self.speed

            self.rect.x += self.xspeed
            self.rect.y += self.yspeed


            if self.contidle < self.timeidle:
                self.contidle+=1
                self.anim = "Idle"
            elif self.contrun < self.timerun:
                self.contrun+=1
                self.anim = "Walk"
            else:
                self.anim = "Attack"


            if self.n < self.speedanim:
                self.n += 1
            else:
                self.n = 0
                if self.anim == "Idle":
                    self.animlimit = 1
                elif self.anim == "Attack":
                    self.animlimit = 2
                else:
                    self.animlimit = 3

                if self.indexanim < self.animlimit:
                    self.indexanim += 1
                else:
                    if self.anim == "Attack":
                        self.disparar()
                        self.contrun = 0
                        self.contidle = 0
                    self.indexanim = 0
            try:
                self.image = self.MatrizAnimations[self.anim][self.dir][self.indexanim]
            except IndexError:
                self.indexanim = 0
                self.image = self.MatrizAnimations[self.anim][self.dir][self.indexanim]

            collisions = pg.sprite.spritecollide(self,c.Grupos["muros"],False)

            for w in collisions:
                if self.dir==0:
                    self.dir=2
                    self.rect.y -= 5
                elif self.dir == 1:
                    self.dir=3
                    self.rect.x -= 5
                elif self.dir == 2:
                    self.dir=0
                    self.rect.y += 5
                elif self.dir == 3:
                    self.dir=1
                    self.rect.x += 5

            collisions = pg.sprite.spritecollide(self,c.Grupos["shoots"],False)

            for b in collisions:
                self.target[0] = self
                im = Impacto(self.rect.center,0)
                text = TextoFlotante((self.rect.x,self.rect.y),"-{} bola de energia".format(b.dano),c.ROJO)
                c.Grupos["todos"].add(text)
                c.Grupos["todos"].add(im)
                b.kill()
                self.vida -= b.dano
            if self.vida <= 0:
                #self.target[0] = None
                self.live = False
        else:
            self.yspeed = Global_speed_y
            self.xspeed = Global_speed_x

            self.rect.x += self.xspeed
            self.rect.y += self.yspeed

            if self.n < self.speedanim:
                self.n += 1
            else:
                self.n = 0
                if self.indexanim < 3:
                    self.indexanim += 1
                else:
                    self.indexanim = 0
                    self.flagdie = False


            if  self.flagdie:
                self.image = self.MatrizAnimations["Die"][0][self.indexanim]
            else:
                if self.timevisible > 0:
                    if self.parpadeo:
                        self.parpadeo = False
                        i = 3
                    else:
                        self.parpadeo = True
                        i = 4
                    self.image = self.MatrizAnimations["Die"][0][i]
                    self.timevisible -= 1
                else:
                    self.generarrecompensa()
                    self.kill()

class TextoFlotante(pg.sprite.Sprite):
        def __init__(self, pos,texto,color):
            pg.sprite.Sprite.__init__(self)
            self.fuente = pg.font.Font(None,24)
            self.vtext = texto
            self.color = color
            self.texto = self.fuente.render(self.vtext,True,self.color)
            self.image = self.texto
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
            self.init_x = self.rect.x
            self.init_y = self.rect.y
            #self.speed = random.randrange(-2,2)
            self.speedyfija = random.randrange(-2,2)
            self.speedxfija = random.randrange(-2,2)
            self.speedx = 0
            self.speedy = 0

            self.timelive = 20

        def update(self):
            self.speedx = Global_speed_x + self.speedxfija
            self.speedy = Global_speed_y + self.speedyfija

            self.rect.x += self.speedx
            self.rect.y += self.speedy

            if self.timelive > 0:
                self.timelive -= 1
            else:
                #print "Bye"
                self.kill()

class Impacto(pg.sprite.Sprite):
        def __init__(self, pos,tipo):
            pg.sprite.Sprite.__init__(self)
            self.tipo = tipo
            self.frames = 0
            if self.tipo == 0:
                self.MatrizAnimations = c.ItemSheets["Impacto"]
                self.frames = 8
            elif self.tipo == 1:
                self.MatrizAnimations = c.ItemSheets["Impacto1"]
                self.frames = 5
            self.image = self.MatrizAnimations[0][0]
            #self.image.fill(c.ROJO)
            self.rect = self.image.get_rect()
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]
            self.init_x = self.rect.x
            self.init_y = self.rect.y
            self.layer = 1
            self.radius = 20

            self.indexanim = 0
            self.n =0
            self.speedanim = 5

        def update(self):

            self.image = self.MatrizAnimations[0][self.indexanim]

            if self.n < self.speedanim:
                self.n += 1
            else:
                if self.indexanim < self.frames:
                    self.indexanim += 1
                else:
                    self.kill()

class Muro(pg.sprite.Sprite):
        def __init__(self, possize):
            pg.sprite.Sprite.__init__(self)
            self.image = pg.Surface((possize[2],possize[3]))
            #self.image.fill(c.ROJO)
            self.rect = self.image.get_rect()
            self.rect.x = possize[0]
            self.rect.y = possize[1]
            self.init_x = self.rect.x
            self.init_y = self.rect.y
            self.layer = 2
        def update(self):
            self.rect.x = self.init_x + Global_posicion_x
            self.rect.y = self.init_y + Global_posicion_y

class Palmera(pg.sprite.Sprite):
        def __init__(self, pos):
            pg.sprite.Sprite.__init__(self)
            self.image = c.Level1Graficos["Palmera"][0][0]
            #self.image.fill(c.ROJO)
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]+4
            self.rect.y = pos[1]-3
            self.init_x = self.rect.x
            self.init_y = self.rect.y
            self.layer = 3
        def update(self):
            self.rect.x = self.init_x + Global_posicion_x
            self.rect.y = self.init_y + Global_posicion_y

class Edificio(pg.sprite.Sprite):
        def __init__(self, pos):
            pg.sprite.Sprite.__init__(self)
            self.image = c.Level1Graficos["Edificio"]
            #self.image.fill(c.ROJO)
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]+4
            self.rect.y = pos[1]-3
            self.init_x = self.rect.x
            self.init_y = self.rect.y
            self.layer = 3
        def update(self):
            self.rect.x = self.init_x + Global_posicion_x
            self.rect.y = self.init_y + Global_posicion_y

class Shoot(pg.sprite.Sprite):
    def __init__(self, xy, dir,t,dano):
        pg.sprite.Sprite.__init__(self)

        self.tipo = t
        if self.tipo == 0:
            self.MatrizAnimations = c.ItemSheets["Shoot"]
            self.animlimit = 1
            self.speed = 10

        elif self.tipo ==1:
            self.MatrizAnimations = c.ItemSheets["Fire"]
            self.animlimit = 2
            self.speed = 7

        elif self.tipo == 2:
            self.MatrizAnimations = c.ItemSheets["Shoot_Minion"]
            self.animlimit = 0
            self.speed = 5

        self.image = self.MatrizAnimations[0][0]
        self.rect = self.image.get_rect()
        self.rect.centerx = xy[0]
        self.rect.centery = xy[1]
        self.init_x = self.rect.x
        self.init_y = self.rect.y
        self.dir = dir
        self.anim = 0
        self.indexanim = 0
        self.speedanim = 5
        self.n = 0
        self.xspeed = 0
        self.yspeed = 0

        self.layer = 1
        self.dano = dano

    def update(self):
        self.xspeed = Global_speed_x
        self.yspeed = Global_speed_y

        if self.dir == 0:
            self.yspeed = Global_speed_y + self.speed
            self.anim = 1
        elif self.dir == 1:
            self.xspeed = Global_speed_x + self.speed
            self.anim = 0
        elif self.dir == 2:
            self.yspeed = Global_speed_y - self.speed
            self.anim = 1
        elif self.dir == 3:
            self.xspeed = Global_speed_x - self.speed
            self.anim = 0

        if self.tipo == 1 or self.tipo == 2:
            self.anim = self.dir



        self.rect.x += self.xspeed
        self.rect.y += self.yspeed

        #self.rect.x = self.init_x + Global_posicion_x
        #self.rect.y = self.init_y + Global_posicion_y

        self.image = self.MatrizAnimations[self.anim][self.indexanim]

        if self.n < self.speedanim:
            self.n +=1
        else:
            self.n = 0
            if self.indexanim < self.animlimit:
                self.indexanim += 1
            else:
                self.indexanim = 0
        if (self.rect.right < 0) or (self.rect.left > c.TAMANO_VENTANA[0]) or (self.rect.top > c.TAMANO_VENTANA[1]) or (self.rect.bottom < 0):
            self.kill()

class Orbes(pg.sprite.Sprite):
        def __init__(self, tipo ,pos):
            pg.sprite.Sprite.__init__(self)
            self.tipo = tipo
            if self.tipo == "Ki":
                self.MatrizAnimations = c.ItemSheets["Orbeki"]
            elif self.tipo == "Vida":
                self.MatrizAnimations = c.ItemSheets["Orbevida"]
            elif self.tipo == "Exp":
                self.MatrizAnimations = c.ItemSheets["Orbeexp"]
            elif self.tipo == "Trampa":
                self.MatrizAnimations = c.ItemSheets["Orbetrampa"]
            else:
                self.MatrizAnimations = c.ItemSheets["Orbeki"]
                print "Tipo de orbe desconocido, por defecto KI"

            self.image = self.MatrizAnimations[0][0]
            #self.image.fill(c.ROJO)
            self.rect = self.image.get_rect()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
            self.init_x = self.rect.x
            self.init_y = self.rect.y
            self.layer = 0

            self.indexanim = 0
            self.speedanim = 5
            self.n = 0

        def update(self):
            self.rect.x = self.init_x + Global_posicion_x
            self.rect.y = self.init_y + Global_posicion_y

            self.image = self.MatrizAnimations[0][self.indexanim]

            if self.n < self.speedanim:
                self.n +=1
            else:
                self.n = 0
                if self.indexanim < 2:
                    self.indexanim += 1
                else:
                    self.indexanim = 0

class Background(pg.sprite.Sprite):
    def __init__(self,tm):
        pg.sprite.Sprite.__init__(self)
        self.image =  pg.transform.scale(c.Level1Graficos["Background"], tm)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.init_x = self.rect.x
        self.init_y = self.rect.y
        self.layer = 3

    def update(self):
        self.rect.x = self.init_x + Global_posicion_x
        self.rect.y = self.init_y + Global_posicion_y
