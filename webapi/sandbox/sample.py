from ixia.webapi import *
import ixchariotApi


webServerAddress = "https://192.168.164.127"
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
src_EndpointsList = ["10.50.1.10/192.168.164.127"]
dst_EndpointsList = ["10.50.2.8/192.168.164.127"]

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
# src_EndpointsList = ["192.168.1.100/192.168.1.101"]
# dst_EndpointsList = ["192.168.1.200/192.168.1.201", "192.168.1.210/192.168.1.211"]
src_EndpointsList = ["10.50.1.10/192.168.164.127"]
dst_EndpointsList = ["10.50.2.8/192.168.164.127"]


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



# ixchariotApi.py

from ixia.webapi import *

def getResourceFromLibrary(session, resourceCategory, resourceName):
	resources = session.httpGet("config/ixchariot/resources/" + resourceCategory)
	for i in range (0, len(resources)):
		resource = resources[i]
		if resourceName == resource.name:
			return resource
	return None

def getEndpointFromResourcesLibrary(session, endpointName):
	return getResourceFromLibrary(session, "endpoint", endpointName)

def getQoSTemplateFromResourcesLibrary(session, qosTemplateName):
	if qosTemplateName == "None":
		qosTemplate = WebObjectBase()
		qosTemplate.name = "None"
		qosTemplate.serviceType = "BEST_EFFORT"
		qosTemplate.type = "NO_QOS"
	else:
		qosTemplate = getResourceFromLibrary(session, "qostemplate", qosTemplateName)
	return qosTemplate

def getFlowScriptFromResourcesLibrary(session, flowName):
	return getResourceFromLibrary(session, "flowscript", flowName)

def getApplicationScriptFromResourcesLibrary(session, applicationName):
	return getResourceFromLibrary(session, "applicationscript", applicationName)

def getFlowScriptParameter(flowScript, parameterName):
	for i in range (0, len(flowScript.scriptParameters)):
		parameter = flowScript.scriptParameters[i]
		if parameterName == parameter.caption:
			return parameter
	return None
	
def changeFlowScriptParameterValue(flowScript, parameterName, parameterValue):
	parameter = getFlowScriptParameter(flowScript, parameterName)
	parameter.value = parameterValue
	
def createFlowGroup(name, direction, topology):
	flowGroup = WebObjectBase()
	flowGroup.network = createNetwork(direction, topology)
	flowGroup.settings = createFlowGroupSettings(name)
	return flowGroup

def createMulticastGroup(name):
	flowGroup = WebObjectBase()
	flowGroup.network = createNetwork("SRC_TO_DEST", "MULTICAST")
	flowGroup.settings = createMulticastGroupSettings(name)
	return flowGroup
	
def createApplicationMix(name, distributionType, noUsers, direction, topology):
	appMix = WebObjectBase()
	appMix.network = createNetwork(direction, topology)
	appMix.settings = createApplicationMixSettings(name, distributionType, noUsers)
	return appMix

def createNetwork(direction, topology):
	network = WebObjectBase()
	network.enabled = True
	network.direction = direction						
	network.topology = topology				
	return network	

def createFlowGroupSettings(name):
	settings = WebObjectBase()
	settings.name = name
	return settings

def createMulticastGroupSettings(name):
	settings = WebObjectBase()
	settings.name = name
	return settings
	
def createApplicationMixSettings(name, distributionType, users):
	settings = WebObjectBase()
	settings.name = name
	settings.distributionType = distributionType
	settings.numberOfUsers = users
	return settings

def createFlow(script, users, protocol, sourceQoS, destinationQoS):
	flow = WebObjectBase()
	flow.script = script
	flow.numberOfUsers = users
	flow.protocol = protocol
	flow.sourceQoS = sourceQoS
	flow.destinationQoS = destinationQoS
	return flow

def createMulticastFlow(script, multicastAddrPort, protocol, sourceQoS):
	mcastFlow = WebObjectBase()
	mcastFlow.script = script
	mcastFlow.multicastIp = multicastAddrPort
	mcastFlow.protocol = protocol
	mcastFlow.sourceQoS = sourceQoS
	return mcastFlow

def createApp(script, ratio):
	app = WebObjectBase()
	app.script = script
	app.ratio = ratio
	return app

def createEndpoint(testIP, mgmtIP):
	endpoint = WebObjectBase()
	endpoint.ips = []
	endpoint.ips.append(createIP(testIP)) # this example demonstrates just 1 test IP, but it's also possible to add multiple test IPs to the list
	endpoint.managementIp = createIP(mgmtIP)
	endpoint.name = mgmtIP # it's also possible to pass the endpoint name as a parameter to the function
	return endpoint

def getIPType(ip):
	if ip.find(":") != -1:
		return "IPV6"
	else:
		return "IPV4"	

def createIP(ip_address):
	ip = WebObjectBase()
	ip.address = ip_address
	ip.type = getIPType(ip_address)
	return ip

def saveConfigToResourcesLibrary(session, configName):
	session.saveConfiguration(configName)

def loadConfigFromResourcesLibrary(session, configName):
	session.loadConfiguration(configName)

def exportConfigFromResourcesLibraryToFile(session, configName, filePath):
	# filePath must have the ".ixcfg" extension
	with open(filePath, "wb+") as exportFile:
		session.exportConfigurationToFile(configName, exportFile)

def importConfigFromFileToResourcesLibrary(session, filePath):
	# filePath must have the ".ixcfg" extension (for configs exported from IxChariot 9.3 or newer) or the ".zip" extension (for configs exported from IxChariot 8.0 - 9.2)
	with open(filePath, "rb") as importFile:
		importedConfig = session.importConfigurationFromFile(importFile)
		importedConfigName = importedConfig.details.name
		return importedConfigName

def deleteOldestTestResults(apiConnection, userName, howManyTestsToDelete):
	testResults = apiConnection.httpGet("results", params = {"start" : 0, "limit" : howManyTestsToDelete, "sortColumn" : "starttime", "sortOrder" : "ascending", "filter" : "userid:%s" % userName})
	for testResult in testResults.testRunInformationList:
		apiConnection.httpDelete("results/%d" % testResult.testRunId)


class StatisticValue:
	"""Describes a value for a statistic at a moment in time.	
    @param timestamp:     	the moment in the test when the value was recorded.
    @param value:	    	the actual value recorded.
    """
	def __init__(self, timestamp, value):
		self.timestamp = timestamp
		if value == None:
			self.value = "N/A"			
		else:
			self.value = value

class Statistic:
	"""Describes a statistic from the test.
    @param name:     	the name of the statistic.
    @param values:	    the list of values for that statistic in time.    
    """
	
	def __init__(self, name):
		self.name = name
		self.values = []
		
	def __str__(self):
		res = self.name + ":\n"
		for val in self.values:
			res = res + str(val.timestamp) + "    " + str(val.value) + "\n"
		return res
		
	def add_value(self, value):
		self.values.append(value)

def getRawResults(session, stats, filter, filterErrorMessage):
	try:
		statsList = WebListProxy([WebObjectProxy(definition = "ixchariot:" + stat) for stat in stats])
		query = WebObjectProxy(stats=statsList, cacheSize=100000, filter=filter)
		channel = session.httpPost("stats/channels", WebObjectProxy(timeToLive=120), headers={"Content-Type" : "application/json", "Accept" : "application/json"})
		query =	session.httpPost("stats/channels/%d/queries" % channel.id, query, headers={"Content-Type" : "application/json", "Accept" : "application/json"})
		requestResult = session.httpPost("stats/channels/%d/requests" % channel.id, WebObjectProxy(count=100000))
		valuesList = requestResult.data.map.__dict__[query.id]
	except:
		raise ValueError(filterErrorMessage)
        finally:
                try:
                        session.httpDelete("stats/channels")
                except:
                        pass

	return (valuesList, query)
		
def getResults(session, stats, filter, filterErrorMessage):
	(valuesList, query) = getRawResults(session, stats, filter, filterErrorMessage)

	statsResults = []
	for i in range(0, len(stats)):
		result = Statistic(stats[i])
		for j in range(0, len(valuesList)):
			value = valuesList[j]

			if len(value.values) == 0:
				raise ValueError(filterErrorMessage)

			statValue = StatisticValue(value.timestamp, value.values[0][i])
			result.add_value(statValue)
		statsResults.append(result)
	
	return statsResults
	
def getTestLevelIndexOfFirstUserForGroupApp(session, group, app, filterErrorMessage):
	# Create a filter that will return all the users associated with the given group and app, for the first timestamp
	filter = WebObjectProxy(
				type = 'boolean',
				leftItem = WebObjectProxy(
								leftItem = "ixchariot:mix",
								operator = '=',
								rightItem = group),
				operator = 'and',
				rightItem = WebObjectProxy(
								type = 'boolean',
								leftItem = WebObjectProxy(
												leftItem = "ixchariot:application",
												operator = '=',
												rightItem = app),
								operator = 'and',
								rightItem = WebObjectProxy(
												leftItem = "ixchariot:timestamp",
												operator = '=',
												rightItem = "2000")))

	try:
		(valuesList, query) = getRawResults(session, ["user"], filter, filterErrorMessage)
		
		# Get the test-level index of the first user for this group and app
		userIndex = min(valuesList[0].values, key=lambda row : int(row[0]))[0]
	except:
		raise ValueError(filterErrorMessage)

	return userIndex
	
def getTestLevelResults(session, stats):
	"""Gets test level results for the specified statistics.
		
	Can be used during the test run or after the test has ended. 
	Will return all available results, since the beginning of the test.

	@param session: 	the current session where test is running / loaded
	@param stats:		the list of statistics names to get the values for; names should be identical to those in the results CSV
    
	@return 			a list of Statistic objects (one object for each requested statistic). Each Statistic object contains a list of StatisticValue objects.
						Each StatisticValue object contains a statistic value at a specific timestamp. This function will return all the available statistic
						values collected since the beginning of the test. See the definition of the Statistic and StatisticValue classes for details.
						
	@exception ValueError
	"""

	filterErrorMessage = "No statistics were reported for this test"
	return getResults(session, stats, None, filterErrorMessage)

def getGroupLevelResults(session, stats, group):
	"""Gets group level results for the specified statistics.
		
	Can be used during the test run or after the test has ended. 
	Will return all available results, since the beginning of the test.

	@param session: 	the current session where test is running / loaded
	@param stats:		the list of statistics names to get the values for	
	@param group:		the app mix/flow group/multicast group to get the stats for; names should be identical to those in the results CSV
    
	@return 			a list of Statistic objects (one object for each requested statistic). Each Statistic object contains a list of StatisticValue objects.
						Each StatisticValue object contains a statistic value at a specific timestamp. This function will return all the available statistic
						values collected since the beginning of the test. See the definition of the Statistic and StatisticValue classes for details.
    
	@exception ValueError
	"""

	filter = WebObjectProxy(leftItem = "ixchariot:mix", operator = "=", rightItem = group)
	filterErrorMessage = "Could not find any values for mix/group " + group
	return getResults(session, stats, filter, filterErrorMessage)

def getAppLevelResults(session, stats, group, app):
	"""Gets application level results for the specified statistics.
		
	Can be used during the test run or after the test has ended. 
	Will return all available results, since the beginning of the test.

	@param session: 	the current session where test is running / loaded
	@param stats:		the list of statistics names to get the values for; names should be identical to those in the results CSV	
	@param group:		the app mix that contains the app
	@param app:			the app to get the stats for
    
	@return 			a list of Statistic objects (one object for each requested statistic). Each Statistic object contains a list of StatisticValue objects.
						Each StatisticValue object contains a statistic value at a specific timestamp. This function will return all the available statistic
						values collected since the beginning of the test. See the definition of the Statistic and StatisticValue classes for details.
    
	@exception ValueError
	"""
	
	filter = WebObjectProxy(
				type = 'boolean',
				leftItem = WebObjectProxy(
								leftItem = "ixchariot:mix",
								operator = '=',
								rightItem = group),
				operator = 'and',
				rightItem = WebObjectProxy(
								leftItem = "ixchariot:application",
								operator = '=',
								rightItem = app))
	filterErrorMessage = "Could not find any values for mix/group " + group + " and app/flow " + app
	return getResults(session, stats, filter, filterErrorMessage)

def getFlowLevelResults(session, stats, group, flow, protocol):
	"""Gets flow level results for the specified statistics.
		
	Can be used during the test run or after the test has ended. 
	Will return all available results, since the beginning of the test.

	@param session: 	the current session where test is running / loaded
	@param stats:		the list of statistics names to get the values for; names should be identical to those in the results CSV	
	@param group:		the flow group / multicast group that contains the flow
	@param flow:		the flow to get the stats for
	@param protocol:	the test protocol for the flow
    
	@return 			a list of Statistic objects (one object for each requested statistic). Each Statistic object contains a list of StatisticValue objects.
						Each StatisticValue object contains a statistic value at a specific timestamp. This function will return all the available statistic
						values collected since the beginning of the test. See the definition of the Statistic and StatisticValue classes for details.
    
	@exception ValueError
	"""
	
	fullFlowName = flow + " (" + protocol + ")"
	return getAppLevelResults(session, stats, group, fullFlowName)
	
def getUserLevelResultsFromApp(session, stats, group, app, user):
	"""Gets user level results for the specified statistics.
		
	Can be used during the test run or after the test has ended. 
	Will return all available results, since the beginning of the test.

	@param session: 	the current session where test is running / loaded
	@param stats:		the list of statistics names to get the values for	
	@param group:		the app mix that contains the app
	@param app:			the app to get the stats for
	@param user:		which user from the app to get results for: number between 1 and number of users in app
    
	@return 			a list of Statistic objects (one object for each requested statistic). Each Statistic object contains a list of StatisticValue objects.
						Each StatisticValue object contains a statistic value at a specific timestamp. This function will return all the available statistic
						values collected since the beginning of the test. See the definition of the Statistic and StatisticValue classes for details.
    
	@exception ValueError
	"""

	filterErrorMessage = "Could not find any values for mix/group " + group + ", app/flow " + app + " and user " + str(user)
	
	# The user index we receive as input parameter is relative to this group and app
	# We need to convert it to the test-level index
	# (the user index as seen in UI or CSV, taking into account the users from the others groups and apps)
	testLevelUserIndex = int(getTestLevelIndexOfFirstUserForGroupApp(session, group, app, filterErrorMessage)) + user - 1
	
	filter = WebObjectProxy(
				type = 'boolean',
				leftItem = WebObjectProxy(
								leftItem = "ixchariot:mix",
								operator = '=',
								rightItem = group),
				operator = 'and',
				rightItem = WebObjectProxy(
								type = 'boolean',
								leftItem = WebObjectProxy(
												leftItem = "ixchariot:application",
												operator = '=',
												rightItem = app),
								operator = 'and',
								rightItem = WebObjectProxy(
												leftItem = "ixchariot:user",
												operator = '=',
												rightItem = testLevelUserIndex)))
	return getResults(session, stats, filter, filterErrorMessage)

def getUserLevelResultsFromFlow(session, stats, group, flow, protocol, user):
	"""Gets user level results for the specified statistics.
		
	Can be used during the test run or after the test has ended. 
	Will return all available results, since the beginning of the test.

	@param session: 	the current session where test is running / loaded
	@param stats:		the list of statistics names to get the values for	
	@param group:		the flow group / multicast group that contains the flow
	@param flow:		the flow to get the stats for
	@param protocol:	the test protocol for the flow
	@param user:		which user from the flow to get results for: number between 1 and number of users in flow
    
	@return 			a list of Statistic objects (one object for each requested statistic). Each Statistic object contains a list of StatisticValue objects.
						Each StatisticValue object contains a statistic value at a specific timestamp. This function will return all the available statistic
						values collected since the beginning of the test. See the definition of the Statistic and StatisticValue classes for details.
    
	@exception ValueError
	"""
	
	fullFlowName = flow + " (" + protocol + ")"
	return getUserLevelResultsFromApp(session, stats, group, fullFlowName, user)
