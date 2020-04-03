# This script detects if some ssh connection event or process has started

import os

logfile_path = "/var/log/auth.log"

class EventDetector:

    def __init__(self,name,outfile):
        self.name = name
        self.outfile = outfile

#class LogEventDetector:

def logParser():
    pass

def logReader(filepath):
    logfile = open(filepath,'r')
    logfile.read()

def runner():
    logReader(logfile_path)
    logParser()

logParser()