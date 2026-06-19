import pygame
import math
import pygame.gfxdraw
import serial
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))

font = pygame.font.SysFont(None , 36)

clock = pygame.time.Clock()
flag = 0
ser = serial.Serial('COM6', 115200, timeout=1)
time.sleep(2)
ser.reset_input_buffer()

angle = 0
radius1 = 399

last_angle = []

running = True

while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    
    screen.fill((0, 0, 0))
    pygame.gfxdraw.arc(
        screen,
        400, 599,
        radius1,# bán kính
        180,
        0,
        (0,255,0)
    )
    for i in range(1 , 5): #print arc
        percent = (i/5)
        radius = int(percent * 399)
        pygame.gfxdraw.arc(
            screen,
            400,599,
            radius,
            180,
            0,
            (0 , 255 , 0)
        )
        
    for i in range (30 , 151 , 30): #paint the line
        rad = math.radians(i)
        cx = 400 + radius1 * math.cos(rad)
        cy = 599 - radius1 * math.sin(rad)
        pygame.draw.aaline(screen , (0 , 255 , 0) , (400 , 599) , (cx , cy))
        s = str(i)
        text = font.render(s , True , (0 , 255 , 0))
        if (cx < 400):
            screen.blit(text , (cx - 30 , cy - 35))
        else:
            screen.blit(text , (cx + 10 , cy - 20))

    last_angle.append(angle)
    
    if (len(last_angle) > 100):
        last_angle.pop(0)
    
    for i , a in enumerate(last_angle): #change the brightness
        rad = math.radians(a)
        
        brightness = int(255 * (i + 1)/(len(last_angle)))
        cx = 400 + radius1 * math.cos(rad)
        cy = 599 - radius1 * math.sin(rad)
        pygame.draw.aaline(screen , (0 , brightness , 0) , (400 , 599) , (cx , cy))
        
    
    if angle <= 0: #move the line
        flag = 1
    elif angle >= 180:
        flag = 0
    if flag == 1:
        angle += 0.2
    else:
        angle -= 0.2 
    # print(angle)
    rad = math.radians(angle)
    cx = 400 + radius1* math.cos(rad)
    cy = 599 - radius1* math.sin(rad)
    pygame.draw.aaline(screen , (0 , 255 , 0) ,(400 , 599) , (cx , cy))
        




    line = ser.readline().decode('utf-8', errors='replace').strip()
    if line:
        parts = line.split(',')
        print(parts)
        if len(parts) != 2:
            continue
        distance , angle = line.split(',')
        distance_numbers = 0
        angle_numbers = 0
        for i in distance:
            if (i < '0' or i > '9'):
                continue
                
        for i in angle:
            if (i < '0' and i > '9'):
                continue
            
                
        distance = int(distance) * 10
        
        angle = int(angle)
        rad = math.radians(angle)
        cx = 400 + distance * math.cos(rad)
        cy = 599 - distance * math.sin(rad)
        if (cx >= 0 and cx <= 800 and cy >= 200 and cy <= 599):
            pygame.draw.circle(screen , (255 , 0 , 0) , (cx , cy) , 15)
            

    
    pygame.display.update()
    clock.tick(240)

pygame.quit()

