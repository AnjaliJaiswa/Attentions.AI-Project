import arxiv
from typing import List
import asyncio
from .base_agent import BaseLLMAgent
from datetime import datetime

class SearchAgent(BaseLLMAgent):
    def __init__(self):
        super().__init__()
        self.client = arxiv.Client()

    async def search(self, topic: str) -> List[dict]:
        # First, use LLM to generate optimal search terms
        search_prompt = f"""
        Given the research topic "{topic}", generate 3-5 specific search terms or phrases 
        that would be most effective for finding relevant academic papers. Format the response 
        as a comma-separated list.
        """
        search_terms = await self.generate(search_prompt)
        search_terms = [term.strip() for term in search_terms.split(",")]

        # Search arxiv using the generated terms
        papers = []
        for term in search_terms:
            search = arxiv.Search(
                query=term,
                max_results=10,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            results = list(self.client.results(search))
            for paper in results:
                # Use LLM to analyze paper relevance
                relevance_prompt = f"""
                Given the research topic "{topic}", analyze if the following paper is relevant:
                Title: {paper.title}
                Abstract: {paper.summary}
                Return only 'yes' or 'no'.
                """
                is_relevant = await self.generate(relevance_prompt)
                
                if is_relevant.strip().lower() == 'yes':
                    papers.append({
                        "title": paper.title,
                        "authors": [author.name for author in paper.authors],
                        "abstract": paper.summary,
                        "url": paper.pdf_url,
                        "published_date": paper.published.isoformat(),
                        "content": await self._extract_key_points(paper.summary)
                    })

        return papers

    async def _extract_key_points(self, abstract: str) -> str:
        prompt = f"""
        Extract and summarize the key points from the following paper abstract in a structured format:
        {abstract}
        Include: main objectives, methodology, key findings, and implications.
        """
        return await self.generate(prompt)
