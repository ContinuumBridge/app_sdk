
from traits.api import Delegate, HasTraits, Instance, Event, Int, Str, Bool, List
import contextlib
#from cb import Device, Service
from .models import Switch

#print "main cb", cb.on_trait_change

'''
class Test(HasTraits):

    tl = List(trait=Str)
    #socket = Instance(Switch)

#t = Test()
#t.__class__.__class_traits__['tl_items'].trait_type
'''

switch = Switch(name="Polly")

'''
import inspect
record=inspect.getouterframes(inspect.currentframe())[1]
frame=record[0]

if 'test' in frame.f_globals:
    print 'FOO in globals'
else:
    print 'nah'
'''




'''
from .sockets import ThermometerSocket, BoilerSocket
from .models import TemperatureControl, BoilerController

### 1
boiler = BoilerController(socket=BoilerSocket.connections[0])

boiler.on = True

for thermometer in ThermometerSocket.connections:
    control = TemperatureControl(thermometer=thermometer)
    boiler.controls.append(control)


### 2
def connect_boiler(boiler):

    def connect_thermometer(thermometer):
        control = TemperatureControl(thermometer=thermometer)
        boiler.controls.append(control)

    ThermometerSocket.onConnection(connect_thermometer)

BoilerSocket.onConnection(connect_boiler)
'''

