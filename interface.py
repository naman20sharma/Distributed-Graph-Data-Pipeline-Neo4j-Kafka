from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def bfs(self, start_node, last_node):
        # TODO: Implement this method
        with self._driver.session() as session:
            result = session.run("""
                MATCH (start:Location {name: $start_node})
                CALL gds.alpha.bfs.stream({
                    startNode: id(start),
                    targetNodes: $last_node,
                    relationshipWeightProperty: 'trip_distance'
                })
                YIELD path, totalCost
                RETURN path, totalCost
            """, start_node=start_node, last_node=last_node)

            # Collect paths to each target node along with their total costs
            paths = [{"path": record["path"], "totalCost": record["totalCost"]} for record in result]
            return paths

    def pagerank(self, max_iterations, weight_property):
        # TODO: Implement this method
        # Implementing PageRank using Neo4j's Graph Data Science (GDS) library.
        with self._driver.session() as session:
            # First, make sure the graph is projected for GDS processing
            session.run("""
                CALL gds.graph.project(
                    'pageRankGraph',
                    'Location',
                    {
                        TRIP: {
                            properties: $weight_properties
                        }
                    }
                )
            """, weight_properties=[weight_property])
            
            # Check if projection was successful
            result = session.run("CALL gds.graph.exists('pageRankGraph') YIELD exists RETURN exists")
            if not result.single()["exists"]:
                raise RuntimeError("Graph projection failed. Please check your data.")

            # Running the PageRank algorithm
            query = """
                CALL gds.pageRank.stream('pageRankGraph', {
                    maxIterations: $max_iterations,
                    dampingFactor: 0.85,
                    relationshipWeightProperty: $weight_property
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS name, score
                ORDER BY score DESC
                LIMIT 2
            """
            result = session.run(query, max_iterations=max_iterations, weight_property=weight_property)
            nodes = result.data()
            return nodes