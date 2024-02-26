import random
import math

import calcs

class Boid:
    all_boids = []
    """
    * Initialize the Boid
    @window_size
    @window
    @graphics_lib
    @show_circles
    """
    def __init__(self, position, spawner, window_size, window, graphics_lib, show_circles=False):
        self.graphics_lib = graphics_lib
        self.window = window
        self.window_size = window_size
        self.show_circles = show_circles

        self.spawner = spawner

        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

        self.dt = 1
        
        self.do_cohesion = True
        self.cohesion_radius = random.uniform(95, 105)
        self.cohesion_burst_speed = random.uniform(7, 8)
        self.cohesion_circle_color = (self.color[0], self.color[1], self.color[2])

        self.do_alignment = True
        self.alignment_radius = random.uniform(65, 75)
        self.alignment_burst_speed = random.uniform(10, 15)
        self.alignment_circle_color = (self.color[0], self.color[1], self.color[2])

        self.do_separation = True
        self.separation_radius = random.uniform(25, 35)
        self.separation_burst_speed = random.uniform(30, 40)
        self.separation_circle_color = (self.color[0], self.color[1], self.color[2])

        self.relaxed_speed = random.uniform(2, 4)
        self.speed_scalar = self.relaxed_speed
        self.steering_speed = random.uniform(1, 2)
        self.direction_degrees = random.uniform(0, 359)
        self.position = position

        self.tail = []

        self.my_neigbors = None

        Boid.all_boids.append(self)

        for boid in Boid.all_boids:
            boid.get_neigbors()
    
    def draw(self, fps):
        if fps > 0:
            self.dt = 60 / fps
        new_direction_radian = (math.pi / 180) * self.direction_degrees
        drawable_position = (
                (self.position[0] - 12 * math.cos(new_direction_radian), self.window_size[1] - (self.position[1] - 12 * math.sin(new_direction_radian))),
                (self.position[0] + 6.4 * math.cos(new_direction_radian + 120 * (math.pi / 180)), self.window_size[1] - (self.position[1] + 6.4 * math.sin(new_direction_radian + 120 * (math.pi / 180)))),
                (self.position[0] + 12 * math.cos(new_direction_radian), self.window_size[1] - (self.position[1] + 12 * math.sin(new_direction_radian))),
                (self.position[0] + 6.4 * math.cos(new_direction_radian - 120 * (math.pi / 180)), self.window_size[1] - (self.position[1] + 6.4 * math.sin(new_direction_radian - 120 * (math.pi / 180)))),
               )
        self.tail.append(drawable_position[0])
        if len(self.tail) > 4:
            self.tail.remove(self.tail[0])
        if len(self.tail) > 2:
            self.graphics_lib.draw.lines(self.window, self.color, False, self.tail, 1)
        if self.show_circles:
            self.graphics_lib.draw.circle(self.window, self.cohesion_circle_color, drawable_position[0], self.cohesion_radius, 1)
            self.graphics_lib.draw.circle(self.window, self.alignment_circle_color, drawable_position[0], self.alignment_radius, 1)
            self.graphics_lib.draw.circle(self.window, self.separation_circle_color, drawable_position[0], self.separation_radius, 1)
        self.graphics_lib.draw.polygon(self.window, self.color, drawable_position)


    """
    * Moves the Boid incrementally towards the destination position.
    @dest_position
    """
    def move(self, dest_position):
        desired_direction_degrees = (180 / math.pi) * math.atan2(dest_position[1]-self.position[1], dest_position[0]-self.position[0])
        self.steer(desired_direction_degrees)
        x_increment = self.dt * self.speed_scalar * math.cos(self.direction_degrees * (math.pi / 180))
        y_increment = self.dt * self.speed_scalar * math.sin(self.direction_degrees * (math.pi / 180))

        self.position = [self.position[0]+x_increment, self.position[1]+y_increment]
        self.avoid_edge()
        if self.direction_degrees >= 360:
            self.direction_degrees = self.direction_degrees - 360
    
    """
    * Steers the Boid towards a particular angle/direction
    @dest_direction_degrees
    """
    def steer(self, dest_direction_degrees):
        # steering_speed = abs(self.direction_degrees - dest_direction_degrees) / 180
        # self.direction_degrees += steering_speed
        if self.direction_degrees > dest_direction_degrees + 10:
            # self.direction_degrees -= steering_speed
            self.direction_degrees -= self.steering_speed
        elif self.direction_degrees < dest_direction_degrees - 10:
            # self.direction_degrees += steering_speed
            self.direction_degrees += self.steering_speed
        # self.direction_degrees = dest_direction_degrees
    

    def cohere_burst(self):
        self.speed_scalar = self.cohesion_burst_speed
    

    def relax(self):
        self.speed_scalar = self.relaxed_speed
    

    def avoid_edge(self):
        if self.position[0] < 10:
            self.direction_degrees += 180
        elif self.position[0] > self.window_size[0] - 10:
            self.direction_degrees += 180
        
        if self.position[1] < 10:
            self.direction_degrees += 180
        elif self.position[1] > self.window_size[1] - 10:
            self.direction_degrees += 180
        
        if self.position[0] < -20 or self.position[0] > self.window_size[0] + 20:
            # self.position[0] = random.randint(100, self.window_size[0]-100)
            self.position[0] = 550
        if self.position[1] < -20 or self.position[1] > self.window_size[1] + 20:
            # self.position[1] = random.randint(100, self.window_size[1]-100)
            self.position[1] = 300


    """
    * Receives the positions of all other Boids
    @others
    """
    def get_neigbors(self):
        self.my_neigbors = list(map(lambda boid: boid, list(filter(lambda boid: boid != self, Boid.all_boids))))
    
    """
    * Filters other Boids that are within the passed radius
    @radius
    """
    def filter_neigbors_within_radius(self, radius):
        seen_neigbors = []
        for neigbor in self.my_neigbors:
            if calcs.calc_distance(neigbor.position, self.position) <= radius:
                seen_neigbors.append(neigbor)
        return seen_neigbors
    
    def align(self):
        pass

    def separate(self):
        pass

    def cohere(self):
        pass