from time import sleep
import pyglet
from lib.graphic import Pizza
from lib.colors import Color


pyglet.options["debug_gl"] = False


def is_mouse_over_square(
    square_pos: tuple, square_width: int, square_height: int, mouse_pos: tuple
):
    mouse_x, mouse_y = mouse_pos
    square_x, square_y = square_pos
    square_ini_x = square_x
    square_end_x = square_x + square_width
    square_ini_y = square_y
    square_end_y = square_y - square_height

    return (
        mouse_x >= square_ini_x
        and mouse_x <= square_end_x
        and mouse_y <= square_ini_y
        and mouse_y >= square_end_y
    )


def is_mouse_over_pie(pie_pos: tuple, pie_radius: int, mouse_pos: tuple):
    mouse_x, mouse_y = mouse_pos
    pie_x, pie_y = pie_pos
    pie_ini_x = pie_x - pie_radius
    pie_end_x = pie_x + pie_radius
    pie_ini_y = pie_y - pie_radius
    pie_end_y = pie_y + pie_radius

    return (
        mouse_x >= pie_ini_x
        and mouse_x <= pie_end_x
        and mouse_y >= pie_ini_y
        and mouse_y <= pie_end_y
    )


window = pyglet.window.Window()
window.width = 1000
window.height = 600
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

"""Colors
    RED GREEN BLUE WHITE BLACK PURPLE ORANGE GRAY AMBER CYAN YELLOW
"""

notas = [18, 27, 13, 20, 10]
notas_labels = (
    "<20000000000000000000000000000",
    "20-40",
    "40-60",
    "60-80",
    ">80",
)
colors = ["red", Color.GREEN, "blue", "orange", Color.PURPLE]

pizza = Pizza(
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


@window.event
def on_draw():
    window.clear()
    pizza.draw()


selected = None


@window.event
def on_mouse_press(x, y, button, modifiers):
    global selected

    title_pos = (
        pizza.title.pos[0] - pizza.title.content_width // 2,
        pizza.title.pos[1] + pizza.title.content_height // 2,
    )
    if button & pyglet.window.mouse.LEFT:
        if is_mouse_over_pie(pizza.position, pizza.radius * pizza.esc[0], (x, y)):
            selected = "PIE" if selected != "PIE" else None
        elif is_mouse_over_square(
            title_pos,
            pizza.title.content_width,
            pizza.title.content_height,
            (x, y),
        ):
            selected = "TITLE" if selected != "TITLE" else None
        elif is_mouse_over_square(
            pizza.legends_list.position,
            pizza.legends_list.width,
            pizza.legends_list.height,
            (x, y),
        ):
            selected = "LEGEND" if selected != "LEGEND" else None


@window.event
def on_mouse_motion(x, y, dx, dy):
    if selected == "PIE":
        pizza.position = (x + dx, y + dy)

    elif selected == "TITLE":
        pizza.title.pos = (
            x + dx,
            y + dy,
        )

    elif selected == "LEGEND":
        pizza.legends_list.position = (
            x + dx - pizza.legends_list.width // 2,
            y + dy + pizza.legends_list.height // 2,
        )
        pizza.legends_list.draw()


def rotate(rot):
    if keys[pyglet.window.key.RIGHT]:
        rot += -1
    if keys[pyglet.window.key.LEFT]:
        rot += 1
    return rot


def escalonate(esc):
    if keys[pyglet.window.key.UP]:
        esc = (esc[0] + 0.01, esc[1] + 0.01) if esc[0] < 2 else (2, 2)
    if keys[pyglet.window.key.DOWN]:
        esc = (esc[0] - 0.01, esc[1] - 0.01) if esc[0] > 0.5 else (0.5, 0.5)
    return esc


@pyglet.clock.schedule
def update(dt):
    global selected

    if selected == "PIE":
        pizza.rot = rotate(pizza.rot)
        pizza.esc = escalonate(pizza.esc)
    elif selected == "TITLE":
        pizza.title.esc = escalonate(pizza.title.esc)
        pizza.title.rot = rotate(pizza.title.rot)
    elif selected == "LEGEND":
        leg = pizza.legends_list
        if keys[pyglet.window.key.LEFT]:
            leg.set_width(leg.width - 1)
        if keys[pyglet.window.key.RIGHT]:
            leg.set_width(leg.width + 1)


pyglet.app.run()
