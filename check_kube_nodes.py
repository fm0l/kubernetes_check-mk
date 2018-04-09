#!/usr/bin/env python

#########################################################
#              check_kube_nodes.py                      #
#                                                       #
#		Check_MK Local script for Kubernetes    #
#		nodes health			        #
#						        #
#       Author:  Federico Mollura                       #
#                                                       #
#########################################################

### Imports

import os
import json
import sys

### I get enviroment variables from kube.conf, it's needed by kubectl

dir = os.path.dirname(os.path.realpath(__file__))
confile = 'kube.conf'

full_path=os.path.join(dir,confile)

with open(full_path, 'r') as f:
    for line in f:
        if 'export' not in line:
            continue
        # Remove leading `export `
        # then, split name / value pair
        key, value = line.replace('export ', '', 1).strip().split('=', 1)
        os.environ[key] = value

## I get a nodes description in JSON format
os.environ["GET_NODES"] = "kubectl get nodes -o json"
getNodes = os.popen('$GET_NODES').read()

## Check if kubectl is working after setting the environment
kubeCheck = int(os.popen('if [ $( $GET_NODES 2>/dev/null | wc -l) -le 30 ]; then echo "3"; else echo "0"; fi').read())

if kubeCheck != 0:
	print "0 Kubernetes_Nodes CRITICAL - unable to connect to Kubernetes via kubectl!"
	sys.exit()

##Output Function

def outFun():
	print str(ERRCODE), str("Kubernetes_Nodes"), str("-"), str(reportedConditions), str(nodesToAdd)
	return ERRCODE;

## I get name of the nodes
parsed_nodes = json.loads(getNodes)
number_list = len(parsed_nodes['items'])

nodeDict = {}
reportedConditions = []
nodesToAdd = []
ERRCODE = 0
for i in range(0,number_list):
	nodeToAdd = parsed_nodes['items'][i]['metadata'].get('name')
	nodeDict[i] = nodeToAdd
	nodesToAdd.append(nodeToAdd)
	number_conditions = len(parsed_nodes['items'][i]['status']['conditions'])
	for k in range(0,number_conditions):
		conditionType = parsed_nodes['items'][i]['status']['conditions'][k]['type']
		typeStatus = parsed_nodes['items'][i]['status']['conditions'][k]['status']
		testCondition = str(conditionType) + '-' + str(typeStatus)
		reportCondition = str(nodeToAdd) + ':', str(testCondition)
		if testCondition == 'OutOfDisk-True':
			ERRCODE += 1
			reportedConditions.append(reportCondition)
		elif testCondition == 'Ready-False':
			ERRCODE += 1
			reportedConditions.append(reportCondition)
		elif testCondition == 'MemoryPressure-True':
			ERRCODE += 2
			reportedConditions.append(reportCondition)
		elif testCondition == 'DiskPressure-True':
			ERRCODE += 2
			reportedConditions.append(reportCondition)
		
if ERRCODE >= 2:
	ERRCODE = 2
elif ERRCODE == 1:
	pass
elif ERRCODE == 0:
	pass
			

outFun()
