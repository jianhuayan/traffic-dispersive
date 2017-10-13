from ixia.webapi import *
import ixchariotApi
import os
from subprocess import call
import dvn

IxiaIPaddr = dvn.const.IxiachariotIP 
# webServerAddress = "https://'dvn.const.IxiachariotIP'"
webServerAddress = "https://" + IxiaIPaddr
print dvn.const.IxiachariotIP
print webServerAddress
apiVersion = "v1"
username = "N/A"
password = "N/A"
apiKey = "e31589d3-4cf1-4bd9-854d-18e9eac768a8" 	  # Get the API Key from the web interface, Menu > My Account > Api Key

print "Connecting to " + webServerAddress
# api = webApi.connect(webServerAddress, apiVersion, None, username, password)
# It is also possible to connect with the API Key instead of username and password, using:
api = webApi.connect(webServerAddress, apiVersion, apiKey, None, None)

session = api.createSession("ixchariot")
print "Created session %s" % session.sessionId

print "Starting the session..."
session.startSession()

print "Configuring the test..."

# Configure few test options
testOptions = session.httpGet("config/ixchariot/testOptions")
testOptions.testDuration = 20
testOptions.consoleManagementQoS = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, "Best Effort")
testOptions.endpointManagementQoS = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, "Best Effort")
session.httpPut("config/ixchariot/testOptions", data = testOptions)

# Available endpoints used in test (list of 'testIP/mgmtIP' strings)
src_EndpointsList = [dvn.const.IxiaEpoint1 + "/" + dvn.const.IxiaMgmt1]
dst_EndpointsList = [dvn.const.IxiaEpoint2 + "/" + dvn.const.IxiaMgmt2]

# Create a new ApplicationMix
name = "AppMix 1"
objective = "USERS"
users = 1
direction = "SRC_TO_DEST"
topology = "FULL_MESH"
appmix = ixchariotApi.createApplicationMix(name, objective, users, direction, topology)
session.httpPost("config/ixchariot/appMixes", data = appmix)

# Configure endpoints for the AppMix

# This demonstrates how to manually assign endpoints to the test configuration using known IP addresses.
# If you want to assign an endpoint discovered by the Registration Server, use the ixchariotApi.getEndpointFromResourcesLibrary() function
# to get the data for httpPost
for src_Endpoint in src_EndpointsList:
	ips = src_Endpoint.split('/')
	session.httpPost("config/ixchariot/appMixes/1/network/sourceEndpoints", data = ixchariotApi.createEndpoint(ips[0], ips[1]))
for dst_Endpoint in dst_EndpointsList:
	ips = dst_Endpoint.split('/')
	session.httpPost("config/ixchariot/appMixes/1/network/destinationEndpoints", data = ixchariotApi.createEndpoint(ips[0], ips[1]))

# Add applications to the AppMix

# 			  appName		     	appRatio
appList = [
			["HTTP Video Enterprise", 			100],
		  ]

for i in range(0, len(appList)):
	appData = appList[i]
	appName = appData[0]
	appRatio = appData[1]
	appScript = ixchariotApi.getApplicationScriptFromResourcesLibrary(session, appName)
	app = ixchariotApi.createApp(appScript, appRatio);
	session.httpPost("config/ixchariot/appMixes/1/settings/applications", data = app)
try:
	print "Starting the test..."
	result = session.runTest()
	
	print "The test ended"
	
	#Save all results to CSV files.
	print "Saving the test results into zipped CSV files...\n"
	filePath = "testResults.zip"
	with open(filePath, "wb+") as statsFile:
		api.getStatsCsvZipToFile(result.testId, statsFile)
		
	# Get results after test run.
	# The functions below can also be used while the test is running, by using session.startTest() to start the execution,
	# calling any of the results retrieval functions during the run, and using session.waitTestStopped() to wait for test end.
	# You can use time.sleep() to call the results retrieval functions from time to time.
	# These functions will return statistics for all the timestamps reported since the beginning of the test until the current moment.
	
	# Get test level results.
	# Note: the statistic names should be identical to those that appear in the results CSV
	results = ixchariotApi.getTestLevelResults(session, ["Throughput"])
	
	print "Test Level Results: \n"
	for res in results:
		# Each object in the list of results is of type Statistic (contains the statistic name and a list of StatisticValue objects).
		print res.name
		for val in res.values:
			# The list will contain StatisticValue objects for all the reported timestamps since the beginning of the test.
			# Each StatisticValue object contains the timestamp and the actual value.
			print str(val.timestamp) + "      " + str(val.value)
		print ""
	
	# Get group level results.
	# Note: the statistic names should be identical to those that appear in the results CSV
	results = ixchariotApi.getGroupLevelResults(session, ["Throughput"], "AppMix 1")
	
	print "Group Level Results for AppMix 1:\n"
	for res in results:
		# Each object in the list of results has a printing function defined.
		# It will print the name of the statistic and the list of timestamp - value pairs.
		# For accessing each of these components separately see the example above.
		print res
		print ""
		

except Exception, e:
	print "Error", e
	
print "Stopping the session..."
session.stopSession()

print "Deleting the session..."
session.httpDelete()

a = int(os.system('ls | grep testResults.zip | wc -l'))
print a        
os.system('echo $appData[0]')

if a == 0:
    os.system('echo $appData[0]')
    os.system('mv testResults.zip (echo $appData[0])_testResults.zip')
    os.system('cp testResults.zip ./runningLog')

else:
    print "the testing is not finishing...."

