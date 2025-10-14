<a href="https://atsign.com#gh-light-mode-only"><img width=250px src="https://atsign.com/wp-content/uploads/2022/05/atsign-logo-horizontal-color2022.svg#gh-light-mode-only" alt="The Atsign Foundation"></a><a href="https://atsign.com#gh-dark-mode-only"><img width=250px src="https://atsign.com/wp-content/uploads/2023/08/atsign-logo-horizontal-reverse2022-Color.svg#gh-dark-mode-only" alt="The Atsign Foundation"></a>

[![SLSA 3](https://slsa.dev/images/gh-badge-level3.svg)](https://slsa.dev)

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

## SLSA

The Docker images created from this repo have SLSA Build Level 3 attestations.

These can be verified using the
[slsa-verifier](https://github.com/slsa-framework/slsa-verifier) tool e.g.:

```sh
IMAGE="atsigncompany/at_swarm_load:latest"
SHA=$(docker buildx imagetools inspect ${IMAGE} \
  --format "{{json .Manifest}}" | jq -r .digest)
slsa-verifier verify-image ${IMAGE}@${SHA} \
  --source-uri github.com/atsign-company/at_swarm_load
```

## Docker image signing

This images from this repo are signed during the build process so that you
can verify their authenticity using
[cosign](https://github.com/sigstore/cosign):

```sh
cosign verify atsigncompany/at_swarm_load:latest \
--certificate-oidc-issuer=https://token.actions.githubusercontent.com \
--certificate-identity-regexp='^https://github.com/atsign-company/at_swarm_load/.+'
```

## Maintainers

Created by [@cpswan](https://github.com/cpswan)
