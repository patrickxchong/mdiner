#!/bin/bash

function localtunnel {
  lt -s mdining-scraper --port 80
}

until localtunnel; do
echo "localtunnel server crashed"
sleep 2
done