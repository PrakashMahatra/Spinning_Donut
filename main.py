# importing libraries

import pygame
import math
from pygame.locals import *
from sys import exit
pygame.init()

# Now we create a window or a canvas to draw our donut
width = 600
height = 600
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont('arial', 10 ,bold =True)

# R1 = radius of donut , R2 = radius of bigger donut from the axis.
R1 = 80
R2 = 150

# To store values color pixel values for easy use.
white = (255,255,255)
black = (0,0,0)

# tTo make a grid
x_space = 10
y_space = 12

cols = int(width / x_space)
rows = int(height / y_space)

# to zoom in so we dont see the x axis line or y axis line

x1 = width / 2
y1 = height / 2


# rotation angles for A and B(initially)
A = 1
B = 1

K2 = 5000 # distance from donut to viewer
K1 = K2 * width * 3 / (8 * (R1 + R2)) # distance from viewer to screen

chars = [".",",","-","~",":",";","=","!","*","#","$","@"]
def draw(x, y, char):
    text = font.render(char, True, white)
    screen.blit(text,(x, y))


while True:
    screen.fill((black)) # clear the previous donut


     # To store chars
    output =[]
    for i in range(rows):
        col1 = []
        for j in range(cols):
            col1.append(" ")
        output.append(col1)

    # To store z values
    z_buffer = []
    for i in range(rows):
        col2 = []
        for j in range(cols):
            col2.append(0)
        z_buffer.append(col2)



    cosA, sinA = math.cos(A), math.sin(A)
    cosB, sinB = math.cos(B), math.sin(B)

    # o to 2*pie (628 = 2* pie* 100)
    for i in range(0, 628, 10):
        cosi , sini = math.cos(i/100), math.sin(i/100) # divide by 100 because we multiplied 2*pie with 100 above.
        x2 = R2 + R1*cosi
        y2 = R1*sini

        for f in range(0,628,3):
            cosf, sinf = math.cos(f/100), math.sin(f/100)

            x = x2 * ( cosB * cosf + sinA * sinB * sinf) - y2 * cosA * sinB
            y = x2 * (cosf * sinB - cosB * sinA * sinf) + y2 * cosA * cosB
            z = K2 + R1 * sinA * sini + cosA * sinf * x2

            z_reciprocal = 1/z

            # projection
            # the negative sign for yp is due to the fact that the y-axis in computer graphics
            # typically increases downwards.

            xp = math.floor(x * K1 * z_reciprocal)
            yp = math.floor(-y * K1 * z_reciprocal)

            # luminance
            l = cosf * cosi * sinB - cosA * cosi * sinf - sinA * sini + cosB * ( cosA*sini - cosi*sinA*sinf)

            # check if point is pointing towards light.
            if l > -0.8:
                l = abs(l)
                yc = int((yp+y1)/ y_space)
                xc = int((xp+x1)/ x_space)
                if z_reciprocal > z_buffer[yc][xc]:
                    z_buffer[yc][xc] = z_reciprocal
                    L = round(l*8)
                    output[yc][xc] = chars[L]
    for a in range(rows):
        for b in range(cols):
            draw(b*x_space, a*y_space, output[a][b])

    # prevent A AND B to go to infinity
    if (A  > 6.283 and A < 6.2831):
        A = 0
        B = 0
    else:
        A += 0.05
        B += 0.03

    for event in pygame.event.get(): #closing window logic
        if event.type == QUIT:
            exit()

    pygame.display.update()



