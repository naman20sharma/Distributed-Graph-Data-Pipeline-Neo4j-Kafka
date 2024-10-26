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
                CALL gds.beta.bfs.stream({
                    startNode: start,
                    targetNodes: [$last_node],
                    relationshipWeightProperty: 'trip_distance'
                })
                YIELD path, totalCost
                RETURN path, totalCost
            """, start_node=start_node, last_node=last_node)

            paths = [{"path": record["path"], "totalCost": record["totalCost"]} for record in result]
            return paths

    def pagerank(self, max_iterations, weight_property):
        # TODO: Implement this method
        with self._driver.session() as session:
            result = session.run("""
                CALL gds.pageRank.stream({
                    nodeProjection: 'Location',
                    relationshipProjection: {
                        type: 'TRIP',
                        properties: $weight_property
                    },
                    maxIterations: $max_iterations,
                    dampingFactor: 0.85
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS location_id, score
                ORDER BY score DESC
            """, max_iterations=max_iterations, weight_property=weight_property)

            pagerank_scores = [{"location_id": record["location_id"], "score": record["score"]} for record in result]
            return pagerank_scores

