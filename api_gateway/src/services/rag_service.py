import os
import httpx
import chromadb
from typing import List, Dict, Any, Optional
from openai import OpenAI
import json
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chromadb_client = chromadb.HttpClient(host="chromadb", port=8000)
        self.collection = self.chromadb_client.get_or_create_collection("commercial_data")
        
    async def process_query(self, query: str) -> Dict[str, Any]:
        try:
            # Perform vector search
            results = self.collection.query(
                query_texts=[query],
                n_results=10,
                include=["documents", "metadatas", "distances"]
            )
            
            # Assemble context
            context = self._assemble_context(results)
            
            # Generate response with LLM
            response = await self._generate_response(query, context)
            
            return {
                "response": response,
                "sources": context,
                "confidence": self._calculate_confidence(results["distances"][0])
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise
    
    def _assemble_context(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        
        context = []
        for i, doc in enumerate(documents):
            if i < len(distances) and distances[i] < 0.3:  # Relevance threshold
                context.append({
                    "content": doc,
                    "source": metadatas[i].get("source", "unknown") if i < len(metadatas) else "unknown",
                    "relevance_score": 1 - distances[i]
                })
        
        return context
    
    async def _generate_response(self, query: str, context: List[Dict[str, Any]]) -> str:
        context_text = "\n".join([f"Source: {ctx['source']}\nContent: {ctx['content']}" for ctx in context])
        
        messages = [
            {
                "role": "system",
                "content": "You are a commercial analytics expert. Use only the provided context to answer questions about sales performance. If the context doesn't contain relevant information, clearly state that."
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {query}"
            }
        ]
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            max_tokens=1500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def _calculate_confidence(self, distances: List[float]) -> float:
        if not distances:
            return 0.0
        
        # Calculate confidence based on distance scores
        relevant_distances = [d for d in distances if d < 0.3]
        if not relevant_distances:
            return 0.0
        
        avg_distance = sum(relevant_distances) / len(relevant_distances)
        confidence = 1 - avg_distance
        return max(0.0, min(1.0, confidence))
    
    async def ingest_documents(self, documents: List[Dict[str, Any]]) -> int:
        try:
            processed_count = 0
            
            for doc in documents:
                # Extract text content
                content = doc.get("content", "")
                if not content:
                    continue
                
                # Generate embedding and store
                self.collection.add(
                    documents=[content],
                    metadatas=[{
                        "source": doc.get("source", "unknown"),
                        "date": doc.get("date", ""),
                        "type": doc.get("type", "document")
                    }],
                    ids=[doc.get("id", f"doc_{processed_count}")]
                )
                
                processed_count += 1
            
            return processed_count
            
        except Exception as e:
            logger.error(f"Error ingesting documents: {e}")
            raise