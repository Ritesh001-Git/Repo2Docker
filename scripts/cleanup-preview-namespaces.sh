#!/usr/bin/env bash
set -euo pipefail

MAX_AGE_HOURS="${MAX_AGE_HOURS:-2}"
NOW_EPOCH="$(date +%s)"

kubectl get namespaces \
  -l repo2docker.io/preview=true \
  -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.metadata.creationTimestamp}{"\n"}{end}' |
while read -r namespace created_at; do
  [ -z "${namespace:-}" ] && continue
  created_epoch="$(date -d "$created_at" +%s)"
  age_hours="$(( (NOW_EPOCH - created_epoch) / 3600 ))"
  if [ "$age_hours" -ge "$MAX_AGE_HOURS" ]; then
    echo "Deleting preview namespace $namespace (${age_hours}h old)"
    kubectl delete namespace "$namespace"
  fi
done
