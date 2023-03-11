import datetime
from typing import List, Optional

USER_TIMEZONE = datetime.timezone(datetime.timedelta(hours=-8))
USER_DATETIME = datetime.datetime.now(USER_TIMEZONE)
USER_WORK_HOURS = "09:00 AM to 05:00 PM"
DEFAULT_EVENT_DURATION = "0:30:00"


def parse_datetime(s: Optional[str]) -> Optional[datetime.datetime]:
    """Convert an iso formatted datetime string to datetime object in user's timezone."""
    if s is None:
        return None
    d = datetime.datetime.strptime(s, "%B %d %Y %I:%M %p")
    return d.replace(tzinfo=USER_TIMEZONE)


def parse_timedelta(s: Optional[str]) -> datetime.timedelta:
    """Convert an HH:MM:SS timedelta formatted string to a timedelta object."""
    s = s or DEFAULT_EVENT_DURATION
    try:
        parts = s.split(":")
        hours = int(parts[0])
        minutes = int(parts[1]) if len(parts) > 1 else 0
        seconds = int(parts[2]) if len(parts) > 2 else 0
    except:
        raise ValueError(f"duration was wrongly formatted: {s}")
    return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
