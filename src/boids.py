import random
import math

class Boid:
    """
    Initialize the Boid
    @window_size
    @window
    @graphics_lib
    """
    def __init__(self, window_size, window, graphics_lib):
        self.graphics_lib = graphics_lib
        self.window = window
        self.window_size = window_size

        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

        self.cohesion_radius = random.uniform(50, 60)
        self.alignment_radius = random.uniform(30, 40)
        self.separation_radius = random.uniform(10, 20)

        self.speed_scalar = random.uniform(1,2)
        self.direction_degrees = 0
        self.position = [
            random.randint(10, self.window_size[0]-10),
            random.randint(10, self.window_size[1]-10),
        ]
        self.drawable_position = self.calc_drawable(self.direction_degrees * (math.pi / 180), self.position)
        
        self.my_neigbors = None
    
    def draw(self):
        self.graphics_lib.draw.polygon(self.window, self.color, self.drawable_position)
        # self.graphics_lib.draw.rect(self.window, (200, 200, 0), (self.drawable_position[0], self.drawable_position[1], 5, 5))
    
    """
    Calculates the coordinates of each corners of the body of the Boid
    @new_direction_radian
    @new_position
    """
    def calc_drawable(self, new_direction_radian, new_position):
        return (
                (new_position[0], self.window_size[1] - new_position[1]),
                (new_position[0] + 8 * math.cos(new_direction_radian + 120 * (math.pi / 180)), self.window_size[1] - (new_position[1] + 8 * math.sin(new_direction_radian + 120 * (math.pi / 180)))),
                (new_position[0] + 15 * math.cos(new_direction_radian), self.window_size[1] - (new_position[1] + 15 * math.sin(new_direction_radian))),
                (new_position[0] + 8 * math.cos(new_direction_radian - 120 * (math.pi / 180)), self.window_size[1] - (new_position[1] + 8 * math.sin(new_direction_radian - 120 * (math.pi / 180)))),
               )

    """
    Move the Boid incrementally towards the destination position.
    @dest_position
    """
    def move(self, dest_position):
        desired_direction_degrees = (180 / math.pi) * math.atan2(dest_position[1]-self.position[1], dest_position[0]-self.position[0])
        self.steer(desired_direction_degrees)
        x_increment = self.speed_scalar * math.cos(self.direction_degrees * (math.pi / 180))
        y_increment = self.speed_scalar * math.sin(self.direction_degrees * (math.pi / 180))

        self.position = [self.position[0]+x_increment, self.position[1]+y_increment]
        self.avoid_edge()
        if self.direction_degrees >= 360:
            self.direction_degrees = 0
        self.drawable_position = self.calc_drawable(self.direction_degrees * (math.pi / 180), self.position)
    
    def steer(self, dest_direction_degrees):
        if self.direction_degrees > dest_direction_degrees + 10:
            self.direction_degrees -= 1
        elif self.direction_degrees < dest_direction_degrees - 10:
            self.direction_degrees += 1

    
    def get_neigbors(self, others):
        print(self.position, ' -> ', others)
        self.my_neigbors = others
    
    def align(self):
        pass

    def separate(self):
        pass

    def cohere(self):
        pass

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
