import arcade
import Health_bar
from nemico import Enemy
WIDTH = 900
HEIGHT = 600

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.enemy_list = arcade.SpriteList()
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 2.8 
        self.enemy_speed = 4.2            
        self.lives = 1.0                
    def spawn_enemy(self):
        nemico = Enemy(height=HEIGHT, scale=0.55, speed=self.enemy_speed)
        self.enemy_list.append(nemico)
    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.enemy_spawn_timer = 0
        self.lives = 1.0
        self.barra = Health_bar.Barra(self.player_sprite, self.lives) 

    def spawn_enemy(self):
        nemico = Enemy(scale=0.55, speed=self.enemy_speed)
        self.enemy_list.append(nemico)

    def on_update(self, delta_time):
        self.player_sprite.center_x += self.change_x
        self.player_sprite.center_y += self.change_y
        self.bullet_list.update()
        for bullet in self.bullet_list[:]:
            if bullet.left > self.window.width:
                bullet.remove_from_sprite_lists()

        # ------------------- NEMICI -------------------
        self.enemy_spawn_timer += delta_time
        
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
        self.enemy_list.update()
        for enemy in self.enemy_list[:]:   
            if arcade.check_for_collision(self.player_sprite, enemy):
                self.lives -= 0.10
                if self.lives < 0:
                    self.lives = 0
                enemy.remove_from_sprite_lists()
        self.barra.percentuale = self.lives

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show_view(self):
        self.window.background_color = arcade.color.ORANGE  

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.game_view.background,
            rect=arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        
        self.game_view.player_list.draw()
        self.game_view.bullet_list.draw()
        self.game_view.barra.on_draw()
        overlay_color = arcade.color.BLACK[:3] + (128,)
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=self.window.width,
            bottom=0,
            top=self.window.height,
            color=overlay_color
        )
        arcade.draw_text("PAUSE",
                         self.window.width / 2,
                         self.window.height / 2 + 50,
                         arcade.color.WHITE,
                         font_size=50,
                         anchor_x="center")
        arcade.draw_text("Press ESC to continue",
                         self.window.width / 2,
                         self.window.height / 2,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press ENTER to reset",
                         self.window.width / 2,
                         self.window.height / 2 - 30,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)

def main():
    window = arcade.Window(WIDTH, HEIGHT, "Endless Galactic Ship", fullscreen=True)
    game_view = GameView()
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()