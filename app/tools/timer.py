import time
import json

import threading
import datetime
from pydub import AudioSegment
from pydub.playback import play

from app.helpers.paths import TIMER_ALARM_PATH, SHORT_TERM_MEMORY_DIR

timers_path = SHORT_TERM_MEMORY_DIR / "timers.json"

timers_path.parent.mkdir(parents=True, exist_ok=True)


def load_timers():
    if timers_path.exists():
        with open(timers_path, "r") as f:
            return json.load(f)
    else:
        return {}


def save_timers(timers):
    with open(timers_path, "w") as f:
        json.dump(timers, f, indent=4)


def cancel_timer(due_timestamp):
    """Cancels the timer with the given due timestamp"""
    timers = load_timers()
    due_timestamp = str(int(due_timestamp))
    if timers == {}:
        return "No timers set"
    elif due_timestamp in timers:
        timers.pop(due_timestamp)
        save_timers(timers)
        return "Timer cancelled"
    else:
        return "Timer with that timestamp not found"


def unix2str(unix):
    """Converts a Unix timestamp to a string"""
    return datetime.datetime.fromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S")


def seconds_to_suitable_units(seconds):
    """Converts seconds to a suitable unit"""
    if seconds < 60:
        return f"{seconds} seconds"
    elif seconds < 3600:
        return f"{seconds // 60} minutes"
    elif seconds < 86400:
        return f"{seconds // 3600} hours"
    else:
        return f"{seconds // 86400} days"


def plan_timer_to_go_off(due_time):
    def play_alarm(due_time):
        timers = load_timers()
        chime = AudioSegment.from_file(TIMER_ALARM_PATH, format="mp3")
        play(chime)
        cancel_timer(due_time)

        print("Timers:", get_timers())

    delay = due_time - int(time.time())
    threading.Timer(delay, play_alarm, args=[due_time]).start()


def set_timer(h=0, m=0, s=0):
    """Plays a chime after h hours, m minutes, and s seconds (h, m, s are optional)"""
    timers = load_timers()
    h, m, s = int(h), int(m), int(s)
    set_time = int(time.time())
    hms = h * 3600 + m * 60 + s
    due_time = set_time + hms
    timers[str(due_time)] = {
        "set_time": set_time,
        "seconds": hms,
    }
    save_timers(timers)

    plan_timer_to_go_off(due_time)

    print(f"Timer set for {hms} seconds")
    print("Timers:", get_timers())


def get_timers():
    """Returns a list of all current timers"""
    timers_info = {}
    for due_time, timer in load_timers().items():
        due_time = int(due_time)
        set_time = timer["set_time"]
        seconds = timer["seconds"]
        remaining = due_time - int(time.time())
        timers_info[due_time] = {
            "set_time": unix2str(set_time),
            "due_time": unix2str(due_time),
            "total": seconds_to_suitable_units(seconds),
            "remaining": seconds_to_suitable_units(remaining),
        }
    return timers_info
