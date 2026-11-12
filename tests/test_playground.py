import pytest

from playground import fit_line, mean, variance


def test_mean():
    assert mean([1, 2, 3]) == 2


def test_variance():
    assert variance([1, 2, 3, 4], ddof=1) == pytest.approx(5 / 3)


def test_fit_line():
    slope, intercept = fit_line([0, 1, 2], [1, 3, 5])
    assert slope == pytest.approx(2)
    assert intercept == pytest.approx(1)
