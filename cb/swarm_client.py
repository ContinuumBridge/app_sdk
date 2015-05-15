
from .rpc import SwarmConnection
#from .devices import Device, Service

class SwarmClient(object):

    def __init__(self):

        self.stores = {}
        self.sockets = {}

        self.swarm = SwarmConnection(self.on_swarm_message)

        self.initialize()

    def initialize(self):
        pass

        '''
        for cls in [Device, Service]:
            self.register_schema(cls)
        '''

    def register_schema(self, cls):
        name = cls.__name__
        schema = cls.class_get_schema()

        def register_success(response):
            print "Register schema success", response
            self.stores[name] = cls

        def register_error(error):
            print "Register schema error", error, cls

        self.swarm.call_remote('registerSchema', name, schema).addCallbacks(register_success, register_error)

    def register_socket(self, cls, schema):
        name = cls.__name__
        if self.swarm.call_remote('registerSchema', name, schema):
            self.sockets[name] = cls

    def create_model(self, name, traits):
        return self.swarm.call_remote('createModel', name, traits)

    def on_trait_change(self, name, traits):
        return self.swarm.call_remote('onTraitChange', name, traits)

    def query(self, verb, type, parameters=None):
        return self.swarm.call_remote('query', verb, type, parameters)

    def on_swarm_message(self, message):
        print "Dispatcher onSwarmMessage", message
        self.deliver(message)

    #def get_store(self, name):

    def deliver(self, message):
        print "dispatcher deliver message", message
        try:
            type = message['type']
            store = self.stores[type]
            data = message['data']
            store.store_deliver(data)
        except KeyError:
            print "Deliver could not find store"






    '''
    def subscribe(self, model):
       self.listeners.append(model)

    def unsubscribe(self, model):
        try:
            self.listeners.remove(model)
        except ValueError:
            pass

    def dispatch(self, message):
        for l in self.listeners:
            l.dispatch(message)
    '''

