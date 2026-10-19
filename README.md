# Otel - Python Demo

This repo includes files to run a local OpenTelemetry ecosystem for demo and play-testing

WARNING: This repo include hard-coded credentials. Don't do that.

## Files

- `datapoints.py`  
  Includes a python script that generates a 15-point guage metric for demonstration purposes
- `values.yaml`  
  OpenTelemetry Collector config
- `grafana-values.yaml`  
  Demo grafana helm chart
- `influxdb-values.yaml`  
  Demo Influxdb helm chart
- `uv.lock`  
  lightweight package manager info stuff
- `pyproject.toml`  
  dummy data for local repo project

## OpenTelemetry

Open-source library and standards for shipping telemetry data between sources and sinks.

Python app is instrumented with `otel` libraries, and exports to a OTEL endpoint. This endpoint is backed by a collector that can process and ship data to a storage and visualization backend. The data is exported in this case to InfluxDB (Time Series Database), and queried and visualized in Grafana.

## How to run

Minikube for local kubernetes cluster

Helm to install these values files

`uv` for python package management
