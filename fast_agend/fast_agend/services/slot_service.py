from datetime import datetime, timedelta, time, date

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

def generate_slots(
    start: time,
    end: time,
    slot_minutes: int,
    base_date: date
):
    slots = []

    current = datetime.combine(base_date, start)
    end_dt = datetime.combine(base_date, end)

    while current + timedelta(minutes=slot_minutes) <= end_dt:
        slots.append({
            "start": current,
            "end": current + timedelta(minutes=slot_minutes)
        })
        current += timedelta(minutes=slot_minutes)

    return slots

def has_conflict(slot_start, slot_end, schedulings):
    for sched in schedulings:
        sched_start = datetime.combine(sched.date, sched.start_time)
        sched_end = datetime.combine(sched.date, sched.end_time)

        if slot_start < sched_end and slot_end > sched_start:
            return True

    return False
