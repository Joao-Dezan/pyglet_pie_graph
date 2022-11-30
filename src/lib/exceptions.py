class ValueNotValid(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InconsistentValue(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
