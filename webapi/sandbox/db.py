#!/usr/bin/python2.7
import pexpect
import os
import sys
import csv
import numpy as np
import Dvnconstant as const 
# import matplotlib
# import pylab as pl

def func():
    print "this is just a testing...\n"
    return 1

def impairments(ip_addr,ifname, delay_value, jitter_value, loss_value):
    #if delay = 0:
        print "OK here..\n"
        tccommand='tc qdisc add dev %s root netem delay %s %s distribution normal loss %s'%(ifname, delay_value, jitter_value, loss_value)  
        print tccommand
        child = pexpect.spawn('ssh -l %s %s'%("root", ip_addr))
        # child = pexpect.spawn ('ssh root@192.168.200.4')
        child.expect('password:')
        child.sendline('D1spers1ve')
        child.expect('#')
        child.sendline('ls -lrt')
        child.expect('#')
        print "We are reaching the middle.\n"
        
        child.sendline(tccommand)
        #child.sendline('tc qdisc add dev p1p1 root netem delay 70ms 5ms distribution normal loss 0.25%')
        child.expect('#') 
        print "we are at the end.\n"         

def udpService():
        newmancommand='newman run GwServiceTest.postman_collection -e Gw.pstman_environment -d gw_service_1.csv -k -n 1'
        print newmancommand
        child = pexpect.spawn('ssh -l %s %s'%("root", const.RestApiIP))
        # child = pexpect.spawn('ssh root@172.16.60.1')
        child.expect('password:')
        child.sendline('D1spers1ve')
        child.expect('#')
        child.sendline('cd /home/seit31/automation/ixia/')
        child.expect('#')
        print "I am here now.\n"
        child.sendline(newmancommand)
        # child.sendline('newman run GwServiceTest.postman_collection -e Gw.pstman_environment -d gw_service_1.csv -k -n 1')
        child.expect('#')
        print "I am done\n"

def dvnrootlogin(system_ip, password):
        child = pexpect.spawn('ssh -l %s %s'%("root",system_ip))
        # print "input need to under quotation mark\n"
        child.expect('password:')
        child.sendline(password)
        child.expect('#')
        child.sendline('ls')
        child.expect('#')


def login(host, user, password):

    child = pexpect.spawn('ssh -l %s %s'%(user, host))
    fout = file ("LOG.TXT","wb")
    # child.setlog (fout)
    
    # i = child.expect([pexpect.TIMEOUT, SSH_NEWKEY, '[Pp]assword: '])
    i = child.expect([pexpect.TIMEOUT, '[Pp]assword: '])
    if i == 0: # Timeout
       print 'ERROR!'
       print 'SSH could not login. Here is what SSH said:'
       print child.before, child.after
       sys.exit (1)
    if i == 1: # SSH does not have the public key. Just accept it.
       child.sendline ('yes')
       child.expect ('[Pp]assword: ')
       child.sendline(password)
       # Now we are either at the command prompt or
       # the login process is asking for our terminal type.
       child.expect ('#')



#This script is intend to parse the IxiaChariot saved log file and extract the data and perform the plot


# Process the csv file
def logPro(csvFile_in):
    with open('ixchariot.csv', 'rb') as ixiafile:
        csv_f = csv.reader(ixiafile)
        Avg_Throughput = []
        Avg_Mos = []
        Avg_RValue = []
        for row in csv_f:
            Avg_Throughput.append(row[4])
            Avg_Mos.append(row[51])
            Avg_RValue.append(row[55])

        Avg_Throughput.pop(0)
        Avg_Throughput=map(float, Avg_Throughput)
        AVG_Throughput=np.mean(Avg_Throughput)
        print "The average Throught for this test is %.2f byte/s" %AVG_Throughput

        Avg_Mos.pop(0)
        Avg_Mos=map(float, Avg_Mos)
        AVG_MOS=np.mean(Avg_Mos)
        print "The average MoS Value for this test is %.2f" %AVG_MOS


        Avg_RValue.pop(0)
        Avg_RValue=map(float, Avg_RValue)
        AVG_RValue=np.mean(Avg_RValue)
        print "The average R-value Value for this test is %.2f" %AVG_RValue



#x = [1, 2, 3, 4, 5]
#y = [1, 4, 9, 16, 25]
#pl.plot(x, y)
#pl.show()
    
