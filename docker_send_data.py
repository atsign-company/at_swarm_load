#!/usr/bin/env python3
from google.cloud import monitoring_v3

import time
import os
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

series = monitoring_v3.TimeSeries()
series.metric.type = "custom.googleapis.com/at_swarm_node_load"
series.resource.type = "gce_instance"
series.resource.labels["instance_id"] = split_gce_name[0]
series.resource.labels["zone"] = split_gce_name[1]

while True:
    load1, load5, load15 = os.getloadavg()

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10 ** 9)
    interval = monitoring_v3.TimeInterval(
        {"end_time": {"seconds": seconds, "nanos": nanos}}
    )
    point = monitoring_v3.Point({"interval": interval, "value": {"double_value": load5}})
    series.points = [point]
    client.create_time_series(request={"name": project_name, "time_series": [series]})
    time.sleep(60)
