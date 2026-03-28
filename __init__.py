#! /usr/bin/env python
# coding=utf-8
# copyright mario negri 2008

import pygame, os, sys, random, math, pixelperfect, imagemanipulation
from pygame.locals import *
from gameobjects import *
from aliens import *
from player import *
from text import *
import version

SOFTWARE_VERSION = version.ver

res = screen_width, screen_height = 1024, 768
fps = 60

pygame.init()

window = pygame.display.set_mode(res, DOUBLEBUF | HWSURFACE | HWACCEL | HWPALETTE, 32)
pygame.display.set_caption(version.name + ' ' + version.ver);
screen = pygame.display.get_surface()

clock = pygame.time.Clock()

#spriteGroup = pygame.sprite.Group()
#shotsGroup = pygame.sprite.Group()



aliens = []
#reddevil.shotsGroup = shotsGroup


#hud.images.append(pygame.image.load(os.path.join('data', 'hud.png')).convert_alpha())
#spaceship = ship((screen_width/2 ,screen_height-screen_height/8))



#s1 = spawn((100,100), 'reddevil')
#aliena = reddevil((100, 100))
#aliena.move((screen_width/2 +30, screen_height/2))
#aliena.attack(spaceship)
#aliens.append()
#aliena.attack(spaceship, 5)

#spriteGroup.add(spaceship)
#f1 = flare((100,100))
#spriteGroup.add(f1)
a1 = None
game = None

#bg = background()
#h = hud((res[0]-res[0]/5,res[1]-res[1]/3))
        
while(1) :
    clock.tick(fps)
    
    #screen.fill([0, 0, 0])
    
    keyPressed = pygame.key.get_pressed()
    
    #while(not pygame.key.get_focused()) :
        #print (not pygame.key.get_focused())
        #pass
    
    
    for event in pygame.event.get() :
        #print(event.type)
        if event.type == pygame.QUIT :
            sys.exit(0)
        elif event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE : sys.exit(0)
    
    #if not s1.alive() :
    #if not isinstance(a1, reddevil) :
    #    pass
        #a1 = reddevil((300,300), spaceship)
        #b = balloon("My eyes\nwill never forgive\nyou!", a1, os.path.join("data", "acmeexplosive.ttf"), 14)
        #a1.engage()
        #a1.attack(20)
        #a1.move((100,100))
        #a1.move_now((0,0))
        #a1.move((400,400))
        #a1.move((800,200))
        #a1.attack(10)
    

        
        
    
    #aliens_aliens = pygame.sprite.groupcollide(alienGroup, alienGroup, 0, 0)
    #for caliena in aliens_aliens.keys() :
        #if len(aliens_aliens) > 0 :
            #caliena.compute_hitmask()
            #for calienb in aliens_aliens[caliena] :
                #calienb.compute_hitmask()
                #if caliena.rect.center != calienb.rect.center :
                    #if pixelperfect.check_collision(caliena, calienb) :
                        #pass
            
        #print pygame.sprite.groupcollide(shotsGroup, alienGroup, 0, 0)[cshot]
    #if keyPressed[K_m] : a1.move((a1.rect.center[0] + 30,300), 1)
    #if keyPressed[K_a] : a1.attack(5)
    
    
    if not isinstance(game, gameobject) :
        #alienformation = gamectobje(5, 2, shotsGroup)
        
        game = gameobject()
        #bg.speed = 3.0
        #txt = text("Hello!!!!", (50,50), 10, (255,255,255), (0,0,0), "data/bitlow.ttf")
        #txt.center = (100,100)
        pass
    else :
        game.update(pygame.time.get_ticks())
        game.draw()
    
    

    

    

    #spriteGroup.update(pygame.time.get_ticks())
    #shotsGroup.update(pygame.time.get_ticks())
    #particleGroup.update(pygame.time.get_ticks())
    #alienGroup.update(pygame.time.get_ticks())
    
    #for sp in spriteGroup.sprites() :
    #    screen.blit(sp.image, sp.rect)
    #for sh in shotsGroup.sprites() :
    #    screen.blit(sh.image, sh.rect)

    
    
#    spriteGroup.draw(screen)
#    shotsGroup.draw(screen)
#    particleGroup.draw(screen)
#    alienGroup.draw(screen)
#    alienshotsGroup.draw(screen)
    
    
    #screen.blit(screen, screen.get_rect())
    pygame.display.flip()
    
    if(keyPressed[K_LCTRL]) : 
        inc = 0
        fname = os.path.join('screenshots', 'screen%s%s' % (str(inc),'.bmp'))
        
        while(os.path.exists(fname)) :
            fname = os.path.join('screenshots', 'screen%s%s' % (str(inc),'.bmp'))
            inc += 1
        
        pygame.image.save(screen.convert(), fname)
    #print clock.get_fps()
    #print clock.get_fps()
    #pygame.display.update()
    #all.clear(screen, screen.get_rect())
    #backgroundTileGroup.clear(screen, screen.get_rect())
    

