#!/usr/bin/env python3
from google.api import label_pb2 as ga_label
from google.api import metric_pb2 as ga_metric
from google.cloud import monitoring_v3

client = monitoring_v3.MetricServiceClient()
project_name = f"projects/development-305719"
descriptor = ga_metric.MetricDescriptor()
descriptor.type = "custom.googleapis.com/at_swarm_node_load"
descriptor.metric_kind = ga_metric.MetricDescriptor.MetricKind.GAUGE
descriptor.value_type = ga_metric.MetricDescriptor.ValueType.DOUBLE
descriptor.description = "5m load average for a Docker Swarm node."

labels = ga_label.LabelDescriptor()
labels.key = "load5m"
labels.value_type = ga_label.LabelDescriptor.ValueType.STRING
labels.description = "Swarm node 5m load average"
descriptor.labels.append(labels)

descriptor = client.create_metric_descriptor(
    name=project_name, metric_descriptor=descriptor
)
print("Created {}.".format(descriptor.name))
