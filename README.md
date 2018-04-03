# Kubernetes Local Checks for Check MK

**TODO** - Pods Checks!

##### 1- How To Install these checks

  - Install Check MK Agent
  - Put the $RELEVANT checks in the local/ directory (default is /usr/lib/check_mk_agent/local)
  - chmod +x *
  - Refresh from WATO
  - Enjoy!

##### 1- How do i know what checks are relevant?
 
###### Master Node (no worker pods):
 - Nodes Check
 - Deployments Check
 
###### Master Node (with worker pods):
 - Nodes Check
 - Deployments Check
 - Pods Check
 
###### Slave Node:
 - Nodes Check
 - Pods Check
