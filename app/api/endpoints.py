from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ..models.search import Searcher
from ..models.vectorizer import Vectorizer

app = FastAPI(title="GOST Search API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models at startup
vectorizer = Vectorizer.load()
searcher = Searcher(vectorizer)

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    score: float
    document: str
    paragraph: str
    document_index: int
    paragraph_index: int

@app.post("/search", response_model=list[SearchResult])
async def search(request: SearchRequest):
    """Search for similar paragraphs in GOST documents"""
    results = searcher.find_similar_paragraphs(request.query, request.top_k)
    return results

@app.get("/health")
async def health_check():
    return {"status": "healthy"}