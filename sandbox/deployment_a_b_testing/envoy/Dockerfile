FROM envoyproxy/envoy:v1.20-latest
RUN apt-get update -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get install python3 -y

ENV ENVOY_CONF_PATH="/etc/envoy"
COPY start_envoy.sh k8s_configmap_watcher.py hot-restarter.py ./
RUN chmod a+x start_envoy.sh
ENTRYPOINT python3 hot-restarter.py start_envoy.sh
