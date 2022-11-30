import pyglet
from pyglet import shapes
from .colors import Color
from .utils import Label


class Group(list):
    def __init__(self):
        super().__init__()

    def draw(self):
        for elem in self:
            elem.draw()


class Legend:
    def __init__(
        self,
        height=60,
        position=(0, 0),
        square_color_size: int = 32,
        font_size: int = 14,
        label: str = None,
        width: int = None,
        square_color: tuple = (255, 255, 255),
        background_color: Color = Color.BLUE.value,
    ):
        self.position = position
        self.square_color = square_color
        self.width = width
        self.height = height
        self.font_size = font_size
        self.square_color_size = square_color_size
        self.background_color = background_color
        self.label = None

        self.set_label(label, font_size=font_size)
        self.set_square_color(square_color)
        self.set_background(
            background_color,
            width,
            height,
        )

    def set_label(self, text, font_size=None):
        x = self.position[0] + self.square_color_size + 20
        y = self.position[1] + (self.height // 2)

        label_color = Color.auto_contrast_font_color(self.background_color)
        font_size = font_size if font_size else self.font_size

        self.label = Label(
            text,
            x=x,
            y=y,
            color=label_color,
            font_size=font_size,
            anchor_x="left",
            anchor_y="center",
        )

    def set_square_color(self, color=None):
        x = self.position[0] + 10
        y = self.position[1] + (self.height // 2 - self.square_color_size // 2)

        self.square_color = self.create_square_color(
            (x, y), color if color else self.square_color, size=self.square_color_size
        )

    def set_background(self, background_color=None, width=None, height=None):
        self.background = shapes.Rectangle(
            self.position[0],
            self.position[1],
            width=width if width else self.width,
            height=height if height else self.height,
            color=background_color if background_color else self.background_color,
        )

    def create_square_color(
        self,
        position,
        color=Color.RED.value,
        size=32,
    ):
        return shapes.Rectangle(
            position[0], position[1], width=size, height=size, color=color
        )

    def draw(self):
        self.set_background()
        self.background.draw()

        if self.label:
            self.label.draw()
        if self.square_color:
            self.square_color.draw()


class LegendsList:
    def __init__(
        self,
        item_height,
        item_count,
        legend_font_size: int = 14,
        square_colors: list = None,
        square_color_size: int = 32,
        label_texts: tuple = None,
        position=(0, 0),
        background_color: Color = Color.BLUE.value,
        item_gap: int = 0,
    ) -> None:
        self.rows = Group()
        self.position = position
        self.label_texts = label_texts
        self.square_colors = square_colors
        self.square_color_size = square_color_size
        self.legend_font_size = legend_font_size
        self.item_gap = item_gap
        self.item_height = item_height
        self.item_count = item_count
        self.background_color = background_color
        self.height = item_height * item_count + (item_gap * item_count - 1)
        self.width = None
        self.esc = (1, 2)
        self.rot = 0

        self.create_rows()

    def create_rows(self):
        pos_x = 0
        pos_y = -self.item_height

        for item in range(self.item_count):
            label_text = self.label_texts[item] if self.label_texts else None
            square_color = self.square_colors[item] if self.square_colors else None
            row = self.create_a_row(
                self.item_height,
                self.width if self.width else 200,
                label_text,
                (pos_x, pos_y),
                self.background_color,
                square_color,
            )
            self.rows.append(row)
            pos_y -= self.item_height + self.item_gap

        if not self.width:
            self.width = self.auto_legend_width()

    def set_width(self, width):
        self.width = width
        for legend in self.rows:
            legend.width = width

    def auto_legend_width(self) -> int:
        longest_label_width = 100

        for legend in self.rows:
            label_width = legend.label.content_width
            longest_label_width = (
                label_width
                if longest_label_width < label_width
                else longest_label_width
            )

        for legend in self.rows:
            legend.width = longest_label_width + self.square_color_size + 30

        return longest_label_width + self.square_color_size + 30

    def create_a_row(
        self, item_height, width, label_text, pos, background_color, square_color
    ) -> Legend:
        legend = Legend(
            item_height,
            width=width,
            square_color_size=self.square_color_size,
            position=pos,
            background_color=background_color,
            label=label_text,
            square_color=square_color,
        )

        return legend

    def draw(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslated(self.position[0], self.position[1], 0)

        self.rows.draw()

        pyglet.gl.glPopMatrix()
