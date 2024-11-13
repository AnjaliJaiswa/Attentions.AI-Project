from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from agents.search_agent import SearchAgent
from agents.qa_agent import QAAgent 
from agents.future_works_agent import FutureWorksAgent
import asyncio


app = FastAPI()

# Initialize agents
search_agent = SearchAgent()
qa_agent = QAAgent()
future_agent = FutureWorksAgent()

class QuestionRequest(BaseModel):
    topic: str
    question: str
    papers: Optional[List[dict]] = None

@app.get("/")
async def root():
    return {"message": "Academic Research Assistant API"}

@app.post("/search")
async def search_papers(topic: str):
    try:
        papers = await search_agent.search(topic)
        return {"papers": papers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        answer = await qa_agent.answer(
            request.topic,
            request.question,
            request.papers if request.papers else []
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-future-works")
async def generate_future_works(topic: str):
    try:
        future_works = await future_agent.generate(topic)
        return future_works
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)