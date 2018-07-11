from p5 import *
from random import randint
import keyboard as kb

class Snake:
    def __init__(self, size):
        self.size = size
        self.pos = Vector(randint(0, width // size) * size, randint(0, height // size) * size)
        self.tail = [self.pos]
        self.speed = Vector(0, 0)

    def update(self):
        self.pos += self.speed * self.size
        self.tail[0] = self.pos
        if len(self.tail) > 1:
            # Move the last element to the front and delete it after
            self.tail.insert(0, self.tail[len(self.tail) - 1])
            self.tail.pop()

        if self.death():
            print(f"YOU DIED!, Your score was: {len(self.tail)}!")
            self.reset()
        # print(self.tail)

    def reset(self):
        self.pos = Vector(randint(0, width // self.size) * self.size, randint(0, height // self.size) * self.size)
        self.tail = [self.pos]
        self.speed = Vector(0, 0)

    def death(self):
        if self.pos.x < 0 or self.pos.x > width - self.size or self.pos.y < 0 or self.pos.y > height - self.size:
            return True
        # It kinda works, but there might be bugs
        # You can't die if you are not over 3 in length, eh calling this a feature 
        # TODO find a better way to check this
        for i in range(2, len(self.tail)):
            if self.pos == self.tail[i]:
                return True

    def add(self):
        self.tail.append(self.pos + self.speed * self.size)

    def show(self):
        fill(0)
        for i in range(0, len(self.tail)):
            rect(self.tail[i], self.size, self.size)
        print(f"Score: {len(self.tail)}", end="\r")

    def control(self):
        if kb.is_pressed("UP"):
            self.speed = Vector(0, -1)
        if kb.is_pressed("DOWN"):
            self.speed = Vector(0, 1)
        if kb.is_pressed("LEFT"):
            self.speed = Vector(-1, 0)
        if kb.is_pressed("RIGHT"):
            self.speed = Vector(1, 0)

class Food:
    def __init__(self, snake):
        self.snake = snake
        self.pos = Vector(randint(0, (width - snake.size) // snake.size) * snake.size, randint(0, (width - snake.size) // snake.size) * snake.size)

    def collide(self):
        if self.pos == snake.pos:
            self.pos = Vector(randint(0, (width - snake.size) // snake.size) * snake.size, randint(0, (width - snake.size) // snake.size) * snake.size)
            snake.add()

    def show(self):
        no_stroke()
        fill(255, 0, 0)
        rect(self.pos, self.snake.size, self.snake.size)

snake = Snake(20)
food = Food(snake)

def mouse_pressed():
    snake.add()

def setup():
    size(500, 500)
    title("Snake Game")

def draw():
    background(255)

    snake.control()
    snake.update()
    snake.show()

    food.collide()
    food.show()

run(frame_rate = 10)