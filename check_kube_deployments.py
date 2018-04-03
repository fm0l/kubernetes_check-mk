#!/usr/bin/env python

#########################################################
#		check_kube_deployments.py               #
#   							#
#		Check_MK Local script for Kubernetes	#
#		deployments health		        #
#							#
#		Author:	Federico Mollura	        #
#							#
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
os.environ["GET_DEPS"] = "kubectl get deployments --all-namespaces -o json"
getDeps = os.popen('$GET_DEPS').read()

## Check if kubectl is working after setting the environment
kubeCheck = int(os.popen('if [ $( $GET_DEPS 2>/dev/null | wc -l) -le 30 ]; then echo "3"; else echo "0"; fi').read())

if kubeCheck != 0:
	print "0 KubeNodes CRITICAL - unable to connect to Kubernetes via kubectl!"
	sys.exit()

##Output Function

def outFun():
	print str(ERRCODE), str("Kubernetes_Nodes"), str("-"), str(reportedConditions)
	return ERRCODE;

## I get name of the nodes
parsed_deps = json.loads(getDeps)
number_list = len(parsed_deps['items'])

depDict = {}
reportedConditions = []
ERRCODE = 0
for i in range(0,number_list):
	depsToAdd = parsed_deps['items'][i]['metadata'].get('name')
	depDict[i] = depsToAdd
	number_conditions = len(parsed_deps['items'][i]['status']['conditions'])
	for k in range(0,number_conditions):
		conditionType = parsed_deps['items'][i]['status']['conditions'][k]['type']
		typeStatus = parsed_deps['items'][i]['status']['conditions'][k]['status']
		reasonCondition = parsed_deps['items'][i]['status']['conditions'][k]['reason']
		testCondition = str(conditionType) + '-' + str(typeStatus)
		reportCondition = str(depsToAdd) + ':', str(testCondition)
		rolloutCondition = str(testCondition) + '-' + str(reasonCondition)
		
		if not testCondition == 'Available-True' and not testCondition == 'Progressing-True':
			ERRCODE += 2
			reportedConditions.append(reportCondition)
		
if ERRCODE >= 2:
	ERRCODE = 2
elif ERRCODE == 1:
	pass
elif ERRCODE == 0:
	pass
			
outFun()
