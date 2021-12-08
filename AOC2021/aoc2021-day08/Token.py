from typing import List, Any


class Token:
    special_lengths = {
        2: [1],
        3: [7],
        4: [4],
        5: [2, 3, 5],
        6: [0, 6, 9],
        7: [8]
    }

    raw_str: str = None
    signals: List[str] = None
    value: int = None

    def __init__(self, raw_str):
        self.raw_str = raw_str
        self.signals = sorted(x for x in self.raw_str)

    def cnt_segments(self) -> int:
        return len(self.raw_str)

    def set_token_value(self, value: int) -> Any:
        self.value = value
        return self

    def __repr__(self):
        return f"_{','.join(self.signals)}_"
