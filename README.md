<img src="https://atsign.dev/assets/img/@dev.png?sanitize=true">

### Now for a little internet optimism

# At_Swarm_Load

Source files for Docker image used to send GCE Custom metrics for 5m load average.

## Why, What, How?

### Why?

We want to have load average on the monitoring dashboard, but the Google
Agent sends too much data, and Flatcar doesn't support it anyway.

### What?

This project uses Python3 in order to incorporate the
`google-cloud-monitoring` pip library.

Scripts are based on
[Getting started with Google Cloud Monitoring](https://medium.com/google-cloud/confused-with-custom-monitoring-metrics-on-gcp-c514cd4a776b)
by Arpana Mehta

### How?

The `Dockerfile` is built using:

```
sudo docker build -t atsigncompany/at_swarm_load .
```

and then pushed to Docker Hub with:

```
sudo docker push atsigncompany/at_swarm_load
```

it can then be installed and run on Swarm nodes with:

```
sudo docker run -d --restart unless-stopped atsigncompany/at_swarm_load
```

TODO - automate Docker build and push with an Action.

## Maintainers

Created by @cpswan
