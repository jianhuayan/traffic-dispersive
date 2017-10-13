#!/usr/bin/python2.7
import pexpect
import os
import sys
import dvn
import Dvnconstant as const
import time

#This script is intend to connecting to DVN systems, performing RESTApi and/or Kennel
#provisioning, invoking IxiaChariot measurements and save/report results.


# Connection to RestApi and provision real time UDP setting

#dvn.udpService()

# Connect to DVN system to configure impairments on DVN network, this must
# refer to network diagram

# time.sleep(30)

# dvn.impairments(const.L3GW_1_IP,"p1p1","80ms", "5ms", "0.02%")

# time.sleep(30)


# Connecting to IxiaChariot system

# dvn.dvnrootlogin(const.IxiachariotIP, "ixia123")
# print child.before
# child.interact()

#run through a list of files, copy the running results to a directory for later #processing

# make a directory under ./runningLog for the release

# Connecting to AutoDB to find impariments and make the setting

#db.connect
#for line in db.row
#do

#{make the impairment setting
#        run the ixia measurements
#        log the results
#        process the data
#        write the results to the db
#        close the db
#        }

command="mkdir" + " ./runningLog/" + dvn.const.ReleaseNum

os.system(command)

dvn.dbconnect()

for 


with open('./flowscripts_skyvoip', 'r') as f:
    for line in f:
        # os.system('%s %s' %('python', 'argument')
        commandstring="python " +line

        cpstring="cp testResults.zip " + "./runningLog/" + dvn.const.ReleaseNum + "/" 
        gologdircmd = "cd " + "./runningLog/" + dvn.const.ReleaseNum + "/"
        os.system(commandstring)
        print cpstring
        os.system(cpstring)
        # starting to process log
        gologdircmd = "cd " + "./runningLog/" + dvn.const.ReleaseNum + "/"
        os.system(gologdircmd)
        # os.system("rm -rf *.*")
        unzipcmd = "unzip " + "testResults.zip" 
        os.system(unzipcmd)
        dvn.logPro(line)




