from process_game_state import is_inside, get_edges


def test_get_edges():
    points = [
        (1, 0),
        (2, 2),
        (4, 1),
        (3, -1),
    ]

    correctResult = [
        ((1, 0), (2, 2)),
        ((2, 2), (4, 1)),
        ((4, 1), (3, -1)),
        ((3, -1), (1, 0)),
    ]
    test_result = get_edges(points)

    # Assert that the filtered DataFrame is not empty
    assert correctResult == test_result


def test_is_inside():
    test_edges = [
        ((1, 0), (2, 2)),
        ((2, 2), (4, 1)),
        ((4, 1), (3, -1)),
        ((3, -1), (1, 0)),
    ]
    failing_test = is_inside((-10, -10), test_edges)
    assert not failing_test

    passing_test = is_inside((2, 1), test_edges)
    assert passing_test
