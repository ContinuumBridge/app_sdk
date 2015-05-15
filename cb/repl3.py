import os, sys, tty, termios
from twisted.application.service import Application, IServiceCollection
from twisted.application import service, strports
from twisted.conch.insults.insults import ServerProtocol
#from twisted.conch.manhole_tap   import _StupidRealm
from twisted.conch.stdio import TerminalProcessProtocol, ConsoleManhole
from twisted.internet import protocol

namespace = {"your_application_object": 'test'}

options = \
{
    # for some reason, these must
    # all exist, even if None
    'namespace'  : namespace,
    'passwd'     : 'users.txt',
    'sshPort'    : None,
    'telnetPort' : '4040',
}

'''
def makeService(options):

    svc = service.MultiService()

    namespace = options['namespace']
    if namespace is None:
        namespace = {}

    #checker = checkers.FilePasswordDB(options['passwd'])

    realm = _StupidRealm(telnet.TelnetBootstrapProtocol,
                               insults.ServerProtocol,
                               manhole.ColoredManhole,
                               namespace)

    portal = portal.Portal(realm, [checker])

    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol(ConsoleManhole)
    telnetService = strports.service(options['telnetPort'],
                                     telnetFactory)
    telnetService.setServiceParent(svc)

    return svc

shell_service = makeService(options)

application = Application('test')
serviceCollection = IServiceCollection(application)

shell_service.setServiceParent(serviceCollection)
'''

'''
from twisted.internet import reactor, stdio
from twisted.conch.insults.insults import ServerProtocol
from twisted.conch.stdio import TerminalProcessProtocol, ConsoleManhole

def runWithREPL():
    fd = sys.__stdin__.fileno()
    oldSettings = termios.tcgetattr(fd)
    tty.setraw(fd)
    try:
        p = ServerProtocol(ConsoleManhole)
        stdio.StandardIO(p)
        reactor.run()
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, oldSettings)
        os.write(fd, "\r\x1bc\r")
'''

'''
if __name__ == "__main__":
    runWithREPL()
    #runWithProtocol()
	#reactor.callWhenRunning( createShellServer )
	#
def createShellServer( ):
	print 'Creating shell server instance'
	factory = telnet.ShellFactory()
	port = reactor.listenTCP( 2000, factory)
	factory.namespace['x'] = 'hello world'
	factory.username = 'mike'
	factory.password = 'which1ta'
	print 'Listening on port 2000'
	return port
reactor.run()
'''
