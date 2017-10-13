from ixia.webapi import *
import ixchariotApi


webServerAddress = "https://ixchariot-server"
apiVersion = "v1"
username = "N/A"
password = "N/A"
apiKey = "N/A" 	  # Get the API Key from the web interface, Menu > My Account > Api Key

print "Connecting to " + webServerAddress
api = webApi.connect(webServerAddress, apiVersion, None, username, password)
# It is also possible to connect with the API Key instead of username and password, using:
#api = webApi.connect(webServerAddress, apiVersion, apiKey, None, None)

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
src_EndpointsList = ["192.168.1.100/192.168.1.101"]
dst_EndpointsList = ["192.168.1.200/192.168.1.201"]

# Create a new ApplicationMix
name = "AppMix 1"
objective = "USERS"
users = 20
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
			["Facebook", 			10],
			["Yahoo Mail", 			40],
			["YouTube Enterprise", 	50]
		  ]

for i in range(0, len(appList)):
	appData = appList[i]
	appName = appData[0]
	appRatio = appData[1]
	appScript = ixchariotApi.getApplicationScriptFromResourcesLibrary(session, appName)
	app = ixchariotApi.createApp(appScript, appRatio);
	session.httpPost("config/ixchariot/appMixes/1/settings/applications", data = app)

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
				# Data flows
				["TCP Baseline Performance", 	1, 		 "TCP",  	"Best Effort",	"Background"],
				["UDP Baseline Performance",	3, 		 "UDP",  	"Background",	"None"],
			
				# VoIP flows
				["G.711a (64 kbps)", 			1, 		 "RTP",  	"Voice",		"None"],
			
				# Video over RTP flows
				["RTP HD (10 Mbps)",			1,		 "RTP", 	"Audio Video",	"None"],
				
				# Adaptive video over HTTP flows
				["Netflix Video SD",			1,		 "TCP", 	"None",			"None"]
			]

for i in range (0, len(flowList)):
	flowData = flowList[i]
	flowName = flowData[0]
	users = flowData[1]
	protocol = flowData[2]
	sourceQoSName = flowData[3]
	destinationQoSName = flowData[4]
	flowScript = ixchariotApi.getFlowScriptFromResourcesLibrary(session, flowName)

	# Example for changing the parameter values
	if i == 3:
		ixchariotApi.changeFlowScriptParameterValue(flowScript, "Bit Rate", "9.8 Mbps")
	
	if i == 4:
		ixchariotApi.changeFlowScriptParameterValue(flowScript, "Segment Duration (s)", "3")
		
	sourceQoSTemplate = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, sourceQoSName)
	destinationQoSTemplate = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, destinationQoSName)
	
	flow = ixchariotApi.createFlow(flowScript, users, protocol, sourceQoSTemplate, destinationQoSTemplate)
	session.httpPost("config/ixchariot/flowGroups/1/settings/flows", data = flow)

# Create a new MulticastGroup
name = "MulticastGroup 1"
mcastgroup = ixchariotApi.createMulticastGroup(name)
session.httpPost("config/ixchariot/multicastGroups", data = mcastgroup)

# Configure endpoints for the MulticastGroup
src_EndpointsList = ["192.168.1.100/192.168.1.101"]
dst_EndpointsList = ["192.168.1.200/192.168.1.201", "192.168.1.210/192.168.1.211"]

# This demonstrates how to manually assign endpoints to the test configuration using known IP addresses.
# If you want to assign an endpoint discovered by the Registration Server, use the ixchariotApi.getEndpointFromResourcesLibrary() function
# to get the data for httpPost
for src_Endpoint in src_EndpointsList:
	ips = src_Endpoint.split('/')
	session.httpPost("config/ixchariot/multicastGroups/1/network/sourceEndpoints", data = ixchariotApi.createEndpoint(ips[0], ips[1]))
for dst_Endpoint in dst_EndpointsList:
	ips = dst_Endpoint.split('/')
	session.httpPost("config/ixchariot/multicastGroups/1/network/destinationEndpoints", data = ixchariotApi.createEndpoint(ips[0], ips[1]))

# Add multicast flows to the MulticastGroup

#					mcastFlowName,			mcastAddress:Port,	 protocol,  source QoS

mcastFlowList = [
					["Skype-Video-180p", 	"224.1.1.1:5000", 	 "UDP",  	"Audio Video"],
					["RTP HD (10 Mbps)",	"224.1.1.2:6000",	 "RTP", 	"Audio Video"]
				]

for i in range (0, len(mcastFlowList)):
	mcastFlowData = mcastFlowList[i]
	flowName = mcastFlowData[0]
	mcastAddressPort = mcastFlowData[1]
	protocol = mcastFlowData[2]
	sourceQoSName = mcastFlowData[3]
	flowScript = ixchariotApi.getFlowScriptFromResourcesLibrary(session, flowName)
	sourceQoSTemplate = ixchariotApi.getQoSTemplateFromResourcesLibrary(session, sourceQoSName)
	mcastFlow = ixchariotApi.createMulticastFlow(flowScript, mcastAddressPort, protocol, sourceQoSTemplate)
	session.httpPost("config/ixchariot/multicastGroups/1/settings/flows", data = mcastFlow)

# As an alternative to creating the test configuration from scratch, you can use ixchariotApi.loadConfigFromResourcesLibrary()
# to load an existing configuration into the given session, or ixchariotApi.importConfigFromFileToResourcesLibrary() followed
# by ixchariotApi.loadConfigFromResourcesLibrary() to use a test configuration file from disk.

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
		
	# Get flow level results
	# Note: the statistic names should be identical to those that appear in the results CSV
	results = ixchariotApi.getFlowLevelResults(session, ["Throughput", "Total Datagrams Sent"], "FlowGroup 1", "RTP HD (10 Mbps)", "RTP")
	
	print "Flow Level Results for RTP HD (10 Mbps) (RTP) from FlowGroup 1:\n"
	for res in results:
		print res
		print ""
		
	# Get user level results
	# Note: the statistic names should be identical to those that appear in the results CSV
	# Get results for the first user
	results = ixchariotApi.getUserLevelResultsFromFlow(session, ["Throughput"], "FlowGroup 1", "RTP HD (10 Mbps)", "RTP", 1)
	
	print "User Level Results for first user in flow RTP HD (10 Mbps) (RTP), FlowGroup 1:\n"
	for res in results:
		print res
		print ""
	

except Exception, e:
	print "Error", e
	
print "Stopping the session..."
session.stopSession()

print "Deleting the session..."
session.httpDelete()
