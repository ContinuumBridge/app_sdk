from twisted.internet import defer
from traits.api import Delegate, HasTraits, Instance, Event, Int, Str, Bool
from traits.has_traits import MetaHasTraits
from traits.trait_base import not_event
from .exceptions import MultipleObjectsReturned
#from .cb import CB


class MetaModel(MetaHasTraits):

    def __init__(cls, name, bases, dct):
        cls.store_objects = {}
        #schema = cls.class_get_schema()
        try:
            #cb = cls.get_cb()
            print "Register schema", cls.__name__
            cb.register_schema(cls)
        except NameError:
            pass
        super(MetaModel, cls).__init__(name, bases, dct)

    '''
    def __call__(cls, *args, **kwargs):
        print "MetaModel called", cls
        print "*args is", args
        print "**kwargs is", kwargs
        #print "dir() is", test
        #return super(MetaModel, cls).__call__(cls, *args, **kwargs)
    '''

class Model(HasTraits):

    id = Str()
    _receiving_data = Bool(False)

    __metaclass__ = MetaModel

    def __new__(cls, *args, **kwargs):
        model = cls.store_create_model(*args, **kwargs)
        #model = super(Model, cls).__new__(cls, *args, **kwargs)
        #model = cls.store_subscribe(model)
        return model

    @classmethod
    def get_cb(self):
        try:
            return cb
        except NameError:
            print "Your python code must be run in the Continuum Bridge framework"

    def traits_dict(self, require_unique=False):
        traits = self.traits(type=not_event)
        del traits['_receiving_data']
        for name in traits:
            value = getattr( self, name )
            traits[name] = value
        print "traits  is", traits
        return traits

    @classmethod
    def class_get_trait_schema(cls, trait_name):

        trait = cls.__class_traits__[trait_name]
        schema = {
            'default': trait.default,
        }

        unique = getattr(trait, 'unique')
        if unique:
            schema['unique'] = unique

        type = trait.trait_type.__class__.__name__

        if type == "Instance":
            schema['item_type'] = trait.handler.klass.__name__
            schema['relation'] = "one"
            print "Instance schema is", schema

        if type == "List":
            schema['type'] = type
            #inner_traits, = trait.handler.inner_traits()
            #schema['item_types'] = [t.handler.aClass.__name__ for t in trait.inner_traits]
            inner_trait, = trait.inner_traits
            schema['item_type'] = inner_trait.handler.aClass.__name__
            schema['relation'] = "many"

        return schema

    @classmethod
    def class_get_schema(cls):
        trait_names = cls.class_editable_traits()
        trait_names.remove('_receiving_data')
        trait_schemas = [cls.class_get_trait_schema(t) for t in trait_names]
        return dict(zip(trait_names, trait_schemas))

    @classmethod
    def class_get_unique_traits(cls):
        trait_names = cls.class_editable_traits()
        traits = {trait_name: cls.__class_traits__[trait_name] for trait_name  in trait_names}
        print "class_get_unique_traits traits is", traits
        unique_traits = {}
        for trait_name in traits:
            trait = traits[trait_name]
            if getattr(trait, 'unique'):
                unique_traits[trait_name] = trait
        return unique_traits

    '''
    @classmethod
    @defer.inlineCallbacks
    def query(cls, method, type, parameters=None):
        data = yield cb.query(method, type)
        #print "query data", data
        yield data
    '''

    @classmethod
    def all(cls):
        return cls.store_objects
        '''
        #data = yield cb.query('all', cls.__name__)
        data = cls.query('all', cls.__name__)
        print "all data is", data
        models = [cls(d) for d in data]
        return models
        '''

    @classmethod
    def get(cls, **kwargs):

        print "get kwargs", kwargs
        found = False
        for id in cls.store_objects:
            model = cls.store_objects[id]
            for key in kwargs:
                value = kwargs[key]
                if value and getattr(model, key) != value:
                    break
                else:
                    if not found:
                        found = model
                    else:
                        raise MultipleObjectsReturned('Get found multiple objects for query', kwargs)
        return found

    @classmethod
    def store_create_model(cls, *args, **kwargs):

        # Check if the model is already instantiated and can be found by a uniquely identifying trait
        unique_traits = cls.class_get_unique_traits()
        print "store_create_model unique_traits  is", unique_traits
        for trait_name in unique_traits:
            trait = unique_traits[trait_name]
            unique_value = kwargs.get(trait_name)
            if unique_value != trait.default:
                query = {
                    '{0}'.format(trait_name): unique_value
                }
                # If a matching model is found in the store, return it
                model = cls.get(**query)
                print "store_create_model found model", model

        def create_success(data):
            print "update_model data", data
            id = data['id']
            model.trait_set(data)
            cls.store_objects[id] = model

        def create_error(error):
            print "Error creating %s:" % cls.__name__, error

        model = super(Model, cls).__new__(cls, *args, **kwargs)
        print "store_create_model model is", model

        model_traits = model.traits_dict()

        print "store_create_model model_traits is", model_traits
        type = cls.__name__
        #cb = cls.get_cb()
        cb.create_model(type, model_traits).addCallbacks(create_success, create_error)

    @classmethod
    def store_deliver(cls, data):
        id = data['id']
        if not id:
            print "Data received at store from swarm has no id"
        try:
            model = cls.store_objects[id]
            model.deliver(data)
        except KeyError:
            cls.store_objects[id] = cls(data)
            #print "Store could not find object", data

    def deliver(self, data):
        self._receiving_data = True
        print "Instance deliver", self.__class__.__name__, data
        self.trait_set(**data)
        self._receiving_data = False

    def _anytrait_changed(self, name, old, new):

        #print "_anytrait_changed ", name

        if name in ['trait_added', '_receiving_data']:
            return
        if self._receiving_data:
            return

        print "_anytrait_changed self._receiving_data", self._receiving_data

        print 'The %s trait changed from %s to %s ' \
              % (name, old, new)

        #cb = self.get_cb()
        traits = self.traits_dict()
        cb.on_trait_change(self.__class__.__name__, traits)
        '''
        try:
            print "cb on_trait_change", cb
        except NameError:
            pass
        '''


class Controller(Model):

    pass

'''
def get_cb():
    try:
        return cb
    except NameError:
        print "Your python code must be run in the Continuum Bridge framework"
'''
