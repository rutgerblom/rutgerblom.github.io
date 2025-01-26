+++
date = '2025-01-26T11:03:30+01:00'
title = 'My First Post'
+++

### Hello

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

