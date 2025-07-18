from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import httpx
import redis
from contextlib import asynccontextmanager

from .models import QueryRequest, QueryResponse, DocumentRequest
from .services.rag_service import RAGService
from .services.embedding_service import EmbeddingService
from .services.guardrails import GuardrailsService

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize services
    app.state.redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
    app.state.rag_service = RAGService()
    app.state.embedding_service = EmbeddingService()
    app.state.guardrails_service = GuardrailsService()
    
    yield
    
    # Cleanup
    app.state.redis_client.close()

app = FastAPI(
    title="RAG Commercial Analytics API",
    description="API Gateway for RAG-powered commercial analytics system",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RAG Commercial Analytics API"}

@app.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    rag_service: RAGService = Depends(lambda: app.state.rag_service),
    guardrails_service: GuardrailsService = Depends(lambda: app.state.guardrails_service)
):
    try:
        # Apply input guardrails
        sanitized_query = await guardrails_service.sanitize_input(request.query)
        
        # Check query relevance
        is_relevant = await guardrails_service.check_relevance(sanitized_query)
        if not is_relevant:
            raise HTTPException(status_code=400, detail="Query not relevant to commercial analytics")
        
        # Process RAG query
        response = await rag_service.process_query(sanitized_query)
        
        # Apply output guardrails
        validated_response = await guardrails_service.validate_output(response)
        
        return QueryResponse(
            query=sanitized_query,
            response=validated_response,
            sources=response.get("sources", []),
            confidence=response.get("confidence", 0.0)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/ingest")
async def ingest_documents(
    request: DocumentRequest,
    rag_service: RAGService = Depends(lambda: app.state.rag_service)
):
    try:
        result = await rag_service.ingest_documents(request.documents)
        return {"status": "success", "processed": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
async def get_metrics():
    redis_client = app.state.redis_client
    
    try:
        total_queries = redis_client.get("total_queries") or 0
        successful_queries = redis_client.get("successful_queries") or 0
        
        return {
            "total_queries": int(total_queries),
            "successful_queries": int(successful_queries),
            "success_rate": float(successful_queries) / max(int(total_queries), 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)