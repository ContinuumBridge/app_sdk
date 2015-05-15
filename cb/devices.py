from traits.api import Delegate, HasTraits, Instance, Event, Int, Str, Bool, List
from .models import Model

class Service(Model):
    pass

def ServiceFactory(name, argnames, BaseClass=Service):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # here, the argnames variable is the one passed to the
            # ClassFactory call
            if key not in argnames:
                raise TypeError("Argument %s not valid for %s"
                    % (key, self.__class__.__name__))
            setattr(self, key, value)
        BaseClass.__init__(self, name[:-len("Class")])
    newclass = type(name, (BaseClass,),{"__init__": __init__})
    return newclass


'''
class Device(Model):

    cbid = Str(unique=True)
    services = List(trait=Service)
    service = Instance(Service)
'''

