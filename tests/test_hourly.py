from datetime import datetime, timezone

from custom_components.medisana.hourly import hourly_statistics

HOUR = 3600
NOW = 1_760_000_000 - 1_760_000_000 % HOUR + 30 * 60  # half past an hour


def hour(hours_ago: int) -> int:
    return NOW - NOW % HOUR - hours_ago * HOUR


def starts(statistics: list[dict]) -> list[int]:
    return [int(s["start"].timestamp()) for s in statistics]


def test_each_reading_lands_on_the_hour_it_was_taken():
    readings = [(hour(30) + 5 * 60, 72.4), (hour(5) + 59 * 60, 72.1)]
    assert hourly_statistics(readings, NOW) == [
        {
            "start": datetime.fromtimestamp(hour(30), tz=timezone.utc),
            "mean": 72.4,
            "min": 72.4,
            "max": 72.4,
        },
        {
            "start": datetime.fromtimestamp(hour(5), tz=timezone.utc),
            "mean": 72.1,
            "min": 72.1,
            "max": 72.1,
        },
    ]


def test_readings_in_one_hour_become_their_mean_min_and_max():
    readings = [(hour(5) + 60, 73.0), (hour(5) + 120, 72.0), (hour(5) + 180, 71.0)]
    [statistic] = hourly_statistics(readings, NOW)
    assert (statistic["mean"], statistic["min"], statistic["max"]) == (72.0, 71.0, 73.0)


def test_hours_that_ended_less_than_an_hour_ago_are_left_out():
    readings = [(hour(2), 1.0), (hour(1), 2.0), (hour(0), 3.0)]
    assert starts(hourly_statistics(readings, NOW)) == [hour(2)]


def test_readings_come_out_oldest_first():
    readings = [(hour(3), 1.0), (hour(9), 2.0), (hour(6), 3.0)]
    assert starts(hourly_statistics(readings, NOW)) == [hour(9), hour(6), hour(3)]


def test_readings_without_a_time_or_a_value_are_left_out():
    readings = [(0, 72.0), (hour(4), None), (hour(3), 71.0)]
    assert starts(hourly_statistics(readings, NOW)) == [hour(3)]
