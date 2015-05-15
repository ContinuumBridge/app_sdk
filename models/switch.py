from traits.api import Bool, Str
from cb import Model

#print "switch cb ", cb.on_trait_change
class Switch(Model):

    name = Str('test', unique=True)
    value = Str('off')