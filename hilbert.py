import functools
import math

import numpy as np
from attrs import define
from loguru import logger
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection


@define
class Point:
    x: int
    y: int


type Curve = list[Point]


class HilbertCurveOp:
    @staticmethod
    def mirror(curve: np.ndarray) -> np.ndarray:
        return np.fliplr(curve)

    @staticmethod
    def negative_mirror(curve: np.ndarray) -> np.ndarray:
        size = int(np.sqrt(len(curve)))
        return size - 1 - np.fliplr(curve)

    @staticmethod
    def shift(curve: np.ndarray, x: int, y: int) -> np.ndarray:
        return curve + np.array([x, y])[np.newaxis, :]

    @staticmethod
    def closest_hilbert_size(n: int) -> int:
        return int(np.ceil(np.log2(n)))


class HilbertCurve:
    curve: np.ndarray

    def __init__(self, kernel_size: int):
        self.curve = self.generate(kernel_size)

    def generate(self, iteration: int):
        if iteration == 1:
            return np.array([[0, 0], [1, 0], [1, 1], [0, 1]])

        prev = self.generate(iteration - 1)
        # logger.info(f"Prev: {prev}")
        prev_size = int(np.sqrt(len(prev)))

        top_left = HilbertCurveOp.mirror(prev)
        top_right = HilbertCurveOp.shift(prev, prev_size, 0)
        bottom_right = HilbertCurveOp.shift(prev, prev_size, prev_size)
        bottom_left = HilbertCurveOp.shift(HilbertCurveOp.negative_mirror(prev), 0, prev_size)

        return np.vstack((top_left, top_right, bottom_right, bottom_left))

    def get(self):
        return self.curve

    def __str__(self):
        size = int(np.sqrt(len(self.curve)))
        output = np.full((size, size), -1, dtype=int)
        output[self.curve[:, 0], self.curve[:, 1]] = np.arange(len(self.curve))
        return '\n'.join(output)

    def visualize(self):
        points = self.curve.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap='viridis', linewidth=2)
        lc.set_array(np.linspace(0, 1, len(self.curve)))

        fig, ax = plt.subplots(figsize=(10, 10))
        ax.add_collection(lc)
        ax.autoscale()
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])

        plt.colorbar(lc, ax=ax, label="progression bruh zaza")
        plt.tight_layout()
        plt.show()


def main() -> None:
    HilbertCurve(10).visualize()


if __name__ == "__main__":
    main()
