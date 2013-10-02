#! /usr/bin/python

import time
import os
from threading import Thread
import threading
import sys

class ResourceMonitor(object):

    # Start monitoring all resources.

    def __init__ (self,duration,numsamples):
        self.duration = duration
        self.numsamples = numsamples
        self.cpuarray = []
        self.iorkbpsarray = []
        self.iowkbpsarray = []

    def Start(self):
        self.t = Thread(target=self.myfunc, args=(self.duration,self.numsamples))
        self.t.start()
    # Stop monitoring all resources.

    def Stop(self):
        self.t.stop()

    def myfunc (self,duration,numsamples):
        while 1:
            self.cpuarray.append (self.GetIndividualStatisticCPU ());
            if (len (self.cpuarray) > numsamples):
                self.cpuarray.pop(0)
            self.iorkbpsarray.append (self.GetIndividualStatisticIORKBPS ());
            if (len (self.iorkbpsarray) > numsamples):
                self.iorkbpsarray.pop(0)
            self.iowkbpsarray.append (self.GetIndividualStatisticIOWKBPS ());
            if (len (self.iowkbpsarray) > numsamples):
                self.iowkbpsarray.pop(0)
            print "Start sleeping for ",duration
            #time.sleep (duration)
            threading.Event().wait(duration)
            print "Stop sleeping"

    # Get the latest value (moving average) for the statistic 'stat_name'.

    def GetIndividualStatisticCPU(self):
        p = os.popen("iostat")
        i=0;
        while 1:
            line = p.readline()
            if not line: break
            if (i==3):
                tmparray = [float(x) for x in line.split()]
                f = float (tmparray[0])
                return f
            i += 1
        print line
    def GetIndividualStatisticIORKBPS(self):
        p = os.popen("iostat -d -x -h -k sda")
        i=0;
        while 1:
            line = p.readline()
            if not line: break
            if (i==3):
                tmparray = [x for x in line.split()]
                f = float (tmparray[5])
                return f
            i += 1
        print line

    def GetIndividualStatisticIOWKBPS(self):
        p = os.popen("iostat -d -x -h -k sda")
        i=0;
        while 1:
            line = p.readline()
            if not line: break
            if (i==3):
                tmparray = [x for x in line.split()]
                f = float (tmparray[6])
                return f
            i += 1
        print line

    def GetStatistic (self,stat_name):
        if (stat_name is "cpu"):
            array = self.cpuarray;
        elif (stat_name == "io-rkbps"):
            array = self.iorkbpsarray;
        elif (stat_name == "io-wkbps"):
            array = self.iowkbpsarray
        else:
            print "Big problem. No such statistic",stat_name
            return -1
        sumarray = sum (array)
        numsamples = len (array)
        avg = sumarray / float (numsamples)
        return avg

resourcemonitor = ResourceMonitor(1,10)
resourcemonitor.Start()
time.sleep (4)
cpuinfo = resourcemonitor.GetStatistic ("cpu");
print "****                cpuinfo is",cpuinfo
iorkbps = resourcemonitor.GetStatistic ("io-rkbps");
print "****                Read I/O bandwidth is ",iorkbps
iowkbps = resourcemonitor.GetStatistic ("io-wkbps");
print "****                Write I/o bandwidth is",iowkbps
sys.exit()

#Output of system ("iostat");
#Linux 3.2.0-33-virtual (ip-10-245-77-20)        08/01/2013      _i686_  (1 CPU)
#
#avg-cpu:  %user   %nice %system %iowait  %steal   %idle
#           0.01    0.03    0.02    0.02    0.14   99.78
#$ iostat -d -x -h -k sda
#Linux 2.6.18-128.el5 (cva-xeon61)       08/01/13
#Device:         rrqm/s   wrqm/s   r/s   w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await  svctm  %util
#sda               0.95    11.19  0.52  1.68     8.12    51.50    54.27     0.11   48.55   4.26   0.94
