from typing import Callable
from abc import ABC, abstractmethod
import numpy as np

class Impedance(ABC):
    def __init__(self, Z: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]) -> None:
        self.__Z: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]] = Z

    @property
    def Z(self) -> Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]:
        return self.__Z
    
class ElectricalImpedance(Impedance):
    def __init__(self, Z_e: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]) -> None:
        super().__init__(Z_e)

    def __add__(self, other: 'ElectricalImpedance') -> 'ElectricalImpedance':
        return ElectricalImpedance(lambda f: self.Z(f) + other.Z(f))
    
    def __rtruediv__(self, other: float) -> 'ElectricalImpedance':
        return ElectricalImpedance(lambda f: other / self.Z(f))
    
    def __or__(self, other: 'ElectricalImpedance') -> 'ElectricalImpedance':
        return 1 / (1 / self + 1 / other)

class MechanicalImpedance(Impedance):
    def __init__(self, Z_m: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]) -> None:
        super().__init__(Z_m)

    def __add__(self, other: 'MechanicalImpedance') -> 'MechanicalImpedance':
        return MechanicalImpedance(lambda f: self.Z(f) + other.Z(f))
    
    def __rtruediv__(self, other: float) -> 'MechanicalImpedance':
        return MechanicalImpedance(lambda f: other / self.Z(f))
    
    def __or__(self, other: 'MechanicalImpedance') -> 'MechanicalImpedance':
        return 1 / (1 / self + 1 / other)

class AcousticalImpedance(Impedance):
    def __init__(self, Z_a: Callable[[np.ndarray[tuple[int], np.dtype[np.float64]]], np.ndarray[tuple[int], np.dtype[np.complex128]]]) -> None:
        super().__init__(Z_a)

    def __add__(self, other: 'AcousticalImpedance') -> 'AcousticalImpedance':
        return AcousticalImpedance(lambda f: self.Z(f) + other.Z(f))
    
    def __rtruediv__(self, other: float) -> 'AcousticalImpedance':
        return AcousticalImpedance(lambda f: other / self.Z(f))
    
    def __or__(self, other: 'AcousticalImpedance') -> 'AcousticalImpedance':
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

class Mass(MechanicalImpedance):
    def __init__(self, m_m: float) -> None:
        super().__init__(lambda f: np.array(1j * 2 * np.pi * f * m_m, dtype = np.complex128))

class Spring(MechanicalImpedance):
    def __init__(self, c_m: float) -> None:
        super().__init__(lambda f: np.array(c_m / (1j * 2 * np.pi * f), dtype = np.complex128))

class Damper(MechanicalImpedance):
    def __init__(self, d_m: float) -> None:
        super().__init__(lambda f: d_m * np.ones_like(f, dtype = np.complex128))
        
class FreeRadiation(AcousticalImpedance):
    def __init__(self, rho: float, c: float) -> None:
        super().__init__(lambda f: rho * c * np.ones_like(f, dtype = np.complex128))

class AcousticalMass(AcousticalImpedance):
    def __init__(self, M_a: float) -> None:
        super().__init__(lambda f: np.array(1j * 2 * np.pi * f * M_a, dtype = np.complex128))

class AcousticalResistance(AcousticalImpedance):
    def __init__(self, R_a: float) -> None:
        super().__init__(lambda f: R_a * np.ones_like(f, dtype = np.complex128))

class AcousticalCompliance(AcousticalImpedance):
    def __init__(self, C_a: float) -> None:
        super().__init__(lambda f: np.array(1 / (1j * 2 * np.pi * f * C_a), dtype = np.complex128))

class CompressionChamber(AcousticalCompliance):
    def __init__(self, V: float, rho: float, c: float) -> None:
        super().__init__(C_a = V / (rho * c**2))

class Transducer[T_in, T_out](ABC):
    @abstractmethod
    def __call__(self, input: T_in) -> T_out: ...

class VoiceCoil(Transducer[MechanicalImpedance, ElectricalImpedance]):
    def __init__(self, Bl: float) -> None:
        self.__Bl: float = Bl

    def __call__(self, Z_m: MechanicalImpedance) -> ElectricalImpedance:
        return ElectricalImpedance(lambda f: self.__Bl**2 / Z_m.Z(f))
    
class Diaphragm(Transducer):
    def __init__(self, S_d: float) -> None:
        self.__S_d: float = S_d

    def __call__(self, Z_a: AcousticalImpedance) -> MechanicalImpedance:
        return MechanicalImpedance(lambda f: self.__S_d**2 * Z_a.Z(f))
    
class Duct(Transducer[AcousticalImpedance, AcousticalImpedance]):
    def __init__(self, rho: float, c: float, L: float, S: float) -> None:
        self.__rho: float = rho
        self.__c: float = c
        self.__L: float = L
        self.__S: float = S

    def __call__(self, Z_a: AcousticalImpedance) -> AcousticalImpedance:
        Z_R: AcousticalResistance = AcousticalResistance((self.__rho * self.__c) / self.__S)
        return AcousticalImpedance(lambda f: Z_R.Z(f) * (Z_a.Z(f) + 1j * Z_R.Z(f) * np.tan(2 * np.pi * f / self.__c * self.__L)) / (Z_R.Z(f) + 1j * Z_a.Z(f) * np.tan(2 * np.pi * f / self.__c * self.__L)))