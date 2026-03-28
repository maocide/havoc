# pixelperfect module http://pygame.seul.org/wiki/FastPixelPerfect
#
# The following is a revision of Joshua Gram's version, by Alfonso Crawford.
#
#Note: You can see an example using an algorithm almost identical to Joshua's at John Eriksson's project, PixelPerfect.
#
#Here is a cleaned up and bug-fixed version of the original by RB[0],
#that now uses the for loop(as suggested here by Joshua Grams), instead of while loops, which are slower.
#There are also a few helper functions that are used to create hitmasks without using pygames surfarray module, as it is currently broken(at least for me), these dont even require Numeric.
#
#This pixelperfect implementation is anywhere from 1.2 to 2.5 times faster
#
#
#--EXAMPLE CODE--#
#pygame.init()
#screen = pygame.display.set_mode([200,200])
#screen.fill([255,255,255])
 
 
#a=my_object('carrots.png',-1,None)
#a.rect.center=(25,25)
 
#b=my_object('carrots.png',None,True)
#b.rect.center=(50,50)
 
#screen.blit(a.image, a.rect)
#screen.blit(b.image, b.rect)
#pygame.display.flip()
 
#def main():
    #av=0
    #for i in xrange(999):
        #st_time=time.clock()
        #check_collision(a, b)
        #av+=time.clock()-st_time
 
    #print "time:", av, check_collision(a, b)
 
#main()

def check_collision(obj1,obj2):
    """checks if two objects have collided, using hitmasks"""
    try:rect1, rect2, hm1, hm2 = obj1.rect, obj2.rect, obj1.hitmask, obj2.hitmask
    except AttributeError:return False
    rect=rect1.clip(rect2)
    if rect.width==0 or rect.height==0:
        return False
    x1,y1,x2,y2 = rect.x-rect1.x,rect.y-rect1.y,rect.x-rect2.x,rect.y-rect2.y
    for x in xrange(rect.width):
        for y in xrange(rect.height):
            try :
                if hm1[x1+x][y1+y] and hm2[x2+x][y2+y]:return True
                else:continue
            except :
                pass
    return False
 
def get_colorkey_hitmask(image, rect, key=None):
    """returns a hitmask using an image's colorkey.
       image->pygame Surface,
       rect->pygame Rect that fits image,
       key->an over-ride color, if not None will be used instead of the image's colorkey"""
    if key==None:colorkey=image.get_colorkey()
    else:colorkey=key
    mask=[]
    for x in xrange(rect.width):
        mask.append([])
        for y in xrange(rect.height):
            mask[x].append(not image.get_at((x,y)) == colorkey)
    return mask
 
def get_alpha_hitmask(image, rect, alpha=0):
    """returns a hitmask using an image's alpha.
       image->pygame Surface,
       rect->pygame Rect that fits image,
       alpha->the alpha amount that is invisible in collisions"""
    mask=[]
    for x in xrange(rect.width):
        mask.append([])
        for y in xrange(rect.height):
            mask[x].append(not image.get_at((x,y))[3]==alpha)
    return mask
 
def get_colorkey_and_alpha_hitmask(image, rect, key=None, alpha=0):
    """returns a hitmask using an image's colorkey and alpha."""
    mask=[]
    for x in xrange(rect.width):
        mask.append([])
        for y in xrange(rect.height):
            mask[x].append(not (image.get_at((x,y))[3]==alpha or\
                                image.get_at((x,y))==colorkey))
    return mask
 
def get_full_hitmask(image, rect):
    """returns a completely full hitmask that fits the image,
       without referencing the images colorkey or alpha."""
    mask=[]
    for x in xrange(rect.width):
        mask.append([])
        for y in xrange(rect.height):
            mask[x].append(True)
    return mask

import pygame, pixelperfect, time
from pygame.locals import *
from pixelperfect import *
 
def load_image(name, colorkey=None, alpha=False):
    """loads an image into memory"""
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha:image = image.convert_alpha()
    else:image=image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
 
class my_object(object):
    def __init__(self, image,colorkey=None,alpha=None):
        self.image, self.rect=load_image(image,colorkey=colorkey, alpha=alpha)
        if colorkey and alpha:
            self.hitmask=get_colorkey_and_alpha_hitmask(self.image, self.rect,
                                                        colorkey, alpha)
        elif colorkey:
            self.hitmask=get_colorkey_hitmask(self.image, self.rect,
                                              colorkey)
        elif alpha:
            self.hitmask=get_alpha_hitmask(self.image, self.rect,
                                           alpha)
        else:
            self.hitmask=get_full_hitmask(self.image, self.rect)
 
