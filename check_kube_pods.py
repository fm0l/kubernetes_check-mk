#!/usr/bin/env python

#########################################################
#              check_kube_pods.py                       #
#                                                       #
#		Check_MK Local script for Kubernetes    #
#		pods number			        #
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
os.environ["GET_SETS"] = "kubectl get pods -o json"
getSets = os.popen('$GET_SETS').read()


## Check if kubectl is working after setting the environment
kubeCheck = int(os.popen('if [ $( $GET_SETS 2>/dev/null | wc -l) -le 30 ]; then echo "3"; else echo "0"; fi').read())

if kubeCheck != 0:
	print "0 Kubernetes_PodsOnline CRITICAL - unable to connect to Kubernetes via kubectl!"
	sys.exit()

##Output Function

def outFun():
	print str(ERRCODE), str("Kubernetes_PodsOnline"), str("-"), str(setDict)
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
#	statesToAdd.append(stateToAdd)
	reportedCondition = parsed_sets['items'][i]['status']['containerStatuses'][0].get('state')
#	reportedConditions.append(reportedCondition)
	setDict.update({stateToAdd: reportedCondition})

outFun()
