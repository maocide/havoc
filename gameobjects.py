import pygame, sys, os, math, random, imagemanipulation, pixelperfect, libxml2
from pygame.locals import *
from aliens import *
from player import *
from text import *
import version

class gameobject() :
    aliens = []
    coords_aliens = []
    player = None
    level = None
    
    tpress = None
    tdestroyed = None
    tover = None
    
    _screen = None
    
    _new_wave_time = 0
    _new_level_time = 0
    _death_time = 0
    
    def __init__(self, l = 1) :
        self._screen = pygame.display.get_surface()
        
        self._screenrect = screenrect = self._screen.get_rect()
        h = screenrect.height / 2
        
        
        self._all = pygame.sprite.Group()
        
        self._playerGroup = pygame.sprite.Group()
        self._thrustGroup = pygame.sprite.Group()
        self._shotsGroup = pygame.sprite.Group()
        self._particleGroup = pygame.sprite.Group()
        self._alienGroup = pygame.sprite.Group()
        self._alienshotsGroup = pygame.sprite.Group()
        self._backgroundTileGroup = pygame.sprite.Group()
        self._starsTileGroup = pygame.sprite.Group()
        self._textLineGroup = pygame.sprite.Group()
        self._balloonGroup = pygame.sprite.Group()
        self._meterGroup = pygame.sprite.Group()
        self._starsGroup = pygame.sprite.Group()
        
        spawnGroup = pygame.sprite.Group()
        
        #assign default groups to each sprite class
        ship.containers = self._playerGroup, self._all
        thrust.containers = self._thrustGroup
        shot.containers = self._shotsGroup, self._all
        flare.containers = self._all
        alienshot.containers = self._alienshotsGroup, self._all
        particle.containers = self._particleGroup, self._all
        explosion.containers = self._particleGroup, self._all
        reddevil.containers = self._alienGroup, self._all
        reddevil.shotsGroup = self._shotsGroup
        backgroundTile.containers = self._backgroundTileGroup
        starsTile.containers = self._starsTileGroup
        star.containers = self._starsGroup
        textLine.containers = self._textLineGroup
        balloon.containers = self._balloonGroup
        meter.containers = self._meterGroup
        homingShot.alienContainers = self._alienGroup
        magneticShot.alienContainers = self._alienGroup
        
        self.__load__()
        
        #spawn.containers = self._spawnGroup, self._all
        
        
        self.player = ship((self._screenrect.width / 2, self._screenrect.height - self._screenrect.height/8))
        self.shotsGroup = self._shotsGroup
        self.player.add_weapon(2)
        self.player.add_weapon(3)
        self.player.add_weapon(4)
        self.player.rest = 2
        
        self.m1 = meter((self._screenrect.width -300,  80), self.player, 'hp', 'HULL', (255, 0, 50), os.path.join('data', 'bitlow.ttf'), 14)
        self.m2 = meter((self._screenrect.width -355, 100), self.player, 'am', 'ANTIMATTER', (50, 0, 255), os.path.join('data', 'bitlow.ttf'), 14)
        self.notifier = notifier((self.m1.rect.topleft[0],self._screenrect.height -100), '')

        self._bg = background()
        self._bg.speed = 3.0
        
        t1 = text(version.name + ' ' + version.ver, (200,100), 20, (255,255,255), (0,0,0),os.path.join('data', 'Backslash.ttf'), False, TFX_STRETCH)
        t1.topleft = (0,self._screenrect.height-t1.rect.height)
        
        self.level = level(1)
        
        
    def update(self, current_time) :
        #displace_aliens = self.displace_aliens
        engaging = []
        attacking = []
        moving = []
        idle = []
        
        keyPressed = pygame.key.get_pressed()
        
        for alien in self.aliens :
            ##alien = aliencoords[1]
            #if alien.engaging : engaging.append(alien)
            #if alien.attacking and not alien.engaging : attacking .append(alien)
            #if alien.moving and not alien.attacking : moving.append(alien)
            #if not alien.moving and not alien.attacking and not alien.engaging : idle.append(alien)
            if not alien.alive() : self.aliens.remove(alien)
        
        self.notifier.update(pygame.time.get_ticks())
        
        if not self.player.alive() and self._death_time == 0 and self.player.rest > 0 :
            self.tdestroyed = text('Destroyed!', (self._screenrect.width/2,self._screenrect.height/2), 40, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_STRETCH)
            self._death_time = current_time + 3000
            
        if self._death_time != 0 and self._death_time <= current_time and self.player.rest > 0 and (type(self.tpress) == type(None) or not self.tpress.alive()) :
            self.tpress = text('Press fire to respawn', (self._screenrect.width/2,self._screenrect.height/2 + 20), 25, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_STRETCH)
            
        if keyPressed[K_SPACE] and not self.player.alive() and self.player.rest > 0 and self._death_time != 0 and self._death_time <= current_time :
            self.player = ship((self._screenrect.width / 2, self._screenrect.height - self._screenrect.height/8))
            self.m1.obj = self.player
            self.m2.obj = self.player
            self.tdestroyed.fadeout = True
            self.tpress.fadeout = True
            for alienc in self.aliens :
                alienc.target = self.player
                alienc.move(alienc._startposition, 8)
                
        if not self.player.alive() and len(self.aliens) > 0 :
            #aliens_to_hide = displace_aliens
            for ah in self.aliens :
                #ah = ahc[1]
                ah.go_offscreen()
                
        if self.player.rest < 0 and not self.player.alive() and (type(self.tover) == type(None) or not self.tover.alive()) :
            self.tdestroyed = text('Destroyed!', (self._screenrect.width/2,self._screenrect.height/2 -30), 40, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_STRETCH, 3000)
            self.tover = text('Game Over', (self._screenrect.width/2,self._screenrect.height/2), 50, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_STRETCH)
                
        if len(self.aliens) == 0 :
            if self._new_wave_time == 0 :
                if self.level.waveno == -1 :
                    t1 = text(self.level.title, (self._screenrect.width/2,self._screenrect.height/2), 35, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_FADE, 6000)
                    t2 = text(self.level.subtitle, (self._screenrect.width/2,self._screenrect.height/2 + 40), 20, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_FADE, 6000)
                    self._new_wave_time = current_time + 6000
                elif self.level.waveno < self.level.wavecount-1 :
                    #t1 = text(("Wave %s annihilated\nmore aliens incoming" % (self.level.waveno)), (self._screenrect.width/2,self._screenrect.height/2), 25, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_FADE, 3000)
                    self._new_wave_time = current_time + 100
                elif self.level.endgame :
                    pass
                else :
                    self.level = level(self.level.levelno+1)
                    t1 = text(self.level.title, (self._screenrect.width/2,self._screenrect.height/2), 35, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_FADE, 6000)
                    t2 = text(self.level.subtitle, (self._screenrect.width/2,self._screenrect.height/2 + 40), 20, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_FADE, 6000)
                    #t1 = text("Level complete" , (self._screenrect.width/2,self._screenrect.height/2), 25, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_FADE, 3000)
                    self._new_wave_time = current_time + 6000
                
            
            if self._new_wave_time <= current_time :
                #(self, content, pos = (0,0), size = 10, color = (255,255,255), colorkey = (0,0,0), f = None, justify = False, effect = TFX_NONE, expire = 0) :
                self._new_wave_time = 0
                self.__startwave__()
            
        self.__collisiondetect__()
        
        self._bg.update(pygame.time.get_ticks())
        self._starsGroup.update(pygame.time.get_ticks())
        self._thrustGroup.update(pygame.time.get_ticks())
        self._all.update(pygame.time.get_ticks())
        self._balloonGroup.update(pygame.time.get_ticks())
        self._textLineGroup.update(pygame.time.get_ticks())
        self._meterGroup.update(pygame.time.get_ticks())
        
    def draw(self) :
        self._backgroundTileGroup.draw(self._screen)
        self._starsGroup.draw(self._screen)
        #starsTileGroup.draw(screen)
        self._thrustGroup.draw(self._screen)
        self._all.draw(self._screen)
        self._balloonGroup.draw(self._screen)
        self._meterGroup.draw(self._screen)
        self._textLineGroup.draw(self._screen)
        
    def __collisiondetect__(self) :
        #collisions between player shots and aliens
        shots_aliens = pygame.sprite.groupcollide(self._shotsGroup, self._alienGroup, 0, 0)
        for cshot in shots_aliens.keys() :
            if len(shots_aliens) > 0 :
                #cshot.compute_hitmask()
                for calien in shots_aliens[cshot] :
                    #calien.compute_hitmask()
                    if pixelperfect.check_collision(calien, cshot) :
                        calien.hit(cshot)
                        self.notifier.notify("HIT!")
                        cshot.explode()
                        if not calien.alive() : self.notifier.notify("DESTROYED!")
        
        #collisions between aliens shots and player
        alienshots_player = pygame.sprite.groupcollide(self._alienshotsGroup, self._playerGroup, 0, 0)
        for calienshot in alienshots_player.keys() :
            if len(alienshots_player) > 0 :
                #calienshot.compute_hitmask()
                for player in alienshots_player[calienshot] :
                    #player.compute_hitmask()
                    if pixelperfect.check_collision(player, calienshot) :
                        player.hit(calienshot)
                        self.notifier.notify("DAMAGE!")
                        calienshot.explode()
        
        alienshots_shots = pygame.sprite.groupcollide(self._alienshotsGroup, self._shotsGroup, 0, 0)
        for calienshot in alienshots_shots.keys() :
            if len(alienshots_shots) > 0 :
                #calienshot.compute_hitmask()
                for cshot in alienshots_shots[calienshot] :
                    #cshot.compute_hitmask()
                    if pixelperfect.check_collision(cshot, calienshot) :
                        cshot.explode()
                        calienshot.explode()
                        
        #make alien move when they collide with each others
        for calien in self._alienGroup.sprites() :
            caliens = pygame.sprite.spritecollide(calien, self._alienGroup, 0)
            if len(caliens) > 1 :
                caliena = calien
                for calienb in caliens :
                    #calienb = caliens[1]
                    if not caliena.rect.center == calienb.rect.center and not caliena.moving  and not calienb.moving:
                        if caliena.rect.center[0] > calienb.rect.center[0] :
                            calienb.move((calienb.rect.center[0]-30,calienb.rect.center[1]))
                            caliena.move((caliena.rect.center[0]+30,caliena.rect.center[1]))
                        else : 
                            caliena.move((caliena.rect.center[0]-30,caliena.rect.center[1]))
                            calienb.move((calienb.rect.center[0]+30,calienb.rect.center[1]))
                            
                                
    def __load__(self) :
        #t1 = text("Loading", (30,30), 25, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_FADE)
        #t1.topleft = (5,5)
        #self.draw()
        tm1 = pygame.time.get_ticks()
        
        ship.images.append(pygame.image.load(os.path.join('data', 'spaceship.png')).convert_alpha())
        reddevil.images.append(pygame.image.load(os.path.join('data', 'reddevil.png')).convert_alpha())
        #reddevil.images.append(pygame.image.load(os.path.join('data', 'alien1b.png')).convert_alpha())
        #reddevil.images.append(pygame.image.load(os.path.join('data', 'alien1c.png')).convert_alpha())
        
        star.images.append(pygame.image.load(os.path.join('data', 'star1.png')).convert_alpha())
        star.images.append(pygame.image.load(os.path.join('data', 'star2.png')).convert_alpha())
        star.images.append(pygame.image.load(os.path.join('data', 'star3.png')).convert_alpha())
        star.images.append(pygame.image.load(os.path.join('data', 'star4.png')).convert_alpha())
        star.images.append(pygame.image.load(os.path.join('data', 'star5.png')).convert_alpha())
        
        shot.images.append(pygame.image.load(os.path.join('data', 'blue_laser.png')).convert_alpha())
        homingShot.images.append(pygame.image.load(os.path.join('data', 'missile.png')).convert_alpha())
        chainShot.images.append(pygame.image.load(os.path.join('data', 'chainshot.png')).convert_alpha())
        alienshot.images.append(pygame.transform.flip(pygame.image.load(os.path.join('data', 'red_laser.png')).convert_alpha(), False, True))
        alienHomingShot.images.append(pygame.transform.flip(pygame.image.load(os.path.join('data', 'missile.png')).convert_alpha(), False, True))
        
        backgroundTile.images.append(pygame.image.load(os.path.join('data', 'skytile_1024_768.png')).convert())
        starsTile.images.append(pygame.image.load(os.path.join('data', 'starfield.png')).convert_alpha())
        balloon.images.append(pygame.image.load(os.path.join('data', 'balloon_big.png')).convert_alpha())

        #self.__load__()
        
        t1 = text("loading time : " + str(pygame.time.get_ticks() - tm1), (30,60), 25, (255,255,255), (0,0,0), os.path.join('data', 'Backslash.ttf'), False, TFX_FADE, 3000)
        t1.topleft = (5,20)
        t1.fade_out = True
        
    def __startwave__(self) :
        
        #move aliens in postion
        if len(self.aliens) > 0 :
            for alien in self.aliens :
                alien.move(alien._startposition, 8)
                
        else :
            #load new wave/level entities and initialize and place all the aliens offscreen
            if self.level.nextwave() :
                for adict in self.level.wave :
                    exec('aclass = ' + adict['name'])
                    pos = adict['pos']
                    hurtquotes = adict['hurtquotes']
                    killquotes = adict['killquotes']
                    
                    for i in xrange(len(hurtquotes)) :
                        hurtquotes[i] = hurtquotes[i].replace("\\n", '\n');
                        
                    for i in xrange(len(killquotes)) :
                        killquotes[i] = killquotes[i].replace("\\n", '\n');
                    
                    self.aliens.append(aclass(pos, self.player, self.shotsGroup))
                    self.aliens[len(self.aliens)-1].hurtquotes = hurtquotes
                    self.aliens[len(self.aliens)-1].killquotes = killquotes
                    self.aliens[len(self.aliens)-1].move(self.aliens[len(self.aliens)-1]._startposition, 8)

                    
class level(object) :
    
    title = None
    subtitle = None
    waves = []
    levelno = 0
    endgame = False
    _waves = []
    _waveno = -1
    
    def __get_waveno__(self) :
        return self._waveno
    
    def __get_wavecount__(self) :
        return len(self._waves)

    
    waveno = property(__get_waveno__)
    wavecount = property(__get_wavecount__)
    
    
    def __init__(self, levelno) :
        self.levelno = levelno
        quotes = dict()
        self.waves= []
        self._waveno = -1
        
        srect = pygame.display.get_surface().get_rect()
        
        doc = libxml2.parseFile(os.path.join('data', 'game.xml'))
        
        if not len(doc.xpathEval('//game/levels/level[@id=%s]' % levelno)) > 0 :
            self.endgame = True
            return
        
        titlenode = doc.xpathEval('//game/levels/level[@id=%s]/title[1]' % levelno)[0]
        subtitlenode = doc.xpathEval('//game/levels/level[@id=%s]/subtitle[1]' % levelno)[0]
        
        self.title = titlenode.get_content()
        self.subtitle = subtitlenode.get_content()
        
        #load each group of quotes in an indexed dictionary
        quotenodes = doc.xpathEval('//game/quotes/group/*')
        for quotenode in quotenodes :
            groupid = int(quotenode.parent.prop("id"), 10)
            if quotes.keys().count(groupid) > 0 :
                quotes[groupid].append(quotenode.get_content())
            else :
                quotes[groupid] = [quotenode.get_content()]
                
        
        wavenodes = doc.xpathEval('//game/levels/level[@id=%s]/waves/*' % levelno)
        
        #a waves is a list containing a list of dictionaries for each entity
        for wavenode in wavenodes :
            
            entities = []
            
            #get all the entitynodes under a wavenode
            for entitynode in wavenode.xpathEval("./*") :
                ent = dict()
                
                ent['name'] = entitynode.get_name()
                
                pos = entitynode.prop("position").split(",")
                if pos[0].isalnum() and pos[1].isalnum() :
                    pos = (int(pos[0], 10), int(pos[1], 10))
                    1#024:100=x:particle
                    pos = ((srect.width*pos[0])/100, (srect.height*pos[1])/100)
                    
                    
                else : pos = (0,0)
                ent['pos'] = pos
                
                if entitynode.prop("hurtquotes").isalnum() :
                    ent['hurtquotes'] = quotes[int(entitynode.prop("hurtquotes"),10)]
                if entitynode.prop("killquotes").isalnum() :
                    ent['killquotes'] = quotes[int(entitynode.prop("killquotes"),10)]
                    
                entities.append(ent)
                
            self.waves.append(entities)
        
        self._waves = self.waves
        
    def nextwave(self) :
        self._waveno += 1
        if(len(self._waves) > self._waveno) :
            self.wave = self._waves[self._waveno]
            return True
        else :
            return False
    
    
class explosion (pygame.sprite.Sprite) :
    endtime = 0
    duration = 0
    next_update = 0
    alpha = 0
    
    def __init__(self, img, center, colors) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        
        self.orig = img
        self.rect = img.get_rect()
        self.rect.center = center
        origrect = self.rect
        origrect.center = center
        
        chop_rect = (0,0,origrect.width/2,origrect.height/2)
        surface = pygame.transform.chop(self.orig, chop_rect)
        surface = surface.convert_alpha()
        surface.set_colorkey((0,0,0))
        particle(surface, self.rect.center)
        
        chop_rect = (origrect.width/2,0,origrect.width/2,origrect.height/2)
        surface = pygame.transform.chop(self.orig, chop_rect)
        surface = surface.convert_alpha()
        surface.set_colorkey((0,0,0))
        particle(surface, self.rect.center)
        
        chop_rect = (origrect.width/2,origrect.height/2,origrect.width/2,origrect.height/2)
        surface = pygame.transform.chop(self.orig, chop_rect)
        surface = surface.convert_alpha()
        surface.set_colorkey((0,0,0))
        particle(surface, self.rect.center)
        
        chop_rect = (0,origrect.height/2,origrect.width/2,origrect.height/2)
        surface = pygame.transform.chop(self.orig, chop_rect)
        surface = surface.convert_alpha()
        surface.set_colorkey((0,0,0))
        particle(surface, self.rect.center)
        
        for i in xrange(100) :
            newimg = pygame.surface.Surface([2,2])
            #newimg.set_at((0,0),random.choice([(255,100,0), (240,49,29), (255,217,0), (230,30,0)]))
            newimg.fill(random.choice(colors))
            newx = random.randint(-1 * self.rect.width/2,self.rect.width/2) + self.rect.center[0]
            newy = random.randint(-1 * self.rect.height/2,self.rect.height/2)  + self.rect.center[1]
            
            particle(newimg, (newx, newy))
        
        self.kill()
        
        
    def update(self, current_time) :
        self.kill()

class particle(pygame.sprite.Sprite) :
    angle = None
    position = (0,0)
    lifetime = 1000
    death = 0
    alpha = 255
    _angle_before = 999.0
    
    def __init__(self, img, position, angle = -999, fade = True) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = img.convert()
        self.orig = img.convert()
        
        self.position = position
        random.seed()
        if angle == -999 : self.angle = random.randint(0, 360)
        else : self.angle = angle
        
        self.rotate_speed = random.randint(-10, 10)

        #else : self.angle = angle
        
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        
        self.speed = speed = random.randrange(2, 10)
        self.offsetx = (math.cos(math.radians(self.angle + 90))) * self.speed
        self.offsety = (math.sin(math.radians(self.angle + 90))) * self.speed
        
    def update(self, current_time) :        
        
        
        
        center = self.rect.center
        
        self.alpha -= 3
        
        if self.rect.width > 2 or self.rect.height > 2 :
            self.angle += self.rotate_speed
            if self.angle >= 361 : self.angle = 1            
            
            if self._angle_before != self.angle :
                self.image = pygame.transform.rotate(self.orig, self.angle)
                self._angle_before = self.angle
            self.rect = self.image.get_rect()
            self.rect.center = center
        
        if self.alpha >= 0 : self.image.set_alpha(self.alpha)
        
        
        
        self.rect.left += self.offsetx
        self.rect.bottom -= self.offsety
        
        #print(self.rect.center, self.rect.left, self.rect.bottom)
        
        if self.rect.topright[0] <= 0 or self.rect.topleft[0] >= pygame.display.get_surface().get_width() or self.rect.bottom <= 0 or self.rect.top >= pygame.display.get_surface().get_height() or self.alpha <= 0 :
            self.kill()
            
            del self
            return
        
        
class flare(pygame.sprite.Sprite) :
    lifetime = 50
    death = 0
    containers =[]
    def __init__(self, position) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        #self.image = pygame.Surface([14, 14])
        
        #for pt in self.ship :
        #    self.image.set_at(pt, color)
        
        self.image = pygame.image.load(os.path.join('data', 'flare.png')).convert_alpha()
        #self.image = pygame.surface.Surface.convert(self.image)
        #self.image = pygame.transform.scale2x(self.image)
        #self.image = pygame.transform.scale2x(self.image)
        
        
        #self.orig = self.image
        
        self.rect = self.image.get_rect()
        self.rect.center = (position[0])
        
    def update(self, current_time) :
        pass
        #if not self.death > 0 : self.death = current_time + 50
        #if self.death <= current_time : self.kill()
        
class balloon(pygame.sprite.Sprite) :
    
    images = []
    containers = []
    txt = None
    _ready = False
    _grow = True
    _shrink = False
    _death_time = 0
    _duration = 0
    
    
    def __init__(self, content, speaker, font = None, size = 10, duration = 5000) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self._duration = duration
        
        self.speaker = speaker
        displayrect = pygame.display.get_surface().get_rect()
        if self.speaker.rect.center[0] > displayrect.center[0] : self.left = True
        else : self.left = False
        
        self.image = self.images[0]
        if self.left : self.image = pygame.transform.flip(self.image, True, False)
        self.orig = self.image
        self.rect = self.image.get_rect()
        
        self.txt = text(content, speaker.rect.bottomleft, size, (0,0,0), (255,255,255), font, TFX_FADE)
        self.txt.alpha = 0
        
        if self.txt.width > self.txt.height :
            self.width = self.txt.width + self.txt.width / 3
            #self.height : self.rect.height = self.width : self.rect.width
            
            self.height = (self.rect.height * self.width) / self.rect.width
            #self.width += self.width*3/7
            
        else :
            self.height = self.txt.height
            #self.width : self.rect.width = self.height : self.rect.height
            
            self.width = (self.rect.width * self.height) / self.rect.height
            #self.height += self.height*4/7
            
        
        self.widtht = 5
        self.heightt = 5        
        
        self.image = pygame.transform.scale(self.image, (self.widtht, self.heightt))
        self.rect = self.image.get_rect()
            
        if self.left :
            self.rect.bottomright = self.speaker.rect.topleft
        else :
            self.rect.bottomleft = self.speaker.rect.topright
        self.txt.center = (self.rect.center[0], self.rect.center[1] - self.rect.height/14)
        
        self._grow = True
        
    def update(self, current_time) :
            
        if self.heightt < self.height and self._grow : self.heightt += self.height /20 +2
        if self.widtht < self.width and self._grow : self.widtht += self.width /20 +2
        
        if self.heightt > 0 and self._shrink : self.heightt -= self.height /20
        if self.widtht > 0 and self._shrink : self.widtht -= self.width /20
        
        if self.heightt >= self.height and self.widtht >= self.width and self._grow :
            #for l in self.txt.lines : l.fadein = True
            self.txt.fadein = True
            self._grow = False
            self._death_time = current_time + self._duration
            self.width, self.height = self.widtht, self.heightt
        
        if self.width != self.widtht or self.heightt != self.height :
            if self.heightt < 0 or self.widtht < 0 :
                self.kill()
                return
            self.image = pygame.transform.scale(self.orig, (self.widtht, self.heightt))
            self.rect = self.image.get_rect()
            
        if self.left :
            self.rect.bottomright = self.speaker.rect.topleft
        else :
            self.rect.bottomleft = self.speaker.rect.topright
            
        #self.image.fill((222,222,222))
        
        #time to disappear, start shrinkin'
        if (self._death_time <= current_time and self._death_time != 0 and not self._shrink) or not self.speaker.alive():
            self.txt.kill()
            self._shrink = True
            self._grow = False
        
        #if not self.speaker : self.kill
        self.txt.center = (self.rect.center[0], self.rect.center[1] - self.rect.height/14)
        #self.image.fill((255,255,255))
        #self.txt.draw();
        
class hud(pygame.sprite.Sprite) :
    
    containers = []
    images = []
    
    def __init__(self, pos) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        #self.image = pygame.surface.Surface((2,2))
        #self.rect = self.image.get_rect()
        #self.rect.center = pos
        
        #pygame.draw.rect(self.image, (0, 100, 255), self.rect, 0)
        
        #self.image = self.images[0]
        self.width = 350
        self.height = 200
        #self.orig = self.image
        #self.image = pygame.transform.scale(self.image, (1, 1))
        #self.rect = self.image.get_rect()
        #self.rect.center = pos
        self.pos = pos
        
    def update(self, current_time) :
        
        #if self.rect.width < self.width :#or self.rect.height < self.height :
            ##self.image.fill((0,0,0,0))
            #self.image = pygame.transform.scale(self.orig, (self.rect.width + 2, 1)) #self.rect.height + 1
            #self.rect = self.image.get_rect()
            ##pygame.draw.rect(self.image, (0, 100, 255, 0), self.rect, 1)
            #self.rect.center = self.pos
        #elif self.rect.height < self.height :
            #self.image = pygame.transform.scale(self.orig, (self.rect.width, self.rect.height + 2)) #self.rect.height + 1
            #self.rect = self.image.get_rect()
            ##pygame.draw.rect(self.image, (0, 100, 255, 0), self.rect, 1)
            #self.rect.center = self.pos
        
        pass
    

class meter(pygame.sprite.Sprite) :
    
    containers = []
    _min = 0
    _max = 100
    _obj = None
    _caption = ""
    
    def __get_obj__(self) :
        return self._obj
    
    def __set_obj__(self, value) :
        self._obj = value
        
    def __get_caption__(self) :
        return self._caption
    
    def __set_caption__(self, value) :
        self._caption = value
        self._txt.kill()
        self._txt = text(self._caption, self._pos, self._fs, self._col, (0,0,0), self._f)
        self._txt.topleft = self._pos
        
    obj = property(__get_obj__, __set_obj__)
    caption = property(__get_caption__, __set_caption__)
    
    def __init__(self, pos, obj, property, caption, col = (255,255,255), f = None, fs = 12, max = 100, size = 200) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        #self._txt = text(self._caption, pos, s, (255,255,255), (0,0,0), f)
        self._txt = text(caption, pos, fs, col, (0,0,0), f)
        self._txt.topleft = pos
        self._f = f
        self._fs = fs
        
        th = self._txt.lineheight
        
        self._mh = th/2
        self._mw = size
        self._mvp = pos[1] + (th - self._mh) / 2
        
        self._col = col
        self._pos = pos
        self._max = max
        self._obj = obj
        self._caption = caption
        self._property = property
        
        #max : val = mw : x
        #print 'self._val = '.join(('self._obj.', self._property))
        exec('self._val = ' + 'self._obj.' + self._property)
        w = (self._val * self._mw) / self._max
        self._tranw = 1
        self.image = pygame.surface.Surface((self._tranw, self._mh))
        self.image.fill(self._col)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self._txt._lines[0][0].rect.width + self._pos[0] + self._mh, self._mvp)
        
        
    def update(self, current_time) :
        
        #self._txt = text(self._caption, self._pos, 12, (255,255,255), (0,0,0))
        self._txt.topleft = self._pos
        
        exec('self._val = self._obj.%s' % self._property)
        w = (self._val * self._mw) / self._max
        if self._tranw < self._mw and self._tranw < w : self._tranw += 2
        if self._tranw > 0 and self._tranw > w : self._tranw -= 2
        if self._tranw > 0 :
            self.image = pygame.surface.Surface((self._tranw, self._mh))
            self.image.fill(self._col)
        else :
            self.image = pygame.surface.Surface((1, 1))
        #if self._tranw > 0 :
        #    for i in xrange(self.image.get_rect().width) :
        #        pygame.draw.line(self.image, (self._col[0] - i,self._col[1] - i, self._col[2] - i), (i,0), (i,self._mh-1))
        
        self.rect.topleft = (self._txt._lines[0][0].rect.width + self._pos[0] + self._mh, self._mvp)
        
class notifier(object) :
    
    _quotes = []
    
    def __init__(self, pos, quote, timeout = 2000) :
        #deathtime = pygame.time.get_ticks() + timeout
        self._pos = pos
        self._quotes.append(text(quote, pos, 15, (255,255,255), (0,0,0), os.path.join('data', 'bitlow.ttf'), False, TFX_STRETCH, timeout))
        self._quotes[0].topleft = pos
        
        #this will refix textline positions, since textlines grow and change size each second
        j = 0
        for i in xrange(len(self._quotes)-1, 0, -1) :
            self._quotes[i][0].center = (self._quotes[i][0].center[0], self._pos[1]-20*j)#self._quotes[i][0].topleft[1]-20)#self._quotes[len(self._quotes)-1][0].height-4)
            j += 1
            
            
    def notify(self, quote, timeout = 2000) :
        #txt = text(quote, (0,0))
        #h = txt.lineheight
        #txt.kill()
        #del txt

        #realheight = self._quotes[0][0].orig.get_rect().height
        
        
        #position old quotes
        for i in xrange(len(self._quotes)) :
            self._quotes[i].center = (self._quotes[i].center[0], self._quotes[i].center[1]-20)#self._quotes[i][0].topleft[1]-20)#self._quotes[len(self._quotes)-1][0].height-4)        
        
        #deathtime = pygame.time.get_ticks() + timeout
        self._quotes.append(text(quote, self._pos, 15, (255,255,255), (0,0,0), os.path.join('data', 'bitlow.ttf'), False, TFX_STRETCH, timeout))
        self._quotes[len(self._quotes)-1].topleft = self._pos
        
        #this will refix textline positions, since textlines grow and change size each second
        j = 0
        for i in xrange(len(self._quotes)-1, 0, -1) :
            self._quotes[i].center = (self._quotes[i].center[0], self._pos[1]-20*j)#self._quotes[i][0].topleft[1]-20)#self._quotes[len(self._quotes)-1][0].height-4)
            j += 1
        
        #self._quotes[0][0].topleft = (self._pos[0], self._pos[1])
        
        
    def update(self, current_time) :
        #for q in self._quotes :
        #    if q[1] <= current_time :
        #        if q[0].alpha == 0 : self._quotes.remove(q)
        #        q[0].fadeout = True
        
        #this will refix textline positions, since textlines grow and change size each second
        j = 0
        for i in xrange(len(self._quotes)-1, 0, -1) :
            self._quotes[i].center = (self._quotes[i].center[0], self._pos[1]-20*j)#self._quotes[i][0].topleft[1]-20)#self._quotes[len(self._quotes)-1][0].height-4)
            j += 1
    
class spawn(pygame.sprite.Sprite) :
    
    containers = []
    orig = None
    anim = 0.0
    factor = 0.2
    quantity = 2.0
    alpha = 50.0
    center = (0,0)
    
    def __init__(self, position, obj, imgn = 0) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        mycode = 'self.orig = .images[%s]' % str(imgn)
        exec(mycode)
        self.center = position
        
        self.orig = self.orig.convert()
        self.image = self.orig
        
        self.rect = self.orig.get_rect()
        self.rect.center = self.center
        origrect = self.rect
        origrect.center = self.center
        #self.orig = self.orig.convert()
        
        chop_rect = (0,0,origrect.width/2,origrect.height/2)
        surface = pygame.transform.chop(self.orig, chop_rect)
        surface.set_colorkey((0,0,0))
        #particle(surface, self.rect.center)
        
        chop_rect = (origrect.width/2,0,origrect.width/2,origrect.height/2)
        surface = pygame.transform.chop(self.orig, chop_rect)
        surface.set_colorkey((0,0,0))
        #particle(surface, self.rect.center)
        
        chop_rect = (origrect.width/2,origrect.height/2,origrect.width/2,origrect.height/2)
        surface = pygame.transform.chop(self.orig, chop_rect)
        surface.set_colorkey((0,0,0))
        #particle(surface, self.rect.center)
        
        chop_rect = (0,origrect.height/2,origrect.width/2,origrect.height/2)
        surface = pygame.transform.chop(self.orig, chop_rect)
        surface.set_colorkey((0,0,0))
        #particle(surface, self.rect.center)
        
    def update(self, current_time) :
        xblocks = range(0, self.rect.width, 2)
        yblocks = range(0, self.rect.height, 2)
        
        img = self.orig
        
        img.set_alpha(self.alpha)
        #self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
        
        self.anim = self.anim + 0.2
        for x in xblocks:
            xpos = (x + (math.sin(self.anim + x * self.factor) * self.quantity)) #+ 2
            for y in yblocks:
                ypos = (y + (math.sin(self.anim + y * self.factor) * self.quantity)) #+ 2
                pygame.display.get_surface().blit(img, (x+self.rect.left, y+self.rect.top), (xpos, ypos, 2, 2))
                
        if self.alpha < 255.0 or self.quantity > 0.0 :
            self.alpha += 2
            if self.quantity > 0.0 :
                self.quantity -= 0.02
            else : self.quantity = 0.0
        else :
            #print self.quantity
            #reddevil(self.center)
            self.kill()
            #self.alpha -= 5
            
class star(pygame.sprite.Sprite) :

    containers = []
    images = []
    _speed = 0
    
    def __init__(self, pos = None) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()
        
        self._speed = random.choice(range(2,6))
        drect = pygame.display.get_surface().get_rect();
        
        self._sw, self._sh = drect.width, drect.height
        
        if pos == None :
            pos = (random.choice(range(self._sw)), 0 - self.rect.height)
        
        self.rect.midbottom = pos
        self._pos = pos
        
    def update(self, current_time) :
        
        #self.rect.midbottom = (self._pos[0], self._pos[1] + self._speed)
        self.rect.top += self._speed
        #self.rect.move_ip(self._pos[0], self._pos[1] + self._speed)
        if self.rect.top > self._sh :
            self.kill()
            del self
            

class background(object) :
    
    containers = []
    tiles = [None, None, None, None]
    next_update_time = 0
    next_star_time = 0
    update_occurrency = 10
    
    _speed = 2.0
    _accel = 0.1
    _new_speed = 2.0
    
    def __get_speed__(self) :
        return self._speed

    def __set_speed__(self, value) :
        self._new_speed = value
        
    speed = property(__get_speed__, __set_speed__)
        
    def __init__(self) :
        """ """
        self.tiles[0] = None
        self.tiles[1] = None
        self.tiles[2] = None
        #self.tiles[3] = None
        
        self.tiles[0] = backgroundTile(pygame.display.get_surface().get_rect().bottom - backgroundTile.images[0].get_rect().bottom, 0)
        #self.tiles[2] = starsTile(0, 1)
        self._stars = []
        pass
    def update(self, current_time) :
        if current_time >= self.next_update_time :
            
            if self.tiles[0].rect.top > pygame.display.get_surface().get_rect().bottom :
                self.tiles[0].kill()
                self.tiles[0] = self.tiles[1]
                self.tiles[1] = None
                
            #if self.tiles[2].rect.top > pygame.display.get_surface().get_rect().bottom :
                #self.tiles[2].kill()
                #self.tiles[2] = self.tiles[3]
                #self.tiles[3] = None
                
            if self.tiles[0].rect.top < pygame.display.get_surface().get_rect().bottom and self.tiles[0].rect.top > 0 :
                if not isinstance(self.tiles[1], backgroundTile) :
                    self.tiles[1] = backgroundTile(self.tiles[0].rect.top - self.tiles[0].rect.height, 0)
                    self.tiles[1].rect.bottom = self.tiles[0].rect.top - 1
                    
            #if self.tiles[2].rect.top < pygame.display.get_surface().get_rect().bottom and self.tiles[2].rect.top > 0 :
                #if not isinstance(self.tiles[3], starsTile) :
                    #self.tiles[3] = starsTile(self.tiles[2].rect.top - self.tiles[2].rect.height, 1)
                    #self.tiles[3].rect.bottom = self.tiles[2].rect.top - 1
                
            self.tiles[0].movedown(math.ceil(self._speed))
            if isinstance(self.tiles[1], backgroundTile) :
                #self.tiles[1].movedown(self._speed)
                self.tiles[1].rect.bottom = self.tiles[0].rect.top# - 1
                pass
                #pygame.display.get_surface().blit(self.tiles[1].image, self.tiles[1].rect)
            
            #pygame.display.get_surface().blit(self.tiles[0].image, self.tiles[0].rect)
            
            
            #self.tiles[2].movedown(self._speed + 2)
            #if isinstance(self.tiles[3], starsTile) :
                ##self.tiles[1].movedown(self._speed)
                #self.tiles[3].rect.bottom = self.tiles[2].rect.top - 1
                #pass
                ##pygame.display.get_surface().blit(self.tiles[1].image, self.tiles[1].rect)
            
            #pygame.display.get_surface().blit(self.tiles[2].image, self.tiles[2].rect)
            
            if self._speed < self._new_speed :
                self._speed += self._accel
                
            if self._speed > self._new_speed :
                self._speed -= self._accel
            
            #for i in xrange(len(self._stars)-1) :
            #    if i >= len(self._stars) : break
            #    if not self._stars[i].alive() :
            #        
            #        self._stars.pop(i)
                    
            
            #if len(self._stars) < 50 :
            if self.next_star_time < current_time :
                self.next_star_time += 40
                star()
            
            
            self.next_update_time = current_time + self.update_occurrency
            

class backgroundTile(pygame.sprite.Sprite) :
    
    containers = []
    images = []
    next_update_time = 0
    update_occurrency = 2
        
    def __init__(self, startheight, imgn = 0) :
        """Initialize background tile using first image and starting at y height"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        #self.orig = self.images[0]
        
        self.image = pygame.surface.Surface.convert_alpha(self.image)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, startheight)
    
    def movedown(self, offset) :
        self.rect.top += offset
        
    def update(self, current_time) :
        #if current_time >= self.next_update_time :
            #pygame.display.get_surface().blit(self.image, self.rect)
            #if self.image.get_rect().bottom < 0 : self.kill()
        #    self.next_update_time = current_time + self.update_occurrency
            pass
            
class starsTile(pygame.sprite.Sprite) :
    
    containers = []
    images = []
    next_update_time = 0
    update_occurrency = 2
        
    def __init__(self, startheight, imgn = 0) :
        """Initialize stars tile using first image and starting at y height"""
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self.image = self.images[0]
        #self.orig = self.images[0]
        
        self.image = pygame.surface.Surface.convert_alpha(self.image)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, startheight)
    
    def movedown(self, offset) :
        self.rect.top += offset
        
    def update(self, current_time) :
        #if current_time >= self.next_update_time :
            #pygame.display.get_surface().blit(self.image, self.rect)
            #if self.image.get_rect().bottom < 0 : self.kill()
        #    self.next_update_time = current_time + self.update_occurrency
            pass
