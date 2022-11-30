import pyglet
from lib.graphic import Pizza
from lib.colors import Color

window = pyglet.window.Window()
window.width = 1000
window.height = 600
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

"""Colors
    RED GREEN BLUE WHITE BLACK PURPLE ORANGE GRAY AMBER CYAN YELLOW
"""

notas = [18, 27, 13, 20, 10]
notas_labels = ("<20", "20-40", "40-60", "60-80", ">80")
frequencias = [140, 60]
colors = ["red", Color.GREEN, "blue", "orange", Color.PURPLE]

pizza1 = Pizza(
    data=notas,
    colors=colors,
    show_labels=True,
    show_legends=True,
    position=(150, window.height // 2),
    legend_texts=notas_labels,
    title="Notas",
    radius=140,
    label_font_size=14,
    legend_font_size=10,
)

pizza2 = Pizza(
    data=frequencias,
    show_labels=True,
    show_legends=True,
    title="Frequências",
    legend_texts=("Aprovados", "Reprovados"),
    colors=("blue", Color.RED),
    position=(650, window.height // 2),
    radius=140,
    legend_font_size=12,
    gap_piece=3,
)


@window.event
def on_draw():
    window.clear()
    pizza1.draw()
    pizza2.draw()


@pyglet.clock.schedule
def update(dt):
    if keys[pyglet.window.key.RIGHT]:
        pizza1.rot += -1
    if keys[pyglet.window.key.LEFT]:
        pizza1.rot += 1
    if keys[pyglet.window.key.UP]:
        pizza2.rot += -1
    if keys[pyglet.window.key.DOWN]:
        pizza2.rot += 1


pyglet.app.run()
