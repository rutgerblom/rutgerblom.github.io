+++
date = '2025-01-26T11:03:30+01:00'
title = 'Avi Load Balancer Metrics with Prometheus and Grafana'
+++

Avi Load Balancer offers a wealth of valuable metrics that can be accessed directly via the Avi Controller’s UI or API.

However, there are various reasons why you might want to make these metrics available outside of its native platform. For instance, you might wish to avoid granting users or systems direct access to the Avi Load Balancer management plane solely for metric consumption. Alternatively, you might need to store and analyze metrics in a centralized system or simply back them up for future use.

Fortunately, there are several methods for fetching metrics from the Avi Load Balancer and processing or storing them externally. In this article, I’ll guide you through the process of setting up an automated workflow where Avi Load Balancer metrics are fetched by Prometheus and visualized in Grafana.

```yaml
##
## avi-api-proxy-deployment.yaml
##
apiVersion: apps/v1
kind: Deployment
metadata:
  name: avi-api-proxy
  namespace: observability
  labels:
    app: avi-api-proxy
spec:
  replicas: 1
  selector:
    matchLabels:
      app: avi-api-proxy
  template:
    metadata:
      labels:
        app: avi-api-proxy
    spec:
      containers:
      - name: avi-api-proxy
        image: avinetworks/avi-api-proxy:latest
        ports:
        - containerPort: 8080
        env:
        - name: AVI_CONTROLLER
          value: "10.203.240.15"
        - name: AVI_USERNAME
          value: "prometheus"
        - name: AVI_PASSWORD
          value: "VMware1!"
        - name: AVI_TIMEOUT
          value: "60"
---
apiVersion: v1
kind: Service
metadata:
  name: avi-api-proxy-service
  namespace: observability
  labels:
    app: avi-api-proxy
spec:
  selector:
    app: avi-api-proxy
  ports:
  - protocol: TCP
    port: 8080
    targetPort: 8080
````

