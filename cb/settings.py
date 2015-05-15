import os
from utils import get_env_variable

SWARM_SOCKET = '/var/tmp/swarm_socket'
#PROJECT_ROOT = get_env_variable("CB_PROJECT_ROOT")
PROJECT_ROOT = os.getenv('CB_PROJECT_ROOT', '/home/vagrant/app')
