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
        with self._driver.session() as session:
            session.run("""
            CALL gds.graph.project(
                'myGraph',
                'Location',
                {
                    TRIP: {
                        orientation: 'UNDIRECTED',
                        properties: $weight_property
                    }
                }
            )
        """, weight_property=weight_property)

        # Step 2: Run the PageRank algorithm on the projected graph
        result = session.run("""
            CALL gds.pageRank.stream('myGraph')
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId).name AS location_id, score
            ORDER BY score DESC
        """, max_iterations=max_iterations)

        # Collect all PageRank results
        pagerank_scores = [{"location_id": record["location_id"], "score": record["score"]} for record in result]

        # Step 3: Clean up the in-memory graph
        session.run("CALL gds.graph.drop('myGraph')")

        # Identify max and min PageRank scores
        if pagerank_scores:
            max_pagerank = pagerank_scores[0]  # Node with the highest PageRank
            min_pagerank = pagerank_scores[-1]  # Node with the lowest PageRank
            return {"max": max_pagerank, "min": min_pagerank}
        else:
            return {"max": None, "min": None}
