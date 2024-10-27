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
            session.run("""
                CALL gds.graph.project(
                    'bfsGraph',
                    'Location',
                    {
                        TRIP: {
                            type: 'TRIP',
                            properties: ['distance']
                        }
                    }
                )
            """)

            # Run BFS algorithm on the projected graph
            query = """
                MATCH (start:Location {name: $start_node}), (end:Location {name: $last_node})
                CALL gds.bfs.stream('bfsGraph', {
                    sourceNode: id(start),
                    targetNodes: [id(end)]
                })
                YIELD path
                RETURN path
            """
            result = session.run(query, start_node=start_node, last_node=last_node)

            # Collect paths from the result
            paths = [
                {
                    "path": [{"name": node["name"]} for node in record["path"].nodes]
                } for record in result
            ]

             # Drop the graph projection to free up resources
            session.run("""
                CALL gds.graph.drop('bfsGraph')
                YIELD graphName
            """)

            return paths


    def pagerank(self, max_iterations, weight_property):
        # TODO: Implement this method
        # Implementing PageRank using Neo4j's Graph Data Science (GDS) library.
        if weight_property not in ["distance", "fare"]:
            raise ValueError("weight_property must be either 'distance' or 'fare'")

        with self._driver.session() as session:
            # Project the graph
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
            
            # Run PageRank
            query = """
                CALL gds.pageRank.stream('pageRankGraph', {
                    maxIterations: $max_iterations,
                    dampingFactor: 0.85,
                    relationshipWeightProperty: $weight_property
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS name, score
            """
            result = session.run(query, max_iterations=max_iterations, weight_property=weight_property)
            all_results = [{"name": record["name"], "score": round(record["score"], 5)} for record in result]

            # Find max and min PageRank nodes
            max_node = max(all_results, key=lambda x: x['score'])
            min_node = min(all_results, key=lambda x: x['score'])

            # Drop the graph projection to free up resources
            session.run("""
                CALL gds.graph.drop('pageRankGraph')
                YIELD graphName
            """)

            return [max_node, min_node]