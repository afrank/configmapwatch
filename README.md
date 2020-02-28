# configmapwatch

This demonstrates how to load a config blob from a configmap-mounted volume in k8s and keep it up to date. An interesting feature of configmaps is if you mount one as a volume and make a change to it, that change will get picked up in your running pod. The way it works is:
1. Your volume mountPath is a directory in your container with your volume bind-mounted as a subdirectory
1a. Each configmap entry is in your volume with the key as the filename, and these are symlinked into your mountPath
2. When a change is made to the configmap, the configmap is re-bind-mounted as a new subdirectory, then through some renaming gymnastics the new config is swapped for the old, and the old one is unmounted.

There are two things that control how often new changes show up. The kubelet `sync-frequency` dictates how often configs are synced to pods (Default: 60s). There is also the configmap cache ttl (Default: 60s).

## How a configmap volume is updated by kubernetes
```
2020-02-27 22:35:16 - Created directory: /opt/config/..2020_02_27_22_35_16.617502340
2020-02-27 22:35:16 - Modified directory: /opt/config
2020-02-27 22:35:16 - Modified directory: /opt/config/..2020_02_27_22_35_16.617502340
2020-02-27 22:35:16 - Created file: /opt/config/..2020_02_27_22_35_16.617502340/config.json
2020-02-27 22:35:16 - Modified directory: /opt/config/..2020_02_27_22_35_16.617502340
2020-02-27 22:35:16 - Modified file: /opt/config/..2020_02_27_22_35_16.617502340/config.json
2020-02-27 22:35:16 - Created file: /opt/config/..data_tmp
2020-02-27 22:35:16 - Modified directory: /opt/config
2020-02-27 22:35:16 - Moved file: from /opt/config/..data_tmp to /opt/config/..data
2020-02-27 22:35:16 - Modified directory: /opt/config
2020-02-27 22:35:16 - Deleted file: /opt/config/..2020_02_27_22_33_49.110340463/config.json
2020-02-27 22:35:16 - Modified directory: /opt/config/..2020_02_27_22_33_49.110340463
2020-02-27 22:35:16 - Deleted directory: /opt/config/..2020_02_27_22_33_49.110340463
2020-02-27 22:35:16 - Modified directory: /opt/config
```

## Running the Demo
Start by applying the configmap and deployment manifests
```
$ kubectl apply -f configmap.yaml 
configmap/test-config created
$ kubectl apply -f deploy.yaml 
deployment.extensions/afrank-test created
```
Now tail your pod logs. You should see the config defined in configmap.yaml
```
$ kubectl -nafrank-dev logs -f deployments/afrank-test
2020-02-28 15:08:56 - {'THIS': 'is a test', 'HERE': 'is another test', 'KEY': "here's another key", 'ANOTHER': 'and yet another key'}
```
Now update your configmap either with `kubectl -nafrank-dev edit cm test-config` or edit configmap.yaml and re-apply it. Within a minute or so you should see your change get picked up in the running pod.
```
2020-02-28 15:12:46 - {'THIS': 'is a test', 'HERE': 'is another test', 'KEY': "here's another key", 'ANOTHER': 'and yet another key'}
2020-02-28 15:12:46 - detected a config change; re-reading config.json.
2020-02-28 15:12:49 - {'THIS': 'is a test', 'HERE': 'is another test', 'KEY': "here's another key", 'ANOTHER': 'and yet another key', 'CHANGE': "here's my new entry"}
2020-02-28 15:12:52 - {'THIS': 'is a test', 'HERE': 'is another test', 'KEY': "here's another key", 'ANOTHER': 'and yet another key', 'CHANGE': "here's my new entry"}
```
