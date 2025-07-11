#!/bin/bash

while true; do
    mensaje=$(python3 read.py)

    if echo "$mensaje" | grep -q "ON"; then
        echo "ON" > /tmp/estado.txt
    elif echo "$mensaje" | grep -q "OFF"; then
        echo "OFF" > /tmp/estado.txt
    fi

    sleep 10  # Revisa cada 10 segundos
done