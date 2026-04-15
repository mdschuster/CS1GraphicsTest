from CS1Graphics import *

x=200
vx=200
radius=20
height=400
width=400

def setup():
    create_canvas(width, height, "Ball")

def draw():
    global x,vx
    x+=vx*dt

    if(x>400-radius):
        x=400-radius
        vx*=-1
    if(x<radius):
        x=radius
        vx*=-1

    circle("Test", x, 200, radius, rgb(0, 100, 255))

run()