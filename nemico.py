import arcade

class nemico:
    def __init__(self, sprite: arcade.Sprite) -> None:
        self.enemy_list = arcade.SpriteList()
    
        enemy= arcade.Sprite("./assets/nemico.png", scale=SPRITE_SCALING)
        enemy.change_x = 2
        self.enemy_list.append(enemy)