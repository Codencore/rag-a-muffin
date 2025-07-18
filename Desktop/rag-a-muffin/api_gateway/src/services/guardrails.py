import os
import re
from openai import OpenAI
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class GuardrailsService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.commercial_terms = [
            'sales', 'revenue', 'performance', 'agent', 'target', 'quota',
            'commission', 'pipeline', 'conversion', 'roi', 'margin', 'profit'
        ]
    
    async def sanitize_input(self, query: str) -> str:
        """Sanitize user input to prevent security issues"""
        if not query:
            raise ValueError("Query cannot be empty")
        
        # Remove script tags and javascript
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', query, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        
        # Remove SQL injection patterns
        sql_patterns = [
            r'(union|select|insert|update|delete|drop|create|alter)\s+',
            r'(\'\s*or\s*\'\s*1\s*=\s*1)',
            r'(\'\s*;\s*--)',
            r'(\'\s*\|\|\s*\')'
        ]
        
        for pattern in sql_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Limit length
        if len(sanitized) > 1000:
            raise ValueError("Query too long - potential security issue")
        
        return sanitized.strip()
    
    async def check_relevance(self, query: str) -> bool:
        """Check if query is relevant to commercial analytics"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a relevance classifier for commercial queries. Reply only 'RELEVANT' or 'NOT_RELEVANT'."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                max_tokens=10,
                temperature=0.0
            )
            
            result = response.choices[0].message.content.strip()
            return result == "RELEVANT"
            
        except Exception as e:
            logger.error(f"Error checking relevance: {e}")
            # Default to True if service fails
            return True
    
    async def validate_output(self, response: Dict[str, Any]) -> str:
        """Validate LLM output for quality and safety"""
        content = response.get("response", "")
        
        if not content:
            raise ValueError("Empty response generated")
        
        # Check for "I don't know" responses
        if any(phrase in content.lower() for phrase in ["i don't have", "cannot find", "don't know"]):
            return "I don't have sufficient information in the knowledge base to answer this question accurately."
        
        # Check for commercial context
        has_commercial_context = any(
            term in content.lower() for term in self.commercial_terms
        )
        
        if not has_commercial_context and len(content) > 100:
            logger.warning("Response may lack commercial context")
        
        # Check for potential hallucinations
        if self._detect_hallucination(content):
            raise ValueError("Response validation failed - potential hallucination detected")
        
        return content
    
    def _detect_hallucination(self, content: str) -> bool:
        """Basic hallucination detection"""
        # Check for overly specific claims without source attribution
        specific_patterns = [
            r'\d{1,2}:\d{2}\s*(am|pm)',  # Specific times
            r'\d{4}-\d{2}-\d{2}',        # Specific dates
            r'exactly\s+\d+',            # Exact numbers
            r'precisely\s+\d+',          # Precise numbers
        ]
        
        for pattern in specific_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                # Check if source is mentioned nearby
                if not re.search(r'(source|according to|based on)', content, re.IGNORECASE):
                    return True
        
        return False
    
    def check_data_freshness(self, timestamp: str) -> bool:
        """Check if data is fresh enough for reliable analysis"""
        from datetime import datetime, timedelta
        
        try:
            data_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            now = datetime.now()
            
            # Data should be less than 24 hours old
            return (now - data_time) < timedelta(hours=24)
            
        except Exception:
            return False