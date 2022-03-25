#!/usr/bin/env python3
from google.cloud import monitoring_v3

import time
import os
import shutil
import json

hostname = os.uname()[1]
keyfile = "aws-metrics.json"
zone = "us-central1-a"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = keyfile

client = monitoring_v3.MetricServiceClient()
project_id = json.load(open(keyfile))['project_id']
project_name = f"projects/{project_id}"

load_series = monitoring_v3.TimeSeries()
load_series.metric.type = "custom.googleapis.com/at_swarm_node_load"
load_series.resource.type = "gce_instance"
load_series.resource.labels["instance_id"] = hostname
load_series.resource.labels["zone"] = zone

du_series = monitoring_v3.TimeSeries()
du_series.metric.type = "custom.googleapis.com/at_swarm_node_root_volume_usage"
du_series.resource.type = "gce_instance"
du_series.resource.labels["instance_id"] = hostname
du_series.resource.labels["zone"] = zone

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