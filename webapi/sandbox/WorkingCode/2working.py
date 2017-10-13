#!/usr/bin/python2.7
import pexpect
import os
import sys
import dvn

#This script is intend to connecting to DVN systems, performing RESTApi and/or Kennel
#provisioning, invoking IxiaChariot measurements and save/report results.


# Connecting to IxiaChariot system

dvn.dvnrootlogin(dvn.const.IxiachariotIP, "ixia123")
# print child.before
# child.interact()

#run through a list of files, copy the running results to a directory for later #processing

# make a directory under ./runningLog for the release

command="mkdir" + " ./runningLog/" + dvn.const.ReleaseNum

os.system(command)

with open('./appscripts_list_s', 'r') as f:
    for line in f:
        # os.system('%s %s' %('python', 'argument')
        commandstring="python " +line
        cpstring="cp testResults.zip " + "./runningLog/" + dvn.const.ReleaseNum + "/" + line
        print commandstring
        os.system(commandstring)
        # sleep 15
        print cpstring
        os.system(cpstring)
