import arcade
import Health_bar
from Nemicobase import Enemy

WIDTH = 900
HEIGHT = 900

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        
        self.shoot_cooldown = 0.4          
        self.shoot_timer = 0
        
        self.player_speed = 6
        self.bullet_speed = 12
        
        self.change_x = 0
        self.change_y = 0
        
        self.background = None
        self.player_sprite = None
        self.barra = None
        
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 0.4
        self.enemy_speed = 6
        self.lives = 1.0
        self.score = 0
        
        self.setup()

    def setup(self):
        self.background = arcade.load_texture("./assets/sfondo.png")
        self.player_sprite = arcade.Sprite("./assets/shooter.png", scale=0.45)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = HEIGHT // 2  
        self.player_list.clear()
        self.player_list.append(self.player_sprite)
        self.barra = Health_bar.Barra(self.player_sprite, self.lives)
        
        self.enemy_list = arcade.SpriteList()
        self.bullet_list.clear()
        self.change_x = 0
        self.change_y = 0
        self.enemy_spawn_timer = 0
        self.lives = 1.0
        self.score = 0

    def spawn_enemy(self):
        nemico = Enemy(screen_height=HEIGHT, scale=0.3, speed=self.enemy_speed)
        self.enemy_list.append(nemico)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background,
            rect=arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        self.enemy_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()
        self.barra.on_draw()
        
        arcade.draw_text(f"Killed: {self.score}",
                         50,
                         self.window.height - 50,
                         arcade.color.WHITE,
                         font_size=24,
                         anchor_x="left")
        
        arcade.draw_text("Press ESC to pause",
                         self.window.width // 2,
                         self.window.height - 50,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

    def on_update(self, delta_time):
        self.player_sprite.center_x += self.change_x
        self.player_sprite.center_y += self.change_y
        if self.shoot_timer > 0:
            self.shoot_timer -= delta_time
        self.bullet_list.update()
        for bullet in self.bullet_list[:]:
            if bullet.left > self.window.width:
                bullet.remove_from_sprite_lists()
        
        self.enemy_spawn_timer += delta_time
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
        
        self.enemy_list.update()

        for bullet in self.bullet_list[:]:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                bullet.remove_from_sprite_lists()
                enemy.remove_from_sprite_lists()
                self.score += 1
        for enemy in self.enemy_list[:]:
            if arcade.check_for_collision(self.player_sprite, enemy):
                self.lives -= 0.10
                if self.lives < 0:
                    self.lives = 0
                enemy.remove_from_sprite_lists()
        
        self.barra.percentuale = self.lives

    def shoot(self):
        if self.shoot_timer > 0:
            return      
        self.shoot_timer = self.shoot_cooldown  
        bullet = arcade.Sprite("./assets/laser.png", scale=0.17)
        bullet.center_x = self.player_sprite.center_x + 90
        bullet.center_y = self.player_sprite.center_y + 15
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
        if key == arcade.key.ESCAPE:
            pause = PauseView(self)
            self.window.show_view(pause)
        if key == arcade.key.SPACE:
            self.shoot()
        if key == arcade.key.SPACE:
            if self.shoot_timer <= 0:
                self.shoot()
    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.change_y = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.change_x = 0
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.shoot_timer <= 0: 
                self.shoot()
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