import os, sys

import runpy
import imp
from .swarm_client import SwarmClient
from .manager_client import ManagerClient
from twisted.internet import reactor, defer
import settings
from .models import Model
#from .devices import Device
#from .repl import runWithREPL

class CB(SwarmClient, ManagerClient):

    def __init__(self):

        SwarmClient.__init__(self)
        ManagerClient.__init__(self)
        #super(CB, self).__init__()

        __builtins__['cb'] = self

        load_deferred = self.load_models()
        load_deferred.addCallback(start_app)

    def call_remote(self, method, *args, **kwargs):
        return self.swarm.call_remote(method, *args)

    def run(self, repl=False):
        if repl:
            runWithREPL()
        else:
            reactor.run()

    def load_models(self):
        models_dir = os.path.join(settings.PROJECT_ROOT, 'models')
        print "models_dir  is", models_dir

        # Load device models
        #schema = Device.class_get_schema()
        #self.call_remote('registerSchema', Device.__name__, schema)
        deferred_list = []

        # Load app models
        for py in [f[:-3] for f in os.listdir(models_dir) if f.endswith('.py') and f != '__init__.py']:
            py_path = os.path.join(models_dir, py) + ".py"
            mod = imp.load_source('user_models', py_path)
            classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
            for cls in classes:
                if issubclass(cls, Model) and cls != Model:
                    schema = cls.class_get_schema()
                    print "register traits", schema
                    register_deferred = self.call_remote('registerSchema', cls.__name__, schema)
                    deferred_list.append(register_deferred)

        print "deferred_list is", deferred_list
        return defer.DeferredList(deferred_list)


    def get(self, type, id):
        pass

    def all(self, type):
        pass

#cb = CB()

def start_app(result):
    reactor.callWhenRunning(run_app)

def run_app():
    print "run_app"
    path, dirname = os.path.split(settings.PROJECT_ROOT)
    sys.path.append(path)
    test = "Testing!"
    app = __import__('app')
    #classes = [getattr(app, x) for x in dir(app) if isinstance(getattr(mod, x), type)]
    for x in dir(app):
        if not x.startswith('__'):
            __builtins__[x] = getattr(app, x)
    #app = imp.load_source('app', path)
    #app = runpy.run_module(dirname, init_globals=__builtins__)
    __builtins__['app'] = app
    #print "app_test is ", app_test
    #runpy.run_path(settings.PROJECT_ROOT)
    #execfile(settings.PROJECT_ROOT, globals(), locals())
    '''
    app = __import__(dirname, globals(), locals(), [], -1)
    print "app  is", app
    Model.test = "Model test"
    #app.init("Testing!")
    '''
    '''
    main_path = os.path.join(settings.PROJECT_ROOT, "main.py")
    path, dirname = os.path.split(settings.PROJECT_ROOT)
    f, filename, description = imp.find_module(dirname, [ path ])
    app = imp.load_module('app', f, filename, description)
    app.test = "Testing!"
    '''