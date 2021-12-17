from typing import Tuple


def bin_to_dec(strbin: str, i: int, size: int) -> Tuple[int, int]:
    data = strbin[i: i + size]
    return int(data, 2), i + size


def bin_to_str(strbin: str, i: int, size: int) -> Tuple[str, int]:
    data = strbin[i: i + size]
    return data, i + size
