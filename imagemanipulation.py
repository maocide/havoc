# coding=utf-8
import pygame
from pygame import *


def set_pixel_alpha(image, alpha) :
    for i in xrange(image.get_rect().width) :
        for j in xrange(image.get_rect().height) :
            #print(self.image.get_at((i,j)))
            a=image.get_at((i,j))[0]
            b=image.get_at((i,j))[1]
            c=image.get_at((i,j))[2]
            if alpha <= 255 : pygame.surface.Surface.set_at(image, (i,j), (a,b,c,alpha))
            #print(image.get_at((i,j)), alpha)
    #aa = pygame.surfarray.array_alpha(image)
    #for i in range(len(aa)) :
    #    aa[i] = alpha    
    
    return image

def get_pixel_list(image) :
    pixellist = []
    
    for i in xrange(image.get_rect().width) :
        for j in xrange(image.get_rect().height) :
            
            a=image.get_at((i,j))[0]
            b=image.get_at((i,j))[1]
            c=image.get_at((i,j))[2]
            d=image.get_at((i,j))[3]
            
            if d > 0 :
                newimg = pygame.surface.Surface([1,1])
                newimg.set_at((0,0),(a,b,c,d))
                
                pixellist.append(((i,j), newimg))
            
    
    return pixellist