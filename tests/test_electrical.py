import pytest
import numpy as np
from impedances.electrical import ElectricalImpedance, Resistor, Capacitor

@pytest.fixture
def RC() -> ElectricalImpedance:
    return Resistor(10) + Capacitor(1e-5)

def test_Resistor_Capacitor(RC):
    assert np.abs(RC.Z(np.float64(100))) == pytest.approx(159.4687929050209)