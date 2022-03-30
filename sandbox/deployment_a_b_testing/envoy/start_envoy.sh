#!/bin/bash
ulimit -n 102400
sysctl fs.inotify.max_user_watches=524288

python3 k8s_configmap_watcher.py $PPID  &

envoy -c $ENVOY_CONF_PATH/envoy.yaml --restart-epoch $RESTART_EPOCH --service-cluster cluster-1 --service-node envoy-instance-1
