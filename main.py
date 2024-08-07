from hilbert import hilbert_curve, closest_hilbert_size
from audio import line_to_audio
import numpy
import cv2
import scipy
from logging_setup import setup_logger
from loguru import logger


def image_to_line(img: numpy.ndarray) -> list[int]:
    size = min(numpy.shape(img)[0], numpy.shape(img)[1])
    hilbert_size = closest_hilbert_size(size)

    cv2.resize(img, (2**hilbert_size, 2**hilbert_size))
    curve = hilbert_curve(hilbert_size)

    return [int(img[p.x][p.y]) for p in curve]


def main() -> None:
    setup_logger()

    cap = cv2.VideoCapture(0)

    result, image = cap.read()

    if result:
        image = cv2.resize(image, (4, 4))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        audio = numpy.array(line_to_audio(image_to_line(gray)))
        scipy.io.wavfile.write("audio.wav", 44100, audio)

        cv2.imshow("Preview", gray)

        cv2.waitKey(0)
        cv2.destroyWindow("Preview")
    else:
        logger.error("Error taking picture")


if __name__ == "__main__":
    main()
