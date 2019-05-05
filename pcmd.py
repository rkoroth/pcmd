#!/usr/bin/python
#
# Parallel Command executor on remote servers
#

import datetime
import threading
import subprocess
from subprocess import Popen, PIPE
import sys
import socket

VER = "1.0"

def usg():
    print ""
    print "USAGE"
    print "         ./pcmd.py [command]..."
    print ""
    print "EXAMPLE"
    print "         ./pcmd.py 'uname -a'"
    print ""
    print "ADDITIONAL INFO"
    print "         Create a file called 'nodelist' with server names in it"
    print ""

try:
    cmd = sys.argv[1]
    if (cmd == "-V"):
        print "Version: %s" % VER
        sys.exit()
except IndexError:
    usg()
    sys.exit()

def succ(x):
    CT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    print "%s  [SUCCESS]  %s" % (CT,x)
def fail(x):
    CT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    print "%s  [FAIL]     %s" % (CT,x)


def sshcheck():
    with open ('nodelist') as n:
        for i in n:
            s=i.split("\n")[0]
            process = Popen(['ssh -q -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@%s uname -a' % (s)], stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = process.communicate()
            if (process.returncode != 0):
               fail("SSH connectivity %s" % s)
               sys.exit()
            else:
               succ("SSH connectivity %s" % s)
    n.close()

def remcmd(s, c):
   process = Popen(['ssh -q %s %s' % (s, c)], stdout=PIPE, stderr=PIPE, shell=True)
   stdout, stderr = process.communicate()
   if (process.returncode != 0):
        fail("Command execution on %s" % s)
   else:
        succ("Command execution on %s" % s)
        print "Server Name %s" % s
        print stdout
 
def multicmd():
    with open ('nodelist') as n:
        for i in n:
            s=i.split("\n")[0]
            threading.Thread(target=remcmd, args=(s,cmd,)).start()
        for i in n:
            s=i.split("\n")[0]
            threading.Thread(target=remcmd, args=(s,cmd,)).join
    n.close()

sshcheck()
multicmd()
