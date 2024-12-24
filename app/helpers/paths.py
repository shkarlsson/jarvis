from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

APP_DIR = PROJECT_DIR / "app"

DATA_DIR = APP_DIR / "data"

SHORT_TERM_MEMORY_DIR = DATA_DIR / "short_term_memory"
AUDIO_DIR = DATA_DIR / "audio"
MESSAGES_DIR = DATA_DIR / "messages"

RECORDED_AUDIO_DIR = AUDIO_DIR / "recorded"
GENERATED_AUDIO_DIR = AUDIO_DIR / "generated"

ASSETS_DIR = APP_DIR / "assets"
CHIME_PATH = ASSETS_DIR / "chime.mp3"
TIMER_ALARM_PATH = ASSETS_DIR / "timer-alarm.mp3"

# Creating all the necessary directories
for dir_ in [
    SHORT_TERM_MEMORY_DIR,
    AUDIO_DIR,
    MESSAGES_DIR,
    RECORDED_AUDIO_DIR,
    GENERATED_AUDIO_DIR,
]:
    dir_.mkdir(exist_ok=True, parents=True)
