from typing import Callable
import numpy as np
from impedances.base import Impedance

class MechanicalImpedance(Impedance):
    def __init__(self, Z_m: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]) -> None:
        super().__init__(Z_m)

    def __add__(self, other: 'MechanicalImpedance') -> 'MechanicalImpedance':
        return MechanicalImpedance(lambda f: self.Z(f) + other.Z(f))
    
    def __rtruediv__(self, other: float) -> 'MechanicalImpedance':
        return MechanicalImpedance(lambda f: other / self.Z(f))
    
    def __or__(self, other: 'MechanicalImpedance') -> 'MechanicalImpedance':
        return 1 / (1 / self + 1 / other)

class Mass(MechanicalImpedance):
    def __init__(self, m_m: float) -> None:
        super().__init__(lambda f: np.array(1j * 2 * np.pi * f * m_m, dtype = np.complex128))

class Damper(MechanicalImpedance):
    def __init__(self, d_m: float) -> None:
        super().__init__(lambda f: d_m * np.ones_like(f, dtype = np.complex128))

class Spring(MechanicalImpedance):
    def __init__(self, c_m: float) -> None:
        super().__init__(lambda f: np.array(c_m / (1j * 2 * np.pi * f), dtype = np.complex128))