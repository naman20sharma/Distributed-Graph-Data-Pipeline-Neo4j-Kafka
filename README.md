# Project-1-nshar108

**ASU ID**: 1230090591  
**ASURITE Email**: nshar108@asu.edu

## NYC Yellow Taxi Data Processing with Neo4j

This project processes NYC Yellow Taxi trip data, loads it into a Neo4j graph database, and applies graph analysis algorithms such as Breadth-First Search (BFS) and PageRank using Neo4j’s Graph Data Science (GDS) plugin.

### Project Structure

- **Dockerfile**: Sets up the environment, installs dependencies, configures Neo4j, and initializes the database with taxi trip data.
- **data_loader.py**: Reads and filters the taxi data, then loads it into Neo4j with nodes and relationships.
- **interface.py**: Implements BFS and PageRank using Neo4j’s GDS library for graph traversal and node ranking.

## Prerequisites

- Docker
- GitHub credentials (for cloning the repository)

### Docker Configuration

The `Dockerfile` configures the Neo4j environment to enable GDS plugin functionality, set up permissions, and manage dependencies:

1. **Neo4j 5.5.0** is installed with OpenJDK 17, along with essential dependencies.
2. **Neo4j Graph Data Science (GDS) Plugin**: Downloaded and stored in the Neo4j plugins directory (`/var/lib/neo4j/plugins`) to allow advanced graph algorithms.
3. **Database Configuration**:
   - The file permissions for `/var/lib/neo4j/import` are set to `777` to allow data import.
   - Authentication credentials are set using `neo4j-admin dbms set-initial-password`.
4. **Network Configuration**:
   - Configured Neo4j to listen on all network interfaces.
   - Exposed Neo4j’s Bolt (7687) and HTTP (7474) ports.
5. **Unrestricted Procedures**:
   - Neo4j security settings are modified to allow unrestricted access to GDS and APOC procedures (`gds.*, gds.graph.*, apoc.*`), allowing execution of all necessary GDS functions.

## Usage

### Build the Docker Image

To create the Docker image, use the following command:
```bash
docker build -t nyc-taxi-neo4j .
```

### Run the Docker Container

Once the image is built, start the Neo4j container:
```bash
docker run -d --name neo4j-container -p 7474:7474 -p 7687:7687 nyc-taxi-neo4j
```

This will start the Neo4j database and load the NYC Yellow Taxi data into Neo4j.

### Access Neo4j Browser

Open a web browser and navigate to:
```
http://localhost:7474
```

Log in with:
- **Username**: `neo4j`
- **Password**: `project1phase1`

### Testing Functions

A Python script `tester.py` is available to validate the PageRank and BFS functions:

```bash
docker exec -it neo4j-container /bin/bash
cd /cse511
python3 tester.py
```

The test cases of `tester.py` were passing successfully for me. You can view the screenshot of the successful test cases [here](https://drive.google.com/file/d/1Ew-lt44iC_Z4r5WtLXdnV85t57q5Hitu/view?usp=sharing).

## File Descriptions

### 1. Dockerfile

The Dockerfile sets up an Ubuntu-based environment with Neo4j 5.5.0, installs required Python libraries (e.g., `neo4j`, `pandas`, `pyarrow`, `requests`), and downloads NYC Yellow Taxi data. Key steps include:

- **Setting Neo4j Initial Password**: Configured via `neo4j-admin dbms set-initial-password`.
- **Downloading GDS Plugin**: The GDS plugin `.jar` file is downloaded from GitHub and placed in the Neo4j plugins directory.
- **Network and Security Settings**: Ports are exposed, and the Neo4j configuration is modified to allow unrestricted access to GDS and APOC procedures.
- **Running Data Loader Script**: The script loads and processes the Yellow Taxi data into Neo4j.

### 2. `interface.py`

This file defines the `Interface` class, which serves as the connection between the Python application and the Neo4j graph database. It provides two key methods for performing graph analysis tasks using Neo4j’s GDS plugin: Breadth-First Search (BFS) and PageRank. These methods allow for the exploration and analysis of the relationships between various nodes in the NYC Yellow Taxi data, such as determining routes between different locations and evaluating the significance of specific nodes within the network.

- **`bfs`**: This method performs a Breadth-First Search (BFS) traversal from a specified start node to one or more target nodes using the GDS library. The process starts by projecting the graph as `bfsGraph` in Neo4j, which involves selecting specific node and relationship types for analysis. Once projected, the BFS algorithm is executed to find paths between the start node and target nodes. The resulting traversal paths are then returned, and the graph projection is subsequently dropped to free up system resources.
  - **Why this approach**: The BFS algorithm is efficient for exploring connections between nodes in a graph. It is particularly useful for determining the shortest path or evaluating reachability within a network, such as finding routes between taxi pick-up and drop-off locations.
  - **Return Values**: The method returns a list of paths, each consisting of nodes that represent possible routes from the starting location to the target location.

- **`pagerank`**: This method calculates PageRank scores for nodes in the projected graph, named `pageRankGraph`. PageRank is used to determine the importance or influence of nodes within the network. The method first projects the graph with the relevant nodes and relationships, then runs the PageRank algorithm using specified parameters, including `maxIterations` and the relationship weight property (e.g., `distance` or `fare`). After calculating the PageRank scores, the method identifies and returns the nodes with the highest and lowest scores, providing insight into which locations are the most or least influential based on the defined criteria. Finally, the graph projection is dropped to conserve resources.
  - **Why this approach**: PageRank is a well-established algorithm originally designed for ranking web pages, but it is also highly effective in evaluating the influence of nodes in various network contexts. For the NYC Yellow Taxi data, it helps identify which locations are central or have the most significant impact on the overall network.
  - **Return Values**: The method returns two nodes: the one with the highest PageRank score and the one with the lowest, along with their respective scores. This allows for quick identification of the most influential and least connected locations within the dataset.


### 3. `data_loader.py`

This file processes the NYC Yellow Taxi data, performing initial transformations and filtering, then loads it into Neo4j with nodes and relationships.

- **Filtering Data**: Trips are filtered by Bronx-specific location IDs, minimum trip distance, and fare amount.
- **Data Transformation**: Reads `.parquet` data, converts it to `.csv` format, and loads it into Neo4j.
- **Creating Nodes and Relationships**: 
  - `Location` nodes are created based on unique location IDs.
  - `TRIP` relationships are established between pickup and dropoff locations with `distance` and `fare` attributes.

## Important Notes

1. **Neo4j Configuration**: Adjustments in the Dockerfile include permissions, unrestricted GDS procedures, and custom configuration for `neo4j.conf`.
2. **Session Management**: The Python code uses Neo4j’s recommended transaction functions within `interface.py`, ensuring efficient use of sessions.
3. **GDS Library Requirement**: The GDS library enables advanced graph functions, so it’s essential that the plugin is downloaded and configured as specified.

## Troubleshooting

- **GDS Plugin Not Detected**: Ensure `dbms.security.procedures.unrestricted=gds.*, gds.graph.*, apoc.*` is correctly set in `neo4j.conf` and Neo4j is restarted.
- **Data Not Loading**: Confirm permissions for `/var/lib/neo4j/import` are correctly set to `777`, as specified in the Dockerfile.
- **Session Closed Error**: This may occur if sessions are not properly managed; the code uses the `with` statement in the Neo4j driver to prevent such issues.
