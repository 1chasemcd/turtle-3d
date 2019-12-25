from pturtle import *

point1 = Vec(0, 0, 100)
point2 = Vec(5, 50, 100)

view = View3D()

def draw():
    view.update()
    t.down()
    view.point(point1)
    view.point(point2)
    t.up()

program = Program(draw)
program.run()
