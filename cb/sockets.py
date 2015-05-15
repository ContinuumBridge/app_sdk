from traits.api import Delegate, HasTraits, Instance, Event, Int, Str, Bool
from .models import Model

class Socket(Model):

    device = Str()
