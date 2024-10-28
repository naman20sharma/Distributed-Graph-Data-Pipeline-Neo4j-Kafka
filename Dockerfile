# Base image: ubuntu:22.04
FROM ubuntu:22.04

# ARGs
# https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# neo4j 5.5.0 installation and cleanup
RUN apt-get update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y wget gnupg software-properties-common && \
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y nano unzip neo4j=1:5.5.0 python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set up environment variables to install the GDS plugin and initial password securely
ARG NEO4J_AUTH=neo4j/project1phase1
RUN neo4j-admin dbms set-initial-password project1phase1 && \
    chmod 777 /var/lib/neo4j/import

# Download the GDS plugin from GitHub Releases
RUN wget -O /var/lib/neo4j/plugins/neo4j-graph-data-science-2.3.1.jar https://github.com/neo4j/graph-data-science/releases/download/2.3.1/neo4j-graph-data-science-2.3.1.jar

# Configure Neo4j to allow unrestricted access and set listening addresses
RUN echo "server.default_listen_address=0.0.0.0" >> /etc/neo4j/neo4j.conf && \
    echo "server.bolt.listen_address=0.0.0.0:7687" >> /etc/neo4j/neo4j.conf && \
    echo "server.http.listen_address=0.0.0.0:7474" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.security.procedures.unrestricted=gds.*,gds.graph.*,apoc.*" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.connector.bolt.enabled=true" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.connector.http.enabled=true" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.connector.bolt.tls_level=DISABLED" >> /etc/neo4j/neo4j.conf

# Build args for cloning without embedding credentials in history
ARG GITHUB_USERNAME
ARG GITHUB_TOKEN
RUN apt-get update && \
    apt-get install -y git && \
    git clone https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/Fall-24-CSE511-Data-Processing-at-Scale/Project-1-nshar108.git /cse511

# Download the NYC Yellow Cab Trip dataset to the root directory
RUN wget -O /yellow_tripdata_2022-03.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet

# Install necessary Python libraries for data processing
RUN pip3 install --upgrade pip && \
    pip3 install neo4j pandas pyarrow requests

# Run the data loader script
RUN chmod +x /cse511/data_loader.py && \
    neo4j start && \
    python3 /cse511/data_loader.py && \
    neo4j stop

# Expose neo4j ports
EXPOSE 7474 7687

# Start neo4j service and show the logs on container run
CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]
