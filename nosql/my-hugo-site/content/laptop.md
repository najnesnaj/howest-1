---
title: Laptop
date: 2025-05-18T09:13:55
draft: false
categories: ["Blog"]
tags: ["sphinx", "hugo"]
---
# Laptop (or PC) mods

/etc/hosts

10.10.10.50 nginx.example.com
10.10.10.50 registry.example.com

> ip route add 10.10.10.0/24 via 192.168.0.251

sudo cp ca.crt /usr/local/share/ca-certificates/ca.crt
sudo update-ca-certificates
Updating certificates in /etc/ssl/certs…
