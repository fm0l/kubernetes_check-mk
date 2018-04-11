# Kubernetes Local Checks for Check MK

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
 - Pods / StatefulSets Check
 
###### Master Node (with worker pods):
 - Nodes Check
 - Deployments Check
 - Pods / StatefulSets Check
 
###### Slave Node:
 - Nodes Check
 - Pods Check


##### Remember to set the kube.conf accordingly to the node. Defaults = { Master = admin.conf, Slave = kubelet.conf }

#### There is also a bash script that creates logfiles, just put it in crontab to monitor each pod.
#### Remeber to put statefulsets logs manually in checmk, it should never change path of the log
#### To Handle different lognames for multiple pods/restarts, in check mk use logwatch.groups plugin in WATO
*/5 * * * * /root/collect_logs.sh start &>/dev/null
00 23 * * * /root/collect_logs.sh auto &>/dev/null

#### TODO LIST
1- Add Multi-Master Support
