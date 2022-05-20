<img width=250px src="https://atsign.dev/assets/img/@platform_logo_grey.svg?sanitize=true">

# At_Swarm_Load

Source files for Docker image used to send GCE Custom metrics for 5m load
average and root volume utilisation.

## Why, What, How?

### Why?

We want to have load average and disk utilisation on the monitoring
dashboard, but the Google Ops Agent sends too much data, and Flatcar
doesn't support it anyway.

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

### AWS

A version has also been created for AWS VMs. It needs a service account key
as a .json file to replace the placeholder.

First install dependencies:

```bash
sudo apt install python3-pip
pip3 install --no-cache-dir google-cloud-monitoring
```

Then copy over the files in the aws directory to their respective places on
the Ubuntu VM filesystem. `sudo` will be needed to copy the systemd service
definition into place.

Finally enable and start the service:

```bash
sudo systemctl enable gcp-mon.service
sudo systemctl start gcp-mon.service
```

## Maintainers

Created by @cpswan
