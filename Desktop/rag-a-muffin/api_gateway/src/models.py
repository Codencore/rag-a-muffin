from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class QueryRequest(BaseModel):
    query: str = Field(..., description="The user query for commercial analytics")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the query")
    max_results: Optional[int] = Field(10, description="Maximum number of results to return")

class QueryResponse(BaseModel):
    query: str
    response: str
    sources: List[Dict[str, Any]]
    confidence: float
    timestamp: datetime = Field(default_factory=datetime.now)

class DocumentRequest(BaseModel):
    documents: List[Dict[str, Any]] = Field(..., description="List of documents to ingest")
    collection_name: Optional[str] = Field("commercial_data", description="Vector collection name")

class DocumentResponse(BaseModel):
    status: str
    processed_count: int
    errors: List[str] = Field(default_factory=list)

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime = Field(default_factory=datetime.now)

class MetricsResponse(BaseModel):
    total_queries: int
    successful_queries: int
    success_rate: float
    timestamp: datetime = Field(default_factory=datetime.now)