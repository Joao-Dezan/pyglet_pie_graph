import pyglet
from .graphic import Grupo


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.elements = Grupo()

    def on_draw(self):
        self.clear()
        for element in self.elements:
            element.draw()

    def add_element(self, element):
        self.elements.append(element)
