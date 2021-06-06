#-----------------------------------------------Importierungen--------------------------------------------------------#
import pygame
from tkinter import *
from tkinter import messagebox
import resources
import sys
import random
import os

#----------------------------------------------Einstellungen---------------------------------------------------#
class Settings:
    höhe = 320          #Standardgröße des Fensters
    breite = 320
    size = 40           #Größe eines tiles
    mines_max = 10      #Standardanzahl maximaler Minen auf dem Spielfeld
    reihen = 9          #Standardanzahl von Reihen
    spalten = 9         #Standardanzahl von Spalten
    counter = 54
    title = "Minesweeper - Lange"   #Titel des Fensters
    fps = 60                        #Bildwiederholungsrate 
    pygame.font.init()              #Initalisierung
    font = pygame.font.SysFont("Helvetica", 30) #Schriftart
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "resources")  #Pfad der Ressourcen
#--------------------------------------------------------------------------------------------------------------#

#-----------------------------------------------Auswahl der Schwierigkeit--------------------------------------------------------#
t = input("Bitte Schwierigkeit wählen: \"1\" (8x8) , \"2\" (16x16) oder \"3\" (30x16) | Ihre Eingabe: ")    #Fragt nach der Schwierigkeit und wartet auf Eingabe
if t == "1":                #Erste Option
    Settings.höhe = 320
    Settings.breite = 320
    Settings.reihen = 8
    Settings.spalten = 8
    Settings.mines_max = 10
    Settings.counter = 54
if t == "2":                #Zweite Option
    Settings.höhe = 640
    Settings.breite = 640
    Settings.reihen = 16
    Settings.spalten = 16
    Settings.mines_max = 40
    Settings.counter = 216
if t == "3":                #Dritte Option
    Settings.höhe = 640
    Settings.breite = 1200
    Settings.reihen = 30
    Settings.spalten = 16
    Settings.mines_max = 99
    Settings.counter = 381
#--------------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------Klasse für den Spielbereich------------------------------------------------------#
class Spielbereich:#Area
    def __init__(self, screen):
        self.size = Settings.size
        self.reihen = Settings.reihen
        self.spalten = Settings.spalten
        self.bereich = [] #Leere Liste
        self.screen = screen
        self.counter = 0


    def matrix(self):   #Hier wird eine Tilemap erstellt, woraufhin minen_spawn ausgeführt wird um die Minen zu spawnen
        for bit_map in range(self.reihen):
            self.bereich.append(["-"]*Settings.spalten) #Für jedes Feld wird ein "-" der Liste "self.bereich" hinzugefügt
        self.minen_spawn()
        self.minen_zähler()


    def gitter(self, x_pos, y_pos):  #Es wird ein Gitter erstellt, damit die einzelnen Tiles besser gesetzt werden können
        rect = pygame.Rect(0, 0, self.size, self.size)  #rect ganz oben links auf 0, 0 mit der Größe 40x40
        for breite in range(0, (x_pos // self.size)+1): #Für jede Reihe wird ein Gitter stellt...
            for länge in range(0, (y_pos // self.size)+1):  #Und das selbe für die Spalten
                rect = pygame.Rect(breite*self.size, länge*self.size, self.size, self.size)
        return rect
    

    def minen_zähler(self): #Soll die auf dem Spielfeld befindlichen Minen zählen
        minen_anz = 0
        if Settings.mines_max != 99:
            for i in range(0, Settings.reihen):
                minen_anz += self.bereich[i].count("x")
            if minen_anz != Settings.mines_max:
                self.bereich = []
                self.matrix()
    

    def minen_spawn(self): #Die Minen werden zufällig auf dem jeweiligen Spielbereich verteilt
        for mine in range(Settings.mines_max+1):    #Maximale Minenanzahl + 1, da "mines_max" = 10,40 oder 99 ist und Python die letzte Zahl nicht mitzählt. Daher muss diese um 1 erhöht werden
            mine_pos_x = random.randrange(0, Settings.breite)     #Zufällige X-Position der Minen
            mine_pos_y = random.randrange(0, Settings.höhe)       #Zufällige Y-Position der Minen
            x = mine_pos_x//self.size               #Minen werden in die Mitte gesetzt
            y = mine_pos_y//self.size
            self.bereich[x][y] = "x"                #Auf den Feldern, auf denen eine Mine ist, wird in der Liste "self.bereich" ein "x" gesetzt um diese Position zu markieren


    def minen_pos(self, area, screen): #Sobald auf eine Mine geklickt wird, mit rechtsklick, werden die Positionen der einzelnen Minen aufgecket. Im Anschluss wird die Funktion "verloren" ausgeführt
        for x in range(Settings.reihen):    #Für alle X-Positionen
            for y in range(Settings.spalten):   #Für alle Y-Positionen
                if area[x][y] == "x":           #Wenn in der Matrix ein "x" verzeichnet ist, wird an dieser Stelle visuell die Mine angezeigt
                    rect = pygame.Rect(x*self.size, y*self.size, self.size, self.size)
                    bomb = resources.images[0]          #Es wird das erste Bild aus der Liste "images" genutzt, welche sich in der extra Datei "resources" befindet. Diese wird oben importiert
                    bomb = pygame.transform.scale(bomb, (self.size, self.size))   #Das Bild wird gescalet
                    screen.blit(bomb, rect)             #Das Bild wird geblitet
                    pygame.display.update()             #Updatet die Minen
                    pygame.time.wait(50)                #Wartet 50 Millisekunden
        self.verloren()                                 #Die Funktion "verloren" wird ausgeführt


    def overlay(self, screen):  #Es wird ein Overlay für das gesamte Spielfeld erstellt
        for x in range(Settings.breite // self.size):   #Auf der X-Achse...
            for y in range(Settings.höhe // self.size): #Und der Y-Achse...
                rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)  #Werden die Tiles gesetzt. Damit ist das Spielfeld sichtbar
                tile = resources.images[1]    #Es wird wieder das erste Bild genutzt, aber diesesmal aus der Liste "test", welche sich in der Datei "resources" befindet
                tile = pygame.transform.scale(tile, (self.size, self.size))   #Das Bild wird auf 40x40 gescalet
                screen.blit(tile, rect)     #Das Bild wird geblitet
                pygame.display.update()     #Es wird geupdatet


    def verloren(self): #Diese Funktion wird ausgeführt, wenn festgestellt wurde, dass auf eine Mine geklickt wurde
        root = Tk().wm_withdraw()
        message = messagebox.askquestion("Lost", "Do you want to play again?", icon='question') #In einer messagebox mit dem Namen "Lost", wird gefragt ob erneut gespielt werden möchte. "icon" zeigt das Symbol links an, kann auch z.B. durch "warning" ersetzt werden
        if message == 'yes':    #Wenn auf die Frage mit Ja geantwortet wird, wird das Spiel erneut ausgeführt
            game = None
            game = Game()
            game.run()
        else:                   #Wenn eine andere Antwort auf die Frage gegeben wird, welche nein ist, wird das Spiel beendet
            sys.exit()

    def gewonnen(self): #Diese Funktion wird ausgeführt, wenn festgestellt wurde, dass auf eine Mine geklickt wurde
        root = Tk().wm_withdraw()
        message = messagebox.askquestion("Won", "Do you want to play again?", icon='question') #In einer messagebox mit dem Namen "Win", wird gefragt ob erneut gespielt werden möchte. "icon" zeigt das Symbol links an, kann auch z.B. durch "warning" ersetzt werden
        if message == 'yes':    #Wenn auf die Frage mit Ja geantwortet wird, wird das Spiel erneut ausgeführt
            game = None
            game = Game()
            game.run()
        else:                   #Wenn eine andere Antwort auf die Frage gegeben wird, welche nein ist, wird das Spiel beendet
            sys.exit()


    def check(self, x, y, area):    #Es wird geschaut, ob auf dem Feld, welches angeklickt wurde, sich eine Mine befindet
        if x >= 0 and y >= 0:
            try:
                if area[x][y] == "x":
                    return True
            except IndexError:
                return False
            else:
                return False
        else:
            return False


    def markierung(self, x, y, r, screen):  #Mit dieser Funktion, kann mit einem Rechtsklick gekennzeichnet werden, wo sich nach der Meinung des Spielers eine Bombe befindet. Dieses Feld wird mit einer Flag gekennzeichnet
        x = x // self.size
        y = y // self.size
        rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
        flag = resources.images[11]
        flag = pygame.transform.scale(flag, (40, 40))
        screen.blit(flag, rect)
        pygame.display.update()     


    def around(self, x, y, r, screen):
        #----------------------------------------------
        x = x // self.size #In diesem ersten "Abschnitt" der Funktion, wird geschaut ob auf ein Feld mit einem "x" geklickt wurde. Falls dies der Fall ist, ist das Spiel verloren
        y = y // self.size
        self.count = 0      #Counter zum schauen wie weit die Mine von der aktuell Position entfernt ist
        if self.bereich[x][y] == "x":
            print("Lost")
            self.minen_pos(self.bereich, self.screen)
        #----------------------------------------------

        elif self.bereich[x][y] != "x": #Wenn auf ein Feldgeklickt wurde, auf dem kein "x" in der Matrix gekennzeichnet ist...
            print(self.bereich)
            if self.bereich[x][y] != "*":
                if self.counter <= Settings.counter:
                    self.counter += 1
                    print(self.counter)
                if self.counter == Settings.counter:
                    self.gewonnen()
                if self.check(x, y-1, self.bereich):    #Wird jede einzelne Position rund um das letzte angeklickte Feld gescannt, ob sich dort Felder mit einem "x" befinden
                    self.count = self.count + 1
                if self.check(x, y+1, self.bereich):
                    self.count = self.count + 1
                if self.check(x+1, y, self.bereich):
                    self.count = self.count + 1
                if self.check(x-1, y, self.bereich):
                    self.count = self.count + 1
                if self.check(x-1, y-1, self.bereich):
                    self.count = self.count + 1
                if self.check(x+1, y+1, self.bereich):
                    self.count = self.count + 1
                if self.check(x-1, y+1, self.bereich):
                    self.count = self.count + 1
                if self.check(x+1, y-1, self.bereich):
                    self.count = self.count + 1
            
        #----------------------------------------------
                rect = pygame.Rect(x*self.size, y*self.size, self.size, self.size)  #Durch die Abfrage oben, wird das Feld "ausgegraut" bzw. so angezeigt, dass dieses bereits angeklickt wurde
                clear = resources.images[10]       #Es wird das vierte Bild aus der Liste "number" genutzt, welche in der Datei "resources" ist
                clear = pygame.transform.scale(clear, (self.size, self.size))
                screen.blit(clear, rect)
                pygame.display.update()
                pygame.time.wait(50)
                #pygame.draw.rect(screen, (185, 185, 185) ,r)

                self.bereich[x][y] = '*'
        
        #----------------------------------------------
                if self.count == 0: #Sollten sich im Umkreis keine Minen befinden, passiert nichts
                    pass
                elif self.count == 1:   #Befindet sich eine Mine im Umkreis der angeklicken Position...
                    rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
                    one = resources.images[2] #...wird das erste Bild aus der Liste "number" genutzt, welches sich ebenfalls in der Datei "resources" befindet. (Alle benötigten Dateien werden ganz oben importiert)
                    one = pygame.transform.scale(one, (40, 40))
                    screen.blit(one, rect)
                    pygame.display.update()
                    self.bereich[x][y] = "*"
                    print("1")
                elif self.count == 2:   #Selbes wie für 1 gilt auch für 2...
                    rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
                    two = resources.images[3]
                    two = pygame.transform.scale(two, (40, 40))
                    screen.blit(two, rect)
                    pygame.display.update()
                    self.bereich[x][y] = "*"
                    print("2")
                elif self.count == 3:   #Sowie die 3...
                    rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
                    three = resources.images[4]
                    three = pygame.transform.scale(three, (40, 40))
                    screen.blit(three, rect)
                    pygame.display.update()
                    self.bereich[x][y] = "*"
                    print("3")
                elif self.count == 4:   #Sowie die 4...
                    rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
                    three = resources.images[5]
                    three = pygame.transform.scale(three, (40, 40))
                    screen.blit(three, rect)
                    pygame.display.update()
                    self.bereich[x][y] = "*"
                    print("4")
                elif self.count == 5:   #Sowie die 4...
                    rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
                    three = resources.images[6]
                    three = pygame.transform.scale(three, (40, 40))
                    screen.blit(three, rect)
                    pygame.display.update()
                    self.bereich[x][y] = "*"
                    print("5")
                elif self.count == 6:   #Sowie die 4...
                    rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
                    three = resources.images[7]
                    three = pygame.transform.scale(three, (40, 40))
                    screen.blit(three, rect)
                    pygame.display.update()
                    self.bereich[x][y] = "*"
                    print("6")
                elif self.count == 7:   #Sowie die 4...
                    rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
                    three = resources.images[8]
                    three = pygame.transform.scale(three, (40, 40))
                    screen.blit(three, rect)
                    pygame.display.update()
                    self.bereich[x][y] = "*"
                    print("7")
                elif self.count == 8:   #Sowie die 4...
                    rect = pygame.Rect(x * self.size, y * self.size, self.size, self.size)
                    three = resources.images[9]
                    three = pygame.transform.scale(three, (40, 40))
                    screen.blit(three, rect)
                    pygame.display.update()
                    self.bereich[x][y] = "*"
                    print("8")

#-----------------------------------------------Klasse für das Spiel an sich--------------------------------------------------------#
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Settings.breite, Settings.höhe))
        pygame.display.set_caption(Settings.title)
        self.done = False
        self.clock = pygame.time.Clock()

        self.bereich = Spielbereich(self.screen)
        self.bereich.matrix()
        
        self.stop = 0

    def run(self):
        while not self.done:    #Hauptprogrammschleife mit Abbruchkriterium   
            self.clock.tick(Settings.fps)   #Setzt die Taktrate auf max 60fps   
            for event in pygame.event.get():    #Durchwandere alle aufgetretenen  Ereignisse
                if event.type == pygame.QUIT:   # Wenn das X oben rechts im Fenster angeklickt wird
                    self.done = True            #Wird self.done auf True gesetzt um somit das Spiel beendet
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: #Selbes gilt für die Taste "Q"
                        self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN: #Wenn mit der Maus geklickt wird
                    maus = pygame.mouse.get_pressed()   #Wird in "maus" gespeichert mit welcher Taste
                    if maus[0]:             #Wird ein Linksklick ausgeführt...
                        x_pos, y_pos = pygame.mouse.get_pos()
                        temporary_rect = self.bereich.gitter(x_pos, y_pos)
                        self.bereich.around(x_pos, y_pos, temporary_rect, self.screen)  #Wird die Funktion "around" der Klasse "Spielbereich" ausgeführt
                    if maus[2]:             #Wird ein Rechtsklick ausgeführt...
                        x, y = pygame.mouse.get_pos()
                        temporary_rect = self.bereich.gitter(x, y)
                        self.bereich.markierung(x, y, temporary_rect, self.screen)  #Wird die Funktion "markierung" der Klasse "Spielbereich" ausgeführt

            if self.stop == 0: #Es wird abgefragt ob sich die Variable "self.stop" auf dem Wert 0 befindet
                self.bereich.overlay(self.screen)   #Dies wird gemacht, damit diese Funktion nur einmal ausgeführt wird und nicht immer wieder.
                self.stop = 1

            pygame.display.update() # Aktualisiert das Fenster


if __name__ == '__main__':

    pygame.init()
    game = Game()
    game.run()

    pygame.quit()