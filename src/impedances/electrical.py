from typing import Callable
import numpy as np
from impedances.base import Impedance

class ElectricalImpedance(Impedance):
    def __init__(self, Z_e: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]) -> None:
        super().__init__(Z_e)

    def __add__(self, other: 'ElectricalImpedance') -> 'ElectricalImpedance':
        return ElectricalImpedance(lambda f: self.Z(f) + other.Z(f))
    
    def __rtruediv__(self, other: float) -> 'ElectricalImpedance':
        return ElectricalImpedance(lambda f: other / self.Z(f))
    
    def __or__(self, other: 'ElectricalImpedance') -> 'ElectricalImpedance':
        return 1 / (1 / self + 1 / other)
    
class Coil(ElectricalImpedance):
    def __init__(self, L_e: float) -> None:
        super().__init__(lambda f: np.array(1j * 2 * np.pi * f * L_e, dtype = np.complex128))

class Resistor(ElectricalImpedance):
    def __init__(self, R_e: float) -> None:
        super().__init__(lambda f: R_e * np.ones_like(f, dtype = np.complex128))

class Capacitor(ElectricalImpedance):
    def __init__(self, C_e: float) -> None:
        super().__init__(lambda f: np.array(1 / (1j * 2 * np.pi * f * C_e), dtype = np.complex128))