
class Block:
    def __init__(
                 self,
                 position: tuple, 
                 size: tuple, 
                 window_size: tuple, 
                 window, 
                 graphics_lib
                ):
        self.graphics_lib = graphics_lib
        self.window = window
        self.window_size = window_size

        self.size = size
        self.position = position
        self.corners = (
                        (self.position[0] - self.size[0] / 2, self.position[1] + self.size[1] / 2),
                        (self.position[0] + self.size[0] / 2, self.position[1] + self.size[1] / 2),
                        (self.position[0] + self.size[0] / 2, self.position[1] - self.size[1] / 2),
                        (self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2)
                      )
        self.edges = (
                        self.corners[0][0],
                        self.corners[1][1],
                        self.corners[2][0],
                        self.corners[3][1]
                     )

        self.color = (100, 100, 100)
    
    def draw(self):
        # drawable_position = (
        #                      self.position[0] - self.size[0] / 2,
        #                      (self.window_size[1] - self.position[1]) - self.size[1] / 2,
        #                      self.size[0] / 2,
        #                      self.size[1] / 2
        #                     )
        drawable_position = (
            (self.corners[0][0], self.window_size[1] - self.corners[0][1]),
            (self.corners[1][0], self.window_size[1] - self.corners[1][1]),
            (self.corners[2][0], self.window_size[1] - self.corners[2][1]),
            (self.corners[3][0], self.window_size[1] - self.corners[3][1]),
        )
        # self.graphics_lib.draw.rect(self.window, self.color, drawable_position)
        self.graphics_lib.draw.polygon(self.window, self.color, drawable_position)
