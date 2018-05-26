import pygame as pg
import Components as comp

TAMANO_VENTANA = (1024,640)
CAPTION = "Default"

#Colores
ROJO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
NEGRO = (0,0,0)
BLANCO = (255,255,255)

#Recortador de Imagenes
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

#Grupos Pygame

Grupos = {
"todos" : pg.sprite.LayeredUpdates(),
"usuarios" : pg.sprite.Group(),
"muros" : pg.sprite.Group(),
"shoots" : pg.sprite.Group(),
"shootsenemigos" : pg.sprite.Group(),
"orbes" : pg.sprite.Group(),
"enemigos" : pg.sprite.Group()
}

#Diccionarios de Recursos
GraficosPantallaPrincipal = {
"LogoUTP" : pg.image.load("Recursos/Graficos/PantallaInicio/logoutp.png"),
"LogoISC" : pg.image.load("Recursos/Graficos/PantallaInicio/logoisc.png"),
"Presentacion" : pg.image.load("Recursos/Graficos/PantallaInicio/presentacion.png")
}

GraficosMenuPrincipal = {
"MenuBackground" :pg.image.load("Recursos/Graficos/Menu/menubackground.png"),
"TitleDBZ" : pg.image.load("Recursos/Graficos/Menu/titleDBZ.png"),
"TitleBMAll" : pg.image.load("Recursos/Graficos/Menu/titleBMAll.png"),
"BotonPlay": pg.image.load("Recursos/Graficos/Menu/btnplay.png"),
"BotonQuit": pg.image.load("Recursos/Graficos/Menu/btnquit.png"),
"BotonCredits": pg.image.load("Recursos/Graficos/Menu/btncredits.png"),
"Puntero": pg.image.load("Recursos/Graficos/Menu/puntero1.png")
}

GokuSheets = {
"Idle":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Goku/idle_goku.png"),(17,33),2),
"Walk":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Goku/walk_goku.png"),(17,33),2),
"Run":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Goku/run_goku.png"),(21,33),2),
"Puno":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Goku/puno3_goku.png"),(28,33),2),
"Puno2":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Goku/puno2_goku.png"),(28,33),2),
"Shoot":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Goku/shoot_goku.png"),(28,33),2),
"Die":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Goku/die_goku.png"),(32,32),2)
}



TriceratopsSheets = {
"Idle" : comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Triceratops/idle_rino.png"),(64,64),2),
"Attack" : comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Triceratops/attack_rino.png"),(64,64),2),
"Die" : comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Triceratops/die_rino.png"),(64,64),2)
}

ItemSheets = {
"Shoot": pg.image.load("Recursos/Sprites/Items/shoot.png"),
"BarLife": pg.image.load("Recursos/Graficos/Foregrounds/barlife.png"),
"RinoBarLife": pg.image.load("Recursos/Graficos/Foregrounds/rino_barlife.png"),
"Impacto1":  pg.image.load("Recursos/Sprites/Items/impactonaranja.png"),
"Impacto":  pg.image.load("Recursos/Sprites/Items/impactoazul.png"),
"Fire":  pg.image.load("Recursos/Sprites/Items/fire.png")
}

Level1Graficos = {
"Background": pg.image.load("Recursos/Graficos/Backgrounds/Background.png"),
"Palmera" : comp.recortarAnimacion(pg.image.load("Recursos/Graficos/Foregrounds/palmera.png"),(48,76),2),
"Edificio" : pg.image.load("Recursos/Graficos/Foregrounds/edificio.png"),
}

'''
self.aniorbes = {
"OrbKi" : comp.recortarAnimacion(c.ItemSheets["Ki"],(32,32),1),
"OrbVida" : comp.recortarAnimacion(c.ItemSheets["Vida"],(32,32),1),
"OrbFuerza" : comp.recortarAnimacion(c.ItemSheets["Fuerza"],(32,32),1),
"OrbTrampa" : comp.recortarAnimacion(c.ItemSheets["Trampa"],(32,32),1),
}
self.aniCell = {
"Run" : comp.recortarAnimacion(c.CellSheets["Run"],(52,52),2),
"Shoot" : comp.recortarAnimacion(c.CellSheets["Shoot"],(64,64),2),
}
'''
