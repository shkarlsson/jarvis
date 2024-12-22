# %%
import time
import re
import threading
import json

import pvporcupine
import struct
import pyaudio
import pvporcupine
from pydub import AudioSegment
from pydub.playback import play
import webrtcvad
import tqdm

from app.helpers.paths import (
    RECORDED_AUDIO_DIR,
    GENERATED_AUDIO_DIR,
    CHIME_PATH,
    MESSAGES_DIR,
)
from app.helpers.config import config
from app.helpers.env_vars import (
    PICOVOICE_ACCESS_KEY as access_key,
)
from app.helpers.ai import transcribe, invoke_ai, generate_audio, parse_ai_response


handle = pvporcupine.create(access_key=access_key, keywords=[config.HOTWORD])

FORMAT = pyaudio.paInt16
SAMPLE_RATE = handle.sample_rate
CHANNELS = 1
CHUNK = 2048
FRAMES_PER_BUFFER = handle.frame_length

# Initialize the VAD
vad = webrtcvad.Vad()

# Configure the aggressiveness from 0 to 3
vad.set_mode(3)
pa = pyaudio.PyAudio()


# %%
def make_listen_stream():
    return pa.open(
        rate=SAMPLE_RATE,
        channels=CHANNELS,
        format=FORMAT,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER,
    )


def get_last_30_ms(frames):
    # For unknown reasons, the last 30ms of the audio * sample rate needs to be multiplied by 2 to avoid errors in webrtcvad
    last_30_ms = frames[-int(0.030 * SAMPLE_RATE * 2) :]
    return last_30_ms


def play_audio(path):
    audio = AudioSegment.from_file(path, format="mp3", frame_rate=SAMPLE_RATE)

    play(audio)


def play_chime():
    play_audio(CHIME_PATH)


def say(text):
    path = GENERATED_AUDIO_DIR / f"{int(time.time())}.mp3"
    generate_audio(text, path)
    play_audio(path)
    time.sleep(0.05)


# %%
if __name__ == "__main__":
    silence_duration = 0
    print(f"SILENCE_THRESHOLD: {config.SILENCE_THRESHOLD}, MIN_COMMAND_DURATION: {config.MIN_COMMAND_DURATION}")

    listen_stream = make_listen_stream()
    print(f"Listening for HOTWORD: {config.HOTWORD}...")
    do_break = False
    force_keyword = False
    while True:
        pcm = listen_stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * FRAMES_PER_BUFFER, pcm)

        keyword_index = handle.process(pcm)
        if keyword_index >= 0 or force_keyword:
            force_keyword = False

            threading.Thread(target=play_chime).start()

            print("HOTWORD Detected")

            # start_time = time.time()

            frames = b""
            print("Recording command...")

            silence_duration = 0
            silence_since = time.time()
            while True:
                time.sleep(0.1)

                data = listen_stream.read(CHUNK, exception_on_overflow=False)
                frames += data

                # if time.time() - start_time < 1:
                #    is_current_speech = True
                # else:
                # Convert pcm to bytes before passing to is_speech
                last_30_ms = get_last_30_ms(frames)
                is_current_speech = vad.is_speech(last_30_ms, SAMPLE_RATE)

                if is_current_speech:
                    silence_duration = 0
                    silence_since = time.time()
                else:
                    silence_duration = time.time() - silence_since

                print(f"Silence duration: {silence_duration}")
                print(f"Message length: {len(frames)}")

                # Check if we've reached the silence threshold
                if silence_duration > SILENCE_THRESHOLD:
                    print("End of speech detected.")

                    if len(frames) < config.MIN_COMMAND_DURATION * SAMPLE_RATE:
                        print(
                            f"Voice recording too short. Restarting the trigger word loop"
                        )
                        frames = b""
                        continue

                    # Save the audio to disk, as mp3
                    audio_path = RECORDED_AUDIO_DIR / f"{int(time.time())}.mp3"
                    AudioSegment(
                        data=frames,
                        sample_width=2,
                        frame_rate=SAMPLE_RATE,
                        channels=CHANNELS,
                    ).export(audio_path, format="mp3")

                    # Possible actions: stop recording, send a message, etc.

                    command = transcribe(audio_path)

                    print(f"Transcribed command: `{command}`")

                    if not re.search(r'\w', command):
                        print(
                            "No command detected. Breaking out of loop, back to trigger word listening..."
                        )
                        break

                    if command.lower().strip(". !") in [
                        "exit",
                        "quit",
                        "reboot",
                        "shutdown",
                        "stop",
                        "restart",
                    ]:
                        print("Exiting...")
                        do_break = True
                        break

                    for text in invoke_ai():
                        say(text)

                    silence_duration = 0
                    silence_since = time.time()
                    frames = b""
                    # print("Restarting the trigger word loop")
                    print("Listening again (as if hotword was detected)")

        if do_break:
            break

    print("Done with listening loop. Closing streams")

    listen_stream.stop_stream()
    listen_stream.close()
    print("Closed wakeup word stream")

    pa.terminate()

    print("Closed PyAudio")

    handle.delete()
    print("Deleted Porcupine handle")

    print("Done")


# %%


# Playing the audio


# %%


path = "/Users/henrik/Code/jarvis/data/audio/generated/1733926281.mp3"

audio = AudioSegment.from_file(
    path,
    format="mp3",
    # parameters=["-q:a", "0"]
    parameters=["-ac", "02"],
    # frame_rate=SAMPLE_RATE,
    # sample_width=2,
    # channels=CHANNELS,
    # duration=0.4,
    # codec="libav",
)
