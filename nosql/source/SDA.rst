SDA (software defined architecture)
====================================


Physical Infrastructure
------------------------

.. blockdiag::
   
   blockdiag {
     orientation = portrait;
     default_shape = roundedbox;
     default_group_color = "#D5E8D4";
     span_width = 220;
     
     "Physical Server" [shape = box, color = "#DAE8FC", width = 200];
     "Physical Server" -> "Proxmox VE Hypervisor" [folded];
     
     group {
       label = "Virtualization Layer";
       color = "#DAE8FC";
       
       "Proxmox VE Hypervisor" [width = 180];
       "Proxmox VE Hypervisor" -> "VM: Talos Node 1";
       "Proxmox VE Hypervisor" -> "VM: Talos Node 2";
       "Proxmox VE Hypervisor" -> "VM: Talos Node N";
       "Proxmox VE Hypervisor" -> "LXC: Router";
     }
     
     group {
       label = "Kubernetes Cluster";
       color = "#FFE6CC";
       
       "VM: Talos Node 1" [label = "Talos Node 1\n(Control Plane)"];
       "VM: Talos Node 2" [label = "Talos Node 2\n(Worker)"];
       "VM: Talos Node N" [label = "Talos Node N\n(Worker)"];
     }
     
     "LXC: Router" [label = "LXC: Router\n(Traffic Management)"];
   }

Proxmox Server Specifications
-----------------------------

The foundation of the architecture is a physical server running Proxmox VE hypervisor.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Component
     - Description
   * - **Hypervisor**
     - Proxmox Virtual Environment (VE)
   * - **Virtual Machines**
     - Multiple Talos OS nodes forming a Kubernetes cluster
   * - **Containers**
     - LXC container serving as a router

Virtual Machine Configuration
-----------------------------

.. admonition:: Talos OS Nodes

   The cluster consists of multiple Talos OS nodes, with dedicated roles:

   * **Control Plane Node(s)**: Manages the Kubernetes control plane
   * **Worker Nodes**: Runs application workloads

.. code-block:: console

   # Example Talos configuration structure (simplified)
   machine:
     type: controlplane  # or worker
     network:
       hostname: talos-node-1
     kubernetes:
       version: v1.26.0

Networking Architecture
-----------------------

.. blockdiag::

   blockdiag {
     orientation = portrait;
     default_shape = roundedbox;
     
     "External Network" [shape = cloud, color = "#DAE8FC"];
     "External Network" -> "LXC Router";
     
     group {
       label = "Internal Network";
       color = "#D5E8D4";
       
       "LXC Router" -> "Proxmox Virtual Bridge";
       "Proxmox Virtual Bridge" -> "Talos Node 1";
       "Proxmox Virtual Bridge" -> "Talos Node 2";
       "Proxmox Virtual Bridge" -> "Talos Node N";
     }
     
     group {
       label = "Kubernetes Overlay Network";
       color = "#FFE6CC";
       
       "Talos Node 1" <-> "Talos Node 2" [folded];
       "Talos Node 2" <-> "Talos Node N" [folded];
       "Talos Node N" <-> "Talos Node 1" [folded];
     }
   }

Network Components
~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Component
     - Function
   * - **Proxmox Virtual Bridge**
     - Creates isolated network segments for VMs and containers
   * - **LXC Router**
     - Routes traffic between internal and external networks
   * - **Kubernetes Overlay Network**
     - Enables pod-to-pod communication (Cilium, Flannel, etc.)

Control & Automation
--------------------

.. blockdiag::

   blockdiag {
     orientation = portrait;
     default_shape = roundedbox;
     default_group_color = "#FFE6CC";
     span_width = 220;
     
     "Administrator" [shape = actor, color = "#DAE8FC"];
     "Administrator" -> "Proxmox API";
     "Administrator" -> "Talos API";
     "Administrator" -> "Kubernetes API";
     
     group {
       label = "Management APIs";
       
       "Proxmox API" [label = "Proxmox API\n(VM/LXC Management)"];
       "Talos API" [label = "Talos API\n(OS Configuration)"];
       "Kubernetes API" [label = "Kubernetes API\n(Workload Orchestration)"];
     }
     
     "Proxmox API" -> "Proxmox VE Hypervisor";
     "Talos API" -> "Talos Nodes";
     "Kubernetes API" -> "Kubernetes Cluster";
     
     "Proxmox VE Hypervisor" [shape = box];
     "Talos Nodes" [shape = box];
     "Kubernetes Cluster" [shape = box];
   }

API Management Layer
~~~~~~~~~~~~~~~~~~~~

This architecture leverages multiple declarative APIs for infrastructure management:

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - API
     - Responsibility
   * - **Proxmox API**
     - Manages physical resources, VMs, and containers
   * - **Talos API**
     - Provides declarative OS configuration and maintenance
   * - **Kubernetes API**
     - Orchestrates applications and services

Benefits of This Architecture
-----------------------------

- **Immutable Infrastructure**: Talos OS provides an immutable, declarative operating system
- **High Availability**: Kubernetes manages service availability and distribution
- **Resource Efficiency**: Consolidates multiple services on a single physical server
- **Isolation**: Separate network segments and container boundaries
- **Automation**: API-driven management at all levels
