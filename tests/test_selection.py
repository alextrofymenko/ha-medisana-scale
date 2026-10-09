from custom_components.medisana.parser import UserMeasurement
from custom_components.medisana.selection import newer_than, newest

NOW = 1_760_000_000


def reading(user_id: int, timestamp: int) -> UserMeasurement:
    return UserMeasurement(user_id=user_id, timestamp=timestamp, weight_kg=70.0)


def stamps(measurements: list[UserMeasurement]) -> list[tuple[int, int]]:
    return [(m.user_id, m.timestamp) for m in measurements]


def test_first_sync_passes_every_reading_oldest_first():
    sync = [reading(2, 300), reading(2, 100), reading(2, 200)]
    assert stamps(newer_than(sync, {}, NOW)) == [(2, 100), (2, 200), (2, 300)]


def test_repeated_history_passes_only_the_new_reading():
    sync = [reading(2, 100), reading(2, 200), reading(2, 300)]
    assert stamps(newer_than(sync, {2: 200}, NOW)) == [(2, 300)]


def test_truncated_sync_after_restart_leaves_newer_values_alone():
    oldest_six = [reading(2, ts) for ts in (10, 20, 30, 40, 50, 60)]
    assert newer_than(oldest_six, {2: 500}, NOW) == []


def test_stale_record_from_an_early_sync_is_ignored():
    assert newer_than([reading(2, 100)], {2: 900}, NOW) == []


def test_each_user_slot_has_its_own_mark():
    sync = [reading(1, 150), reading(2, 150)]
    assert stamps(newer_than(sync, {1: 100, 2: 200}, NOW)) == [(1, 150)]


def test_duplicate_reading_in_one_sync_passes_once():
    sync = [reading(2, 100), reading(2, 100)]
    assert stamps(newer_than(sync, {}, NOW)) == [(2, 100)]


def test_readings_without_a_time_or_from_the_future_are_left_out():
    sync = [reading(2, 0), reading(2, NOW + 3600), reading(2, 100)]
    assert stamps(newer_than(sync, {}, NOW)) == [(2, 100)]


def test_newest_picks_the_latest_across_users():
    sync = [reading(1, 300), reading(2, 200)]
    assert stamps([newest(sync, 0)]) == [(1, 300)]


def test_newest_is_none_when_nothing_beats_the_mark():
    assert newest([reading(2, 100)], 100) is None
    assert newest([], 0) is None
