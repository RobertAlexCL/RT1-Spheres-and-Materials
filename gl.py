
from mymath import *
from math import pi, sin, cos, tan
from obj import Obj, texture
from figures import Material, Sphere





#Renderer

class Render(object):
    STEPS = 1
    camPos = V3(0, 0, 0)
    scene = []
    fov = 60

    def __init__(self):
        self.clear_color = color(0,0,0)
        self.draw_color = color(255,255,233)
    
    def glClear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)] 
            for y in range(self.height)
        ]


    def glCreateWindow(self, width, height): #width and height from window are renderer
        self.width = width
        self.height = height
        self.framebuffer = []
        self.glViewPort(0, 0, width, height)
        self.glClear()
    
    def point(self, x,y, color=None):
        if color == None:
            return
        self.framebuffer[int(y)][int(x)] = color 

    def glInit(self):
        pass

    def glViewPort(self, x, y, width, height):
        self.x_VP = x
        self.y_VP = y
        self.width_VP = width
        self.height_VP = height


    def glClearColor(self, r, g, b):
        self.clear_color = color(int(round(r*255)),int(round(g*255)),int(round(b*255)))

    def glColor(self, r,g,b):
        self.draw_color = color(int(round(r*255)),int(round(g*255)),int(round(b*255)))

    def glVertex(self, x, y):
        xPixel = round((x+1)*(self.width_VP/2)+self.x_VP)
        yPixel = round((y+1)*(self.height_VP/2)+self.y_VP)
        self.point(xPixel, yPixel)
    
    def glVertex(self, x, y):
        xPixel = round((x+1)*(self.width_VP/2)+self.x_VP)
        yPixel = round((y+1)*(self.height_VP/2)+self.y_VP)
        self.point(xPixel, yPixel)

    def glFinish(self, filename):
        f = open(filename, 'bw')

        #file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))   
        f.write(dword(0))
        f.write(dword(24))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0)) 
        f.write(dword(0))

        # pixel data

        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[x][y])
        
        f.close()
    

    def raytracing(self):
        for y in range(0, self.height, self.STEPS):
            for x in range(0, self.width , self.STEPS):
                Px = 2 * ((x + 0.5) / self.width) - 1
                Py = 2 * ((y + 0.5) / self.height) - 1
                t = tan( (self.fov * pi / 180) / 2)
                r = t * self.width / self.height

                Px *= r
                Py *= t
                direction = V3(Px, Py, -1)
                direction = norm(direction)
                self.point(x, y, self.cast(self.camPos, direction))
    
    def cast(self, o = V3(0, 0, 0), d = V3(0, 0, -1)):
        mat = self.intersect(o, d)
        if mat != None:
            return mat.diffuse
        return None

    def intersect(self, o, d):
        depth = float('inf')
        material = None

        for obj in self.scene:
            intersect = obj.ray_intersect(o, d)
            if intersect != None:
                if intersect.distance < depth:
                    depth = intersect.distance
                    material = obj.material

        return material




r = Render()
r.glCreateWindow(512, 512)
#r.STEPS = 2
#snow
r.scene.append(Sphere(V3(0, 3, -20), 1, Material(color(255, 255, 255))))
r.scene.append(Sphere(V3(0, 0, -20), 2, Material(color(255, 255, 255))))
r.scene.append(Sphere(V3(0, -5, -20), 3, Material(color(255, 255, 255))))

#buttons
r.scene.append(Sphere(V3(0, 0, -10), 0.2, Material(color(0, 0, 0))))
r.scene.append(Sphere(V3(0, -1, -10), 0.2, Material(color(0, 0, 0))))
r.scene.append(Sphere(V3(0, -2.5, -10), 0.2, Material(color(0, 0, 0))))

#eyes
r.scene.append(Sphere(V3(0.2, 1.6, -10), 0.05, Material(color(0, 0, 0))))
r.scene.append(Sphere(V3(-0.2, 1.6, -10), 0.05, Material(color(0, 0, 0))))

#nose
r.scene.append(Sphere(V3(0, 1.5, -10), 0.05, Material(color(255, 0.4, 0))))

#smile
r.scene.append(Sphere(V3(-0.3, 1.4, -10), 0.05, Material(color(0, 0, 0))))
r.scene.append(Sphere(V3(-0.2, 1.3, -10), 0.05, Material(color(0, 0, 0))))
r.scene.append(Sphere(V3(0, 1.2, -10), 0.05, Material(color(0, 0, 0))))
r.scene.append(Sphere(V3(0.2, 1.3, -10), 0.05, Material(color(0, 0, 0))))
r.scene.append(Sphere(V3(0.3, 1.4, -10), 0.05, Material(color(0, 0, 0))))

r.raytracing()
r.glFinish('out.bmp')
