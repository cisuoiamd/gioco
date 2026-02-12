import arcade

class nemico:
    def setup(self):
        self.enemy_list = arcade.SpriteList()
    
        enemy= arcade.Sprite("./assets/nemico.png", scale=SPRITE_SCALING)
        enemy.change_x = 2
        self.enemy_list.append(enemy)
        enemy.boundary_right = SPRITE_SIZE * 8
        enemy.boundary_left = SPRITE_SIZE * 3
        enemy.change_x = 2
        self.enemy_list.append(enemy)