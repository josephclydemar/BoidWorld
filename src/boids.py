import random
import math

import calcs

class Boid:
    all_boids = []
    def __init__(
                 self,
                 position, 
                 summoner, 
                 obstacles,
                 window_size, 
                 window, 
                 graphics_lib, 
                 show_circles=False
                ):
        self.graphics_lib = graphics_lib
        self.window = window
        self.window_size = window_size
        self.show_circles = show_circles

        self.summoner = summoner
        self.obstacles = obstacles

        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        # self.color = (255,50,50)

        self.dt = 1
        
        self.cohesion_radius = random.uniform(95, 105)
        self.alone_speed = random.uniform(7, 8)
        self.cohesion_circle_color = (self.color[0], self.color[1], self.color[2])

        self.alignment_radius = random.uniform(65, 75)
        self.alignment_burst_speed = random.uniform(10, 15)
        self.alignment_circle_color = (self.color[0], self.color[1], self.color[2])

        self.is_too_crowded = False
        self.separation_radius = random.uniform(25, 35)
        self.separation_burst_speed = random.uniform(20, 25)
        self.separation_circle_color = (self.color[0], self.color[1], self.color[2])

        self.relaxed_speed = random.uniform(2, 4)
        self.speed_scalar = self.relaxed_speed
        self.steering_speed = random.uniform(1, 2)
        self.direction_degrees = random.uniform(0, 359)
        self.position = position

        self.tail = []

        self.my_neigbors = None
        self.neigbors_within_cohesion_radius = []
        self.neigbors_within_alignment_radius = []

        Boid.all_boids.append(self)
        for boid in Boid.all_boids:
            boid.get_neigbors()
    
    # Draws the Boid to the screen.
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
        if len(self.tail) > 5:
            self.tail.remove(self.tail[0])
        if len(self.tail) > 2:
            self.graphics_lib.draw.lines(self.window, self.color, False, self.tail, 1)
        if self.show_circles:
            self.graphics_lib.draw.circle(self.window, self.cohesion_circle_color, drawable_position[0], self.cohesion_radius, 1)
            self.graphics_lib.draw.circle(self.window, self.alignment_circle_color, drawable_position[0], self.alignment_radius, 1)
            self.graphics_lib.draw.circle(self.window, self.separation_circle_color, drawable_position[0], self.separation_radius, 1)
        self.graphics_lib.draw.polygon(self.window, self.color, drawable_position)
        if not(self.is_too_crowded):
            self.cohere()
            self.align()


    # Moves the Boid incrementally towards a desired position.
    def move(self, dest_position, direction=1):
        desired_direction_degrees = (180 / math.pi) * math.atan2(dest_position[1]-self.position[1], dest_position[0]-self.position[0])
        if direction < 0:
            desired_direction_degrees += 180
        
        if desired_direction_degrees >= 360:
            desired_direction_degrees = desired_direction_degrees - 360

        self.steer(desired_direction_degrees)
        x_increment = self.dt * self.speed_scalar * math.cos(self.direction_degrees * (math.pi / 180))
        y_increment = self.dt * self.speed_scalar * math.sin(self.direction_degrees * (math.pi / 180))

        self.position = [self.position[0]+x_increment, self.position[1]+y_increment]

        self.avoid_obstacles()
    
    # Steer the Boid towards a desired angle/direction.
    def steer(self, dest_direction_degrees, steering_force=1):
        if self.direction_degrees > dest_direction_degrees + 10:
            self.direction_degrees -= self.steering_speed * steering_force
        elif self.direction_degrees < dest_direction_degrees - 10:
            self.direction_degrees += self.steering_speed * steering_force


        # # Constrainting the Boid angle within 0 to 360
        # if self.direction_degrees < 0:
        #     self.direction_degrees = self.direction_degrees + 360
        # if self.direction_degrees >= 360:
        #     self.direction_degrees = self.direction_degrees - 360

        # #! Potential Fix for incorrect Boid Steering (Not Yet Fully Tested)
        # if dest_direction_degrees > self.direction_degrees:
        #     subcircle0 = self.direction_degrees + (360 - dest_direction_degrees)
        #     subcircle1 = dest_direction_degrees - self.direction_degrees
        #     if subcircle0 < subcircle1: # Clockwise
        #         self.direction_degrees -= self.steering_speed * steering_force
        #     elif subcircle0 > subcircle1: # Counter-Clockwise
        #         self.direction_degrees += self.steering_speed * steering_force
        #     else: # Random between Clockwise or Counter-Clockwise
        #         self.direction_degrees += self.steering_speed * steering_force * random.randint(-1, 1)
        # if dest_direction_degrees < self.direction_degrees:
        #     subcircle0 = dest_direction_degrees + (360 - self.direction_degrees)
        #     subcircle1 = self.direction_degrees - dest_direction_degrees
        #     if subcircle0 < subcircle1: # Counter-Clockwise
        #         self.direction_degrees += self.steering_speed * steering_force
        #     elif subcircle0 > subcircle1: # Clockwise
        #         self.direction_degrees -= self.steering_speed * steering_force
        #     else: # Random between Clockwise or Counter-Clockwise
        #         self.direction_degrees += self.steering_speed * steering_force * random.randint(-1, 1)
        
    # Speed up the Boid.
    def burst(self):
        self.speed_scalar = self.alone_speed
    
    # Slow down the Boid.
    def relax(self):
        self.speed_scalar = self.relaxed_speed
    

    def avoid_obstacles(self):
        if self.position[0] < 10:
            self.position[0] = 11
            self.direction_degrees += 180
        elif self.position[0] > self.window_size[0] - 10:
            self.position[0] = self.window_size[0] - 11
            self.direction_degrees += 180
        
        if self.position[1] < 10:
            self.position[1] = 11
            self.direction_degrees += 180
        elif self.position[1] > self.window_size[1] - 10:
            self.position[1] = self.window_size[1] - 11
            self.direction_degrees += 180
        
        if self.position[0] < -20 or self.position[0] > self.window_size[0] + 20:
            # self.position[0] = random.randint(100, self.window_size[0]-100)
            self.position[0] = 550
        if self.position[1] < -20 or self.position[1] > self.window_size[1] + 20:
            # self.position[1] = random.randint(100, self.window_size[1]-100)
            self.position[1] = 300
        

        for obstacle in self.obstacles:
            if ((self.position[0] + 10 > obstacle.edges[0]) and (self.position[0] - 10 < obstacle.edges[2])) and ((self.position[1] + 10 > obstacle.edges[3]) and (self.position[1] - 10 < obstacle.edges[1])):
                if self.position[1] > obstacle.edges[3] and self.position[1] < obstacle.edges[1]:
                    if self.position[0] < obstacle.position[0]:
                        self.position[0] = obstacle.edges[0] - 11
                    if self.position[0] > obstacle.position[0]:
                        self.position[0] = obstacle.edges[2] + 11
                elif self.position[0] > obstacle.edges[0] and self.position[0] < obstacle.edges[2]:
                    if self.position[1] < obstacle.position[1]:
                        self.position[1] = obstacle.edges[3] - 11
                    if self.position[1] > obstacle.position[1]:
                        self.position[1] = obstacle.edges[1] + 11
                self.direction_degrees += 180


    # Receives the positions of all other Boids.
    def get_neigbors(self):
        self.my_neigbors = list(map(lambda boid: boid, list(filter(lambda boid: boid != self, Boid.all_boids))))
    
    # Filters other Boids that are within a given radius.
    def filter_neigbors_within_radius(self, boids_collection, radius):
        seen_neigbors = []
        for neigbor in boids_collection:
            if calcs.calc_distance(neigbor.position, self.position) <= radius:
                seen_neigbors.append(neigbor)
        return seen_neigbors
    
    # Align to the average direction/angle of other Boids that are within the alignment radius.
    def align(self):
        self.neigbors_within_alignment_radius = self.filter_neigbors_within_radius(self.neigbors_within_cohesion_radius, self.alignment_radius)
        total_direction_degrees = 0
        for neigbor in self.neigbors_within_alignment_radius:
            total_direction_degrees += neigbor.direction_degrees
        if len(self.neigbors_within_alignment_radius) != 0:
            average_close_neigbors_direction = total_direction_degrees / len(self.neigbors_within_alignment_radius)
            self.steer(average_close_neigbors_direction, steering_force=3)

    # Move away from other Boids that are too close.
    def separate(self):
        pass

    # Move to the average position of other Boids that are within the cohesion radius.
    def cohere(self):
        self.neigbors_within_cohesion_radius = self.filter_neigbors_within_radius(self.my_neigbors, self.cohesion_radius)
        total_xy = [0, 0]
        for neigbor in self.neigbors_within_cohesion_radius:
            if len(self.neigbors_within_cohesion_radius) == 0:
                break
            total_xy[0] += neigbor.position[0]
            total_xy[1] += neigbor.position[1]
        if len(self.neigbors_within_cohesion_radius) != 0:
            average_close_neigbors_position = (
                    total_xy[0]/len(self.neigbors_within_cohesion_radius),
                    total_xy[1]/len(self.neigbors_within_cohesion_radius),
                )
            self.speed_scalar = self.relaxed_speed
            self.move(average_close_neigbors_position, 1)
        else:
            self.speed_scalar = self.alone_speed
            self.move((self.summoner.position[0], self.window_size[1]-self.summoner.position[1]))
    

    def find_summoner(self):
        pass

    # Follow a path given by the summoner.
    def follow_path(self):
        pass

