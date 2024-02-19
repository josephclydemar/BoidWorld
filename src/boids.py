import random
import math

class Boid:
    """
        @environment_size
        @window
        @graphics_lib
    """
    def __init__(self, environment_size, window, graphics_lib):
        self.graphics_lib = graphics_lib
        self.window = window
        self.environment_size = environment_size

        self.speed_scalar = random.uniform(1,3)
        self.direction_radian = 0
        self.position = [
            random.randint(10, self.environment_size[0]-10),
            random.randint(10, self.environment_size[1]-10),
        ]
        self.drawable_position = self.update_drawable_position(self.position)
    
    def draw(self):
        self.graphics_lib.draw.rect(self.window, (200, 200, 0), (self.drawable_position[0], self.drawable_position[1], 5, 5))
    
    def update_drawable_position(self, new_position):
        return [new_position[0], self.environment_size[1]-new_position[1]]

    """
        @destination_position
    """
    def move(self, destination_position):
        # Angle of the Boid when facing @position
        self.direction_radian = math.atan2(destination_position[1]-self.position[1], destination_position[0]-self.position[0])
        # Incremental X axis and Y axis movement of the Boid towards @position
        x_movement = self.speed_scalar * math.cos(self.direction_radian)
        y_movement = self.speed_scalar * math.sin(self.direction_radian)
        # print('angle->',(180/math.pi) * self.direction_radian, ' movement->', (x_movement, y_movement))

        self.position = [self.position[0]+x_movement, self.position[1]+y_movement]
        self.drawable_position = self.update_drawable_position(self.position)
