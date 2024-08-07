import math
from loguru import logger

MIN_FREQUENCY = 20
MAX_FREQUENCY = 15000
DEFAULT_SAMPLERATE = 44100
DEFAULT_LENGTH = 1.0
DEFAULT_VOLUME = 1


def frequencies(num: int) -> list[float]:
    min_freq_log = math.log(MIN_FREQUENCY, 10)
    max_freq_log = math.log(MAX_FREQUENCY, 10)

    res = []
    step = (max_freq_log - min_freq_log) / (num-1)
    freq_log = min_freq_log
    for i in range(num):
        res.append(10 ** freq_log)
        freq_log += step

    return res


def smart_sin(x: float, frequency: float = 1/(2*math.pi), amplitude: float = 1) -> float:
    return amplitude * math.sin(frequency * 2*math.pi * x)


def normalise(audio: list[float], volume) -> list[float]:
    peak = max(max(audio), -min(audio))
    factor = volume/peak
    return [sample * factor for sample in audio]


def line_to_audio(line: list[int],
                  samplerate: int = DEFAULT_SAMPLERATE,
                  length: float = DEFAULT_LENGTH,
                  volume: float = DEFAULT_VOLUME) -> list[float]:
    freq = frequencies(len(line))

    res = []
    for t in range(math.floor(samplerate * length)):
        sample = 0
        for f in freq:
            sample += smart_sin(t/samplerate, frequency=f, amplitude=line[freq.index(f)]/255)
        res.append(sample)

    return normalise(res, volume)


def main() -> None:
    print(frequencies(10))


if __name__ == "__main__":
    main()
