"""Constants for the Medisana BS scale integration."""
from __future__ import annotations

DOMAIN = "medisana"
MANUFACTURER = "Medisana"

# BLE — Weight service exposed by BS410/BS430/BS440/BS444
SERVICE_UUID = "000078b2-0000-1000-8000-00805f9b34fb"

CHAR_PERSON = "00008a82-0000-1000-8000-00805f9b34fb"
CHAR_WEIGHT = "00008a21-0000-1000-8000-00805f9b34fb"
CHAR_BODY = "00008a22-0000-1000-8000-00805f9b34fb"
CHAR_COMMAND = "00008a81-0000-1000-8000-00805f9b34fb"

# Scale stores "seconds since 2010-01-01 00:00:00 UTC"; add this to get Unix time.
SCALE_EPOCH_OFFSET = 1_262_304_000

# The scale starts advertising BEFORE it has finished the body-composition
# analysis. A sync command sent before the weighing is committed gets a stale
# record from history instead of the new weighing. Waiting this long after the
# first advertisement lets the weighing commit first; the scale's BLE window
# stays open long enough for it (tested 30+s).
ADVERTISEMENT_TO_SESSION_DELAY_SECONDS = 25.0

# The scale only accepts a connection for a short window right after a
# measurement. If we don't finish the history dump within this long, we bail
# and wait for the next advertisement.
CONNECT_TIMEOUT_SECONDS = 45.0

# After the final indication the scale takes a beat before it actively
# disconnects. Empirically the BS444 can sit quiet for 4–5 seconds between
# the Person packet and the follow-up Weight/Body packets, so a short quiet
# window causes us to disconnect early and lose the body composition data.
# The upstream keptenkurk/BS440 code just unconditionally sleeps 30s after
# writing the command; a 10s quiet window is the safer equivalent.
POST_PACKET_QUIET_SECONDS = 10.0

MAX_USERS = 8

# Option keys for per-user display names. Values live in entry.options under
# CONF_USER_NAMES as a dict keyed by str(user_id): e.g. {"1": "Alice", "2": "Bob"}.
CONF_USER_NAMES = "user_names"
