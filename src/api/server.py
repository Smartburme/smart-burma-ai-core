from fastapi import FastAPI
from ai_summarizer.summary_engine import SummaryEngine
from pydantic import BaseModel

app = FastAPI(
    title="Smart Burma AI Summary API",
    description="AI Issue Summary for Myanmar/English content"
)

engine = SummaryEngine()

class SummaryRequest(BaseModel):
    text: str
    ratio: float = 0.3

class SummaryResponse(BaseModel):
    summary: str
    language: str
    metrics: dict

@app.post("/summarize", response_model=SummaryResponse)
async def create_summary(request: SummaryRequest):
    result = engine.summarize(request.text, request.ratio)
    return {
        "summary": result["summary"],
        "language": result["language"],
        "metrics": {
            "compression_ratio": f"{request.ratio*100:.0f}%",
            "original_length": result["original_length"],
            "summary_length": result["summary_length"]
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
