#!/bin/bash

## This is a temporary workaround, this should be replace by a real log collector

export KUBECONFIG=/etc/kubernetes/admin.conf 
LOGDIR=/root/logs

function startLogs {

for app in $(kubectl get deployments | sed "1d" | awk '{print $1}' | tr "\n" " "); do
  for i in $(kubectl get po -l app=$app | sed "1d" | awk '{print $1}' | tr "\n" " ");do
    if [ $(ps -ef | grep -v grep | grep "kubectl logs -f $i" | wc -l) -eq 0 ]; then
      kubectl logs -f $i >> $LOGDIR/$i.log &
    fi
  done
done

}


function cleanLogs {

mkdir -p $LOGDIR/archive
for i in $(find $LOGDIR -maxdepth 1 -type f -printf "%f\n" -name "*.log"); do
    cp $LOGDIR/$i $LOGDIR/archive/$i-$(date '+%Y-%m-%d-%H:%M:%S')
    gzip -9v $LOGDIR/archive/$i-$(date '+%Y-%m-%d-%H:%M:%S')
    echo > $LOGDIR/$i
done

}

function stopLogs {

for app in $(kubectl get deployments | sed "1d" | awk '{print $1}' | tr "\n" " "); do
  for i in $(kubectl get po -l app=$app | sed "1d" | awk '{print $1}' | tr "\n" " ");do
    if [ $(ps -ef | grep -v grep | grep "kubectl logs -f $i" | wc -l) -ne 0 ]; then
      kill $(ps -ef | grep -v grep | grep "kubectl logs -f $i"|awk '{print $2}')
    fi
  done
done

}

case $1 in
	start)
		startLogs
	;;

	stop)
		stopLogs
	;;
	
	clean)
		cleanLogs
	;;

	*)
		echo " INCORRECT USAGE!, please use start or stop"
	;;
esac
