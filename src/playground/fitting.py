"""Least-squares line fit (pretend an AI wrote most of this)."""

from .stats import mean


def fit_line(xs, ys):
    """Return slope and intercept of the least-squares line through (xs, ys)."""
    xs, ys = list(xs), list(ys)
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("need at least two points, and as many x as y values")
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        raise ValueError("all x values are equal")
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    return slope, my - slope * mx
