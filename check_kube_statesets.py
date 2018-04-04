#!/usr/bin/env python

#########################################################
#              check_kube_statesets.py                  #
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
os.environ["GET_SETS"] = "kubectl get statefulsets -o json"
getSets = os.popen('$GET_SETS').read()


## Check if kubectl is working after setting the environment
kubeCheck = int(os.popen('if [ $( $GET_SETS 2>/dev/null | wc -l) -le 30 ]; then echo "3"; else echo "0"; fi').read())

if kubeCheck != 0:
	print "0 KubeNodes CRITICAL - unable to connect to Kubernetes via kubectl!"
	sys.exit()

##Output Function

def outFun():
	print str(ERRCODE), str("Kubernetes_StatefulSets"), str("-"), str(reportedConditions), str(statesToAdd)
	return ERRCODE;

## I get name of the nodes
parsed_sets = json.loads(getSets)
number_list = len(parsed_sets['items'])

setDict = {}
reportedConditions = []
podsToCheck = []
statesToAdd = []
ERRCODE = 0
for i in range(0,number_list):
	stateToAdd = parsed_sets['items'][i]['metadata'].get('name')
	statesToAdd.append(stateToAdd)

for i in statesToAdd:
### I get the JSON Pods
	os.environ["POD"] = i
	command = "kubectl get po -l app=" + i + " " + "-o json"
	getPods =  os.popen(command).read()
	parsed_pods = json.loads(getPods)
### Now i can analyze them
	pods_list = len(parsed_pods['items'])
	for n in range(0,pods_list):
		podName = parsed_pods['items'][n]['metadata']['name']
		phasePod = parsed_pods['items'][n]['status']['phase']
		if not phasePod == "Running":
			reportCondition = str(podName) + ': ' + str(phasePod)	
			reportedConditions.append(reportCondition)
			ERRCODE = 2


if ERRCODE >= 2:
	ERRCODE = 2
elif ERRCODE == 1:
	pass
elif ERRCODE == 0:
	pass
			

outFun()
