#!/usr/bin/env bash

set -e -u -x

python3 -m pip install paho-mqtt tcping

python3 main.py \
  --mqtt-hostname="${MQTT_HOSTNAME}" \
  --mqtt-port="${MQTT_PORT}" \
  --mqtt-user="${MQTT_USER}" \
  --mqtt-password="${MQTT_PASSWORD}" "$@"
