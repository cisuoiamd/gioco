import arcade
import Barra
class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(900, 600, "Endless Galactic Ship", fullscreen=True)
        
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        
        self.player_speed = 6
        self.bullet_speed = 12
        
        self.change_x = 0
        self.change_y = 0
        
        self.background = None
        self.player_sprite = None
        
        self.setup()

    def setup(self):
        self.background = arcade.load_texture("./assets/sfondo.png")
        
        self.player_sprite = arcade.Sprite("./assets/shooter.png", scale=0.5)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = self.height // 2
        self.player_list.append(self.player_sprite)
        self.barra = Barra.Barra(self.player_sprite, 0.7)


    def on_draw(self):
        self.clear()
        
        arcade.draw_texture_rect(
            self.background,
            rect=arcade.LBWH(0, 0, self.width, self.height)
        )
        
        self.player_list.draw()
        self.bullet_list.draw()

        self.barra.on_draw()

    def on_update(self, delta_time):
        self.player_sprite.center_x += self.change_x
        self.player_sprite.center_y += self.change_y
        self.barra.percentuale -= 0.001
        
        self.bullet_list.update()
        
        for bullet in self.bullet_list:
            if bullet.left > self.width:
                bullet.remove_from_sprite_lists()

    def shoot(self):
        bullet = arcade.Sprite("./assets/laser.png", scale=0.17)
        
        bullet.center_x = self.player_sprite.center_x +90
        bullet.center_y = self.player_sprite.center_y +15
        bullet.change_x = self.bullet_speed
        bullet.change_y = 0
        
        self.bullet_list.append(bullet)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.change_y = self.player_speed
        elif key == arcade.key.S:
            self.change_y = -self.player_speed
        elif key == arcade.key.A:
            self.change_x = -self.player_speed
        elif key == arcade.key.D:
            self.change_x = self.player_speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.change_y = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot()

def main():
    game = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()