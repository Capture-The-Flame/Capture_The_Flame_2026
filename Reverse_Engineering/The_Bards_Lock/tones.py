import wave
import struct
import math

bins = [41, 49, 55, 61, 65, 61, 55, 49, 41]

sample_rate = 44100
fft_size = 4096
windows_per_note = 5  # >= 400ms
samples_per_note = fft_size * windows_per_note
duration = samples_per_note / sample_rate
amplitude = 32760

hz_per_bin = sample_rate / fft_size
frequencies = [b * hz_per_bin for b in bins]

with wave.open("solve.wav", "w") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(sample_rate)

    for freq in frequencies:
        for i in range(samples_per_note):
            sample = amplitude * math.sin(
                2 * math.pi * freq * (i / sample_rate)
            )
            wav.writeframes(struct.pack("<h", int(sample)))

print("Generated window-aligned solve.wav")
print("Duration per note:", duration)
print("Frequencies:", frequencies)