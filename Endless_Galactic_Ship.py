import arcade

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)

        self.sprite = None
        self.playerSpriteList = arcade.SpriteList()

        self.speed = 6
        self.change_x = 0
        self.change_y = 0

        self.setup()

    def setup(self):
        self.sprite = arcade.Sprite("./assets/shooter.png")
        self.sprite.center_x = 100
        self.sprite.center_y = 300
        self.playerSpriteList.append(self.sprite)

        self.background = arcade.load_texture("./assets/sfondo.png")

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0,0,self.width,self.height)
        )
        self.playerSpriteList.draw()

    def on_update(self, delta_time):
        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y
        self.sprite.width=150
        self.sprite.height=200

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.change_y = self.speed
        elif key == arcade.key.S:
            self.change_y = -self.speed
        elif key == arcade.key.A:
            self.change_x = -self.speed
        elif key == arcade.key.D:
            self.change_x = self.speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.change_x = 0


def main():
    game = MyGame(600, 600, "Endless Galactic Ship")
    arcade.run()


if __name__ == "__main__":
    main()
