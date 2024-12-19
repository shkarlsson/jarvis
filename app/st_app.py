import streamlit as st
from pydub import AudioSegment

# import pyaudio

from audio_recorder_streamlit import audio_recorder
import time

import streamlit as st

import streamlit_webrtc
from streamlit_webrtc import webrtc_streamer
import av


# %%

debug = st.empty()

debug.write("Starting")
i = 0
while True:
    i += 1
    audio = audio_recorder(
        text="",
        icon_size="2x",
        auto_start=True,
        energy_threshold=0,
        key=f"audio_recorder_{i}",
    )
    while not audio:
        time.sleep(1)
        debug.write("No audio. Waiting...")
    if audio:
        st.audio(audio, format="audio/wav")

        debug.write(f"Len of audio: {len(audio)} from recorder with key {i}")

st.stop()


def app_sst():
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=streamlit_webrtc.WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": False, "audio": True},
    )

    status_indicator = st.empty()

    if not webrtc_ctx.state.playing:
        return

    status_indicator.write("Loading...")
    text_output = st.empty()
    stream = None

    while True:
        if webrtc_ctx.audio_receiver:
            # if stream is None:
            #    from deepspeech import Model

            #    model = Model(model_path)
            #    model.enableExternalScorer(lm_path)
            #    model.setScorerAlphaBeta(lm_alpha, lm_beta)
            #    model.setBeamWidth(beam)

            #    stream = model.createStream()

            #    status_indicator.write("Model loaded.")

            sound_chunk = pydub.AudioSegment.empty()
            try:
                audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                status_indicator.write("No frame arrived.")
                continue

            status_indicator.write("Running. Say something!")

            for audio_frame in audio_frames:
                sound = pydub.AudioSegment(
                    data=audio_frame.to_ndarray().tobytes(),
                    sample_width=audio_frame.format.bytes,
                    frame_rate=audio_frame.sample_rate,
                    channels=len(audio_frame.layout.channels),
                )
                sound_chunk += sound

            if len(sound_chunk) > 0:
                sound_chunk = sound_chunk.set_channels(1).set_frame_rate(
                    model.sampleRate()
                )
                buffer = np.array(sound_chunk.get_array_of_samples())
                # stream.feedAudioContent(buffer)
                # text = stream.intermediateDecode()
                # text_output.markdown(f"**Text:** {text}")
                text_output.markdown(f"Len of sound_chunk: {len(sound_chunk)}")
        else:
            status_indicator.write("AudioReciver is not set. Abort.")
            break


app_sst()
st.stop()


def get_continuous_listener():
    i = 0
    while True:
        i += 1
        audio_bytes = audio_recorder(
            # text="",
            # icon_size="2x",
            auto_start=True,
            # energy_threshold=0,
            pause_threshold=2,  # 2 seconds of non-speech before stopping
            key=f"audio_recorder_{i}",
        )
        if audio_bytes:
            yield audio_bytes


for audio_bytes in get_continuous_listener():
    st.write(len(audio_bytes))
    st.audio(audio_bytes, format="audio/wav")


st.stop()


def get_continuous_listener():
    """Record audio from the microphone in a continuous loop."""
    turn_on_mic = st.empty()

    for i in range(10):
        audio_bytes = audio_recorder(
            text="",
            icon_size="2x",
            auto_start=True,
            # energy_threshold=0,
            key=f"{i}",
        )

        if audio_bytes is None:
            turn_on_mic.write("No audio detected. Turn on the microphone.")
            time.sleep(0.1)
        else:
            turn_on_mic.empty()
            return audio_bytes


import struct
from main import handle

audio_bytes = get_continuous_listener()
print(len(audio_bytes))
st.write(len(audio_bytes))

log = st.empty()
stop = st.button("Stop")
while True:

    # pcm = listen_stream.read(handle.frame_length, exception_on_overflow=False)
    pcm = struct.unpack_from("h" * handle.frame_length, audio_bytes)
    # log.write(f"PCM: {pcm}")
    log.write(len(audio_bytes))

    keyword_index = handle.process(pcm)
    if keyword_index >= 0:
        break

st.write("Keyword detected")

# Saving audio to disk

audio_path = "audio.wav"

audio = AudioSegment(data=audio_bytes)
audio.export(audio_path, format="wav")
