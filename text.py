import pygame, sys, os, math, random, libxml2, imagemanipulation, pixelperfect
from pygame.locals import *

TFX_NONE = 0
TFX_FADE = 1
TFX_STRETCH = 2


class text(object) :
    containers = []
    _lines = []
    rects = []
    _justify = False
    _alpha = 0
    _fadein = False
    
    def __set_fade_in(self, value) :
        self._fadein = value
        for ln in self._lines :
            for l in ln :
                l.fadein = value
        
    def __set_fade_out(self, value) :
        self._fadeout = value
        if value :
            for ln in self._lines :
                for l in ln :
                    l.fadeout = value
    
    def __get_fate_in(self) :
        return self._fadein
        
    def __get_fate_out(self) :
        return self._fadeout
    

    
    def __get_alpha__(self) :
        return self._lines[0][0].image.get_alpha()
    
    def __set_alpha__(self, value) :
        self._alpha = value
        for i in xrange(len(self._lines)) :
            for j in xrange(len(self._lines[i])) :
                self._lines[i][j]._alpha = value
                self._lines[i][j].image.set_alpha(value)
        
    
    def __get_fate_in(self) :
        return self._fadein
    
    def __get_center__(self) :
        return self.rect.center
        
    def __set_center__(self, value) :
        self.rect = pygame.Rect(self.rects[0])
        self.rect.unionall_ip(self.rects)
        
        self.rect.center = value
        if not self._justify : cpos = self.rect.midtop
        else : cpos = (self.rect.left, self.rect.top)
        
        #cpos = (self.rect.left, self.rect.midtop[1])
        
        for i in xrange(len(self._lines)) :
            
            for j in xrange(len(self._lines[i])) :
                
                if self._justify :
                    self._lines[i][j].rect.topleft = cpos
                    self.rects[i] = self._lines[i][j].rect
                    if j > 0 :
                        self._lines[i][j].rect.midleft = self._lines[i][j-1].rect.midright
                    cpos = (cpos[0], self._lines[i][j].rect.bottom + 1)
                else :
                    if len(self._lines[i]) > 1 and j == 0 :
                        maxl = 0
                        for l in self._lines[i] :
                            maxl += l.rect.width 
                        self._lines[i][j].rect.bottomleft = (cpos[0] - maxl/2, cpos[1])
                    else :
                        self._lines[i][j].rect.midtop = cpos
                        
                    if j > 0 :
                        self._lines[i][j].rect.midleft = self._lines[i][j-1].rect.midright
                    cpos = (self._lines[0][0].rect.midbottom[0], self._lines[i][j].rect.bottom + 1)
                    
                    self._lines[i][j]._pos = self._lines[i][j].rect.center
                    self.rects[i] = self._lines[i][j].rect
        
        #for i in xrange(len(self._lines)) :
            #if self._justify :
                #self._lines[i].rect.topleft = lastTop
                #self._lines[i]._pos = self._lines[i].rect.center
                #self.rects[i] = self._lines[i].rect
                #lastTop = (self.rect.left, self.rects[i].midbottom[1] + 1)
            #else :
                #self._lines[i].rect.midtop = lastTop
                #self._lines[i]._pos = self._lines[i].rect.center
                #self.rects[i] = self._lines[i].rect
                #lastTop = (self.rects[i].midbottom[0], self.rects[i].midbottom[1] + 1)
                
        self.rect = pygame.Rect(self.rects[0])
        self.rect.unionall_ip(self.rects)
                
    def __get_topleft__(self) :
        return self.rect.topleft
        
    def __set_topleft__(self, value) :
        self.rect = pygame.Rect(self.rects[0])
        self.rect.unionall_ip(self.rects)
        
        self.rect.topleft = value
        
        maxwidth = 0
        #for l in self._lines[0] :
        #    maxwidth = l.rect.width
        xpos = self.rect.center[0] - self.rect.width/2
        ypos = self.rect.top
        
        offx = value[0] - xpos
        offy = value[1] - ypos
        oldc = self.center
        self.center = (oldc[0] - offx, oldc[1] - offy)
        
    def __get_lineheight__(self) :
        self._lines[0][0].rect = self._lines[0][0].image.get_rect()
        return self._lines[0][0].rect.height
    
    def __get_height__(self) :
        return self.lineheight * len(self._lines)
    
    def __get_width__(self) :
        max = 0
        for i in xrange(len(self._lines)) :
            for l in self._lines[i] :
                if l.rect.width > max : max = l.rect.width
        
        return max
                
    def kill(self) :
        for i in xrange(len(self._lines)) :
            for l in self._lines[i] :
                l.kill()
        
    def alive(self) :
        al = False
        for ln in self._lines :
            for l in ln : al |= l.alive()
        return al
    
    center = property(__get_center__, __set_center__)
    topleft = property(__get_topleft__, __set_topleft__)
    fadein = property(__get_fate_in, __set_fade_in)
    fadeout = property(__get_fate_out, __set_fade_out)
    alpha = property(__get_alpha__, __set_alpha__)
    lineheight = property(__get_lineheight__)
    height = property(__get_height__)
    width = property(__get_width__)
    
    
    
    def __init__(self, content, pos = (0,0), size = 10, color = (255,255,255), colorkey = (0,0,0), f = None, justify = False, effect = TFX_NONE, expire = 0) :
        #pygame.sprite.Sprite.__init__(self, self.containers)
        self._justify = justify
        
        self._lines = []
        self.rects = []
        
        if expire != 0 : self._expire = expire + pygame.time.get_ticks()
        else : self._expire = 0
        
        lines = []
        posl = pos
        
        #content = '<html><body><p><span style="color: #FF0000; font-size: 12; font-face: data/Backslash.ttf;">All</span><span style=""> your base</span></p><p><span style="color: #FFFFFF;">are belong to us.</span></p><body><html>'
        #if html tag parse as html
        if content.strip()[0:6] == '<html>' :
            #try :
            doc = libxml2.htmlParseDoc(content, 'utf-8')
            pnodes = doc.xpathEval('//body/p')
            index = 0
            for pnode in pnodes :
                spannodes = pnode.xpathEval('./span')
                ln = []
                for spannode in spannodes :
                    col = color
                    s = size
                    font = f
                    if type(spannode.prop('style')) != type(None) and len(spannode.prop('style')) > 0 :
                        styleprop = spannode.prop('style')
                        styles = styleprop.split(';')
                        if styles.count('') > 0 : styles.remove('')
                        for style in styles :
                            style = style.strip()
                            n, v = style.split(':')
                            if n == 'color' :
                                v = v.strip().replace('#', '')
                                col = (int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16))
                            if n == 'font-size' and v.strip().isdigit() :
                                v = v.strip()
                                s = int(v)
                            if n == 'font-face' :
                                v = v.strip()
                                font = v.split('/')
                                if isinstance(f, (tuple, list)) and len(f) > 0 :
                                    font = os.path.join(f)
                                else :
                                    font = v
                            pass
                    if not isinstance(size, int) : s = size
                    if not isinstance(size, str) : font = f
                    if not isinstance(col, tuple) : col = color
                    ln.append(textLine(spannode.getContent(), posl, size, col, colorkey, font, effect, self._expire))
                    posl = ln[len(ln)-1].rect.midleft
                    ln[len(ln)-1].rect.midleft = posl
                    
                    self.rects.append(ln[len(ln)-1].image.get_rect())
                    
                lines.append(ln)
                if justify : posl = lines[index][0].rect.topleft
                else : posl = lines[index][0].rect.midbottom
                index += 1
                    
            self._lines = lines
                    
            #except Exception :
                #print e
             #   print Exception
             
        
        if content.strip()[0:6] != '<html>' : #old strings... disabled for now
            font = pygame.font.Font(f, size)
            strings = content.split('\n')
            lastLine = None
            
            for string in strings :
                ll = []
                line = textLine(string, pos, size, color, colorkey, f, effect, self._expire)
                if isinstance(lastLine, textLine) :
                    if justify : line.rect.topleft = (pos[0], lastLine.rect.midbottom[0] + 1)
                    else : line.rect.midtop = (lastLine.rect.midbottom[0], lastLine.rect.midbottom[0] + 1)
                
                #line.image.set_alpha(40)
                ll.append(line)
                self._lines.append(ll)
                self.rects.append(line.image.get_rect())
                
                lastLine = line
                
            
            #self.image.set_colorkey(colorkey)
            #self.rect = pygame.Rect()
            self.rect = pygame.Rect(self.rects[0])
            self.rect.unionall_ip(self.rects)
    
            self.rect.center = pos
            #lastTop = self.rect.midtop
            
        
        cpos = pos
        
        for i in xrange(len(self._lines)) :
            
            for j in xrange(len(self._lines[i])) :
                
                if justify :
                    self._lines[i][j].rect.topleft = cpos
                    self.rects[i] = self._lines[i][j].rect
                    if j > 0 :
                        self._lines[i][j].rect.midleft = self._lines[i][j-1].rect.midright
                    cpos = (pos[0], self._lines[i][j].rect.bottom + 1)
                else :
                    if len(self._lines[i]) > 1 and j == 0 :
                        maxl = 0
                        for l in self._lines[i] :
                            maxl += l.rect.width 
                        self._lines[i][j].rect.bottomleft = (cpos[0] - maxl/2, cpos[1])
                    else :
                        self._lines[i][j].rect.midbottom = cpos
                    
                    
                    
                    if j > 0 :
                        self._lines[i][j].rect.midleft = self._lines[i][j-1].rect.midright
                    cpos = (cpos[0], self._lines[i][j].rect.bottom + 1)
                    
                    self.rects[i] = self._lines[i][j].rect
        
        self.rect = pygame.Rect(self.rects[0])
        self.rect.unionall_ip(self.rects)
        if effect == TFX_FADE :
            self.fadein = True
            self._alpha = 0
            self.alpha = 0
        
        #pygame.display.get_surface().blit(self.image, self.rect)
        #for image in self.images :
            #pygame.display.get_surface().blit(image, self.rect)
            
    #def draw(self) :
    #    for l in self._lines :
    #        pygame.display.get_surface().blit(l.image, l.rect)
        
    def update(self, current_time) :
        pass
        #if self._fadein and self._alpha < 255 :
            #self._alpha += 5
            #self.alpha = self._alpha
        #if self._fadeout and self._alpha > 0 :
            #self._alpha -= 5
            #self.alpha = self._alpha
        #if self._alpha <= 0 or self._alpha >= 255 : self._fadein = self._fadeout = False
        #if not self._fadein and not self._fadeout :
            #self._alpha = 255
            #self.alpha = 255
    
class textLine(pygame.sprite.Sprite) :
    
    containers = []
    _fadein = False
    _fadeout = False
    _alpha = 0
    _effect = None
    
    def __set_fade_in(self, value) :
        self._fadein = value
        if value : self._fadeout = False
        self._alpha = self.image.get_alpha()
        
    def __set_fade_out(self, value) :
        self._fadeout = value
        if value : self._fadein = False
        self._alpha = self.image.get_alpha()
    
    def __get_fate_in(self) :
        return self._fadein
        
    def __get_fate_out(self) :
        return self._fadeout
    
    fadein = property(__get_fate_in, __set_fade_in)
    fadeout = property(__get_fate_out, __set_fade_out)
    
    def __init__(self, content, pos = (0,0), size = 10, color = (255,255,255), colorkey = (0,0,0), f = None, effect = TFX_NONE, expire = 0) :
        pygame.sprite.Sprite.__init__(self, self.containers)
        
        self._content = content
        self._color = color
        self._font = f
        self._size = size
        self._colorkey = colorkey
        
        self._expire = expire
        
        font = pygame.font.Font(f, size)
        self.image = font.render(content, True, color, colorkey).convert()
        self.image.set_colorkey(colorkey)
        self.orig = self.image
            
        self._effect = effect
        
        self.rect = self.image.get_rect()
        
        self.rect.center = pos
        self._pos = pos
        
        if effect == TFX_FADE :
            self.image.set_alpha(0);
            self.fadein = True
        if effect == TFX_STRETCH :
            self._tw = 0
            self._th = 0
            self._mw = self.rect.width
            self._mh = self.rect.height
            self._alpha = 255
            self.image.set_alpha(self._alpha)

        
    def update(self, current_time) :
        #if expire time reached start fade out
        if self._expire != 0 and self._expire <= current_time :
            self.fadeout = True
            self._expire = 0
        
        #fade in
        if self._fadein and self.image.get_alpha() < 255 :
            self._alpha += 8
            self.image.set_alpha(self._alpha)
        #fade out
        if self._fadeout and self.image.get_alpha() > 0 :
            self._alpha -= 8
            self.image.set_alpha(self._alpha)
        #stretch
        if self._effect == TFX_STRETCH and self._th <= self._mh:
            self._th += 1
            self.image = pygame.transform.scale(self.orig, (self.rect.width, self._th))
            self.rect = self.image.get_rect()
            self.image.set_alpha(self._alpha)
            self.rect.center = self._pos
            if self._th == self._mh : self.image = self.orig
            
        if self.fadeout and self.image.get_alpha() == 0 :
            self.kill()
            
            
        #if self._alpha <= 0 and self._fadeout : self._fadeout = False
        #if self._fadein and self._alpha >= 255 : self._fadein = False
        #if not self._fadein and not self._fadeout :
        #    self._alpha = 255
        #    self.image.set_alpha(255)