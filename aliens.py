import pygame, sys, os, math, random, imagemanipulation, pixelperfect
from pygame.locals import *
#from gameobjects import *
import gameobjects
import player

class reddevil(pygame.sprite.Sprite) :
    
    images = []
    containers = []
    
    _attacking = False
    _moving = False
    _engaging = False
    _angle_before = -999.0
    _angle = 0.0
    max_speed = 8
    _accel = 1.0
    _rotate_angle = 2.0
    speed = 0
    offsetx = 0
    offsety = 0
    anglenext = 0.0
    _next_update_time = 0
    _next_move_down_time = 0
    _max_engaging = 1
    update_occurrency = 2
    
    waypoints = []
    
    _target = None
    
    _next_shot = 0
    _reloading_time = 200
    _reloading = False
    _shots = 0
    _max_shots = 3
    _engage_shots = 0
    _position_before_action = ()
    _enmode = -1
    
    _balloon = None
    hurtquotes = []
    killquotes = []
    
    _hp = 100
    
    hitmask = None

    def __get_target__(self) :
        return self._target
    
    def __set_target__(self, target) :
        if target != None : self._target = target
        
    def __get_moving__(self) :
        return self._moving
    
    def __get_attacking__(self) :
        return self._attacking
    
    def __get_engaging__(self) :
        return self._engaging
    
    def __get_hp__(self) :
        return self._hp
    
    def __set_hp__(self, hp) :
        self._hp = hp
        
    def __get_angle__(self) :
        return self._angle
    
    def __get_angle__(self) :
        return self._angle
    
    def __get_completely_onscreen__(self) :
        srect = pygame.display.get_surface().get_rect()
        if self.rect.top < 0 or self.rect.left < 0 or self.rect.right > srect.width or self.rect.bottom > srect.height :
            return False;
        else :
            return True
    
    target = property(__get_target__, __set_target__)
    moving = property(__get_moving__)
    attacking = property(__get_attacking__)
    engaging = property(__get_engaging__)
    hp = property(__get_hp__, __set_hp__)
    angle = property(__get_angle__)
    completely_onscreen = property(__get_completely_onscreen__)
    
    def __init__(self, position, target = None, shotsGroup = None) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self._startposition = position
        
        self.image = random.choice(self.images)
        self.target = target
        #self.image = pygame.surface.Surface.convert(self.image)
        
        self.orig = self.image
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, pygame.display.get_surface().get_rect().width), 0-self.rect.height)
        #self.rect.center = position
        
        #self._startposition = (0,0)
        self._angle = 0.0
        self._next_update_time = 0
        self._next_move_down_time = 0
        
        self.waypoints = []
        
        self.hurtquotes = []
        self.killquotes = []
        
        if shotsGroup != None : self.shotsGroups = shotsGroup
        #self.shotsGroups = None
        
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
        self._fire = alienshot
        
    def update(self, current_time) :
        #if current_time >= self._next_update_time :
            #if set to true a redraw will be issued
            #blit = False
            
            self.center = self.rect.center
            
            if self._next_shot <= current_time :
                self._reloading = False
            else :
                self._reloading = True
                
            if len(self.waypoints) > 0  and not self._moving:
                self.newposition = self.waypoints[0][0]
                self.max_speed = self.waypoints[0][1]
                self.waypoints.pop(0)
                self._moving = True
            
            #move
            if self._moving :
                self.__move__(current_time)
            
            #attack
            if self._attacking and not self.target.animating :
                self.__attack__(current_time) 
                
                        
            #evade attack if not alredy moving or engaging
            if not self._moving and not self._engaging :#and not self.attacking :
                self.__evade__(current_time)
            
            #engage until n# shots are fired
            if self._engaging and not self._moving and not self.target.animating :
                self.__engage__(current_time)
                
            #behave
            if not self._moving and not self.target.animating :
                self.__behave__(current_time)
            
            #reset angle and set speed = 0 if not moving
            if not self._moving and not self._attacking and not self._engaging:
                if self._angle > 0.0 :
                    self._angle -= 2.0
                if self._angle < 0.0 : 
                    self._angle += 2.0
                if self._angle != 0 and self._angle < 2.0 and self._angle > -2.0 : self._angle = 0.0
                if self.speed > 0 : self.speed = 0            
                
            #draw and rotate according to self._angle
            if self._angle != self._angle_before :
                self.image = pygame.transform.rotate(self.orig, self._angle)
                #self.image = self.image.convert_alpha()
                self._angle_before = self._angle
                #blit = True
            #self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = self.center
            
            #stop attacking if target is dead
            if not self.target.alive() :
                self._attacking = False
            
            #move according to the calculated offset
            if self.offsetx != 0 or self.offsety != 0 :
                self.rect = self.rect.move(math.floor(self.offsetx), math.floor(self.offsety))
                #blit = True
                
            #thrust(self.rect.center)
            
            #if blit : pygame.display.get_surface().blit(self.image, self.rect)
            
            self._next_update_time = current_time + self.update_occurrency
            #no, too cpu hungry
            #self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
            
    def say(self, quote, font = os.path.join('data', 'acmeexplosive.ttf'), size = 16, duration = None) :
        if(type(self._balloon) == type(None) or not self._balloon.alive()) :
            if duration == None : duration = len(quote)*200
            self._balloon = gameobjects.balloon(quote, self, font, size, duration)

    def compute_hitmask(self) :
        """Calculate alpha hitmask using pixelperfect module"""
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
    
    def move(self, position, speed = 8) :
        """Set moving to True and new max speed, on update movement to specified position will start"""
        self.newposition = position
        self.max_speed = speed
        self._moving = True
        
    def add_move_point(self, position, speed = 8) :
        """Add a new waypoint, on update waypoints will be processed"""
        self.waypoints.append((position, speed))
        #self.newposition = position
        #self.max_speed = speed
        #self._moving = True
        
    def engage(self, max_shots = 10, target = None) :
        """Start an attack getting closer to target"""
        if target != None : self.target = target
        if self.target != None and self.target.alive() : self._engaging = True
        self._position_before_action = self.rect.center
        self._engage_shots = max_shots
        
    
        
    def attack(self, max_shots = 3, target = None) :
        """Start shoting to target until max_shots are reached, if specified sets target"""
        self._attacking = True
        if target != None : self.target = target
        self._max_shots = max_shots
        
    def get_shotpos(self) :
        origrect = self.orig.get_rect()
        origrect.center = self.rect.center
        
        xc = self.rect.center[0]
        yc = self.rect.center[1]
        lm = origrect.midbottom[1] - yc -5 #offset to alien's hood
        
        xm1 = xc + math.ceil(lm * math.sin(math.radians(-1 * self.angle))) * -1
        ym1 = yc + math.ceil(lm * math.cos(math.radians(-1 * self.angle)))
        
        
        return((xm1,ym1), self.angle)
    
    def hit(self, bullet) :
        """Decrement hits point according to bullet damage, if hp < 0 starts explosion and kills sprite.
        If the alien survives it will fight back shooting 3 times"""
        self._hp -= bullet.damage

        if self._hp <= 35 and len(self.hurtquotes) > 0 :
            if(len(self.hurtquotes)>0) :
                self.say(self.hurtquotes.pop(random.randint(0,len(self.hurtquotes)-1)))
                self.hurtquotes = []
        
        if self._hp <= 0 :
            self.explode()
        else :
            self.attack(3, self.target)
    
    def explode(self) :
        """Create a new explosion object and kill the sprite"""
        gameobjects.explosion(self.orig, self.rect.center, [(200,0,0), (220,50,50), (220,100,50), (200,100,100)])
        self.kill()
        
    def go_offscreen(self) :
        """Starts moving above the top of the screen"""
        if not self._moving or self._engaging :
            x = random.randint(self.rect.center[0] -100, self.rect.center[0] +100)
            y = random.randint(-300, -1 * self.rect.height)
            if type(self._balloon) != type(None) and self._balloon.alive() : self.move((x, y), 3)
            else : self.move((x, y), 7)
            
    #def go_startposition(self) :
        #if not self._moving or self._engaging :
            #self.move(self._startposition, 8)
                
        
        
        
    def __move__(self, current_time) :
        if self.rect.center[0] == self.newposition[0] and self.rect.center[1] == self.newposition[1] :
            self.offsetx = 0
            self.offsety = 0
            self._moving = False
            self.speed = 0
        
        if self.speed < self.max_speed and self._next_update_time <= current_time:
            self.speed += self._accel
        
        cat1, cat2 = self.newposition[0] - self.rect.center[0], self.newposition[1] - self.rect.center[1]
        ipot = math.sqrt(pow(cat1, 2) + pow(cat2, 2))
        try :
            self.anglenext = math.degrees(math.acos(cat2 / ipot)) * -1
            #if self.anglenext > 180 : self.anglenext -180
            #if self.anglenext < -180 : self.anglenext + 180
        except ZeroDivisionError :
            self.anglenext = 0.0
        
        if self.newposition[0] < self.rect.center[0] : xmult = -1
        else : xmult = 1
        #if self.newposition[1] < self.rect.center[1] : ymult = -1
        #else : ymult = 1
        
        #if ipot < 80 :
        #    self.speed -= 0.4
        
        self.offsetx = (math.cos(math.radians(self.anglenext + 90))) * self.speed * xmult
        self.offsety = (math.sin(math.radians(self.anglenext + 90))) * self.speed# * ymult
        
        if self.newposition[0] == self.rect.center[0] and self.offsetx < 1.0 :
            #self.anglenext = -360.0
            pass
        
        if not self._attacking :
            if self._angle < self.anglenext * xmult and self._angle < 20.0 : self._angle += self._rotate_angle
            if self._angle > self.anglenext * xmult and self._angle > -20.0 : self._angle -= self._rotate_angle
            
        if abs(self.offsetx) >= abs(cat1) :
            self.center = (self.newposition[0], self.center[1])
            self.offsetx = 0
        if abs(self.offsety) >= abs(cat2) :
            self.center = (self.center[0], self.newposition[1])
            self.offsety = 0
    
    def __attack__(self, current_time) :
        if not self.target.alive() :
            self._attacking = False
            self._engaging = False
            return
        
        
        #if random.randint(0,1) == 0 :
        cat1, cat2 = self.target.rect.center[0] + self.target.pps * 4.0 - self.rect.center[0], self.target.rect.center[1] - self.rect.center[1]
        #else :
        #cat1, cat2 = self.target.rect.center[0] - self.rect.center[0], self.target.rect.center[1] - self.rect.center[1]
        ipot = math.sqrt(pow(cat1, 2) + pow(cat2, 2))
        try :
            self.angletarget = math.degrees(math.acos(cat2 / ipot))
            #self.angletarget = 90 - math.degrees(math.acos(math.radians(((self.target.pps  + cat1) / alienshot.speed))))
        except ZeroDivisionError :
            self.angletarget = 0.0
        #delta + vt * (Halieno / (vs * sin(alpha))) = vs * (Halieno / (vs * sin(alpha))) * cos(alpha)
        #delta / (Halieno / (vs * sin(alpha))) + vt = vs * cos(alpha)
        #5 + 5*3 = 5*4
        if self.target.rect.center[0] < self.rect.center[0] : xmult = -1
        else : xmult = 1
        
        if self._angle < math.floor(self.angletarget) * xmult : self._angle += 1.0
        if self._angle > math.floor(self.angletarget) * xmult : self._angle -= 1.0
        
        
        #if self._angle * xmult == math.floor(self.angletarget) and not self._reloading :
        #    alienshot(self.get_shotpos()[0], self.get_shotpos()[1])
        #    self._next_shot = current_time + self._reloading_time
        
        if self._angle == math.floor(self.angletarget) * xmult and not self._reloading :
            self._fire(self.get_shotpos()[0], self.get_shotpos()[1], self)
            self._next_shot = current_time + self._fire.reload_time
            self._shots += 1
            if self._shots >= self._max_shots :
                self._attacking = False
                if not self._engaging : self._shots = 0
                
    def __engage__(self, current_time) :        
        srect = pygame.display.get_surface().get_rect()
        screenh, screenw = srect.height, srect.width
        
        #rotate around target
        #cat1, cat2 = self.target.rect.center[0] - self.rect.center[0], self.target.rect.center[1] - self.rect.center[1]
        #ipot1 = math.sqrt(pow(cat1, 2) + pow(cat2, 2))
        #try :
            #anglet = math.degrees(math.acos(cat2 / ipot1))
        #except ZeroDivisionError :
            #anglet = 0.0
            
        #if self.target.rect.center[0] <= self.rect.center[0] :
            #anglet *= -1
            
        #anglet = 180.0 - anglet -90.0
            
        #xcoord = (self.target.rect.center[0] - (math.cos(math.radians(anglet)) * ipot1))
        #ycoord = (self.target.rect.center[1] - (math.sin(math.radians(anglet)) * ipot1))
        
        #xcoord, ycoord = math.ceil(xcoord), math.ceil(ycoord)
        if self._enmode == -1 : self._enmode = random.randint(0,1)
        if self._enmode == 0 :
            ycoords = range(self.rect.center[1], screenh - (screenh - self.target.rect.top) -50, 50)
            xcoord = self.target.rect.center[0] - random.choice((random.randint(-150, -100), random.randint(100, 150)))# * mult
            if self.rect.center[1] < self.target.rect.center[1] -300 : ycoord = self.rect.center[1] + 20
            else : ycoord = self.rect.center[1]
            
            if xcoord < 0 : xcoord = 0
            if xcoord > screenw : xcoord = screenw
            
            #self.waypoints = []
            #ycoord = self.rect.center[1] + math.sin(anglet) * float(cat1/2)* -1
            #for i in range(len(ycoords)) :
            #    ycoord = ycoords[i]
            #    if i % 2 == 0 : mult = 1
            #    else : mult = -1
            
            #xcoord = self.target.rect.center[0] -10
            if not self.moving :
                self.move((xcoord, ycoord), 7)
                #print (xcoord, ycoord)
            #self.add_move_point(self.rect.center, 8)
            if self._shots >= self._engage_shots :
                self._engage_shots = 0
                self.move(self._position_before_action)
                self._position_before_action = ()
                self._engaging = False
                self._enmode = -1
                
            if not self._attacking : self.attack(self._engage_shots)
            #else : self._engaging = False
            
            #self._engaging = False
            
        else :
            #if not self.moving : 
                #randh = random.randint(self.rect.center[1]+20, self.rect.center[1]+40)
                #points = ((screenw - self.rect.width, randh), (0 + self.rect.width, randh))
                #self.move(random.choice(points), 8)
            ##self.add_move_point(self.rect.center, 8)
            #if self._shots >= self._engage_shots :
                #self._engage_shots = 0
                #self.move(self._position_before_action)
                #self._position_before_action = ()
                #self._engaging = False
                
            #rotate around target
            cat1, cat2 = self.target.rect.center[0] - self.rect.center[0], self.target.rect.center[1] - self.rect.center[1]
            ipot1 = math.sqrt(pow(cat1, 2) + pow(cat2, 2))
            try :
                anglet = math.degrees(math.acos(cat2 / ipot1))
            except ZeroDivisionError :
                anglet = 0.0
                
            increment = 10
                
            if self.target.rect.center[0] <= self.rect.center[0] :
                anglet *= -1
                increment *= -1
                
            
            
            anglet = 180.0 - anglet -90.0 + increment
                
            xcoord = (self.target.rect.center[0] - (math.cos(math.radians(anglet)) * ipot1))
            ycoord = (self.target.rect.center[1] - (math.sin(math.radians(anglet)) * ipot1))
            
            xcoord, ycoord = math.floor(xcoord), math.floor(ycoord)
            #self.add_move_point((xcoord, ycoord), 8)
            if not self.moving : 
                #randh = random.randint(self.rect.center[1]+20, self.rect.center[1]+40)
                #points = ((screenw - self.rect.width, randh), (0 + self.rect.width, randh))
                #self.add_move_point((xcoord, ycoord), 8)
                self.move((xcoord, ycoord), 5)
                pass
            
            if self._shots >= self._engage_shots or not self.completely_onscreen:
                self._engage_shots = 0
                self.move(self._position_before_action)
                self._position_before_action = ()
                self._engaging = False
                self._enmode = -1
                
            if not self._attacking : self.attack(self._engage_shots)
           
        
    def __evade__(self, current_time) :
        
        alienbottom = self.rect.bottom
        
        alienbottomleftx = self.rect.bottomleft[0]
        alienbottomlefty = self.rect.bottomleft[1]
        
        alienbottomrightx = self.rect.bottomright[0]
        alienbottomrighty = self.rect.bottomright[1]
        
        aliencenterx = self.rect.center[0]
        aliencentery = self.rect.center[1]
        
        alienleft = self.rect.left
        alienright = self.rect.right
        
        displaywidth = pygame.display.get_surface().get_rect().width
        
        for sh in self.shotsGroup.sprites() :
            
            evadex = 60
            evadey = 0
            
            
            shotbottom = sh.rect.bottom
            shotmidtopx =  sh.rect.midtop[0]
            shotmidtopy = sh.rect.midtop[1]
            
            #do calculation only if shot in not behind alien
            if alienbottom < shotbottom and (shotbottom - alienbottom) <= 170.0:
                
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
                
                if ((sh.angle >= anglesh1 and sh.angle <= anglesh2) or (sh.angle >= anglesh2 and sh.angle <= anglesh1)) and ipot3 <= 170.0  and ipot3 > 150.0:
                    #diffa = self._angle
                    
                    #if sh.rect.midtop[0] <= self.rect.center[0] :
                    if sh.angle > anglesh3 :
                        mult = 1
                    else :
                        mult = -1
                    
                    if alienleft + evadex * mult < 0 : mult *= -2
                    if alienright + evadex * mult > displaywidth : mult *= -2
                    
                    evadex *= mult
                    
                    newx = alienleft + evadex
                    
                    self.move((self.center[0] + evadex, self.center[1] + evadey), 8)
                    self.attack(1)
                
         
        #old evade, less reliable
        #for sh in self.shotsGroup.sprites() :
        ##sh = self.shotsGroup.sprites()[i]
        #if sh.rect.left <= self.rect.right and sh.rect.right >= self.rect.left and sh.rect.top < (self.rect.bottom + self.rect.height +35) and sh.rect.top > self.rect.bottom :
            #if center[0] < sh.rect.midtop[0] and self.rect.left - 60 > 0 :
                #self.move((center[0] - 60, center[1]), 8)
            #elif center[0] < sh.rect.midtop[0] and not self.rect.left - 60 > 0 :
                #self.move((center[0] + 120, center[1]), 8)
            #elif center[0] >= sh.rect.midtop[0] and self.rect.right + 60 < pygame.display.get_surface().get_rect().width :
                #self.move((center[0] + 60, center[1]), 8)
            #elif center[0] >= sh.rect.midtop[0] and not self.rect.right + 60 < pygame.display.get_surface().get_rect().width :
                #self.move((center[0] - 120, center[1]), 8)
            ##fight back
            #self.attack(1)
            
    def __behave__(self, current_time) :
        
        eng = 0
        
        if self.target.alive() :
            for a in self.containers[0] :
                if a._engaging : eng += 1
            
        if eng < self._max_engaging :
            self.engage()
            return
        
        if self._next_move_down_time == 0 : self._next_move_down_time = current_time + random.choice(range(2000, 5000, 1000))
        if self._next_move_down_time <= current_time :
            self._next_move_down_time = current_time + random.choice(range(2000, 5000, 1000))
            self.move((self.rect.center[0], self.rect.center[1] + 50), 2)
            self.attack(1)
            
    
class alienshot(pygame.sprite.Sprite) :
    hitmask = None
    images = []
    _angle = 0.0
    position = (0,0)
    speed = 18.0
    damage = 20
    reload_time = 200
    
    def __get_angle__(self) :
        return self._angle
    
    angle = property(__get_angle__)
    
    def __init__(self, position, angle, shooter) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.position = position
        self._angle = angle
        self.shooter = shooter
        
        #self.image = pygame.Surface([6, 10])
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        
        
        #pygame.draw.rect(self.image, (255,0,0), self.rect, 0)
        #self.image.set_colorkey((0,0,0))
        
        
        self.orig = self.image
        
        self.image = pygame.transform.rotate(self.orig, self._angle)
        #self.image = self.image.convert_alpha()
        
        self.rect = self.image.get_rect()        
        self.rect.center = (position[0], position[1])
        
        #for i in range(4) :
        #    newimg = pygame.surface.Surface([1,1])
        #    #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
        #    newimg.fill(random.choice([(255,255,255)]))
        #    newx = random.randint(-1 * self.rect.width/2,self.rect.width/2) + self.rect.center[0]
        #    newy = random.randint(-1 * self.rect.height/2,self.rect.height/2)  + self.rect.center[1]
        #    
        #    particle(newimg, (newx, newy), random.randint(self._angle -20, self._angle +20))
        
        self.offsetx = (math.cos(math.radians(self._angle + 90))) * self.speed * -1
        self.offsety = (math.sin(math.radians(self._angle + 90))) * self.speed
        
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
    def update(self, current_time) :
        
        #self.rect.left += self.offsetx
        #self.rect.bottom -= self.offsety
        self.rect = self.rect.move(self.offsetx, self.offsety)
        
        if self.rect.topleft[0] <= 0 or self.rect.topright[0] >= pygame.display.get_surface().get_width() or self.rect.bottom <= 0 or self.rect.top >= pygame.display.get_surface().get_height():
            self.kill()
    
    def compute_hitmask(self) :
        self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
    def explode(self) :
        for i in xrange(4) :
            newimg = pygame.surface.Surface([2,2])
            #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
            newimg.fill(random.choice([(255,100,100)]))
            newx = random.randint(-1 * self.rect.width/2,self.rect.width/2) + self.rect.center[0]
            newy = random.randint(-1 * self.rect.height/2,self.rect.height/2)  + self.rect.center[1]
            
            gameobjects.particle(newimg, (newx, newy), random.randint(self._angle -20 +180, self._angle +21 +180))
        
        self.kill()
        
        

class alienHomingShot(alienshot) :

    images = []
    alienContainers = []
    reload_time = 350
    am_cost = 20
    damage = 35
    angle = 0
    
    def __init__(self, position, angle, shooter, target) :
        alienshot.__init__(self, position, angle, shooter)
        #self.image = self.images[0]
        self.target = target
        self.angle = angle
        
    def update(self, current_time) :
        self.rect = self.rect.move(self.offsetx, self.offsety)
        anglesmall = 360
        
        #self.hitmask = pixelperfect.get_alpha_hitmask(self.image, self.rect)
        
        #target selection by angle
                    

        if self.target :
            cat1, cat2 =  self.rect.center[0] - self.target.rect.center[0], self.target.rect.center[1] - self.rect.center[1]
            ipot = math.sqrt(math.pow(cat1, 2) + math.pow(cat2, 2))
            
            try :
                #if cat2 < 0 : cat1 *= -1
                anglesh1 = math.degrees(math.acos(cat2 / ipot))
            except ZeroDivisionError :
                anglesh1 = 0.0
                    
            if cat1 > 0 :
                anglesh1 *= -1
                        
            if ipot < 300 :
                if anglesh1 < self.angle : self.angle -= 4
                #if anglesh1 < self.angle and not cat2 > 0 : self.angle += 4
                if anglesh1 > self.angle : self.angle += 4
                
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.image = self.image.convert_alpha()
        #self.image.set_colorkey((0,0,0))
        
        self.offsetx = (math.cos(math.radians(self.angle + 90))) * self.speed * -1
        self.offsety = (math.sin(math.radians(self.angle + 90))) * self.speed
        
        radius = random.randrange(1, 4, 1)
        surf = pygame.surface.Surface((radius*3, radius*3))
        smokecolor = random.choice(((200,200,200), (100,100,100), (255,255,255)))
        pygame.draw.circle(surf, (200,200,200), surf.get_rect().center, radius, 0)
        surf.set_colorkey((0,0,0))

        pangle = random.choice((-10 -180 + self.angle, 10 -180 + self.angle + 5))
        
        gameobjects.particle(surf, self.rect.center, pangle)
        
        if self.rect.topleft[0] <= 0 or self.rect.topright[0] >= pygame.display.get_surface().get_width() or self.rect.top <= 0 :
            self.kill()

        