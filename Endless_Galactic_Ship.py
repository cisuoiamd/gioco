import arcade
import random
import Health_bar    
from Nemicobase import Enemy   #da nemicobase importa tutti i parametri di Enemy 

WIDTH = 650  
HEIGHT = 800

# Schermata di splash (è una schermata creata apposta per i crediti) iniziale con nome studio (dura max 3.5 secondi o salta con click)
class Ezuripresents(arcade.View):
    def __init__(self):
        super().__init__()
        self.timer = 0.0                        # contatore per passare automaticamente al menu

    def on_update(self, delta_time):
        self.timer += delta_time                # accumula il tempo reale trascorso
        if self.timer >= 3.5:                   # dopo 3.5 secondi -> vai al menu
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_draw(self):
        self.clear()                            # pulisce lo schermo prima di disegnare
        arcade.draw_text("Ezuri's Studios", WIDTH / 1, HEIGHT / 1.5,
                         arcade.color.WHITE, font_size=150, anchor_x="center")
        arcade.draw_text("Presents:", WIDTH / 1, HEIGHT / 2 - 125,
                         arcade.color.RED, font_size=50, anchor_x="center")
        arcade.draw_text("Click to skip", WIDTH / 1, HEIGHT / 2 - 500,
                         arcade.color.GREEN, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        menu_view = MenuView()
        self.window.show_view(menu_view)        # qualsiasi click -> salta al menu

# Schermata titolo + musica di intro
class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        Intro = arcade.load_sound("./assets/EndlessGalacticShipIntro.mp3")
        self.Intro1 = Intro.play()              # parte la musica e la salva per poterla fermare

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK   # sfondo nero quando appare

    def on_draw(self):
        self.clear()
        arcade.draw_text("ENDLESS GALACTIC SHIP", WIDTH / 1, HEIGHT / 1.5,
                         arcade.color.PURPLE, font_size=95, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 1, HEIGHT / 2 - 255,
                         arcade.color.RED, font_size=20, anchor_x="center")
           
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)
        #donduz è stato qui (easter egg)
        arcade.stop_sound(self.Intro1)          # ferma la musica quando si va avanti
        self.Intro1 = None                      # pulisce il riferimento

# Schermata comandi / istruzioni
class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK

    def on_draw(self):
        self.clear()
        arcade.draw_text("Comands Screen for PC", WIDTH / 1, HEIGHT / 1.3,
                         arcade.color.YELLOW, font_size=95, anchor_x="center")
        arcade.draw_text("Click to start the game", WIDTH / 1, HEIGHT / 2.2 - 330,
                         arcade.color.RED, font_size=30, anchor_x="center")
        arcade.draw_text("Fire = Left Mouse, SPACE", WIDTH / 1, HEIGHT / 2 +100,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Go Up: W", WIDTH / 1, HEIGHT / 2 +0,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Go Down: S", WIDTH / 1, HEIGHT / 2 -100 ,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Go Left: A", WIDTH / 1, HEIGHT / 2 -200 ,
                         arcade.color.WHITE, font_size=40, anchor_x="center")
        arcade.draw_text("Go Right: D", WIDTH / 1, HEIGHT / 2 -300,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)        # click -> inizia la partita

# Schermata game over
class GameOverView(arcade.View):
    def __init__(self, punteggio: int = 0):
        super().__init__()
        self.punteggio = punteggio                           # verrà riempito dopo

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Game Over",
            x=WIDTH / 1,
            y=550,
            color=arcade.color.WHITE,
            font_size=150,
            anchor_x="center"
        )
        arcade.draw_text(
            "You Died",
            x=WIDTH / 1,
            y=300,
            color=arcade.color.RED,
            font_size=200,
            anchor_x="center"
        )
        arcade.draw_text("Press ENTER to restart",
         x=WIDTH / 1,
            y=170,
            color=arcade.color.WHITE,
            font_size=30,
            anchor_x="center"
        )
        arcade.draw_text(f"Final Score: {self.punteggio}",
         x=WIDTH / 1 +400,
            y=60,
            color=arcade.color.WHITE,
            font_size=30,
            anchor_x="center"
        )

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)         # ENTER -> nuova partita

# Schermata di gioco principale
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = arcade.SpriteList()      # lista sprite del giocatore 
        self.bullet_list = arcade.SpriteList()      # tutti i proiettili
        self.enemy_list = arcade.SpriteList()       # tutti i nemici

        self.blaster = arcade.load_sound(path=("./assets/blasterfakesound.wav"))
        self.dead_enemy = arcade.load_sound(path=("./assets/enemy_dead.wav"))
        self.gameover = arcade.load_sound(path=("./assets/gameoversound.wav"))
        self.hurt = arcade.load_sound(path=("./assets/hurtsound.wav"))

        self.shoot_cooldown = 0.4               # secondi tra uno sparo e l'altro
        self.shoot_timer = 0                    # timer countdown per il cooldown

        self.player_speed = 6
        self.bullet_speed = 12

        self.change_x = 0                       # velocità orizzontale attuale
        self.change_y = 0                       # velocità verticale attuale

        self.background = None
        self.player_sprite = None
        self.barra = None

        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 0.3         # ogni quanti secondi spawnare un nemico
        self.enemy_speed = 6
        self.lives = 1.0
        self.punteggio = 0
        self.setup()                            # inizializza tutto

    def setup(self):
        self.background = arcade.load_texture("./assets/sfondo.png")
        self.player_sprite = arcade.Sprite("./assets/shooter.png", scale=0.45)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = HEIGHT // 2  
        self.player_list.clear()
        self.player_list.append(self.player_sprite)     # aggiunge il giocatore alla lista
        self.barra = Health_bar.Barra(self.player_sprite, self.lives)
        self.enemy_list = arcade.SpriteList()
        self.bullet_list.clear()
        self.change_x = 0
        self.change_y = 0
        self.enemy_spawn_timer = 0
        self.lives = 1.0
        self.punteggio = 0

    def spawn_enemy(self):
        nemico = Enemy(screen_height=HEIGHT, scale=0.3, speed=self.enemy_speed)
        self.enemy_list.append(nemico)          # aggiunge il nemico alla lista

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
        arcade.draw_text(f"Killed: {self.punteggio}",
                         50,
                         self.window.height - 50,
                         arcade.color.WHITE,
                         font_size=24,
                         anchor_x="left")
        arcade.draw_text("Press ESC to pause",
                         self.window.width // 2,
                         self.window.height - 50,
                         arcade.color.WHITE,
                         font_size=30,
                         anchor_x="center")

    def on_update(self, delta_time):
        self.player_sprite.center_x += self.change_x    # applica movimento orizzontale
        self.player_sprite.center_y += self.change_y    # applica movimento verticale

        if self.shoot_timer > 0:
            self.shoot_timer -= delta_time              # decrementa cooldown sparo

        self.bullet_list.update()                       # muove tutti i proiettili

        for bullet in self.bullet_list[:]:
            if bullet.left > self.window.width:
                bullet.remove_from_sprite_lists()       # elimina proiettili usciti dallo schermo

        self.enemy_spawn_timer += delta_time
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0                  # resetta timer spawn

        self.enemy_list.update()                        # muove/aggiorna tutti i nemici

        # Collisione proiettili → nemici
        for bullet in self.bullet_list[:]:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            for enemy in hit_list:
                arcade.play_sound(self.dead_enemy)
                bullet.remove_from_sprite_lists()
                enemy.remove_from_sprite_lists()
                self.punteggio += 1

        # Collisione giocatore → nemici
        for enemy in self.enemy_list[:]:
            if arcade.check_for_collision(self.player_sprite, enemy):
                arcade.play_sound(self.hurt)
                self.lives -= 0.125
                if self.lives < 0:
                    self.lives = 0
                enemy.remove_from_sprite_lists()        # nemico scompare dopo contatto

        self.barra.percentuale = self.lives             # aggiorna barra vita

        if (self.lives) == 0:
            arcade.play_sound(self.gameover)
            game_over_view = GameOverView(self.punteggio)
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)       # game over -> cambia schermata

    def shoot(self):
        if self.shoot_timer > 0:
            return                                      # ancora in cooldown -> non spara
      
        self.shoot_timer = self.shoot_cooldown          # resetta timer cooldown

        bullet = arcade.Sprite("./assets/laser.png", scale=0.17)
        bullet.center_x = self.player_sprite.center_x + 90
        bullet.center_y = self.player_sprite.center_y + 15
        bullet.change_x = self.bullet_speed             # proiettile va a destra
        bullet.change_y = 0
        self.bullet_list.append(bullet)                 # aggiunge alla lista proiettili
        arcade.play_sound(self.blaster)

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
            self.window.show_view(pause)                # ESC -> pausa

        if key == arcade.key.SPACE:
            self.shoot()
        if key == arcade.key.SPACE:                     # duplicato (ridondante)
            if self.shoot_timer <= 0:
                self.shoot()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.change_y = 0                           # ferma movimento verticale
        if key == arcade.key.A or key == arcade.key.D:
            self.change_x = 0                           # ferma movimento orizzontale

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.shoot_timer <= 0: 
                self.shoot()                            # click sinistro = sparo

# Schermata pausa
class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view                  # tiene riferimento al gioco per riprendere

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
        self.game_view.enemy_list.draw()

        overlay_color = arcade.color.BLACK[:3] + (128,)     # nero semitrasparente
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=self.window.width,
            bottom=0,
            top=self.window.height,
            color=overlay_color
        )
        arcade.draw_text("PAUSE",
                         self.window.width / 2,
                         self.window.height / 2 + 150,
                         arcade.color.WHITE,
                         font_size=150,
                         anchor_x="center")
        arcade.draw_text("Press ESC to resume",
                         self.window.width / 2,
                         self.window.height / 2 - 30,
                         arcade.color.WHITE,
                         font_size=40,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)   # ESC -> riprende gioco

# Avvio del programma
def main():
    window = arcade.Window(WIDTH, HEIGHT, "Endless Galactic Ship", fullscreen=True)
    splash = Ezuripresents()
    window.show_view(splash)
    arcade.run()

if __name__ == "__main__":
    main()