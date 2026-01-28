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

def generate_slots(start_time, end_time, slot_minutes, date):
    slots = []

    current = datetime.combine(date, start_time)
    end_dt = datetime.combine(date, end_time)

    while current + timedelta(minutes=slot_minutes) <= end_dt:
        slot_end = current + timedelta(minutes=slot_minutes)

        slots.append({
            "start": current,
            "end": slot_end
        })

        current = slot_end

    return slots

def has_conflict(slot_start, slot_end, schedulings):
    for sched in schedulings:
        sched_start = datetime.combine(sched.date, sched.start_time)
        sched_end = datetime.combine(sched.date, sched.end_time)

        if slot_start < sched_end and slot_end > sched_start:
            return True

    return False

def to_datetime(date, t):
    return datetime.combine(date, t)

def normalize_time(t: time) -> time:
    return t.replace(tzinfo=None)