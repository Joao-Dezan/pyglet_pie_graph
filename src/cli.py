import pyglet
from lib.graphic import Pizza
from lib.colors import Color
from time import sleep


def get_values(amount: int, value_label: str = "Valor", type: str = "int") -> list:
    values = []
    for i in range(amount):
        value = getattr(__builtins__, type)(input(f"{value_label} {i+1}: "))
        values.append(value)

    return values


def input_question(text: str) -> bool:
    return input(f"{text}").startswith(("s", "S", "y", "Y"))


def title(text, decorator: str = "-=", multiplier: int = 5) -> None:
    print(f"\n{decorator * multiplier} {text} {decorator * multiplier}")


"""Colors
    RED GREEN BLUE WHITE BLACK PURPLE ORANGE GRAY AMBER CYAN YELLOW
"""

title("Gerador de Gráficos")

title_text = input("\nTítulo: ")
radius = int(input("\nTamanho do gráfico (raio): "))

data_quantity = int(input("\nQuantidade de dados: "))
data = get_values(data_quantity, type="float")

has_add_legends: bool = input_question("\nDeseja adicionar legendas [s/n]? ")
legend_texts = None
if has_add_legends:
    title("Valores para as legendas", decorator="-")
    has_auto_add_legends = input_question(
        "\nDeseja gerar as legendas automaticamente [s/n]? "
    )
    legend_texts = (
        get_values(data_quantity, value_label="Legend", type="str")
        if not has_auto_add_legends
        else None
    )


has_add_labels: bool = input_question("\nDeseja adicionar labels [s/n]? ")
label_texts = None
if has_add_labels:
    title("Valores para as labels", decorator="-")
    has_auto_add_labels = input_question(
        "\nDeseja gerar as labels automaticamente [s/n]? "
    )
    label_texts = (
        get_values(data_quantity, value_label="Label", type="str")
        if not has_auto_add_labels
        else None
    )

has_add_colors: bool = not input_question(
    "\nDeseja gerar cores automaticamente [s/n]? "
)
if has_add_colors:
    colors = []
    for i in range(data_quantity):
        color = input(f"Cor {i+1}: ")
        if len(color.split(" ")) == 3:
            try:
                color = tuple(map(lambda x: int(x.strip()), color.split(" ")))
            except:
                raise Exception("Invalid Input Color")
        elif len(color.split(" ")) == 1:
            color = Color[color.upper().strip()].value
        else:
            raise Exception("Invalid Input Color")
        colors.append(color)

else:
    colors = None

window = pyglet.window.Window()
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
window.width = 800
window.height = 600
graphs = []

pizza = Pizza(
    data,
    position=(window.width // 2, window.height // 2),
    radius=180,
    title=title_text,
    show_labels=has_add_labels,
    show_legends=has_add_legends,
    legend_texts=legend_texts,
    label_texts=label_texts,
    colors=colors,
)

title("Gráfico gerado com sucesso", decorator=">")


@window.event
def on_draw():
    window.clear()
    pizza.draw()


@pyglet.clock.schedule
def update(dt):
    if keys[pyglet.window.key.RIGHT]:
        pizza.rot += -1
    if keys[pyglet.window.key.LEFT]:
        pizza.rot += 1
    if keys[pyglet.window.key.UP]:
        pizza.esc = (
            (pizza.esc[0] + 0.01, pizza.esc[1] + 0.01) if pizza.esc[0] < 2 else (2, 2)
        )
    if keys[pyglet.window.key.DOWN]:
        pizza.esc = (
            (pizza.esc[0] - 0.01, pizza.esc[1] - 0.01)
            if pizza.esc[0] > 0.5
            else (0.5, 0.5)
        )


pyglet.app.run()
