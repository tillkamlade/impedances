from typing import Callable
import numpy as np
from impedances.base import Impedance

class AcousticalImpedance(Impedance):
    def __init__(self, Z_a: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]) -> None:
        super().__init__(Z_a)

    def __add__(self, other: 'AcousticalImpedance') -> 'AcousticalImpedance':
        return AcousticalImpedance(lambda f: self.Z(f) + other.Z(f))
    
    def __rtruediv__(self, other: float) -> 'AcousticalImpedance':
        return AcousticalImpedance(lambda f: other / self.Z(f))
    
    def __or__(self, other: 'AcousticalImpedance') -> 'AcousticalImpedance':
        return 1 / (1 / self + 1 / other)
    
class AcousticalMass(AcousticalImpedance):
    def __init__(self, M_a: float) -> None:
        super().__init__(lambda f: np.array(1j * 2 * np.pi * f * M_a, dtype = np.complex128))

class AcousticalResistance(AcousticalImpedance):
    def __init__(self, R_a: float) -> None:
        super().__init__(lambda f: R_a * np.ones_like(f, dtype = np.complex128))

class AcousticalCompliance(AcousticalImpedance):
    def __init__(self, C_a: float) -> None:
        super().__init__(lambda f: np.array(1 / (1j * 2 * np.pi * f * C_a), dtype = np.complex128))

class FreeRadiation(AcousticalImpedance):
    def __init__(self, rho: float, c: float) -> None:
        super().__init__(lambda f: rho * c * np.ones_like(f, dtype = np.complex128))

class CompressionChamber(AcousticalCompliance):
    def __init__(self, V: float, rho: float, c: float) -> None:
        super().__init__(C_a = V / (rho * c**2))