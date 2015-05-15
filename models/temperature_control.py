
'''
from traits.api import Int, Instance, DelegatesTo
from cb import Model

#from ...sockets import ThermometerSocket

class TemperatureControl(Model):

    min = Int(unique=True)
    #temperature = DelegatesTo('thermometer')

    #thermometer = Instance(ThermometerSocket, unique=True)
'''

