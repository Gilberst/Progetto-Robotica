import numpy as np
from typing import Optional

class Derivate:

    def __init__(self):
        self.prevInput = 0

    def evaluate(self, delta_t, _input):
        out = (_input - self.prevInput) / delta_t
        self.prevInput = _input
        return out


class Integrate:

    def __init__(self):
        self.prevOutput = 0

    def evaluate(self, delta_time, input_value):
        out = self.prevOutput + input_value * delta_time
        self.prevOutput = out
        return out


def saturate(input: float, saturation: float) -> tuple[float, bool]:
    if input > saturation:
        return (saturation, True)
    if input < - saturation:
        return (-saturation, True)
    return (input, False)


class PID_Controller:
    #kp decide quanto reagire, Kd qfrena la reazione, Ki corregge un errore che persiste.
    def __init__(self, Kp: float, Ki: float, Kd : float, Sat: Optional[float] = None,on_measure:Optional[bool]=False):
        self.kp = Kp #gain proporzionale
        self.ki = Ki #gain integrato
        self.kd = Kd #gain derivato
        self.saturation = Sat #saturazione
        self.in_saturation = False
        self.integ = Integrate()
        self.deriv = Derivate()
        self.mode=on_measure

    def evaluate(self, delta_time: float, error: float,value:Optional[float]=None) -> float:
        output = self.kp * error

        if self.in_saturation:
            output = output + self.ki * self.integ.prevOutput
        else:
            output = output + self.ki * self.integ.evaluate(delta_time, error)
        if self.mode:
            output = output + self.kd * self.deriv.evaluate(delta_time, value)
        output = output + self.kd * self.deriv.evaluate(delta_time, error)
        
        if self.saturation is not None:
            output, self.in_saturation = saturate(output, self.saturation)

        return output