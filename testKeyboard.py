import pygame

keys=pygame.key.get_pressed()
if keys[K_LEFT]:
    location-=1
    if location==-1:
        location=0
if keys[K_RIGHT]:
    location+=1
    if location==5:
        location=4
