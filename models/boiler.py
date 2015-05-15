
from traits.api import Int, List, DelegatesTo, Instance
from cb import Model

#from ...sockets import BoilerSocket
#from .models import TemperatureControl

class BoilerController(Model):

    #on = DelegatesTo('socket')
    #socket = Instance(BoilerSocket)

    #controls = List(TemperatureControl)

    def _controls_items_changed(self, old, new):
        for control in self.controls:
            if control.on:
                self.on = True
                return
        self.on = False
