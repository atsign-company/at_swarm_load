#!/usr/bin/env python3
from google.api import label_pb2 as ga_label
from google.api import metric_pb2 as ga_metric
from google.cloud import monitoring_v3

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

client = monitoring_v3.MetricServiceClient()
descriptor = ga_metric.MetricDescriptor()
descriptor.type = "custom.googleapis.com/at_swarm_node_root_volume_usage"
descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
descriptor.description = "Disk usage on root volume for a Docker Swarm node."

labels = ga_label.LabelDescriptor()
labels.key = "rootdu"
labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
labels.description = "Swarm node root disk usage"
descriptor.labels.append(labels)

descriptor = client.create_metric_descriptor(
    name=project_name, metric_descriptor=descriptor
)
print("Created {}.".format(descriptor.name))
