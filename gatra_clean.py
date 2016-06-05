import datetime
import django
import os
from django.utils import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gatra.settings")
django.setup()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Base Exceptions
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.core.exceptions import *

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# App Model
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from gatra_player.models import Hash

from daemon import Daemon
from sys    import exit
from sys    import argv

import logging
import time

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Basic Config
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
LOG_FILE = './log/clean.log'
ERR_FILE = './log/clean.err'
PID_FILE = './pid/clean.pid'


def clean_main():

    logging.basicConfig(format   = '%(asctime)s - gatra_clean.py -[%(levelname)s]: %(message)s',
                        filename = LOG_FILE,
                        level    = logging.INFO)

    
    while True:
	i = 0
	_hash = Hash.objects.all()
	for h in _hash:
	    if h.expiration < timezone.now():
		h.delete()
		i = i + 1
	logging.info("clean(): %d hash cleaned" % i)
	time.sleep(600)


class DaemonMain(Daemon):
    def run(self):
        try:
            clean_main()
        except KeyboardInterrupt:
            exit()

if __name__ == "__main__":
    daemon = DaemonMain(PID_FILE, stdout=LOG_FILE, stderr=ERR_FILE)
    if len(argv) == 2:
        if 'start'     == argv[1]:
            daemon.start()
        elif 'stop'    == argv[1]:
            daemon.stop()
        elif 'restart' == argv[1]:
            daemon.restart()
        elif 'run'     == argv[1]:
            daemon.run()
        elif 'status'  == argv[1]:
            daemon.status()
        else:
            print "Unknown command"
            exit(2)
        exit(0)
    else:
        print "usage: %s start|stop|restart|run" % argv[0]
        exit(2)
