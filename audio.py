import functools
import math
from loguru import logger
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

MIN_FREQUENCY = 20
MAX_FREQUENCY = 15000
DEFAULT_SAMPLERATE = 44100 // 4
DEFAULT_DURATION = 5
DEFAULT_VOLUME = 1


def frequencies(num: int) -> np.ndarray:
    return np.logspace(np.log10(MIN_FREQUENCY), np.log10(MAX_FREQUENCY), num)


def custom_sin(frequency: float, duration: float, sample_rate: int = DEFAULT_SAMPLERATE, amplitude: float = 1):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return amplitude * np.sin(2 * np.pi * frequency * t)


def normalise(audio: np.ndarray, volume: float) -> np.ndarray:
    peak = np.max(np.abs(audio))
    return audio * (volume / peak)


def line_to_audio(line: np.ndarray,
                  samplerate: int = DEFAULT_SAMPLERATE,
                  duration: float = DEFAULT_DURATION,
                  volume: float = DEFAULT_VOLUME) -> np.ndarray:
    line_len = len(line)
    freqs = frequencies(line_len)

    audio = np.zeros(int(samplerate * duration))
    for freq, ampl in zip(freqs, line / 255):
        audio += custom_sin(freq, duration, samplerate, ampl)

    plt.figure(figsize=(12, 4))
    plt.plot(np.linspace(0, duration, int(samplerate * duration)), audio)
    plt.show()
    return audio / np.max(np.abs(audio)) * volume


def main() -> None:
    print(frequencies(10))


if __name__ == "__main__":
    main()
