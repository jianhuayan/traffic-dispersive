#!/usr/bin/python2.7
import pexpect
import os
import sys
import dvn
#This script is intend to connecting to DVN systems, performing RESTApi and/or Kennel
#provisioning, invoking IxiaChariot measurements and save/report results.


# Connecting to IxiaChariot system

child = pexpect.spawn('ssh root@gatewayIP')
# child = pexpect.spawn ('ssh root@10.1.0.212')
child.expect('password:')
child.sendline('ixia123')
child.expect('#')
child.sendline('ls')
child.expect('#')
print child.before
# child.interact()


# Set up jitter, delay and error rate on Gateway
child = pexpect.spawn ('ssh root@192.168.120.1')
child.expect('password:')
child.sendline('D1spers1ve$#')
child.expect('#')
child.sendline('tc ---------ls')
child.expect('#')



#Perform IxiaChariot measurement
# os.system('python testapp_RTMP.py')
os.system('python jeff.py')

child = pexpect ('ls -l')
child.expect('testResults.zip')
os.system('mv testResults.zip ./runningLog/')



