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
from gatra_player.models import Play
from gatra_player.models import Event


from daemon import Daemon
from sys    import exit
from sys    import argv

import logging
import time

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Basic Config
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
LOG_FILE = './log/reduce.log'
ERR_FILE = './log/reduce.err'
PID_FILE = './pid/reduce.pid'


##
# Retorna una lista con los eventos asociados a un play
def getEvents(play):
    return Event.objects.filter(play=play)
##
# Retorna los eventos a reducir
def getPlayToReduce():
    return Play.objects.filter(reduced=False)

##
# Retorna el tiempo de reproduccion
def getRepTime(events):
    if len(events) > 0:
	if events[0].position < 40:
	    n = events[0].position
	else:
	    n = 30.00
	return len(events) * n
    return 0;

def reduceRepTime():
    i = 0
    delta = datetime.timedelta(hours=-2) 
    play  = getPlayToReduce()
    for p in play:
	if p.date <= timezone.now() + delta:
	    event = getEvents(p)
	    p.reduced  = True
	    p.rep_time = getRepTime(event)
	    p.save()
	    i = i + 1
    return i


def reduce_main():

    logging.basicConfig(format   = '%(asctime)s - gatra_reduce.py -[%(levelname)s]: %(message)s',
                        filename = LOG_FILE,
                        level    = logging.INFO)

    
    while True:
	logging.info("Running Reduce Rep Time")
	r = reduceRepTime()
	logging.info("reduceRepTime(): %d Play Event reduced" % r);
	time.sleep(600)


class DaemonMain(Daemon):
    def run(self):
        try:
            reduce_main()
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
