import arcade                       
import random                        # per generare posizione y casuale dei nemici

class Enemy(arcade.Sprite):
    def __init__(self, screen_height, scale=0.55, speed=4.2):
        super().__init__("./assets/nemico.png", scale=scale)
        self.center_x = 1500 #modificare questo parametro per far spaware i nemici all'inizio dello schermo a destra (2000 per schermi pc fissi, 1500 per laptop)
        # così il nemico non esce mai sopra/sotto lo schermo
        #           |
        #           V
        self.center_y = random.randint(100, screen_height - 70)
        #si muove da destra verso sinistra
        self.change_x = -speed

    def update(self, delta_time):
        # Chiama l'update della classe base (muove lo sprite usando change_x/change_y)
        super().update(delta_time)
        
        # Se il nemico è completamente uscito a sinistra dello schermo (right < 0)
        # viene rimosso dalle SpriteList in cui si trova (in questo caso enemy_list)
        if self.right < 0:
            self.remove_from_sprite_lists()     # pulisce la memoria e toglie il nemico dal gioco