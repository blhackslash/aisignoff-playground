"""Basic statistics, written by hand."""


def mean(values):
    """Arithmetic mean of a non-empty sequence."""
    values = list(values)
    if not values:
        raise ValueError("mean of an empty sequence")
    return sum(values) / len(values)


def variance(values, ddof=0):
    """Variance with ``ddof`` delta degrees of freedom."""
    values = list(values)
    if len(values) <= ddof:
        raise ValueError("not enough values")
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / (len(values) - ddof)
