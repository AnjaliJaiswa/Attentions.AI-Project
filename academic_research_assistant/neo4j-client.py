from neo4j import GraphDatabase
from datetime import datetime
from typing import List, Optional

class Neo4jClient:
    def __init__(self):
        self.uri = "neo4j://localhost:7687"
        self.auth = ("neo4j", "password")  # Change in production
        self.driver = GraphDatabase.driver(self.uri, auth=self.auth)

    async def store_paper(self, paper):
        async with self.driver.session() as session:
            # Create paper node
            query = """
            CREATE (p:Paper {
                title: $title,
                abstract: $abstract,
                url: $url,
                published_date: $published_date,
                content: $content
            })
            """
            await session.run(query, paper.dict())

    async def get_papers(self, topic: str, start_year: Optional[int] = None, end_year: Optional[int] = None):
        async with self.driver.session() as session:
            query = """
            MATCH (p:Paper)
            WHERE p.title CONTAINS $topic
            """
            if start_year and end_year:
                query += f" AND datetime(p.published_date).year >= {start_year}"
                query += f" AND datetime(p.published_date).year <= {end_year}"
            query += " RETURN p"
            
            result = await session.run(query, {"topic": topic})
            return [dict(record["p"]) for record in result]

    def close(self):
        self.driver.close()
