#I know that this does not seem impressive but I know pygame alot better
#at pygame now so i think i could develop somthing alot better and quicker with time.
#This was made after i realised i was not going to be able to finish my pytorch project
#in time so i didi this instead.


import pygame as pg
import random as rd
import tkinter as tk

colours={'black':[0,0,0],'white':[255,255,255],'yellow':[0,255,255],'grey':[220,220,220],'dark_grey':[128,128,128],'red':[255,0,0],'weird_green':[164,196,176],'purple':[164, 96, 176]}#rgb(176, 163, 51)

pg.init()


class dude:
  def __init__(self,x,y):
    self.health=800
    self.x=x
    self.y=y
    self.jumping=False
    self.falling=False
    self.grounded=True
    self.direction='r'#default is right
    self.score=0


  def walk(self,direction,speed):
    self.x+=direction*speed

  def draw_self(self):
    self.body=pg.draw.rect(screen,colours['black'],(self.x,self.y,40,60))
class bad_dude():
  def __init__(self,x,y,health,reload):
    self.x=x
    self.y=y
    self.health=health
    self.reload=reload
    self.ogreload=reload
    self.shot_projectiles=[]
    self.colour=[rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)]
    self.body=pg.draw.rect(screen,self.colour,(self.x,self.y,40,60))
  def think(self):
    if self.reload!=0:
      self.reload-=1
    if player.y==self.y:
      if self.reload==0:
        if self.x<player.x:
          self.shot_projectiles.append(bullet(self.x,self.y,1))
        else:
          self.shot_projectiles.append(bullet(self.x,self.y,-1))
        self.reload=self.ogreload
    else:
      if self.x<player.x:
        self.walk(1,5)
      elif self.x>player.x:
        self.walk(-1,5)
      else:
        if self.reload!=0:
          self.reload-=1
        if self.reload==0:
          if self.y<player.y:
            self.shot_projectiles.append(bullet_up(self.x,self.y,1))
          else:
            self.shot_projectiles.append(bullet_up(self.x,self.y,-1))
          self.reload=self.ogreload


  def walk(self,direction,speed):
    self.x+=direction*speed

  def draw_self(self):
    body=pg.draw.rect(screen,self.colour,(self.x,self.y,40,60))

class bullet():
  def __init__(self,x,y,direction):
    self.x=x+20
    self.y=y+20
    self.direction=direction

  def move(self):
    self.x+=self.direction*30

  def draw_self(self):
    self.body=pg.draw.rect(screen,colours['yellow'],(self.x,self.y,10,10))

class bullet_up(bullet):
  def __init__(self, x, y, direction):
    super().__init__(x, y, direction)
  def move(self):
    self.y+=self.direction*30

class platform:
  def __init__(self,y):
    self.y=y
  def draw_self(self):
    pg.draw.line(screen,colours['black'], (0,self.y),(1000,self.y))


class userBar:
  def __init__(self,player):
    self.xmax=800
    self.health=player.health
  def draw_self(self):
    pg.draw.rect(screen,colours['weird_green'],(0,900,1000,1000))#
    pg.draw.rect(screen,colours['grey'],(50,920,self.xmax,40))
    pg.draw.rect(screen,colours['red'],(50,920,self.health,40))
class level:
  def __init__(self,difficulty):
    self.villians=self.generate_level(difficulty)

  def generate_level(self,diff):
    ycoords={1:120,2:300,3:480,4:660,5:840}
    villians=[]
    if diff>10:
      diff=10
    for i in range(diff):
      ycoord=rd.randint(1,5)
      xcoord=rd.choice([i*10 for i in range(20,80)])
      enemy_reload=200-(diff*20)
      if enemy_reload<20:
        enemy_reload=20
      health=diff*50
      villians.append(bad_dude(xcoord,ycoords[ycoord],health,enemy_reload))
    return villians


widlen=(1000,1000)
screen=pg.display.set_mode(widlen)
clock=pg.time.Clock()
player=dude(200,840)
projectiles=[]
platforms=[]
cool_down=0
gravity=1
jump_height=20
y_velocity=20
healthBar=userBar(player)
run=True
for i in range(0,10):
  platforms.append(platform(i*180))
platforms_y_pos=[i.y for i in platforms]
difficulty_count=1
l=level(1)
bad_guys=l.villians
while run:
  alive=0
  for i in l.villians:
    if i.health>0:
      alive+=1
  if alive==0:
    player.score+=(difficulty_count*10)
    difficulty_count+=1
    l=level(difficulty_count)
    bad_guys=l.villians



  for e in pg.event.get():
    if e.type == pg.QUIT:
      run=False
    if player.health==0:
      run=False
  #print(player.y+60,'-',platforms_y_pos)

  keys=pg.key.get_pressed()
  #print(player.y)
  if player.x!=1000-40:
    if keys[pg.K_d]:
      player.walk(1,10)
      player.direction='r'
  if player.x!=0:
    if keys[pg.K_a]:
      player.walk(-1,10)
      player.direction='l'
  if keys[pg.K_w]:
    player.jumping=True
    player.direction='u'
  if keys[pg.K_s] and (player.y+60 in platforms_y_pos):
    #print(player.falling)
    if (player.y-60)!=780:
      player.falling=True
      player.y+=10
      player.direction='d'
  #print(player.direction)
  if cool_down==0:
    #print('in')
    if keys[pg.K_RIGHT]:
      projectiles.append(bullet(player.x,player.y,1))
      cool_down=20
    if keys[pg.K_LEFT]:
      projectiles.append(bullet(player.x,player.y,-1))
      cool_down=20
    if keys[pg.K_UP]:
      projectiles.append(bullet_up(player.x,player.y,-1))
      cool_down=20
    if keys[pg.K_DOWN]:
      projectiles.append(bullet_up(player.x,player.y,1))
      cool_down=20	
  if cool_down!=0:#shooting bulletiu8
    #print(cool_down)
    cool_down-=1


  if player.jumping:
    player.y -= y_velocity
    y_velocity -= gravity
    print(y_velocity)
    if y_velocity < 0:
      for p in platforms:
        if player.y + 60 >= p.y and player.y <= p.y:
          player.jumping=False
          player.y=p.y-60
    if y_velocity < -jump_height:
      player.jumping = False
      y_velocity = jump_height


  #print(platforms_y_pos)
  if player.y==-60:
    player.y+=10
    player.falling=True
  if player.falling:
    player.y+=10
    if player.y+60 in platforms_y_pos:
      player.falling=False


  screen.fill(colours['dark_grey'])
  healthBar.draw_self()
  for i in platforms:
    i.draw_self()
  player.draw_self()

  for i in projectiles:
    i.draw_self()
    i.move()
    for j in bad_guys:
      if j.body.colliderect(i.body):
        #print('---------------HIT---------------')
        j.health-=50



  for i in bad_guys:
    if i.health>0:
      i.draw_self()
      i.think()
      for j in i.shot_projectiles:
        j.move()
        j.draw_self()

        if j.body.colliderect(player.body):
          #print('---------------HIT---------------')
          player.health-=50
          if player.health<0:
            player.health=0
          healthBar.health=player.health




  clock.tick(50)
  pg.display.flip()



window=tk.Tk()
window.geometry('500x500')
tk.Label(window,text=f'You died your score is {player.score}').pack()
window.mainloop()
