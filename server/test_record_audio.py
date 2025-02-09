import sounddevice as sd
import numpy as np
import wave

RATE = 44100
CHANNELS = 1
DURATION = 5  # seconds
OUTPUT_FILENAME = "recorded.wav"

print("Recording...")
audio_data = sd.rec(int(RATE * DURATION), samplerate=RATE, channels=CHANNELS, dtype=np.int16)
sd.wait()
print("Finished recording.")

# Save as WAV
with wave.open(OUTPUT_FILENAME, "wb") as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 16-bit audio
    wf.setframerate(RATE)
    wf.writeframes(audio_data.tobytes())

print(f"Saved to {OUTPUT_FILENAME}")
