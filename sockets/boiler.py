from traits.api import Bool, Str, Int
from cb import Socket

class BoilerSocket(Socket):

    max_connections = 1

    on = Bool()