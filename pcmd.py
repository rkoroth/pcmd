#!/usr/bin/python
#
# Parallel Command executor on remote servers

import datetime
import threading
import subprocess
from subprocess import Popen, PIPE
import sys
import socket
import os

VER = "1.01"

def usg():
    print ("")
    print ("USAGE")
    print ("         ./pcmd.py [command]...")
    print ("")
    print ("EXAMPLE")
    print ("         ./pcmd.py 'uname -a'")
    print ("")
    print ("ADDITIONAL INFO")
    print ("         Create a file called 'nodelist' with server names and commands(if any) in it")
    print ("         if there is no command against a server in the 'nodelist' file, the command in the argument will be executed")
    print ("")

if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if (cmd == "-V"):
        print ("Version: %s" % VER)
        sys.exit()


class LogWrite:
  
    def __init__(self, logFile):
        self.logFile = logFile

    def write(self, level, message):
    
        if self.logFile:
          logging = True
        
        CT = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        if level == "success":
            logData = "{} [SUCCESS] {}".format(CT, message)
            print (logData)
        elif level == "fail":
            logData = "{} [FAIL] {}".format(CT, message)
            print (logData)
        elif level == "info":
            logData = "{} [INFO] {}".format(CT, message)
            print (logData)        
        elif level == "error":
            logData = "{} [ERROR] {}".format(CT, message)
            print (logData)
        elif level == "warning":
            logData = "{} [WARNING] {}".format(CT, message)
            print (logData)
        elif level == "passed":
            logData = "{} [PASSED] {}".format(CT, message)
            print (logData)

        if logging:
           logFileHandler = open(self.logFile, "aw")  
           logFileHandler.write(logData + "\n")
           logFileHandler.close()   

log_file = "pcmd.log"
stdoutmsg =  LogWrite(log_file)   


def validateNodelist():
    if os.path.isfile("nodelist"):
        stdoutmsg.write("success", "nodelist file found. Proceeding further")
    else:
        stdoutmsg.write("fail", "Missing nodelist file")
        sys.exit(1)


def sshcheck():
    stdoutmsg.write("info", "Validating SSH connectivity")
    with open ('nodelist') as n:
        for i in n:
            if ";" in i:
                s=i.split(";")[0]
            else:
                s=i.strip()
            process = Popen(['ssh -q -o StrictHostKeyChecking=no -o ConnectTimeout=10 root@%s uname -a' % (s)], stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = process.communicate()
            if (process.returncode != 0):
               stdoutmsg.write("fail", "SSH connectivity {}".format(s))
               sys.exit()
            else:
               stdoutmsg.write("success", "SSH connectivity {}".format(s))
    stdoutmsg.write("success", "All node are connecting, proceeding with command execution")
    n.close()

def remcmd(s, c):
   process = Popen(['ssh -q %s %s' % (s, c)], stdout=PIPE, stderr=PIPE, shell=True)
   stdout, stderr = process.communicate()
   if (process.returncode != 0):
        stdoutmsg.write("fail", "Command execution on {}".format(s))
   else:
        stdoutmsg.write("success", "Command {} execution on {}".format(c, s))
        print ("############################################")
        print ("Server Name %s" % s)
        stdout = stdout.decode("utf-8")
        print (stdout)
 
def multicmd():
    with open ('nodelist') as n:
        for line in n:
            if ";" not in line:
                server = line.strip()
                command = cmd
            else:
                server  = line.split(";")[0]
                command = line.split(";")[1].strip()
            threading.Thread(target=remcmd, args=(server,command,)).start()
        for line in n:
            if ";" not in line:
                server = line.strip()
                command = cmd
            else:
                server  = line.split(";")[0]
                command = line.split(";")[1].strip()
            threading.Thread(target=remcmd, args=(server,command,)).join
    n.close()

#MAIN
validateNodelist()
sshcheck()
multicmd()
