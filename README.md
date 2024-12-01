# Project-1-nshar108

**ASU ID**: 1230090591  
**ASURITE Email**: nshar108@asu.edu  

## NYC Yellow Taxi Data Processing with Neo4j, Kafka, and Kubernetes  

This project extends the NYC Yellow Taxi trip data processing from Phase-1 by integrating a robust pipeline with Apache Kafka, Zookeeper, Neo4j, and Kubernetes. The ecosystem enables real-time ingestion, processing, and analysis of data using graph algorithms like Breadth-First Search (BFS) and PageRank with Neo4j's Graph Data Science (GDS) plugin.

---

**Pod Readiness: Ensure each pod is in a healthy state before proceeding to the next step. Transitioning prematurely can cause errors in data flow and service connections.**

---

## Project-1 Phase-2  

### Prerequisites  
- **Minikube**: For creating a local Kubernetes cluster.  
- **Helm**: For deploying and managing the Neo4j database with charts.  
- **Python Libraries**: `confluent-kafka`, `neo4j`, `pandas`, `pyarrow`, `requests`.  

### Project Overview  

In **Phase-2**, the primary focus is on building an ecosystem to process streaming data, as opposed to the static dataset analysis in **Phase-1**. Kafka serves as the backbone for real-time data ingestion, while Neo4j is used for storage and analysis. Zookeeper ensures Kafka's distributed environment stability, and Minikube provides a localized Kubernetes environment for managing the system.

---

## Steps to Execute  

### Step 0: Start Minikube  
Start the Minikube cluster with sufficient resources:  
```bash
minikube start --cpus=6 --memory=8192
minikube status
```

To monitor and interact with the cluster visually, use the optional dashboard:  
```bash
minikube dashboard
```

Verify cluster information (optional):  
```bash
kubectl cluster-info
```

---

### Step 1: Deploy Zookeeper and Kafka  

Apply the Zookeeper setup:  
```bash
kubectl apply -f zookeeper-setup.yaml
```

Check the progress of deployments (optional):  
```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

Deploy Kafka using the provided setup:  
```bash
kubectl apply -f kafka-setup.yaml
kubectl exec -it kafka-deployment-<pod-id> -- bash
```

---

### Step 2: Deploy Neo4j  

Ensure Helm is installed in the environment. Use the following commands to deploy Neo4j:

Optional: Start a Minikube tunnel (recommended for environments requiring load balancers):  
```bash
minikube tunnel
```

Deploy Neo4j using the Helm chart:  
```bash
helm install neo4j-standalone neo4j/neo4j -f neo4j-values.yaml
```

Monitor the Neo4j pod status:  
```bash
kubectl rollout status --watch --timeout=600s statefulset/neo4j-standalone
```

Apply the Neo4j service configuration:  
```bash
kubectl apply -f neo4j-service.yaml
```

---

### Step 3: Deploy Kafka-Connect  

Deploy the Kafka-Neo4j connector:  
```bash
kubectl apply -f kafka-neo4j-connector.yaml
```

> **Note:** Allow sufficient time for the Kafka-Connect pod to initialize fully before proceeding.

---

### Step 4: Data Processing and Testing  

Ensure no conflicting services are running on required ports. Kill any process if necessary:  
```bash
kill -9 <PID>
```

Forward the required ports for Neo4j and Kafka:  
```bash
kubectl port-forward svc/neo4j-service 7474:7474 7687:7687
kubectl port-forward svc/kafka-service 9092:9092
```

Install required Python libraries:  
```bash
pip3 install confluent-kafka neo4j pandas pyarrow requests
```

Run the data producer to send trip data to Kafka:  
```bash
python3 data_producer.py
```

Test the implementation using the provided tester script:  
```bash
python3 tester.py
```

---

## Important Notes  

1. **Pod Readiness**: Ensure each pod is in a healthy state before proceeding to the next step. Transitioning prematurely can cause errors in data flow and service connections.  
2. **Neo4j Credentials**: Update the `tester.py` file to match the Neo4j credentials (`neo4j/project1phase2`).  
3. **Kafka-Connect Initialization**: It may take longer for the Kafka-Connect pod to become active. Monitor logs and status as needed.  

---

## References  

- [Neo4j Graph Data Science Documentation](https://neo4j.com/docs/graph-data-science/current/)  
- [Kafka Documentation](https://kafka.apache.org/documentation/)  
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)  
- [Helm Charts for Neo4j](https://github.com/neo4j-contrib/neo4j-helm)  

---

## Test Cases  

The `tester.py` script validates the implementation by:  
- **Verifying Data Load**: Checks if the correct number of nodes and edges are present in the database.  
- **Running PageRank**: Ensures that the PageRank algorithm calculates correct node scores.  
- **Executing BFS**: Validates the BFS implementation and checks for connectivity between specified nodes.  

> The final test case results can be viewed [here](https://drive.google.com/file/d/1nixk1csqtYa3H3C3HxPDFWbXeD0or85H/view?usp=sharing).  
