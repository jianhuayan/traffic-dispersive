from ixia.webapi import *
import ixchariotApi
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
testOptions.testDuration = 30
testOptions.consoleManagementQoS = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, "Best Effort")
testOptions.endpointManagementQoS = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, "Best Effort")
session.httpPut("config/ixchariot/testOptions", data = testOptions)

# Available endpoints used in test (list of 'testIP/mgmtIP' strings)
src_EndpointsList = [dvn.const.IxiaEpoint1 + "/" + dvn.const.IxiaMgmt1]
dst_EndpointsList = [dvn.const.IxiaEpoint2 + "/" + dvn.const.IxiaMgmt2]

# Create a new FlowGroup
name = "FlowGroup 1"
direction = "SRC_TO_DEST"
topology = "FULL_MESH"
flowgroup = ixchariotApi.createFlowGroup(name, direction, topology)
session.httpPost("config/ixchariot/flowGroups", data = flowgroup)

# Configure endpoints for the FlowGroup

# This demonstrates how to manually assign endpoints to the test configuration using known IP addresses.
# If you want to assign an endpoint discovered by the Registration Server, use the ixchariotApi.getEndpointFromResourcesLibrary() function
# to get the data for httpPost
for src_Endpoint in src_EndpointsList:
	ips = src_Endpoint.split('/')
	session.httpPost("config/ixchariot/flowGroups/1/network/sourceEndpoints", data = ixchariotApi.createEndpoint(ips[0], ips[1]))
for dst_Endpoint in dst_EndpointsList:
	ips = dst_Endpoint.split('/')
	session.httpPost("config/ixchariot/flowGroups/1/network/destinationEndpoints", data = ixchariotApi.createEndpoint(ips[0], ips[1]))
	
# Add flows to the FlowGroup

#				flowName,						users,	 protocol,  source QoS, 	destination QoS

flowList = [
			# Voice Flow
				["AMR-WB (15.85 kbps)", 			1, 		 "RTP",  	"Voice",		"None"],
				
			]

for i in range (0, len(flowList)):
	flowData = flowList[i]
	flowName = flowData[0]
	users = flowData[1]
	protocol = flowData[2]
	sourceQoSName = flowData[3]
	destinationQoSName = flowData[4]
	flowScript = ixchariotApi.getFlowScriptFromResourcesLibrary(session, flowName)

	sourceQoSTemplate = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, sourceQoSName)
	destinationQoSTemplate = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, destinationQoSName)
	
	flow = ixchariotApi.createFlow(flowScript, users, protocol, sourceQoSTemplate, destinationQoSTemplate)
	session.httpPost("config/ixchariot/flowGroups/1/settings/flows", data = flow)
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
	# results = ixchariotApi.getTestLevelResults(session, ["Throughput"])
	results = ixchariotApi.getTestLevelResults(session, ["Avg Mos"])
	# results = ixchariotApi.getTestLevelResults(session, ["Min Mos"])
	
	print "Test Level Results: \n"
	for res in results:
		# Each object in the list of results is of type Statistic (contains the statistic name and a list of StatisticValue objects).
		print res.name
		for val in res.values:
			# The list will contain StatisticValue objects for all the reported timestamps since the beginning of the test.
			# Each StatisticValue object contains the timestamp and the actual value.
			print str(val.timestamp) + "      " + str(val.value)
		print ""
	
		
	# Get flow level results
	# Note: the statistic names should be identical to those that appear in the results CSV
	results = ixchariotApi.getFlowLevelResults(session, ["Avg Mos", "Avg R-value"], "FlowGroup 1", "G.711a (64 kbps)", "RTP")
	
	print "Flow Level Results for AMR-WB (15.85 kbps) from FlowGroup 1:\n"
	for res in results:
		print res
		print ""
		
	# Get user level results
	# Note: the statistic names should be identical to those that appear in the results CSV
	# Get results for the first user
	results = ixchariotApi.getUserLevelResultsFromFlow(session, ["Avg Mos"], "FlowGroup 1", "G.711a (64 kbps)", "RTP", 1)
	
	print "User Level Results for first user in flow G.711a (64 kbps) (RTP), FlowGroup 1:\n"
	for res in results:
		print res
		print ""
	

except Exception, e:
	print "Error", e
	
print "Stopping the session..."
session.stopSession()

print "Deleting the session..."
session.httpDelete()
