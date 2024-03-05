import math

import boids

class Summoner:
    def __init__(
                 self, 
                 position, 
                 obstacles,
                 window_size, 
                 window, 
                 graphics_lib
                ):
        self.window_size = window_size
        self.window = window
        self.graphics_lib = graphics_lib

        self.position = position
        self.direction_degrees = 90
        self.relaxed_speed = 3
        self.burst_speed = 12
        self.speed_scalar = self.relaxed_speed
        self.color = (255, 255, 0)

        self.obstacles = obstacles

        self.tail = []

        self.myBoids = boids.Boid.all_boids
    
    def draw(self, fps):
        new_direction_radian = (math.pi / 180) * self.direction_degrees
        drawable_position = (
                (self.position[0] - 18 * math.cos(new_direction_radian), self.window_size[1] - (self.position[1] - 18 * math.sin(new_direction_radian))),
                (self.position[0] + 12 * math.cos(new_direction_radian + 120 * (math.pi / 180)), self.window_size[1] - (self.position[1] + 12 * math.sin(new_direction_radian + 120 * (math.pi / 180)))),
                (self.position[0] + 18 * math.cos(new_direction_radian), self.window_size[1] - (self.position[1] + 18 * math.sin(new_direction_radian))),
                (self.position[0] + 12 * math.cos(new_direction_radian - 120 * (math.pi / 180)), self.window_size[1] - (self.position[1] + 12 * math.sin(new_direction_radian - 120 * (math.pi / 180)))),
               )
        self.tail.append(drawable_position[0])
        if len(self.tail) > 5:
            self.tail.remove(self.tail[0])
        if len(self.tail) > 2:
            self.graphics_lib.draw.lines(self.window, self.color, False, self.tail, 1)
        self.graphics_lib.draw.polygon(self.window, self.color, drawable_position)
        self.avoid_obstacles()

        my_key = self.graphics_lib.key.get_pressed()
        for boid in self.myBoids:
            boid.draw(fps)
            # boid.move(self.position, 1)

        if my_key[self.graphics_lib.K_q]:
            self.summon_boid()

        if my_key[self.graphics_lib.K_w]:
            self.move()
        if my_key[self.graphics_lib.K_a]:
            self.steer(7)
        if my_key[self.graphics_lib.K_d]:
            self.steer(-7)

        if my_key[self.graphics_lib.K_SPACE]:
            self.burst()
        else:
            self.relax()
    
    def move(self):
        self.position[0] += self.speed_scalar * math.cos((math.pi / 180) * self.direction_degrees)
        self.position[1] += self.speed_scalar * math.sin((math.pi / 180) * self.direction_degrees)
    
    def steer(self, steer_amount):
        self.direction_degrees += steer_amount
        if self.direction_degrees >= 360:
            self.direction_degrees = self.direction_degrees - 360
        if self.direction_degrees < 0:
            self.direction_degrees = self.direction_degrees + 360
    
    def burst(self):
        self.speed_scalar = self.burst_speed
    
    def relax(self):
        self.speed_scalar = self.relaxed_speed
    
    def avoid_obstacles(self):
        if self.position[0] < 10:
            self.position[0] = 11
            # self.direction_degrees += 180
        elif self.position[0] > self.window_size[0] - 10:
            self.position[0] = self.window_size[0] - 11
            # self.direction_degrees += 180
        
        if self.position[1] < 10:
            self.position[1] = 11
            # self.direction_degrees += 180
        elif self.position[1] > self.window_size[1] - 10:
            self.position[1] = self.window_size[1] - 11
            # self.direction_degrees += 180
        
        if self.position[0] < -20 or self.position[0] > self.window_size[0] + 20:
            # self.position[0] = random.randint(100, self.window_size[0]-100)
            self.position[0] = 550
        if self.position[1] < -20 or self.position[1] > self.window_size[1] + 20:
            # self.position[1] = random.randint(100, self.window_size[1]-100)
            self.position[1] = 300
        

        for obstacle in self.obstacles:
            if ((self.position[0] + 20 > obstacle.edges[0]) and (self.position[0] - 20 < obstacle.edges[2])) and ((self.position[1] + 20 > obstacle.edges[3]) and (self.position[1] - 20 < obstacle.edges[1])):
                if self.position[1] > obstacle.edges[3] and self.position[1] < obstacle.edges[1]:
                    if self.position[0] < obstacle.position[0]:
                        self.position[0] = obstacle.edges[0] - 21
                    if self.position[0] > obstacle.position[0]:
                        self.position[0] = obstacle.edges[2] + 21
                elif self.position[0] > obstacle.edges[0] and self.position[0] < obstacle.edges[2]:
                    if self.position[1] < obstacle.position[1]:
                        self.position[1] = obstacle.edges[3] - 21
                    if self.position[1] > obstacle.position[1]:
                        self.position[1] = obstacle.edges[1] + 21
                self.relax()
                # self.direction_degrees += 180
    
    def summon_boid(self):
        boids.Boid(
                        (self.position[0], self.position[1]), 
                        self,
                        self.obstacles,
                        self.window_size,
                        self.window,
                        self.graphics_lib,
                        show_circles=False
                    )

