from datetime import datetime, timedelta, time

def generate_time_slots(
    start: time,
    end: time,
    slot_minutes: int
) -> list[str]:
    slots = []

    current = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)

    while current + timedelta(minutes=slot_minutes) <= end_dt:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=slot_minutes)

    return slots