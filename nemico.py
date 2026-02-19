from Endless_Galactic_Ship import WIDTH, HEIGHT 
import arcade
import random

class Enemy(arcade.Sprite):
    def __init__(self, height: int, scale=0.6, speed=4.2):
        super().__init__("./assets/nemico.png", scale=scale)
        
        self.center_x = 950
        self.center_y = random.randint(60, height - 60)  
        
        self.change_x = -speed
        self.change_y = 0

    def update(self):
        super().update()
        if self.right < 0:
            self.remove_from_sprite_lists()