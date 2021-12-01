from Main import depth_measurement_increments, rolling_sum

depths_raw = ['199',
              '200',
              '208',
              '210',
              '200',
              '207',
              '240',
              '269',
              '260',
              '263']

depths = list(map(int, depths_raw))


# PART 1 TESTS
def test_depth_measurement_increments():
    data = depth_measurement_increments(depths)

    assert data == 7


# PART 2 TESTS
def test_rolling_sum():
    data = rolling_sum(depths, 3)

    assert data == [607, 618, 618, 617, 647, 716, 769, 792]


def test_depth_measurement_increments_with_rolling_window():
    rolling_data = rolling_sum(depths, 3)
    data = depth_measurement_increments(rolling_data)

    assert data == 5
