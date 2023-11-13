import pygame, math, random
  
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
scale = 15
brightness = 1
k = 0.00
vis = 0.5
dt = 1
dim =  0.99
fric = 1
rest = 0.05
g = 0
clock = pygame.time.Clock()

def lerp(a,b,k):
    return(a+k*(b-a))

class square():
    def __init__(self, density, velocity, coords, r, g, b, bd = False):
        self.dc = density
        self.dn = 0
        self.pcx = velocity[0]*density
        self.pnx = 0
        self.pcy = velocity[1]*density
        self.pny = 0
        self.p = 0
        self.pn = 0
        self.coords = coords
        self.r = r
        self.g = g
        self.b = b
        self.e = False
        self.bd = bd
        if self.coords[0] == 0 or self.coords[1] == 0 or self.coords[0] == len(squares)-1 or self.coords[1] == len(squares[0])-1:
            self.e = True

    def boundry(self, squares):
        n = 0
        x = 0
        y = 0
        if self.coords[0] != 0:
            if squares[self.coords[0]-1][self.coords[1]].bd == False:
                x += squares[self.coords[0]-1][self.coords[1]].pcx
                y -= squares[self.coords[0]-1][self.coords[1]].pcy
                n+=1
        if self.coords[0] != len(squares)-1:
            if squares[self.coords[0]+1][self.coords[1]].bd == False:
                x += squares[self.coords[0]+1][self.coords[1]].pcx
                y -= squares[self.coords[0]+1][self.coords[1]].pcy
                n+=1
        if self.coords[1] != 0:
            if squares[self.coords[0]][self.coords[1]-1].bd == False:
                y += squares[self.coords[0]][self.coords[1]-1].pcy
                x -= squares[self.coords[0]][self.coords[1]-1].pcx
                n+=1
        if self.coords[1] != len(squares)-1:
            if squares[self.coords[0]][self.coords[1]+1].bd == False:
                y += squares[self.coords[0]][self.coords[1]+1].pcy
                x -= squares[self.coords[0]][self.coords[1]+1].pcx
                n+=1
        if n != 0:
            x /= -n
            y /= -n
            self.pcx = x
            self.pcy = y

    def dim(self):
        self.r *= dim
        self.g *= dim
        self.b *= dim
    
    def diffuse(self, squares):
        if self.e:
            n = 0
            Sn = 0
            Pnx = 0
            Pny = 0
            R = 0
            G = 0
            B = 0
            if self.coords[0] > 0:
                Sn += squares[self.coords[0]-1][self.coords[1]].dn
                Pnx += squares[self.coords[0]-1][self.coords[1]].pnx
                Pny += squares[self.coords[0]-1][self.coords[1]].pny
                R += squares[self.coords[0]-1][self.coords[1]].r
                G += squares[self.coords[0]-1][self.coords[1]].g
                B += squares[self.coords[0]-1][self.coords[1]].b
                n += 1
            else:
                Sn += self.dn
                Pnx += self.pnx
                Pny += self.pny
                R += self.r
                G += self.g
                B += self.b
                n += 1
            if self.coords[1] > 0:
                Sn += squares[self.coords[0]][self.coords[1]-1].dn
                Pnx += squares[self.coords[0]][self.coords[1]-1].pnx
                Pny += squares[self.coords[0]][self.coords[1]-1].pny
                R += squares[self.coords[0]][self.coords[1]-1].r
                G += squares[self.coords[0]][self.coords[1]-1].g
                B += squares[self.coords[0]][self.coords[1]-1].b
                n += 1
            else:
                Sn += self.dn
                Pnx += self.pnx
                Pny += self.pny
                R += self.r
                G += self.g
                B += self.b
                n += 1
            if self.coords[0] < len(squares)-1:
                Sn += squares[self.coords[0]+1][self.coords[1]].dn
                Pnx += squares[self.coords[0]+1][self.coords[1]].pnx
                Pny += squares[self.coords[0]+1][self.coords[1]].pny
                R += squares[self.coords[0]+1][self.coords[1]].r
                G += squares[self.coords[0]+1][self.coords[1]].g
                B += squares[self.coords[0]+1][self.coords[1]].b
                n += 1
            else:
                Sn += self.dn
                Pnx += self.pnx
                Pny += self.pny
                R += self.r
                G += self.g
                B += self.b
                n += 1
            if self.coords[1] < len(squares[0])-1:
                Sn += squares[self.coords[0]][self.coords[1]+1].dn
                Pnx += squares[self.coords[0]][self.coords[1]+1].pnx
                Pny += squares[self.coords[0]][self.coords[1]+1].pny
                R += squares[self.coords[0]][self.coords[1]+1].r
                G += squares[self.coords[0]][self.coords[1]+1].g
                B += squares[self.coords[0]][self.coords[1]+1].b
                n += 1
            else:
                Sn += self.dn
                Pnx += self.pnx
                Pny += self.pny
                R += self.r
                G += self.g
                B += self.b
                n += 1
        else:
            n = 4
            Sn = squares[self.coords[0]-1][self.coords[1]].dn+squares[self.coords[0]][self.coords[1]-1].dn+squares[self.coords[0]+1][self.coords[1]].dn+squares[self.coords[0]][self.coords[1]+1].dn
            Pnx = squares[self.coords[0]-1][self.coords[1]].pnx+squares[self.coords[0]][self.coords[1]-1].pnx+squares[self.coords[0]+1][self.coords[1]].pnx+squares[self.coords[0]][self.coords[1]+1].pnx
            Pny = squares[self.coords[0]-1][self.coords[1]].pny+squares[self.coords[0]][self.coords[1]-1].pny+squares[self.coords[0]+1][self.coords[1]].pny+squares[self.coords[0]][self.coords[1]+1].pny
            R = squares[self.coords[0]-1][self.coords[1]].r+squares[self.coords[0]][self.coords[1]-1].r+squares[self.coords[0]+1][self.coords[1]].r+squares[self.coords[0]][self.coords[1]+1].r
            G = squares[self.coords[0]-1][self.coords[1]].g+squares[self.coords[0]][self.coords[1]-1].g+squares[self.coords[0]+1][self.coords[1]].g+squares[self.coords[0]][self.coords[1]+1].g
            B = squares[self.coords[0]-1][self.coords[1]].b+squares[self.coords[0]][self.coords[1]-1].b+squares[self.coords[0]+1][self.coords[1]].b+squares[self.coords[0]][self.coords[1]+1].b
    
        Sn /= n
        Pnx /= n
        Pny /= n
        R /= n
        G /= n
        B /= n
        self.dn = (self.dc + k*Sn)/(1+k)
        self.pnx = (self.pcx + vis*Pnx)/(1+vis)
        self.pny = (self.pcy + vis*Pny)/(1+vis)
        self.r = (self.r + k*R)/(1+k)
        self.g = (self.g + k*G)/(1+k)
        self.b = (self.b + k*B)/(1+k)

    def velocities(self, squares):
        P_b = (self.pcx**2 + self.pcy**2)**0.5
        if self.coords[0] != 0:
            self.pcx += (squares[self.coords[0]-1][self.coords[1]].b-self.b)*rest
            self.pcx += (squares[self.coords[0]-1][self.coords[1]].b-self.b)*rest
        if self.coords[0] != len(squares)-1:
            self.pcx -= (squares[self.coords[0]+1][self.coords[1]].b-self.b)*rest
        if self.coords[1] != 0:
            self.pcy += (squares[self.coords[0]][self.coords[1]-1].b-self.b)*rest
        if self.coords[1] != len(squares[0])-1:
            self.pcy -= (squares[self.coords[0]][self.coords[1]+1].b-self.b)*rest
        
##        P_a = (self.pcx**2 + self.pcy**2)**0.5
##        if P_a != 0:
##            self.pcx *= P_b/P_a
##            self.pcy *= P_b/P_a
        f = [self.coords[0]-self.pcx*dt/self.dc,self.coords[1]-self.pcy*dt/self.dc]
        if f[0] <= 0:
            f[0] = 0.001
##            self.pcx = 0
        elif f[0] >= len(squares)-1:
            f[0] = len(squares[0])-1.001
##            self.pcx = 0
        if f[1] < 0:
            f[1] = 0.001
##            self.pcy = 0
        elif f[1] >= len(squares[0])-1:
            f[1] = len(squares[0])-1.001
##            self.pcy = 0
        
        i = [int(f[0]),int(f[1])]
        j = [f[0]-i[0],f[1]-i[1]]
        d1 = lerp(squares[i[0]][i[1]].dc, squares[i[0]+1][i[1]].dc, j[0])
        px1 = lerp(squares[i[0]][i[1]].pcx, squares[i[0]+1][i[1]].pcx, j[0])
        py1 = lerp(squares[i[0]][i[1]].pcy, squares[i[0]+1][i[1]].pcy, j[0])
        r1 = lerp(squares[i[0]][i[1]].r, squares[i[0]+1][i[1]].r, j[0])
        g1 = lerp(squares[i[0]][i[1]].g, squares[i[0]+1][i[1]].g, j[0])
        b1 = lerp(squares[i[0]][i[1]].b, squares[i[0]+1][i[1]].b, j[0])
        d2 = lerp(squares[i[0]][i[1]+1].dc, squares[i[0]+1][i[1]+1].dc, j[0])
        px2 = lerp(squares[i[0]][i[1]+1].pcx, squares[i[0]+1][i[1]+1].pcx, j[0])
        py2 = lerp(squares[i[0]][i[1]+1].pcy, squares[i[0]+1][i[1]+1].pcy, j[0])
        r2 = lerp(squares[i[0]][i[1]+1].r, squares[i[0]+1][i[1]+1].r, j[0])
        g2 = lerp(squares[i[0]][i[1]+1].g, squares[i[0]+1][i[1]+1].g, j[0])
        b2 = lerp(squares[i[0]][i[1]+1].b, squares[i[0]+1][i[1]+1].b, j[0])
        self.dct = lerp(d1,d2,j[1])
        self.pnx = lerp(px1,px2,j[1])*fric
        self.pny = lerp(py1,py2,j[1])*fric
        self.rt = lerp(r1,r2,j[1])
        self.gt = lerp(g1,g2,j[1])
        self.bt = lerp(b1,b2,j[1])
##        if f[0] == 0.001:
##            self.pcx = 0
##        elif f[0] == len(squares)-2.001:
##            self.pcx = 0
##        if f[1] == 0:
##            self.pcy = 0
##        elif f[1] == len(squares[0])-2.001:
##            self.pcy = 0

    def vs(self, squares):
        coords = self.coords
        if self.e:
            self.v = 0
            if self.coords[0] == 0:
                self.v += squares[coords[0]+1][coords[1]].pcx - self.pcx
            elif self.coords[0] == len(squares)-1:
                self.v += - squares[coords[0]-1][coords[1]].pcx + self.pcx
            else:
                self.v += squares[coords[0]+1][coords[1]].pcx- squares[coords[0]-1][coords[1]].pcx
            if self.coords[1] == 0:
                self.v += squares[coords[0]][coords[1]+1].pcy - self.pcy
            elif self.coords[1] == len(squares[0])-1:
                self.v += -squares[coords[0]][coords[1]-1].pcy + self.pcy
            else:
                self.v += squares[coords[0]][coords[1]+1].pcy-squares[coords[0]][coords[1]-1].pcy
        else:
            self.v = (squares[coords[0]+1][coords[1]].pcx - squares[coords[0]-1][coords[1]].pcx + squares[coords[0]][coords[1]+1].pcy - squares[coords[0]][coords[1]-1].pcy)/2

    def pns(self, squares):
        coords = self.coords
        if self.e:
            self.pn = -self.v
            if self.coords[0] == 0:
                self.pn += squares[coords[0]+1][coords[1]].pn
            elif self.coords[0] == len(squares)-1:
                self.pn += squares[coords[0]-1][coords[1]].pn
            else:
                self.pn += squares[coords[0]+1][coords[1]].pn + squares[coords[0]-1][coords[1]].pn
            if self.coords[1] == 0:
                self.pn += squares[coords[0]][coords[1]+1].pn
            elif self.coords[1] == len(squares[0])-1:
                self.pn += squares[coords[0]][coords[1]-1].pn
            else:
                self.pn += squares[coords[0]][coords[1]+1].pn + squares[coords[0]][coords[1]-1].pn
            self.pn /= 4
        else:
            self.pn = (squares[coords[0]+1][coords[1]].pn+squares[coords[0]-1][coords[1]].pn+squares[coords[0]][coords[1]+1].pn+squares[coords[0]][coords[1]-1].pn-self.v)/4

    def ps(self, squares):
        coords = self.coords
        if self.e:
            p = [0,0]
            if self.coords[0] == 0:
                p[0] = (squares[coords[0]+1][coords[1]].pn)/2
            elif self.coords[0] == len(squares)-1:
                p[0] = (-squares[coords[0]-1][coords[1]].pn)/2
            else:
                p[0] = (squares[coords[0]+1][coords[1]].pn-squares[coords[0]-1][coords[1]].pn)/2
            if self.coords[1] == 0:
                p[1] = (squares[coords[0]][coords[1]+1].pn)/2
            elif self.coords[1] == len(squares)-1:
                p[1] = (-squares[coords[0]][coords[1]-1].pn)/2
            else:
                p[1] = (squares[coords[0]][coords[1]+1].pn-squares[coords[0]][coords[1]-1].pn)/2
        else:
            p = [(squares[coords[0]+1][coords[1]].pn-squares[coords[0]-1][coords[1]].pn)/2,(squares[coords[0]][coords[1]+1].pn-squares[coords[0]][coords[1]-1].pn)/2]
        self.pcx -= p[0]
        self.pcy -= p[1]
##        self.p = p
    
    def print(self):
        if self.bd:
            pygame.draw.rect(screen, (255, 255, 255), (self.coords[0]*scale, self.coords[1]*scale, scale, scale))
        else:
            pygame.draw.rect(screen, (self.r*255, self.g*255, self.b*255), (self.coords[0]*scale, self.coords[1]*scale, scale, scale))
##            pygame.draw.rect(screen, (255, 255, 255), (self.coords[0]*scale, self.coords[1]*scale, scale, scale), 1)
            
        
    def showVec(self):
        pygame.draw.line(screen, (255, 0, 0), (scale*(self.coords[0]+0.5), scale*(self.coords[1]+0.5)), (scale*(self.coords[0]+0.5+self.pcx), scale*(self.coords[1]+0.5+self.pcy)), 2)
##        pygame.draw.line(screen, (0, 255, 0), (scale*(self.coords[0]+0.5), scale*(self.coords[1]+0.5)), (scale*(self.coords[0]+0.5+self.p[0]), scale*(self.coords[1]+0.5+self.p[1])), 2)
             

squares = []
boundries = []
for i in range(int(size[0]/scale)):
    squares.append([])
    for j in range(int(size[1]/scale)):
##        squares[i].append(square(1, [(random.random()-0.5)*2,(random.random()-0.5)*10], [i, j],0,0,0))
        if False:#i == 0 or i == int(size[0]/scale)-1 or j == 0 or j == int(size[1]/scale)-1:
            squares[i].append(square(1, [0,0], [i, j],0,0,0, True))
            boundries.append(squares[i][j])
        else:
            squares[i].append(square(1, [(random.random()-0.5)*0,(random.random()-0.5)*0], [i, j],0,0,0))

##for i in range(25):
##    for j in range(25):
##        squares[i+2][j+4].r = 1
##        squares[i+20][j+10].b = 1
##        squares[i+9][j+15].g = 1


  
pygame.display.set_caption("Fluid")
run = True

speed = 3
si = 6
h = 6

def printScreen(pSize, squares):
    for i in range(int(size[0]/pSize)-int(scale/pSize)):
        for j in range(int(size[1]/pSize)-int(scale/pSize)):
            x = [int(i/scale*pSize), i/scale*pSize-int(i/scale*pSize)]
            y = [int(j/scale*pSize), j/scale*pSize-int(j/scale*pSize)]
        
            r1 = lerp(squares[x[0]][y[0]].r, squares[x[0]+1][y[0]].r, x[1])
            g1 = lerp(squares[x[0]][y[0]].g, squares[x[0]+1][y[0]].g, x[1])
            b1 = lerp(squares[x[0]][y[0]].b, squares[x[0]+1][y[0]].b, x[1])
            r2 = lerp(squares[x[0]][y[0]+1].r, squares[x[0]+1][y[0]+1].r, x[1])
            g2 = lerp(squares[x[0]][y[0]+1].g, squares[x[0]+1][y[0]+1].g, x[1])
            b2 = lerp(squares[x[0]][y[0]+1].b, squares[x[0]+1][y[0]+1].b, x[1])
            r = lerp(r1,r2,y[1])
            g = lerp(g1,g2,y[1])
            b = lerp(b1,b2,y[1])
            pygame.draw.rect(screen, (r*255, g*255, b*255), (i*pSize, j*pSize, pSize, pSize))

def get_results(result):
    global results
    results.append(result)

def section(sec):
    results = []
    for i in sec:
        for j in i:
            results.append(j.diffuse)
    return results

count = 0
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        if not squares[int(pos[0]/scale)][int(pos[1]/scale)] in boundries and keys[pygame.K_p]:
            boundries.append(squares[int(pos[0]/scale)][int(pos[1]/scale)])
            squares[int(pos[0]/scale)][int(pos[1]/scale)].bd = True
        elif squares[int(pos[0]/scale)][int(pos[1]/scale)] in boundries and not keys[pygame.K_p]:
            boundries.remove(squares[int(pos[0]/scale)][int(pos[1]/scale)])
            squares[int(pos[0]/scale)][int(pos[1]/scale)].bd = False
    if keys[pygame.K_w]:
        if keys[pygame.K_r]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-h,h+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].r = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcy = -speed
                    except:
                        pass
        elif keys[pygame.K_g]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-h,h+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].g = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcy = -speed
                    except:
                        pass
        elif keys[pygame.K_b]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-h,h+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].b = 1#-(((i**2+j**2)**0.5)/((si**2+si**2)**0.5))**5
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcy = -speed
                    except:
                        pass
    elif keys[pygame.K_a]:
        if keys[pygame.K_r]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-h,h+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].r = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcx = -speed
                    except:
                        pass
        elif keys[pygame.K_g]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-si,si+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].g = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcx = -speed
                    except:
                        pass
        elif keys[pygame.K_b]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-10,10+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].b = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcx = -speed
                    except:
                        pass
    elif keys[pygame.K_s]:
        if keys[pygame.K_r]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-si,si+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].r = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcy = speed
                    except:
                        pass
        elif keys[pygame.K_g]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-si,si+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].g = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcy = speed
                    except:
                        pass
        elif keys[pygame.K_b]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-si,si+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].b = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcy = speed
                    except:
                        pass
    elif keys[pygame.K_d]:
        if keys[pygame.K_r]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-si,si+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].r = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcx = speed
                    except:
                        pass
        elif keys[pygame.K_g]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-si,si+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].g = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcx = speed
                    except:
                        pass
        elif keys[pygame.K_b]:
            pos = pygame.mouse.get_pos()
            for i in range(-si,si+1,1):
                for j in range(-si,si+1,1):
                    try:
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].b = 1
                        squares[int(pos[0]/scale)+i][int(pos[1]/scale)+j].pcx = speed
                    except:
                        pass
    screen.fill((0, 0, 0))
    for i in squares:
        for j in i:
            j.showVec()
    for n in range(6):
        for i in squares:
            for j in i:
                if not j in boundries:
                    j.diffuse(squares)
    for i in squares:
        for j in i:
            j.pcx = j.pnx
            j.pcy = j.pny
    for i in range(6):
        for i in squares:
            for j in i:
                    j.vs(squares)
                    j.pns(squares)
    for i in squares:
        for j in i:
                j.ps(squares)
    for i in squares:
        for j in i:
            j.print()
            if not j in boundries: #j.coords[0] != 0 and j.coords[1] != 0 and j.coords[0] != len(squares)-1 and j.coords[1] != len(squares[0])-1:
                j.dc = j.dn
                j.velocities(squares)
            else:
                j.boundry(squares)
    for i in squares:
        for j in i:
            if not j in boundries:
                j.b = j.bt
                j.dn = 0
                j.pnx = 0
                j.pny = 0
                j.dim()
                j.pcy += g
##    printScreen(8, squares)
    for i in squares:
        for j in i:
            pass
            j.showVec()
    pygame.display.update()
    if count == 50:
        print(clock.get_fps())
        count = 0
        drag = 0
        lift = 0
        for j in boundries:
            if j.coords[0] != 0 and j.coords[1] != 0 and j.coords[0] != len(squares)-1 and j.coords[1] != len(squares[0])-1:
                drag += j.pcx
                lift -= j.pcy
        drag = abs(drag)
        if drag == 0:
            LD = 0
        else:
            LD = lift / drag
        print('Drag = ' +  str(drag) + ', Lift = ' + str(lift) + ', L/D = ' +str(LD))
    else:
        count += 1
    clock.tick()
pygame.quit()
