import random
import math

class Boid:
    """
    Initialize the Boid
    @environment_size
    @window
    @graphics_lib
    """
    def __init__(self, environment_size, window, graphics_lib):
        self.graphics_lib = graphics_lib
        self.window = window
        self.environment_size = environment_size

        self.cohesion_radius = random.uniform(50, 60)
        self.alignment_radius = random.uniform(30, 40)
        self.separation_radius = random.uniform(10, 20)
        self.speed_scalar = random.uniform(1,3)
        self.direction_degrees = 0
        self.position = [
            random.randint(10, self.environment_size[0]-10),
            random.randint(10, self.environment_size[1]-10),
        ]
        self.drawable_position = self.calc_drawable(self.direction_degrees * (math.pi / 180), self.position)
    
    def draw(self):
        self.graphics_lib.draw.polygon(self.window, (200, 200, 0), self.drawable_position)
        # self.graphics_lib.draw.rect(self.window, (200, 200, 0), (self.drawable_position[0], self.drawable_position[1], 5, 5))
    
    """
    Calculates the coordinates of each corners of the body of the Boid
    @new_direction_radian
    @new_position
    """
    def calc_drawable(self, new_direction_radian, new_position):
        return (
                (new_position[0], self.environment_size[1] - new_position[1]),
                (new_position[0] + 8 * math.cos(new_direction_radian + 120 * (math.pi / 180)), self.environment_size[1] - (new_position[1] + 8 * math.sin(new_direction_radian + 120 * (math.pi / 180)))),
                (new_position[0] + 15 * math.cos(new_direction_radian), self.environment_size[1] - (new_position[1] + 15 * math.sin(new_direction_radian))),
                (new_position[0] + 8 * math.cos(new_direction_radian - 120 * (math.pi / 180)), self.environment_size[1] - (new_position[1] + 8 * math.sin(new_direction_radian - 120 * (math.pi / 180)))),
               )

    """
    Move the Boid incrementally towards the destination position.
    @destination_position
    """
    def move(self, destination_position):
        # Angle of the Boid when facing @position
        # self.direction_degrees = (180 / math.pi) * math.atan2(destination_position[1]-self.position[1], destination_position[0]-self.position[0])
        # # Incremental X axis and Y axis movement of the Boid towards @position
        # x_movement = self.speed_scalar * math.cos(self.direction_degrees)
        # y_movement = self.speed_scalar * math.sin(self.direction_degrees)
        # print('angle->',(180/math.pi) * self.direction_degrees, ' movement->', (x_movement, y_movement))

        # self.position = [self.position[0]+x_movement, self.position[1]+y_movement]
        self.direction_degrees += 1
        if self.direction_degrees >= 360:
            self.direction_degrees = 0
        self.drawable_position = self.calc_drawable(self.direction_degrees * (math.pi / 180), self.position)
    
    def align(self):
        pass

    def separate(self):
        pass

    def cohere(self):
        pass

    def avoid_edge(self):
        pass
