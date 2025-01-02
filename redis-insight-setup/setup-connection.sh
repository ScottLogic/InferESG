#!/bin/sh -
sleep 30s

response=$(curl -s -X "GET" "http://host.docker.internal:5540/api/databases/")

if [[ "$response" == "[]" ]] ; then
  echo "Creating Redis connection"

  curl -s -X "POST" "http://host.docker.internal:5540/api/databases/" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d '{"host": "'${REDIS_CONNECTION_HOST}'","name": "redis","port": '${REDIS_CONNECTION_PORT}',"compressor": "NONE","ssh": false,"tls":false,"verifyServerCert":false}'
else
  echo "$response"
  echo "Redis database connection already setup"
fi
