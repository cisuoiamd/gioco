import arcade
import random

class Enemy(arcade.Sprite):
    def __init__(self, screen_height, scale=0.55, speed=4.2):
        super().__init__("./assets/nemico.png", scale=scale)
        self.center_x = 1500 #modificare questo parametro per far spaware i nemici all'inizio dello schermo a destra (2000 per schermi pc fissi, 1500 per laptop)
        self.center_y = random.randint(100, screen_height - 70)
        self.change_x = -speed
        self.change_y = 0

    def update(self, delta_time):
        super().update(delta_time)
        if self.right < 0:
            self.remove_from_sprite_lists()