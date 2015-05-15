import sys
import socket
#import symmetricjsonrpc

import json

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver, NetstringReceiver
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.endpoints import UNIXClientEndpoint
#from fastjsonrpc.client import ProxyFactory
from txjsonrpc.netstring.jsonrpc import Proxy, BaseQueryFactory

from .settings import SWARM_SOCKET

class SwarmProxy(NetstringReceiver):

    def __init__(self, onMessage):
        self.whenDisconnected = Deferred()
        self.onMessage = onMessage

    def connectionMade(self):
        pass
        #self.sendLine("Hello, world!")
        #self.sendLine("What a fine day it is.")

    '''
    def dataReceived(self, netstring):

        print "netstring received:", netstring
        try:
            data = json.loads(netstring[:-1].split(':', 1)[1])
            #data = json.loads("""82:{"type":"Switch","data":{"value":"off","name":"test","id":"2_LXh06+swarm~nodejs"}},"""[:-1].split(':', 1)[1])
            print "data received", data
            self.onMessage(data)
        except ValueError:
            print "Invalid json received", netstring
    '''


    def stringReceived(self, string):
        print "stringReceived", string
        data = json.loads(string)
        self.onMessage(data)
        '''
        try:
        except ValueError:
            print "Invalid json received", string
        '''

    '''
    def lineReceived(self, line):
        print "SwarmClient received:", line
        self.onMessage(line)
        #if line==self.end:
        #    self.transport.loseConnection()
    '''

    def whenDisconnected(self):
        pass

class SwarmClientFactory(ClientFactory):

    #protocol = SwarmClient
    #quiet = True

    def __init__(self, onMessage):
        self.onMessage = onMessage
        print "SwarmClientFactory", onMessage

    def buildProtocol(self, addr):
        p = SwarmProxy(self.onMessage)
        p.factory = self
        return p

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()

def printValue(value):
    print "Result: %s" % str(value)

def printError(error):
    print 'error', error

'''
class QueryProtocol(LineReceiver):

    def connectionMade(self):
        self.data = ''
        msg = self.factory.payload
        packet = '%d:%s,' % (len(msg), msg)
        self.transport.write(packet)

    def stringReceived(self, string):
        self.factory.data = string
        self.transport.loseConnection()

class QueryFactory(BaseQueryFactory):

    protocol = QueryProtocol
    data = ''

    def clientConnectionLost(self, _, reason):
        self.parseResponse(self.data)
'''

class SwarmRPC(Proxy):

    def callRemote(self, method, *args, **kwargs):
        version = self._getVersion(kwargs)
        #print "version  is", version
        factoryClass = self._getFactoryClass(kwargs)
        #print "factoryClass  is", factoryClass
        factory = factoryClass(method, version, *args)
        #factory = QueryFactory(method, version, *args)
        rpc_socket = SWARM_SOCKET + '_rpc'
        #rpc_socket = "/var/tmp/swarm_listen"
        reactor.connectUNIX(rpc_socket, factory)
        #reactor.connectTCP(self.host, self.port, factory)
        return factory.deferred


class SwarmConnection(object):

    def __init__(self, onMessage):
        #s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.onMessage = onMessage
        self.rpc = SwarmRPC('nowhere', 1234, version=2)
        self.setup_client()


    def call_remote(self, method, *args, **kwargs):
        #print "SwarmConnection call_remote", kwargs
        swarm_method = "swarm." + method
        return self.rpc.callRemote(swarm_method, *args)
        #request.addCallbacks(printValue, printError)

    def setup_client(self):

        factory = SwarmClientFactory(self.onMessage)
        endpoint = UNIXClientEndpoint(reactor, SWARM_SOCKET)
        connected = endpoint.connect(factory)

        '''
        def succeeded(client):
            print "Succeeded"
            return client.whenDisconnected
        def failed(reason):
            print "Could not connect:", reason.getErrorMessage()
        def disconnected(ignored):
            print "Disconnected"
            reactor.stop()

        connected.addCallbacks(succeeded, failed)
        connected.addCallback(disconnected)
        '''


'''
# Call a method on the server
res = client.request("swarm.ping", wait_for_response=True)
print "client.ping => %s" % (repr(res),)
assert res == "pong"

# Notify server it can shut down
client.notify("shutdown")

client.shutdown()
'''

'''
class SwarmRPCClient(symmetricjsonrpc.RPCClient):

    class Request(symmetricjsonrpc.RPCClient.Request):
        def dispatch_request(self, subject):
            # Handle callbacks from the server
            print "dispatch_request(%s)" % (repr(subject),)
            assert subject['method'] == "pingping"
            return "pingpong"
'''