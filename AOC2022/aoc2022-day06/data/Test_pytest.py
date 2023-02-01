import pytest
from Main import detect_marker


@pytest.mark.parametrize("test_data, expected", [
    ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7),
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', 5),
    ('nppdvjthqldpwncqszvftbrmjlhg', 6),
    ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10),
    ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11)
])
def test_detect_marker(test_data, expected):
    data = detect_marker(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected", [
    ('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19),
    ('bvwbjplbgvbhsrlpgdmjqwftvncz', 23),
    ('nppdvjthqldpwncqszvftbrmjlhg', 23),
    ('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29),
    ('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26)
])
def test_detect_message(test_data, expected):
    data = detect_marker(test_data, 14)
    assert data == expected
