from typing import Callable
from abc import ABC
import numpy as np

class Impedance(ABC):
    def __init__(self, Z: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]) -> None:
        self.__Z: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]] = Z

    @property
    def Z(self) -> Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]:
        return self.__Z