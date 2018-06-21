import pyglet
from math import pi, sin, cos, sqrt
from random import uniform, randint
import keyboard as kb

class Vec2:
    def __init__(self, x, y):
        self.x  = x
        self.y = y

    def add(self, vec):
        self.x += vec.x
        self.y += vec.y

    def sub(self, vec):
        self.x -= vec.x
        self.y -= vec.y

    def mult(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def mag(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def copy(self):
        return Vec2(self.x, self.y)

    def coords(self):
        return (self.x, self.y)

class Circle:
    def __init__(self, pos, radius, color):
        self.pos = pos
        self.r = radius
        self.p = int(radius * 2)
        self.c = color

    def show(self):
        angle = 0
        increment = (pi * 2) / self.p
        coords = []
        colors = []
        for i in range(0, self.p):
            x = self.r * sin(angle) + self.pos.x
            y = self.r * cos(angle) + self.pos.y
            coords.append(x)
            coords.append(y)
            angle += increment

            for i in range(0, 4):
                colors.append(self.c[i])

        pyglet.graphics.draw(self.p, pyglet.gl.GL_TRIANGLE_FAN, ("v2f", tuple(coords)), ("c4B", tuple(colors)))


class Particle:
    def __init__(self, pos, size, color):
        self.pos = pos
        self.vel = Vec2(0, 0)
        self.acc = Vec2(0, 0)
        self.size = size
        self.lifespan = 255
        self.color = color

    def show(self):
        Circle(self.pos, self.size / 2, [self.color[0], self.color[1], self.color[2], int(self.lifespan)]).show()

    def update(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)

        self.acc.mult(0)
        self.lifespan -= 2

    def is_dead(self):
        return self.lifespan <= 0

    def apply_force(self, force):
        self.acc.add(force)

    # TODO
    def collide(self, obj):
        dist = Vec2(obj.pos.x - self.pos.x, obj.pos.y - self.pos.y)
        dist = dist.mag()
        return dist < (self.size / 2 + obj.size / 2)
        

class ParticleSystem:
    def __init__(self, pos):
        self.pos = pos
        self.particles = []

    def run(self):
        x = uniform(self.pos.x - 200, self.pos.x + 200)
        y = uniform(self.pos.y - 200, self.pos.y + 200)
        if frame_count % 13 == 0:
            self.particles.append(Particle(Vec2(x, y), uniform(5, 35), [int(randint(0, 255)), int(randint(0, 255)), int(randint(0, 255))]))

        for i in range(len(self.particles) - 1, -1, -1):
            self.particles[i].show()
            self.particles[i].update()

            # Random force
            self.particles[i].apply_force(Vec2(uniform(-0.2, 0.2), uniform(-0.1, 0)))
            if self.particles[i].is_dead():
                self.particles.pop(i)
            
        # print(len(self.particles))
    def apply_force(self, force):
        for particle in self.particles:
            particle.apply_force(force)

    def collide(self, obj):
        for i in range(len(self.particles) - 1, -1, -1):
            if self.particles[i].collide(obj) and not obj.attacking:
                obj.size += self.particles[i].size * 0.25
                self.particles.pop(i)

class Player:
    def __init__(self, pos, controls, color):
        self.pos = pos
        self.acc = Vec2(0, 0)
        self.vel = Vec2(0, 0)
        self.size = 15
        self.color = color
        self.attacking = False
        # 0 - LEFT, 1 - RIGHT, 2 - UP, 3 - DOWN, 4 - ATTACK
        self.controls = controls
        self.power = None
        self.score = 0
        self.hp = 100

    def show(self):
        Circle(self.pos, self.size / 2, self.color).show()

    def update(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)

        self.acc.mult(0)
        self.vel.mult(0.95)

        width = window.get_size()[0]
        height = window.get_size()[1]

        self.power = (2 - (self.size / 100)) * 0.5

        if self.pos.x < 0 or self.pos.x > width:
            self.vel.x *= -1
        if self.pos.y < 0 or self.pos.y > height:
            self.vel.y *= -1

        if kb.is_pressed(self.controls[4]):
            self.attacking = True
            self.size -= 0.5
            Circle(self.pos, self.size, self.color).show()
        else:
            self.attacking = False

        self.score += self.size * 0.001

        if self.size < 2.1:
            self.size = 2.2
            

    def move(self):
        if kb.is_pressed(self.controls[0]):
            self.acc.x -= self.power
        if kb.is_pressed(self.controls[1]):
            self.acc.x += self.power
        if kb.is_pressed(self.controls[2]):
            self.acc.y += self.power      
        if kb.is_pressed(self.controls[3]):
            self.acc.y -= self.power

    def fight(self, player):
        dist = Vec2(player.pos.x - self.pos.x, player.pos.y - self.pos.y)
        dist = dist.mag()
        if dist < (self.size + player.size) and self.attacking and not player.attacking:
            player.hp -= 1
        elif dist < (self.size + player.size) and not self.attacking and player.attacking:
            self.hp -= 1
        elif dist < (self.size + player.size) and self.attacking and player.attacking:
            self.hp -= 1
            player.hp -= 1

    def is_dead(self):
        return self.size < 0.01 or self.hp <= 0

    def reset(self):
        self.size = 15
        self.score = 0
        self.hp = 100

    def run(self):
        self.show()
        self.move()
        self.update()

class DisplayStats:
    def __init__(self, stats):
        self.stats = stats

    def show(self):
        for i in range(0, len(self.stats)):
            pyglet.text.Label(self.stats[i][0], font_name = "Times New Roman", font_size = 19, 
                x = self.stats[i][1], y = self.stats[i][2], anchor_x = "center", anchor_y = "center", color = (0, 0, 0, 255)).draw()

def winner(player1, player2):
    if player1.is_dead():
        label = pyglet.text.Label("Player 2 Wins!", font_name = "Times New Roman", font_size = 42, 
            x = 400, y = 400, anchor_x = "center", anchor_y = "center", color = (0, 0, 0, 255)).draw()
        # player1.reset()
        # player2.reset()
    elif player2.is_dead():
        label = pyglet.text.Label("Player 1 Wins!", font_name = "Times New Roman", font_size = 42, 
            x = 400, y = 400, anchor_x = "center", anchor_y = "center", color = (0, 0, 0, 255)).draw()
        # player1.reset()
        # player2.reset()

# Keeps track of the frames
frame_count = 0

class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 800, "Simple pyglet game")

        # The game loop
        pyglet.clock.schedule_interval(self.update, 1 / 60)

        self.particle_system = ParticleSystem(Vec2(400, 800))
        self.player1 = Player(Vec2(370, 500), ("LEFT", "RIGHT", "UP", "DOWN", "SPACE"), (0, 0, 255, 255))
        self.player2 = Player(Vec2(370, 500), ("A", "D", "W", "S", "R"), (255, 0, 0, 255))

    def on_draw(self):
        self.clear()
        global frame_count
        frame_count += 1

        # Window background color
        pyglet.gl.glClearColor(1, 1, 1, 1)

        # Used for alpha
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

        # self.test.show()
        # self.test.update()
        # self.test.apply_force(Vec2(0, -0.2))

        # Gravity
        self.particle_system.apply_force(Vec2(0, -0.01))

        self.stats = DisplayStats([[f"Score: {round(self.player1.score, 1)} HP: {round(self.player1.hp, 1)}", 140, 780], [f"Score: {round(self.player2.score, 1)} HP: {round(self.player2.hp, 1)}", 660, 780]])

        self.particle_system.collide(self.player1)
        self.particle_system.collide(self.player2)
        self.particle_system.run()
        self.player1.run()
        self.player2.run()
        self.player1.fight(self.player2)
        self.stats.show()
        winner(self.player1, self.player2)
        # print(self.player.size, self.player.score)
        # print(pyglet.clock.get_fps(), end="\r")


    def update(self, dt):
        pass

window = MainWindow()
pyglet.app.run()