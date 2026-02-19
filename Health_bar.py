import arcade   

class Barra:
    def __init__(self, sprite: arcade.Sprite, percentuale=1.0) -> None:
        self.sprite = sprite
        self.percentuale = percentuale
        self.max_width = 180

    def on_draw(self):
        x = self.sprite.center_x
        y = self.sprite.center_y + 70

        arcade.draw_rect_filled(
            arcade.rect.XYWH(x, y, self.max_width, 12),
            arcade.color.BLACK
        )
        
        green_width = self.percentuale * self.max_width
        arcade.draw_rect_filled(
            arcade.rect.XYWH(x, y, green_width, 9),
            arcade.color.GREEN
        )
        
        # opzionale
        arcade.draw_rect_outline(
            arcade.rect.XYWH(x, y, self.max_width, 12),
            arcade.color.WHITE, border_width=2
        )