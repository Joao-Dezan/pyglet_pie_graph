from enum import Enum
from random import shuffle


class Color(Enum):
    RED = (244, 67, 54)
    GREEN = (76, 175, 80)
    BLUE = (33, 150, 243)
    WHITE = (255, 255, 255)
    BLACK = (20, 20, 20)
    PURPLE = (156, 39, 176)
    ORANGE = (255, 193, 7)
    GRAY = (158, 158, 158)
    AMBER = (255, 193, 7)
    CYAN = (0, 188, 212)
    YELLOW = (255, 235, 59)

    @classmethod
    def generate_colors(cls, amount: int) -> tuple:
        limit = len(cls)
        colors = list(cls)
        shuffle(colors)

        return tuple(
            color.value for color in (colors * ((amount // limit) + 1))[:amount]
        )

    @classmethod
    def auto_contrast_font_color(cls, color: tuple) -> tuple:
        red = color[0]
        green = color[1]
        blue = color[2]

        if (red * 0.299 + green * 0.587 + blue * 0.114) > 186:
            return (0, 0, 0, 255)
        else:
            return (255, 255, 255, 255)
