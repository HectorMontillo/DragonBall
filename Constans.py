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
AMARILLO = (255,255,0)

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
def limpiargrupos():
    for i in Grupos:
        Grupos[i].empty()

Grupos = {
"todos" : pg.sprite.LayeredUpdates(),
"usuarios" : pg.sprite.Group(),
"muros" : pg.sprite.Group(),
"shoots" : pg.sprite.Group(),
"shootsenemigos" : pg.sprite.Group(),
"orbes" : pg.sprite.Group(),
"enemigos" : pg.sprite.Group(),
"collisions" : pg.sprite.Group(),
"ciudadanos" : pg.sprite.Group()
}

Gokusaves = {
"Nivel" : 1,
"Exp" : 0
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

MinionSheets = {
"Idle" : comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Minion/idle_minion.png"),(16,32),2),
"Walk" : comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Minion/walk_minion.png"),(16,32),2),
"Attack" : comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Minion/attack_minion.png"),(30,32),2),
"Die" : comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Minion/die_minion.png"),(16,32),2)
}

Androide17Sheets = {
"Idle":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Androide17/idle_17.png"),(17,31),2),
"Run":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Androide17/run_17.png"),(17,31),2),
"Hit":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Androide17/hit_17.png"),(27,32),2),
"Shoot":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Androide17/shoot_17.png"),(22,32),2),
"Die":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Androide17/die_17.png"),(27,32),2)
}

ItemSheets = {
"Shoot": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/shoot.png"),(64,64),1),
"Shoot_Minion": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/shoot_minion.png"),(16,16),2),
"BarLife": pg.image.load("Recursos/Graficos/Foregrounds/barlife.png"),
"BarLifePro": pg.image.load("Recursos/Graficos/Foregrounds/barlifepro.png"),
"RinoBarLife": pg.image.load("Recursos/Graficos/Foregrounds/rino_barlife.png"),
"MinionBarLife": pg.image.load("Recursos/Graficos/Foregrounds/minion_barlife.png"),
"Impacto1": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/impactonaranja.png"),(64,64),1),
"Impacto": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/impactoazul.png"),(80,80),1),
"Impactogrande": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/impactogrande.png"),(256,256),1),
"Fire": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/fire.png"),(96,96),1),
"Orbeki": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/orbki.png"),(32,32),1),
"Orbevida":comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/orbvida.png"),(32,32),1),
"Orbeexp": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/orbexp.png"),(32,32),1),
"Orbetrampa": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/orbtrampa.png"),(32,32),1),
"Spawn": comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Items/spawn.png"),(64,96),2)
}



LevelTutorial = {
"Background" : pg.image.load("Recursos/Graficos/Backgrounds/background_tutorial.png"),
"TeclasMovimiento" : pg.transform.scale(pg.image.load("Recursos/Graficos/Tutorial/teclasmovimiento.png"),(300,195)),
"Espacio" : pg.transform.scale(pg.image.load("Recursos/Graficos/Tutorial/espacio.png"),(300,195)),
"Orbes" : pg.transform.scale(pg.image.load("Recursos/Graficos/Tutorial/orbes.png"),(300,195)),
"Generador" : pg.transform.scale(pg.image.load("Recursos/Graficos/Tutorial/generador.png"),(300,195)),
"Pelea" : pg.transform.scale(pg.image.load("Recursos/Graficos/Tutorial/pelea.png"),(300,195)),
"Mision" : pg.transform.scale(pg.image.load("Recursos/Graficos/Tutorial/mision.png"),(300,195)),
"Krilin" : comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Krilin/krilin.png"),(19,30),2),
"Dialogo" :pg.image.load("Recursos/Graficos/Tutorial/dialogo.png")

}
'''
"TeclasMovimiento" : pg.image.load("Recursos/Graficos/Tutorial/teclasmovimiento.png"),
"Espacio" : pg.image.load("Recursos/Graficos/Tutorial/espacio.png")
'''


Level1Graficos = {
"Background": pg.image.load("Recursos/Graficos/Backgrounds/Background.png"),
"Palmera" : comp.recortarAnimacion(pg.image.load("Recursos/Graficos/Foregrounds/palmera.png"),(48,76),2),
"Edificio" : pg.image.load("Recursos/Graficos/Foregrounds/edificio.png"),
"Bulma" :  comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Bulma/bulma.png"),(19,32),2),
"Milk" :  comp.recortarAnimacion(pg.image.load("Recursos/Sprites/Milk/milk.png"),(18,32),2),
}

LevelFinalGraficos = {
"Background": pg.image.load("Recursos/Graficos/Backgrounds/background_final.png"),
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
