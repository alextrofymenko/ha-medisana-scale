"""Turn the scale's stored readings into hourly long-term statistics.

Home Assistant's history chart draws a sensor's past from its long-term
statistics, which hold a mean, min and max per hour. Writing each reading
there puts it on the hour it was taken, not the moment a sync passed it on.
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime, timezone
from typing import Any

HOUR = 3600


def hourly_statistics(
    readings: Iterable[tuple[int, float | None]], now: int
) -> list[dict[str, Any]]:
    """Return the mean, min and max of each hour's readings, oldest first.

    Each reading pairs a Unix timestamp with a value. Readings with no time or
    no value are left out. So are hours that ended less than an hour ago.
    Home Assistant compiles each hour from the sensor's states just after it
    ends, and a row already written for that hour makes the compile fail.
    """
    by_hour: dict[int, list[float]] = defaultdict(list)
    for timestamp, value in readings:
        start = timestamp - timestamp % HOUR
        if timestamp > 0 and value is not None and start + 2 * HOUR <= now:
            by_hour[start].append(value)
    return [
        {
            "start": datetime.fromtimestamp(start, tz=timezone.utc),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }
        for start, values in sorted(by_hour.items())
    ]
