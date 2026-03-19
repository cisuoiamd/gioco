import arcade        

class Barra:
    def __init__(self, sprite: arcade.Sprite, percentuale) -> None:
        # Memorizza riferimento allo sprite (giocatore) -> così la barra lo segue
        self.sprite :arcade.Sprite = sprite
        # Percentuale vita (da 0.0 a 1.0) -> passata dal GameView
        self.percentuale = percentuale
    def on_draw(self):
        # Coordinate della barra: centrata sopra il giocatore
        x = self.sprite.center_x
        y = self.sprite.center_y + 70
        # Lunghezza della parte "piena" della barra
        # 140 = lunghezza massima quando percentuale = 1.0
        dimensione_barra = self.percentuale * 140
        # 1. Sfondo nero della barra (sempre 150 pixel di larghezza)
        arcade.draw_rect_filled(arcade.rect.XYWH(x, y, 150, 10), arcade.color.BLACK)
        # 2. Parte verde che rappresenta la vita attuale (la barra verde della vita)
        arcade.draw_rect_filled(arcade.rect.XYWH(x, y, dimensione_barra, 7), arcade.color.GREEN)