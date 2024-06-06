from datetime import datetime, timezone


async def unix_time_millis(dt):
    epoch = datetime(
        1970,
        1,
        1,
        tzinfo=timezone.utc
    )

    return int((dt - epoch).total_seconds())
