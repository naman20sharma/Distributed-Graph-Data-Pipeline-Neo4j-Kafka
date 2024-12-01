#!/bin/bash

# Script to deploy Kafka-Neo4j connector and monitor pod readiness

echo "Applying Kafka-Neo4j Connector configuration..."
kubectl apply -f kafka-neo4j-connector.yaml

echo "Waiting for Kafka-Neo4j Connector pod to initialize..."
while true; do
    POD_STATUS=$(kubectl get pods -l app=kafka-neo4j-connector -o jsonpath='{.items[0].status.phase}')
    if [[ $POD_STATUS == "Running" ]]; then
        echo "Kafka-Neo4j Connector pod is running."
        break
    else
        echo "Current pod status: $POD_STATUS. Retrying in 10 seconds..."
        sleep 10
    fi
done

echo "Deployment complete. You can proceed to the next step."
