from time import sleep
import pyglet
from lib.graphic import Pizza
from lib.colors import Color
from lib.window import Window


window = pyglet.window.Window()
window.width = 1000
window.height = 600
batch = pyglet.graphics.Batch()

input_title = pyglet.gui.widgets.TextEntry("Título", 200, 200, 150, batch=batch)
# submit = pyglet.gui.widgets.PushButton(560, 200, pressed, depressed, batch=batch)


@window.event
def on_draw():
    window.clear()
    batch.draw()


@pyglet.clock.schedule
def on_update(dt):
    print(input_title.value)
    sleep(0.5)


pyglet.app.run()
