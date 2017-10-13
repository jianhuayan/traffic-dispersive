#!/usr/bin/python2.7
import pexpect
import os
import sys
import time

#This script is intend to connecting to DVN systems, performing RESTApi and/or Kennel
#provisioning, invoking IxiaChariot measurements and save/report results.


# Connecting to DVN systems

gatewayIP = '10.1.0.212'

# child = pexpect.spawn('ssh root@gatewayIP')
child = pexpect.spawn ('ssh root@10.1.0.212')
child.expect('password:')
child.sendline('ixia123')
child.expect('#')
child.sendline('ls')
child.expect('#')
print child.before
# child.interact()

#run through a list of files, copy the running results to a directory for later #processing

with open('./appscripts_list', 'r') as f:
    for line in f:
        # os.system('%s %s' %('python', 'argument')
        cmdstring="python " +line
        cpstring="cp testResults.zip " + "./runningLog/"+line
        print cmdstring
        os.system(cmdstring)
        time.sleep(30)
        print cpstring
        os.system(cpstring)
