import turtle
import Tkinter as tk
from time import sleep
from math import sin, cos, tan, atan, sqrt, pi

# Setup for Tkinter
root = tk.Tk()
root.geometry('+0+0')

# Bring window to front
root.lift()
root.attributes('-topmost', True)
root.attributes('-topmost', False)

canvas = tk.Canvas(master=root, width=root.winfo_screenwidth(),
    height=root.winfo_screenheight()-25,)
canvas.pack(fill=tk.BOTH, expand=tk.YES)
# Setup for turtle and TurtleScreen
screen = turtle.TurtleScreen(canvas)
t = turtle.RawTurtle(screen)
screen.tracer(0, 0)
t.ht()


###############################################################################


class Program:
    def __init__(self, draw, delay=(1.0/30.0)):
        self.draw = draw
        self.stop = False
        self.delay = delay

    def run(self):
        while not self.stop:
            self.draw()
            sleep(self.delay)
            screen.update()

        root.mainloop()

    def stop():
        self.stop = True


###############################################################################


class View3D:
    def __init__(self, fov=pi/2):
        self.pos = Vec()
        self.ang = Vec()
        self.fov = fov

        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight() - 25

        self.screen_z = (self.width/2) / (tan(self.fov/2))

        self.mouse_x = 0
        self.mouse_y = 0
        root.bind('<Motion>', self.set_mouse_pos)

    def update(self):
        self.ang.set(2.0 * pi * self.mouse_x / self.width,
                     2.0 * pi * self.mouse_y / self.height)
        print(self.ang)

    def point(self, p, y=None, z=None):
        if (y != None and z != None):
            p = Vec(p, y, z)

        point = Vec(p.x, p.y, p.z)

        point.sub(self.pos)
        point.rotate(self.ang)

        screen_x = self.screen_z * point.x / point.z
        screen_y = self.screen_z * point.y / point.z
        print(screen_x, screen_y)

        t.goto(screen_x, screen_y)

    def set_mouse_pos(self, event):
         self.mouse_x = event.x - self.width / 2
         self.mouse_y = -(event.y - self.height / 2)


###############################################################################


class Vec:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return('(' + str(self.x) + ', ' + str(self.y) + ', '+ str(self.z) + ')')

    def set(self, other, y=None, z=None):
        if y != None and z != None:
            other = Vec(other, y, z)
        elif y != None:
            other = Vec(other, y)

        self.x = other.x
        self.y = other.y
        self.z = other.z

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    @classmethod
    def class_add(cls, v1, v2):
        return cls(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    @classmethod
    def class_sub(cls, v1, v2):
        return cls(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)

    def mult(self, factor):
        self.x *= factor
        self.y *= factor
        self.z *= factor

    @classmethod
    def class_mult(cls, v1, factor):
        return cls(v1.x * factor, v1.y * factor, v1.z * factor)

    def div(self, divis):
        self.x /= divis
        self.y /= divis
        self.z /= divis

    @classmethod
    def class_div(cls, v1, divis):
        return cls(v1.x / divis, v1.y / divis, v1.z / divis)

    def rotate(self, ang, y=None):
        if y != None:
            ang = Vec(ang, y)

        current_ang = Vec.to_angle(self)
        new_ang = Vec.class_add(current_ang, ang)
        self.set(Vec.from_angle(new_ang))

    # Note that 3d angles store the radius in the variable z
    @classmethod
    def to_angle(cls, vec):
        x = atan(vec.x / vec.z)
        hyp = sqrt(vec.x**2 + vec.z**2)
        y = atan(vec.y / hyp)

        z = sqrt(hyp**2 + vec.y**2)

        return cls(x, y, z)

    @classmethod
    def from_angle(cls, ang):
        x = ang.z * sin(ang.x) * cos(ang.y)
        y = ang.z * sin(ang.y)
        z = ang.z * cos(ang.x) * cos(ang.y)

        return cls(z, y, z)
