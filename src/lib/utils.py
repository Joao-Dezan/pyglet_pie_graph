import pyglet


class Label(pyglet.text.Label):
    def __init__(
        self,
        text="",
        font_name=None,
        font_size=20,
        bold=False,
        italic=False,
        stretch=False,
        color=...,
        x=0,
        y=0,
        width=None,
        height=None,
        anchor_x="left",
        anchor_y="top",
        align="left",
        multiline=False,
        dpi=None,
        batch=None,
        group=None,
    ):
        super().__init__(
            text,
            font_name,
            font_size,
            bold,
            italic,
            stretch,
            color,
            x=0,
            y=0,
            width=width,
            height=height,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            align=align,
            multiline=multiline,
            dpi=dpi,
            batch=batch,
            group=group,
        )
        self.pos = (x, y)
        self.rot = 0
        self.esc = (1, 1)

    def draw(self):
        pyglet.gl.glPushMatrix()
        pyglet.gl.glTranslated(self.pos[0], self.pos[1], 0)
        pyglet.gl.glRotated(self.rot, 0, 0, 1)
        pyglet.gl.glScaled(self.esc[0], self.esc[1], 0)
        super().draw()
        pyglet.gl.glPopMatrix()
