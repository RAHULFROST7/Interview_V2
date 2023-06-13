import pyaudio
import wave
import os
from pydub import AudioSegment
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set the recording parameters
chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 44100

# Create an instance of PyAudio
p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

# Create a list to store the recorded data
frames = []

# Record the audio
while True:
    data = stream.read(chunk)
    frames.append(data)

    # Check if stop recording file exists
    if os.path.isfile('stop_recording'):
        # print("inside it")
        os.remove('stop_recording')
        break

print("\n!! End of recording !!")

# Stop and close the microphone stream
stream.stop_stream()
stream.close()

# Terminate the PyAudio instance
p.terminate()

# Find the next available file name
counter = 1
while os.path.isfile(f"out_{counter}.mp3"):
    counter += 1

# Generate the file name
output_file_name = f"out_{counter}.mp3"

# Convert the recorded audio to an AudioSegment
audio = AudioSegment(
    data=b"".join(frames),
    sample_width=p.get_sample_size(sample_format),
    channels=channels,
    frame_rate=fs
)

# Save the audio as an MP3 file
audio.export(output_file_name, format="mp3")

print(f"Saved audio as {output_file_name}")