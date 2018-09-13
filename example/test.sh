#!/usr/bin/env bash

set -eu -o pipefail

docker build -t knorg/docker-registry-credential-generator:1.0.0 ../
kubectl delete deployment registry-deployment || true

kubectl apply -f deploy.yaml

rm -f tmp_htpasswd.txt tmp_passwd.txt

kubectl get secret docker-registry-htpasswd -o jsonpath='{.data.auth}' | base64 -d > tmp_htpasswd.txt
kubectl get secret docker-registry-passwords -o jsonpath='{.data.password}' | base64 -d > tmp_passwd.txt

docker run \
    --entrypoint=bash \
    --rm=true \
    -v $(pwd):/example \
    -i knorg/docker-registry-credential-generator:1.0.0 \
    -c 'htpasswd -vb /example/tmp_htpasswd.txt registry $(cat /example/tmp_passwd.txt)'