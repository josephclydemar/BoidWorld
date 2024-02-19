import random

class Boid:
    def __init__(self, environment_size, window, graphics_lib):
        self.graphics_lib = graphics_lib
        self.window = window
        self.environment_size = environment_size
        self.position = [
            random.randint(10, self.environment_size[0]-10),
            random.randint(10, self.environment_size[1]-10),
        ]
        self.drawable_position = [self.position[0], self.environment_size[1]-self.position[1]]
    
    def draw(self):
        self.graphics_lib.draw.rect(self.window, (200, 200, 0), (self.drawable_position[0], self.drawable_position[1], 5, 5))