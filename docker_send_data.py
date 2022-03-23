#!/usr/bin/env python3
from google.cloud import monitoring_v3

import time
import os
import shutil
import requests
metadata_server = "http://metadata/computeMetadata/v1/"
metadata_flavor = {'Metadata-Flavor' : 'Google'}
#gce_id = requests.get(metadata_server + 'instance/id', headers = metadata_flavor).text
gce_name = requests.get(metadata_server + 'instance/hostname', headers = metadata_flavor).text
gce_project = requests.get(metadata_server + 'project/project-id', headers = metadata_flavor).text
split_gce_name=gce_name.split(".",2)

client = monitoring_v3.MetricServiceClient()
project_id = gce_project
project_name = f"projects/{project_id}"

load_series = monitoring_v3.TimeSeries()
load_series.metric.type = "custom.googleapis.com/at_swarm_node_load"
load_series.resource.type = "gce_instance"
load_series.resource.labels["instance_id"] = split_gce_name[0]
load_series.resource.labels["zone"] = split_gce_name[1]

du_series = monitoring_v3.TimeSeries()
du_series.metric.type = "custom.googleapis.com/at_swarm_node_root_volume_usage"
du_series.resource.type = "gce_instance"
du_series.resource.labels["instance_id"] = split_gce_name[0]
du_series.resource.labels["zone"] = split_gce_name[1]


while True:
    load1, load5, load15 = os.getloadavg()
    root_total, root_used, root_free = shutil.disk_usage("/")

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )
    load_point = monitoring_v3.Point({"interval": interval, "value": {"double_value": load5}})
    load_series.points = [load_point]
    client.create_time_series(request={"name": project_name, "time_series": [load_series]})

    du_point = monitoring_v3.Point({"interval": interval, "value": {"double_value": root_used/root_total}})
    du_series.points = [du_point]
    client.create_time_series(request={"name": project_name, "time_series": [du_series]})

    time.sleep(60)
