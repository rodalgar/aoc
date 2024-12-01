from TileTemplate import TileTemplate


class Tile:
    tile_template: TileTemplate = None
    is_path: bool = None
    path_direction: tuple[int, int] = None
    enclosing_type: int = None

    INNER_ENCLOSING: int = 0
    OUTER_ENCLOSING: int = 1

    def __init__(self, tile_template=None):
        self.tile_template = tile_template

    def __int__(self):
        self.is_path = False

    def __repr__(self):
        template = '[{}] {} [{}][{}]'
        if self.tile_template is None:
            return template.format(' ', '(X, X)', self.path_direction, self.enclosing_type)
        else:
            return template.format(' ' if not self.is_path else '#', self.tile_template.direction,
                                   self.path_direction,
                                   self.enclosing_type)

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return NotImplemented

        return self.tile_template == other.tile_template \
            and self.is_path == other.is_path \
            and self.path_direction == other.path_direction \
            and self.enclosing_type == other.enclosing_type
