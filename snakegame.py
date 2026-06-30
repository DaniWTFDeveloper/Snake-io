import pyxel
import random

class MiniProject:
    def __init__(self):
        pyxel.init(width=1024, height=1024, title="Project No. 1")

        x = random.randint(4, 12)
        y = random.randint(4, 12)
        self.direc = (1, 0)
        self.Snake = [[16, 16, x*16, y*16, self.direc, "head"]]
        self.speed = 3

        self.head = 270
        self.gameOver = False

        x = random.randint(0, 15)*16
        y = random.randint(0, 15)*16
        self.toeat = (x, y)
        self.angles = {(0,1): 0, (0,-1):180, (1, 0):270, (-1,0):90}
        
        pyxel.mouse(True)
        pyxel.load("pixels.pyxres")
        pyxel.run(self.update, self.draw)
    
    def move(self):
        for i in range(len(self.Snake) - 1, 0, -1):
            
            self.Snake[i][2], self.Snake[i][3], self.Snake[i][4], self.Snake[i][5] = self.Snake[i-1][2], self.Snake[i-1][3], self.Snake[i-1][4], "tail" if i == len(self.Snake) - 1 else "body"

        self.Snake[0][2], self.Snake[0][3], self.Snake[0][4] = self.Snake[0][2] + self.direc[0]*16, self.Snake[0][3] + self.direc[1]*16, self.direc
        
        if (self.Snake[0][2], self.Snake[0][3]) == self.toeat:
            self.toEat()
            self.Snake.append([16, 16, self.Snake[-1][2] - (self.Snake[-1][4][0]*16), self.Snake[-1][3] - (self.Snake[-1][4][1]*16), self.Snake[-1][4], "tail"])

    def toEat(self):
        x = random.randint(0, 15)*16
        y = random.randint(0, 15)*16
        for snake in self.Snake:
            if (x, y) not in (snake[2], snake[3]):
                self.toeat = (x, y)

    def speed_cof(self):
        if pyxel.btnp(pyxel.KEY_SHIFT) and self.speed != 1:
            self.speed -= 1
        elif pyxel.btnp(pyxel.KEY_CTRL):
            self.speed += 1

    def way(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W): 
            if not self.direc == (0, 1) :
                self.direc = (0, -1)
                self.head = 180
        elif pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D): 
            if not self.direc == (-1, 0) :
                self.direc = (1, 0)
                self.head = 270
        elif pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S): 
            if not self.direc == (0, -1) :
                self.direc = (0, 1)
                self.head = 0
        elif pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A) : 
            if not self.direc == (1, 0) :
                self.direc = (-1, 0)
                self.head = 90

    def limits(self):
        if self.Snake[0][2] <= -8 or self.Snake[0][2] >= 256 or self.Snake[0][3] <= -8 or self.Snake[0][3] >= 256:
            self.gameOver = True
            if self.Snake[0][2] >= 256:
                self.Snake[0][2] = 240
            if self.Snake[0][3] >= 256:
                self.Snake[0][3] = 240
            if self.Snake[0][2] <= -8:
                self.Snake[0][2] = 0
            if self.Snake[0][3] <= -8:
                self.Snake[0][3] = 0

    def gameOverScreen(self):
        pyxel.rect(89, 112, 78, 32, 5)
        pyxel.blt(95, 120, 0, 32, 0, 16, 16)
        pyxel.text(115, 126, "Rejouer", 10)
        
    def update(self):
        self.limits()
        if self.gameOver == False:
            if pyxel.frame_count % self.speed == 0: 
                self.move()
            self.way()
            self.speed_cof()
                
    def draw(self):
        pyxel.cls(7)
        pyxel.text(10, 10, f"{self.speed}", 0)

        for i in range(len(self.Snake)):
            x, y, w, h, direc, part = self.Snake[i][2], self.Snake[i][3], self.Snake[i][0], self.Snake[i][1], self.Snake[i][4], self.Snake[i][5]

            if part == "head":
                pyxel.blt(x, y, 0, 16, 0, w, h, rotate=self.angles[direc])

            elif part == "body":
                if 0 < i < len(self.Snake) - 1:
                    dir_prev = (self.Snake[i-1][2] - x, self.Snake[i-1][3] - y)
                    dir_next = (self.Snake[i+1][2] - x, self.Snake[i+1][3] - y)

                    if dir_prev[0] != dir_next[0] and dir_prev[1] != dir_next[1]:
                        angle = 0 if {dir_prev, dir_next} == {(16, 0), (0, 16)} else 90 if {dir_prev, dir_next} == {(0, 16), (-16, 0)} else 180 if {dir_prev, dir_next} == {(-16, 0), (0, -16)} else 270
                        pyxel.blt(x, y, 0, 32, 16, w, h, rotate=angle, colkey=7)
                        continue

                pyxel.blt(x, y, 0, 48, 0, w, h, rotate=self.angles[direc], colkey=7)
            elif part == "tail":
                tail_angles = {
                    (0, -1): 0,    # yukarı
                    (1, 0): 90,    # sağ
                    (0, 1): 180,   # aşağı
                    (-1, 0): 270   # sol
                }
                pyxel.blt(x, y, 0, 32, 32, w, h, rotate=tail_angles[self.Snake[i][4]], colkey=7)

        pyxel.blt(self.toeat[0], self.toeat[1], 0, 0, 0, 16, 16)
        if self.gameOver: self.gameOverScreen()
        
MiniProject()
