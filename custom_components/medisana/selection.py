"""Pick the readings from a sync that may become current sensor values.

The scale sends its stored history, oldest first, on every sync. A sync can
be cut short, and it always repeats readings already shown, so a reading only
becomes current when it is newer than what its user slot already shows.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping

from .parser import UserMeasurement


def newer_than(
    measurements: Iterable[UserMeasurement],
    latest_by_user: Mapping[int, int],
    now: int,
) -> list[UserMeasurement]:
    """Return the readings newer than their slot's latest, oldest first.

    Readings without a timestamp were taken before the scale's clock was set,
    and readings stamped after `now` come from a clock glitch. Neither can be
    placed in time, so both are left out.
    """
    marks = dict(latest_by_user)
    out: list[UserMeasurement] = []
    for m in sorted(measurements, key=lambda m: m.timestamp):
        if 0 < m.timestamp <= now and m.timestamp > marks.get(m.user_id, 0):
            marks[m.user_id] = m.timestamp
            out.append(m)
    return out


def newest(measurements: Iterable[UserMeasurement], latest: int) -> UserMeasurement | None:
    """Return the newest reading, if it is newer than `latest`."""
    candidate = max(measurements, key=lambda m: m.timestamp, default=None)
    return candidate if candidate is not None and candidate.timestamp > latest else None
