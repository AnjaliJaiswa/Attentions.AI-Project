from typing import List, Optional
from .base_agent import BaseLLMAgent

class QAAgent(BaseLLMAgent):
    def __init__(self):
        super().__init__()

    async def answer(self, topic: str, question: str, papers: List[dict]) -> str:
        # Create context from papers
        context = self._create_context(papers)
        
        # Generate system prompt for the QA task
        system_prompt = f"""
        You are an academic research assistant specialized in {topic}. 
        Your task is to answer questions based on the provided research papers.
        Always cite the specific papers and sections you use in your answers.
        Use a formal academic tone and be precise in your responses.
        """

        # Create the main prompt
        qa_prompt = f"""
        Based on the following papers:
        {context}

        Answer this question: {question}

        Provide citations to specific papers and sections used in your answer.
        If the information cannot be found in the provided papers, say so explicitly.
        """

        # Get initial answer
        initial_answer = await self.generate(qa_prompt, system_prompt)

        # Use LLM to verify and improve the answer
        verification_prompt = f"""
        Verify and improve the following answer:
        {initial_answer}

        Check for:
        1. Accuracy of citations
        2. Completeness of the answer
        3. Clarity and academic tone
        4. Proper support for all claims

        Provide the improved answer:
        """

        final_answer = await self.generate(verification_prompt, system_prompt)
        return final_answer

    def _create_context(self, papers: List[dict]) -> str:
        context = ""
        for i, paper in enumerate(papers, 1):
            context += f"""
            Paper {i}:
            Title: {paper['title']}
            Authors: {', '.join(paper['authors'])}
            Key Points: {paper['content']}
            ---
            """
        return context
