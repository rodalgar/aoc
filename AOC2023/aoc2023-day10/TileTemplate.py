class TileTemplate:
    direction: tuple[int, int]
    glyph: str
    is_pipe: bool

    def __init__(self, glyph: str, direction: tuple[int, int], is_pipe: bool):
        self.direction = direction
        self.is_pipe = is_pipe
        self.glyph = glyph
