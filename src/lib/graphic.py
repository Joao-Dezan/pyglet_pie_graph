import pyglet
from math import sin, cos, radians

from .exceptions import ValueNotValid, InconsistentValue
from .colors import Color
from .utils import Label
from .list import LegendsList


GAP_TITLE = 30  # Distancia entre o titulo e o grafico


class Grupo(list):
    def __init__(self):
        super().__init__()

    def draw(self):
        for elem in self:
            elem.draw()


class Pizza:
    def __init__(
        self,
        data: list,
        position: tuple = (0, 0),
        radius: int = 200,
        colors: list = None,
        show_labels=False,
        show_legends=False,
        title: str = None,
        label_font_size: int = 16,
        legend_font_size: int = 14,
        title_font_size: int = 20,
        label_texts: tuple = None,
        legend_texts: tuple = None,
        gap_piece: int = 0,
    ):
        self.fatias = Grupo()
        self.show_labels = show_labels
        self.show_legends = show_legends
        self.label_font_size = label_font_size
        self.legend_font_size = legend_font_size
        self.title_font_size = title_font_size
        self.colors = Color.generate_colors(len(data)) if not colors else colors
        self.position = position
        self.selected = False
        self.rot = self.title_rot = 0
        self.esc = self.title_esc = (1, 1)
        self.radius = radius
        self.label_texts = label_texts
        self.legend_texts = legend_texts
        self.gap_piece = gap_piece
        self.data = tuple(map(lambda x: x * 100 / sum(data), data))
        self.title = title
        self.legends_list = None

        self.format_colors()
        self.validate_colors()
        self.create_legends()
        self.create_pieces()
        self.create_title()

    def draw(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslated(self.position[0], self.position[1], 0)
        pyglet.gl.glScaled(self.esc[0], self.esc[1], 0)
        pyglet.gl.glRotated(self.rot, 0, 0, 1)

        self.fatias.draw()

        pyglet.gl.glPopMatrix()

        if self.title:
            self.title.draw()

        if self.show_legends and self.legends_list:
            self.legends_list.draw()

    def create_legends(
        self,
        bg_color=Color.WHITE.value,
    ):
        item_count = len(self.data)
        square_color_size = int(self.legend_font_size * 2.5)
        item_height = int(square_color_size + 10)
        item_gap = 1
        x = int(self.position[0] + self.radius + 20)
        y = int(self.position[1] + (item_height * item_count + item_gap) // 2)

        if not self.legend_texts:
            self.legend_texts = self.label_texts

        self.legends_list = LegendsList(
            item_height,
            item_count,
            legend_font_size=self.legend_font_size,
            square_colors=self.colors,
            square_color_size=square_color_size,
            label_texts=self.legend_texts,
            position=(
                x,
                y,
            ),
            background_color=bg_color,
            item_gap=item_gap,
        )

    def create_title(self):
        pos = (
            self.position[0],
            self.position[1] + self.radius + GAP_TITLE,
        )

        if type(self.title) == str:
            self.title = Label(
                self.title,
                x=pos[0],
                y=pos[1],
                color=(255, 255, 255, 255),
                font_size=self.title_font_size,
            )
        self.title.x -= self.title.content_width // 2
        self.title.y += self.title.content_height // 2

    def create_pieces(self):
        position_ini = 0
        position_fim = 0

        label_texts = []
        for index, valor in enumerate(self.data):
            position_fim += int((valor * 360 / 100) - self.gap_piece)

            if position_fim > 360 or index == len(self.data) - 1:
                position_fim = 360 - self.gap_piece

            if self.label_texts:
                label_text = self.label_texts[index]
            else:
                label_text = None

            label_text = format_text_label(label_text, valor)

            label_texts.append(label_text)

            self.fatias += [
                self.create_a_piece(
                    position_ini, position_fim, label_text, color=self.colors[index]
                )
            ]

            position_fim += self.gap_piece
            position_ini = position_fim
        self.label_texts = label_texts

    def create_a_piece(self, position_ini, position_fim, label_text, color):
        fatia = Fatia(position_ini, position_fim, self.radius, cor=color)

        if self.show_labels:
            fatia.add_label(
                text=label_text,
                font_size=self.label_font_size,
            )

        return fatia

    def validate_colors(self):
        if not self.colors:
            raise ValueNotValid(
                "O atributo 'colors' deve seguir o modelo: [Color.WHITE, ...]"
            )

        if len(self.colors) != len(self.data):
            raise InconsistentValue("Deve ser passado uma cor para cada valor!")

    def format_colors(self):
        colors = []
        for color in self.colors:
            try:
                if isinstance(color, Color):
                    color = color.value
                elif type(color) == str:
                    color = Color[color.upper().strip()].value
                elif not type(color) == tuple:
                    raise Exception()
            except:
                raise ValueNotValid(
                    f'Invalid color: "{color}". Try to choose a color in lib/colors Enum class!'
                )
            else:
                colors.append(color)
        self.colors = colors


class Fatia:
    def __init__(self, ini, fim, radius, cor):
        tam = abs(fim - ini) + 2
        self.vert = [0.0, 0.0]
        self.ini = ini
        self.fim = fim
        self.radius = radius
        self.cor = cor
        self.label = None

        for i in range(ini, fim + 1):
            ang = radians(i)
            self.vert += [sin(ang) * radius, cos(ang) * radius]

        self.vert_list = pyglet.graphics.vertex_list(
            tam, ("v2f", self.vert), ("c3B", cor * tam)
        )

    def add_label(self, text, font_size, pos="inner"):
        mid = self.ini + ((self.fim - self.ini) // 2)
        x = sin(radians(mid)) * (self.radius)
        y = cos(radians(mid)) * (self.radius)

        if pos.lower() == "outer":
            anchor_x = "right"
            anchor_y = "bottom"

            if mid < 270 and mid > 90:
                anchor_y = "top"
                x, y = x - 5, y - 5

            if mid > 0 and mid < 180:
                anchor_x = "left"
                x += 5
        else:
            anchor_x = anchor_y = "center"
            x, y = x // 1.5, y // 1.5

        label_color = Color.auto_contrast_font_color(self.cor)

        self.label = Label(
            text,
            x=x,
            y=y,
            color=label_color,
            font_size=font_size,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
        )

    def draw(self):
        self.vert_list.draw(pyglet.gl.GL_TRIANGLE_FAN)

        if self.label:
            self.label.draw()


def format_text_label(text, valor):
    if text != None:
        label_text = text + f" ({valor:.1f}%)"
    else:
        label_text = f"{valor:.1f}%"

    return label_text
