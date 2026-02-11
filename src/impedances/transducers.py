from abc import ABC, abstractmethod
import numpy as np
from impedances.electrical import ElectricalImpedance
from impedances.mechanical import MechanicalImpedance
from impedances.acoustical import AcousticalImpedance, AcousticalResistance

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