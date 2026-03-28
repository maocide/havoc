import pygame, sys, os, math, random, imagemanipulation, pixelperfect
from pygame.locals import *
from gameobjects import *
import gameobjects

class thrust(pygame.sprite.Sprite) :
    next_update = 0
    alpha = 200
    colors = [(255,100,0), (240,49,29), (255,217,0), (230,30,0)]
    
    def __init__(self, position) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = pygame.Surface([25,25])
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        
        for i in xrange(0, 2) :
            color = random.choice(self.colors)
            radius = random.randrange(1, 6, 1)
            x = random.randrange(0 + radius*2, self.rect.width - radius*2, 1)
            y = random.randrange(0 + radius*2, self.rect.height - radius*2, 1)
            pygame.draw.circle(self.image, color, (x,y), 5, 0)
        #pygame.draw.circle(self.image, (255,255,255), (12,12), 5, 0)
        
        self.rect = self.image.get_rect()
        self.rect.center = position
        
    
    def update(self, current_time) :
        
        if self.next_update <= current_time :
            self.alpha -= 10
            self.image.set_alpha(self.alpha)
            self.rect.center = (self.rect.center[0], self.rect.center[1] + 1)
        
        if self.alpha <= 0 :
            self.kill()
            del self
            return
        
        self.next_update = current_time + 15
        
class shot(pygame.sprite.Sprite) :
    angle = 0.0
    position = (0,0)
    speed = 18.0
    damage = 20
    reload_time = 200
    target = None
    am_cost = 0
    
    images = []
    
    hitmask = None
    
    def __init__(self, position, angle) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.position = position
        self.angle = angle
        
        #self.image = pygame.Surface([6, 10])
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
        
        #pygame.draw.rect(self.image, (255,255,255), self.rect, 0)
        #self.image.set_colorkey((0,0,0))
        
        self.orig = self.image
        
        self.image = pygame.transform.rotate(self.orig, angle)
        
        #self.image = self.image.convert_alpha()
        #self.image.set_colorkey((0,0,0))
        #self.orig.set_colorkey((0,0,0))
        
        self.rect = self.image.get_rect()        
        self.rect.center = (position[0], position[1])

        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
        #for i in range(4) :
        #    newimg = pygame.surface.Surface([1,1])
        #    #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
        #    newimg.fill(random.choice([(255,255,255)]))
        #    newx = random.randint(-1 * self.rect.width/2,self.rect.width/2) + self.rect.center[0]
        #    newy = random.randint(-1 * self.rect.height/2,self.rect.height/2)  + self.rect.center[1]
        #    
        #    particle(newimg, (newx, newy), random.randint(self.angle -20, self.angle +20))
        
        self.offsetx = (math.cos(math.radians(self.angle + 90))) * self.speed
        self.offsety = (math.sin(math.radians(self.angle + 90))) * self.speed * -1
        
    def update(self, current_time) :
        
        #self.rect.left += self.offsetx
        #self.rect.bottom -= self.offsety
        self.rect = self.rect.move(self.offsetx, self.offsety)
        
        #self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
        if self.rect.topleft[0] <= 0 or self.rect.topright[0] >= pygame.display.get_surface().get_width() or self.rect.top <= 0 :
            self.kill()
    
        
    def compute_hitmask(self) :
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
            
    def explode(self) :
        for i in xrange(4) :
            newimg = pygame.surface.Surface([2,2])
            #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
            newimg.fill(random.choice([(180,180,255)]))
            newx = random.randint(-1 * self.rect.width/2,self.rect.width/2) + self.rect.center[0]
            newy = random.randint(-1 * self.rect.height/2,self.rect.height/2)  + self.rect.center[1]
            
            gameobjects.particle(newimg, (newx, newy), random.randint(self.angle-20, self.angle+21))
        
        self.kill()
        
        
class chainShot(shot) :
    
    images = []
    reload_time = 100
    am_cost = 4
    damage = 15
    speed = 20.0
    
    def __init__(self, position, angle) :
        shot.__init__(self, position, angle)
        #self.image = self.images[0]
        
    def explode(self) :
        for i in xrange(4) :
            newimg = pygame.surface.Surface([2,2])
            #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
            newimg.fill(random.choice([(180,180,180)]))
            newx = random.randint(-1 * self.rect.width/2,self.rect.width/2) + self.rect.center[0]
            newy = random.randint(-1 * self.rect.height/2,self.rect.height/2)  + self.rect.center[1]
            
            gameobjects.particle(newimg, (newx, newy), random.randint(self.angle-20, self.angle+21))
        
        self.kill()
        
class magneticShot(shot) :
    
    images = []
    reload_time = 460
    am_cost = 30
    damage = 60
    #speed = 20.0
    
    def __init__(self, position, angle) :
        #shot.__init__(self, position, angle)
        #self.image = self.images[0]
        
        self.angle = angle
        self.position = position
        
        #make particles arount the player
        for i in xrange(10) :
            newimg = pygame.surface.Surface([2,2])
            #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
            newimg.fill(random.choice([(180,180,180)]))
            #newx = random.randint(-1 * al.rect.width/2,al.rect.width/2) + al.rect.center[0]
            #newy = random.randint(-1 * al.rect.height/2,al.rect.height/2)  + al.rect.center[1]
            
            gameobjects.particle(newimg, position, random.randint(self.angle-30, self.angle+31))
        
        
        #self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
        shotmidtopx = position[0]
        shotmidtopy = position[1]
        candidates = []
        
        #target impact prevision
        for al in self.alienContainers :
            alienbottom = al.rect.bottom
                    
            alienbottomleftx = al.rect.bottomleft[0]
            alienbottomlefty = al.rect.bottomleft[1]
            
            alienbottomrightx = al.rect.bottomright[0]
            alienbottomrighty = al.rect.bottomright[1]
            
            aliencenterx = al.rect.center[0]
            aliencentery = al.rect.center[1]
            
            alienleft = al.rect.left
            alienright = al.rect.right
            
            #angle shot - alien bottomleft
            cat1, cat2 = shotmidtopx - alienbottomleftx, shotmidtopy - alienbottomlefty
            ipot1 = math.sqrt(pow(cat1, 2) + pow(cat2, 2))
            try :
                anglesh1 = math.degrees(math.acos(cat2 / ipot1))
            except ZeroDivisionError :
                anglesh1 = 0.0
            
            if cat1 < 0 : anglesh1 *= -1
            
            #angle shot - alien bottomright
            cat1, cat2 = shotmidtopx - alienbottomrightx, shotmidtopy - alienbottomrighty
            ipot2 = math.sqrt(pow(cat1, 2) + pow(cat2, 2))
            try :
                anglesh2 = math.degrees(math.acos(cat2 / ipot2))
            except ZeroDivisionError :
                anglesh2 = 0.0
            
            if cat1 < 0 : anglesh2 *= -1
            
            #angle shot - alien center
            cat1, cat2 = shotmidtopx - aliencenterx, shotmidtopy - aliencentery
            ipot3 = math.sqrt(pow(cat1, 2) + pow(cat2, 2))
            try :
                anglesh3 = math.degrees(math.acos(cat2 / ipot3))
            except ZeroDivisionError :
                anglesh3 = 0.0
            
            if cat1 < 0 : anglesh3 *= -1

            
            
            #if this shot angle is between calculated angles append (distance, target) to a list
            if ((self.angle >= anglesh1 and self.angle <= anglesh2) or (self.angle >= anglesh2 and self.angle <= anglesh1)) :
                candidates.append((ipot3, al))
                #diffa = self._angle
                
                #if sh.rect.midtop[0] <= self.rect.center[0] :
                if self.angle > anglesh3 :
                    mult = 1
                else :
                    mult = -1
                    
            #if hit sort list to get the closest alien
        if len(candidates)>0 :
            candidates.sort()
                
            for i in xrange(40) :
                newimg = pygame.surface.Surface([2,2])
                #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
                newimg.fill(random.choice([(180,180,255), (100,100,255), (150,150,255), (60,60,255)]))
                newx = random.randint(-1 * candidates[0][1].rect.width/2,candidates[0][1].rect.width/2) + candidates[0][1].rect.center[0]
                newy = random.randint(-1 * candidates[0][1].rect.height/2,candidates[0][1].rect.height/2)  + candidates[0][1].rect.center[1]
                
                gameobjects.particle(newimg, (newx, newy), random.randint(self.angle-20, self.angle+21))

            candidates[0][1].rect.top -= 5
            candidates[0][1].hit(self)
            
        else :
            pass
        
        del self
        
        
    def explode(self) :
        for i in xrange(4) :
            newimg = pygame.surface.Surface([2,2])
            #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
            newimg.fill(random.choice([(180,180,180)]))
            newx = random.randint(-1 * self.rect.width/2,self.rect.width/2) + self.rect.center[0]
            newy = random.randint(-1 * self.rect.height/2,self.rect.height/2)  + self.rect.center[1]
            
            gameobjects.particle(newimg, (newx, newy), random.randint(self.angle-20, self.angle+21))
        
        self.kill()
        
class homingShot(shot) :

    images = []
    alienContainers = []
    reload_time = 350
    am_cost = 20
    damage = 35
    
    def __init__(self, position, angle) :
        shot.__init__(self, position, angle)
        self.image = self.images[0]
        
    def update(self, current_time) :
        self.rect = self.rect.move(self.offsetx, self.offsety)
        anglesmall = 360
        
        #self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
        #target selection by angle
        if not isinstance(self.target, pygame.sprite.Sprite) :
            for al in self.alienContainers :
                cat1, cat2 =  self.rect.center[0] - al.rect.center[0], self.rect.center[1] - al.rect.center[1]
                ipot = math.sqrt(math.pow(cat1, 2) + math.pow(cat2, 2))
                
                try :
                    #if cat2 < 0 : cat1 *= -1
                    anglesh1 = math.degrees(math.acos(cat2 / ipot))
                except ZeroDivisionError :
                    anglesh1 = 0.0
                    
                if cat1 < 0 :
                    anglesh1 *= -1
                
                
                if abs(self.angle - anglesh1) < abs(anglesmall) and al.alive() :
                    anglesmall = abs(self.angle - anglesh1)
                    self.target = al
                    

        if self.target :
            cat1, cat2 =  self.rect.center[0] - self.target.rect.center[0], self.rect.center[1] - self.target.rect.center[1]
            ipot = math.sqrt(math.pow(cat1, 2) + math.pow(cat2, 2))
            
            try :
                #if cat2 < 0 : cat1 *= -1
                anglesh1 = math.degrees(math.acos(cat2 / ipot))
            except ZeroDivisionError :
                anglesh1 = 0.0
                    
            if cat1 < 0 :
                anglesh1 *= -1
                        
            if ipot < 300 :
                if anglesh1 < self.angle : self.angle -= 4
                #if anglesh1 < self.angle and not cat2 > 0 : self.angle += 4
                if anglesh1 > self.angle : self.angle += 4
                
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.image = self.image.convert_alpha()
        #self.image.set_colorkey((0,0,0))
        
        self.offsetx = (math.cos(math.radians(self.angle + 90))) * self.speed
        self.offsety = (math.sin(math.radians(self.angle + 90))) * self.speed * -1
        
        radius = random.randrange(1, 4, 1)
        surf = pygame.surface.Surface((radius*3, radius*3))
        smokecolor = random.choice(((200,200,200), (100,100,100), (255,255,255)))
        pygame.draw.circle(surf, (200,200,200), surf.get_rect().center, radius, 0)
        surf.set_colorkey((0,0,0))

        pangle = random.choice((-10 -180 + self.angle, 10 -180 + self.angle + 5))
        
        gameobjects.particle(surf, self.rect.center, pangle)
        
        if self.rect.topleft[0] <= 0 or self.rect.topright[0] >= pygame.display.get_surface().get_width() or self.rect.top <= 0 :
            self.kill()
        
class ship(pygame.sprite.Sprite) :
    images = []
    hitmask = None
    
    _reloading = False
    _next_shot = 0
    _angle = 0.0
    _angle_before = 999.0
    _max_angle = 20.0
    speed = 0.0
    max_speed = 5.0
    offsetx = 0
    hp = 100
    am = 50
    _am_next = 0
    direction = 0
    pps = 0.0
    rest = 0
    _position = (0,0)
    
    _weapons = [True, False, False, False]
    
    _fire_released = True
    
    animating = False
    exploding = False
    
    def __init__(self, position) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        #self.image = pygame.Surface([14, 14])
        res = pygame.display.get_surface().get_rect().width, pygame.display.get_surface().get_rect().height
        #for pt in self.ship :
        #    self.image.set_at(pt, color)
        #self.image = pygame.image.load(os.path.join('data', 'spaceship.png')).convert_alpha()
        self.image = self.images[0]
        #self.image = pygame.surface.Surface.convert(self.image)
        
        
        self.orig = self.image
        
        self.rect = self.image.get_rect()
        self.rect.center = position[0], res[1] + (self.rect.height/2)
        
        self._position = position
        
        #self.thrust.set_alpha(255)
        
        self._angle = 0.0
        self.next_update = 0
        self.next_update_time = 0
        self.last_time = 0
        self.last_position = self.rect.center
        
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
        self._lowspeed = 5.0
        self._hispeed = 12.0
        
        self.set_weapon(1)
        
    def update(self, current_time) :
        
        if current_time >= self.next_update_time :
            
            if self.rect.center[1] > self._position[1] :
                self.rect.center = (self.rect.center[0], self.rect.center[1]-2)
                self.animating = True
            else :
                self.animating = False
            
            busy = self.animating or self.exploding
            center = self.rect.center
            
            if current_time >= self._am_next :
                self._am_next = current_time + 200
                if self.am < 100 : self.am += 1
            
            if self._next_shot <= current_time :
                self._reloading = False
            else :
                self._reloading = True
            
            if not busy :
                
                #get keys and modifiers keys into lists
                keyPressed = pygame.key.get_pressed()
                keyMods = pygame.key.get_mods()
                
                #switch weapon
                if keyPressed[K_1] : self.set_weapon(1)
                if keyPressed[K_2] : self.set_weapon(2)
                if keyPressed[K_3] : self.set_weapon(3)
                if keyPressed[K_4] : self.set_weapon(4)
                
                
                #speed up using antimatter
                if (keyMods & KMOD_LSHIFT == 1 or keyMods & KMOD_RSHIFT == 1) and self.am > 0 :
                    thrust(self.get_thrustpos())
                    thrust(self.get_thrustpos())
                    thrust(self.get_thrustpos())
                    thrust(self.get_thrustpos())
                    self.max_speed = self._hispeed
                    self.am -= 1
                else :
                    self.max_speed = self._lowspeed
                    if self.speed > self._lowspeed : self.speed -= 0.5
                
                #turn left set direction negative increment speed
                if keyPressed[K_LEFT] and not keyPressed[K_RIGHT] :
                    if self.rect.left > 0 :
                        if self.direction == 1 : self.speed = 0.0
                        if self.speed < self.max_speed : self.speed += 0.5
                        self.direction = -1
                        self.offsetx = self.direction * self.speed
                    
                    if not self._angle >= self._max_angle :
                        self._angle += 3.0
                    
                    #center = self.rect.center
                    
                #turn right increment speed set direction positive
                if keyPressed[K_RIGHT] and not keyPressed[K_LEFT]:
                    if self.rect.right < pygame.display.get_surface().get_width() :
                        if self.direction == -1 : self.speed = 0.0
                        if self.speed < self.max_speed : self.speed += 0.5
                        self.direction = 1
                        self.offsetx = self.direction * self.speed
                    
                    if not self._angle <= -1 * self._max_angle :
                        self._angle -= 3.0
                    
                    #center = self.rect.center
                    
                #if no arrow or both arrows pressed, then straiten up and decrese speed
                if (not keyPressed[K_LEFT] and not keyPressed[K_RIGHT]) or (keyPressed[K_LEFT] and keyPressed[K_RIGHT]) :
                    if self._angle > 0.0 : self._angle -= 3.0
                    if self._angle < 0.0 : self._angle += 3.0
                    if self._angle < 3.0 and self._angle > -3.0 : self._angle = 0.0
                    if self.speed > 0.0 : self.speed -= 0.2 # * self.direction
                    if self.speed < 0.2  and self.speed > -0.2 : self.speed = 0.0
                    self.offsetx = self.speed * self.direction

                #for event in pygame.event.get() :
                #    if event.type == pygame.KEYUP:
                #        if event.key == pygame.K_SPACE:
                #            self._fire_released = True
                    
                if not keyPressed[K_SPACE] :
                    self._fire_released = True
                    
                #if nor reloading shot with weapon
                #_fire is a reference to weapon object, the reference change according to selection
                if keyPressed[K_SPACE] and not self._reloading and self._fire_released :
                    if self._fire == homingShot or self._fire == chainShot :
                        shotpos = self.get_side_shotpos()
                        self._next_shot = current_time + self._fire.reload_time
                        self._reloading = True
                        self._fire_released = False
                        if self.am >= self._fire.am_cost :
                            self._fire(shotpos[0], shotpos[2])
                            self._fire(shotpos[1], shotpos[2])
                            self.am -= self._fire.am_cost
                    else :
                        shotpos = self.get_shotpos()
                        self._next_shot = current_time + self._fire.reload_time
                        self._reloading = True
                        self._fire_released = False
                        if self.am >= self._fire.am_cost :
                            self._fire(shotpos[0], shotpos[1])
                            self.am -= self._fire.am_cost
                    #homingShot(shotpos[0], shotpos[1])
                    #flare((shotpos[0], shotpos[1]))
                
                #suicide... does it make sense? up yours.
                if keyPressed[K_k] : 
                    self.exploding = True
                    self.rest -= 1
                    self.explode()
            
            #if angle changes then rotate according to new angle
            if self._angle_before != self._angle :
                self.image = pygame.transform.rotate(self.orig, self._angle)
                self._angle_before = self._angle
            
            #self.image.set_colorkey((0,0,0))
            
            self.rect = self.image.get_rect()
            self.rect.center = center
            
            #if offset is present move by this value
            if self.offsetx != 0.0 and self.rect.center[0] + self.offsetx > 0 and self.rect.center[0] + self.offsetx < pygame.display.get_surface().get_rect().width :
                self.rect.center = ((self.rect.center[0] + self.offsetx, self.rect.center[1]))
            
            #spawn a thrust object.. dies by himself
            thrust(self.get_thrustpos())
            
            #calculate aprox speed by pps!!
            current_time = pygame.time.get_ticks()
            if current_time >= self.next_update :
                self.pps = float(self.last_position[0] - self.rect.center[0]) / float(current_time - self.last_time) * -1 * float(current_time - self.last_time)
                #self.pps
                #print self.pps, float(current_time - self.last_time)
                #if self.last_position[0] < self.rect.center[0] - 10 :
                #    pass
                self.last_position = self.rect.center
                self.next_update = current_time + 100
                self.last_time = pygame.time.get_ticks()
            
            
            
            
            self.next_update_time = current_time + 2
        
        
    def compute_hitmask(self) :
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
    def add_weapon(self, number) :
        """Add weapon number to player's weapons (array index is weapon # -1)."""
        if (number - 1) >= 0 :
            self._weapons[number-1] = True
            
    def del_weapon(self, number) :
        """Del weapon number from player's weapons (array index is weapon # -1)."""
        if (number - 1) >= 0 :
            self._weapons[number-1] = False
    
    def set_weapon(self, number) :
        if self._weapons[number-1] :
            if number == 1 :
                self._fire = shot
            if number == 2 :
                self._fire = homingShot
            if number == 3 :
                self._fire = chainShot
            if number == 4 :
                self._fire = magneticShot
        
    def get_shotpos(self) :
        
        if self._angle != 0.0 :
            origrect = self.orig.get_rect()
            origrect.center = self.rect.center
            
            xc = self.rect.center[0]
            yc = self.rect.center[1]
            lm = origrect.midtop[1] - yc
            
            xm1 = xc + math.ceil(lm * math.sin(math.radians(-1 * self._angle))) * -1
            ym1 = yc + math.ceil(lm * math.cos(math.radians(-1 * self._angle)))
            
            
            return((int(xm1),int(ym1)), self._angle)
        else :
            return(self.rect.midtop, 0.0)
    
    def get_side_shotpos(self) :
        
        if self._angle != 0 :
        
            origrect = self.orig.get_rect()
            origrect.center = self.rect.center
            center = self.rect.center
            
            m = center[0] + 20, center[1] - 20
            p = center[0] - 20, center[1] - 20
            
            cm = math.sqrt(math.pow(center[0] - m[0],2) + math.pow(center[1] - m[1],2))
            m1x = center[0] + cm * math.cos(math.radians(self._angle))
            m1y = center[1] + cm * math.sin(math.radians(self._angle)) * -1
            
            m1 = (int(m1x), int(m1y))
            
            cp = math.sqrt(math.pow(center[0] - p[0],2) + math.pow(center[1] - p[1],2))
            p1x = center[0] + cp * math.cos(math.radians(self._angle)) * -1
            p1y = center[1] + cp * math.sin(math.radians(self._angle))
            
            p1 = (int(p1x), int(p1y))
            
            return(m1, p1, self._angle)
        
        else :
            
            center = self.rect.center
            m = center[0] + 20, center[1] - 20
            p = center[0] - 20, center[1] - 20
            
            return(m, p, 0.0)
    
    def get_thrustpos(self) :
        origrect = self.orig.get_rect()
        origrect.center = self.rect.center
    
        
        xc = self.rect.center[0]
        yc = self.rect.center[1]

        lm = origrect.midbottom[1] - yc
        
        xm1 = xc + math.ceil(lm * math.sin(math.radians(-1 * self._angle))) * -1
        ym1 = yc + math.ceil((lm) * math.cos(math.radians(-1 * self._angle)))
        
        return(xm1, ym1)
    
    def hit(self, bullet) :
        self.hp -= bullet.damage
        if self.hp <= 0 :
            ship.rest -= 1
            bullet.shooter.say(random.choice(bullet.shooter.killquotes))
            self.explode()
    
    def explode(self) :
        gameobjects.explosion(self.orig, self.rect.center, [(0,0,255), (50,50,255), (100,200,255), (100,100,255)])
        self.kill()