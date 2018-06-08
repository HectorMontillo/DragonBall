from Controller import Control
from Setup import Setup
import States

def main():
    print "---------Iniciando Dragon Ball Z Beat'm All--------------"
    Setup()
    print "-----------Configuracion inicial, Terminada--------------"

    diccionarioEstados = {
        "PantallaInicio": States.PantallaInicio("Pantalla de Inicio","Menu"),
        "Menu": States.MenuPrincipal("Menu principal","Prologo"),
        "Prologo": States.Prologo("Prologo","Tutorial"),
        "Tutorial": States.LevelTutorial("Tutorial","Level1"),
        "Level1" :States.Level1("Level 1","QUIT"),
        "Interludio1" : None,
        "LevelFinal" : States.LevelFinal("Level Final","Menu"),
        "Interludio2" : None,
        "Level3" : None,
        "Interludio3" : None,
        "Creditos": None,
        "GameOver": None,
        "Victoria": None
    }

    diccionarioEstados["Tutorial"].setup()

    controlador = Control()
    controlador.preparar_estados(diccionarioEstados,diccionarioEstados["LevelFinal"])
    print "-----------Sistema de estados, Inicializado--------------"
    controlador.main()
    print "-----------------Aplicaion Finalizada--------------------"
