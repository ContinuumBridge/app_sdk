from traits.api import Bool, Str, Int
from cb import Socket

class ThermometerSocket(Socket):

    temperature = Int()
