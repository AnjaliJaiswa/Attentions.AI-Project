from typing import List, Dict
from .base_agent import BaseLLMAgent

class FutureWorksAgent(BaseLLMAgent):
    def __init__(self):
        super().__init__()

    async def generate(self, topic: str) -> Dict[str, List[str]]:
        system_prompt = f"""
        You are a research direction analyst specialized in {topic}.
        Your task is to identify promising future research directions based on current literature.
        Focus on identifying gaps, potential improvements, and novel applications.
        """

        future_works_prompt = f"""
        Based on the current state of research in {topic}, provide:
        1. List 5 major research gaps
        2. Suggest 3 novel methodological improvements
        3. Propose 4 potential applications or extensions
        4. Identify 3 cross-disciplinary research opportunities

        Format the response as a JSON-like structure with these categories.
        """

        response = await self.generate(future_works_prompt, system_prompt)
        
        # Generate detailed explanations for each suggestion
        detailed_prompt = f"""
        For each research direction identified, provide:
        1. Rationale for its importance
        2. Potential challenges and prerequisites
        3. Expected impact on the field

        Original suggestions:
        {response}
        """
        
        detailed_response = await self.generate(detailed_prompt, system_prompt)
        
        return {
            "summary": response,
            "detailed_analysis": detailed_response
        }

    async def generate_review(self, topic: str) -> str:
        system_prompt = """
        You are an academic review paper writer. 
        Generate a comprehensive review paper that follows standard academic structure and formatting.
        Include proper citations and maintain a formal academic tone.
        """

        review_prompt = f"""
        Create a review paper for {topic} with the following sections:
        1. Introduction
        2. Current State of the Field
        3. Major Research Directions
        4. Challenges and Limitations
        5. Future Research Opportunities
        6. Conclusion

        Follow these guidelines:
        - Use formal academic language
        - Maintain objective tone
        - Include specific examples and references
        - Highlight key contributions and findings
        - Identify research gaps and opportunities
        """

        initial_draft = await self.generate(review_prompt, system_prompt)

        # Enhance the review with specific improvements
        enhancement_prompt = f"""
        Improve the following review paper draft:
        {initial_draft}

        Focus on:
        1. Strengthening the analytical depth
        2. Adding more specific examples
        3. Ensuring logical flow between sections
        4. Enhancing the future research section
        5. Adding clear conclusions and implications
        """

        final_review = await self.generate(enhancement_prompt, system_prompt)
        return final_review
