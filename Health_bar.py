import arcade

class Barra:
    def __init__(self, sprite: arcade.Sprite, percentuale) -> None:
        self.sprite :arcade.Sprite = sprite
        self.percentuale = percentuale


    def on_draw(self):
        x = self.sprite.center_x
        y = self.sprite.center_y+70

        dimensione_barra = self.percentuale * 200

        arcade.draw_rect_filled(arcade.rect.XYWH(x, y, 150, 10), arcade.color.BLACK)
        arcade.draw_rect_filled(arcade.rect.XYWH(x, y, dimensione_barra, 7), arcade.color.GREEN)


