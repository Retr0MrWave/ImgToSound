import time

import numpy as np

from hilbert import HilbertCurve, HilbertCurveOp
from audio import line_to_audio
import cv2
import scipy
from logging_setup import setup_logger
from loguru import logger
from matplotlib import pyplot as plt


def image_to_line(img: np.ndarray) -> np.ndarray:
    hilbert_size = HilbertCurveOp.closest_hilbert_size(
        min(np.shape(img)[0], np.shape(img)[1])
    )

    resized_img = cv2.resize(img, (2**hilbert_size, 2**hilbert_size))
    curve = HilbertCurve(hilbert_size).get()

    return resized_img[curve[:, 0], curve[:, 1]]  # np.ndarray([int(img[p.x][p.y]) for p in curve])


def calc(image: np.ndarray, kernel_size: tuple[int, int]) -> None:
    img = cv2.cvtColor(cv2.resize(image, kernel_size), cv2.COLOR_BGR2GRAY)
    scipy.io.wavfile.write("audio.wav", 44100, line_to_audio(image_to_line(img)))


def main(kernel_start: int, kernel_end: int) -> None:
    start_time = time.perf_counter()
    setup_logger()

    result, image = cv2.VideoCapture(0).read()
    if not result:
        return
    logger.info(f"📸 Image done, 🕔 time: {(time.perf_counter() - start_time):.2f}s")

    durations = []

    for i in range(kernel_start, kernel_end + 1):
        start_time = time.perf_counter()
        kernel = (2**i, 2**i)
        calc(image, kernel)
        logger.info(f"✅ Kernel size {kernel} done, 🕔 exec time: {(time.perf_counter() - start_time):.2f}s")
        durations.append(time.perf_counter() - start_time)

    plt.figure(figsize=(12, 8))
    plt.plot(list(range(len(durations))), durations, marker='o', label='execution time')
    plt.plot([2**i * 0.1 for i in range(1, 10)], label='2^x')
    plt.title("Execution times")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


if __name__ == "__main__":
    try:
        main(7, 7)
    except Exception:
        logger.exception("bro really got that premium zaza")
