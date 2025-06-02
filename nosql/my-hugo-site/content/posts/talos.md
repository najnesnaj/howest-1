---
title: Talos
date: 2025-05-18T09:13:55
draft: false
categories: ["Blog"]
tags: ["sphinx", "hugo"]
---
# Talos

Talos is a modern OS for Kubernetes. It is designed to be secure, immutable, and minimal. Talos is a self-hosted Kubernetes distribution that runs on bare metal or virtualized infrastructure. Talos is designed to be managed by a central Kubernetes control plane, which can be hosted on the same cluster or on a separate cluster.

talosctl config add my-cluster –endpoints 192.168.0.242

talosctl config info

talosctl config endpoint 192.168.0.242

talosctl gen config my-cluster [https://192.168.0.242:6443](https://192.168.0.242:6443) –output-dir ./talos-config –force

## new install talos

[https://www.talos.dev/v1.9/talos-guides/install/virtualized-platforms/proxmox/](https://www.talos.dev/v1.9/talos-guides/install/virtualized-platforms/proxmox/)

> > talosctl gen config my-cluster [https://192.168.0.218:6443](https://192.168.0.218:6443)
> > talosctl -n 192.168.0.169 get disks –insecure (check disks)
> > talosctl config endpoint 192.168.0.218
> > talosctl config node 192.168.0.218

> > talosctl apply-config –insecure –nodes 192.168.0.218 –file controlplane.yaml

> > talosctl bootstrap
> > talosctl kubeconfig . (retrieve kubeconfig)
> > talosctl –nodes 192.168.0.218 version (verify)

> > export KUBECONFIG=./talos-config/kubeconfig

> > > kubectl get nodes
> > > kubectl get pods -n kube-system
> > > kubectl get pods -n kube-system -o wide

> kubectl describe pod my-postgres-postgresql-0 (is very useful in case the pod does get deployed

> [https://factory.talos.dev/](https://factory.talos.dev/) (create your custom image)

> ```bash
> talosctl upgrade --nodes 10.10.10.178 --image  factory.talos.dev/installer/c9078f9419961640c712a8bf2bb9174933dfcf1da383fd8ea2b7dc21493f8bac:v1.9.5
> ```

watching nodes: [10.10.10.178]
: talosctl get extensions –nodes 10.10.10.178

NODE           NAMESPACE   TYPE              ID   VERSION   NAME          VERSION
10.10.10.178   runtime     ExtensionStatus   0    1         iscsi-tools   v0.1.6
10.10.10.178   runtime     ExtensionStatus   1    1         schematic     c9078f9419961640c712a8bf2bb9174933dfcf1da383fd8ea2b7dc21493f8bac
