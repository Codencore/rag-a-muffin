#!/usr/bin/env python3
"""
Database initialization script for RAG Commercial Analytics
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', 5432),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'password'),
        database=os.getenv('POSTGRES_DB', 'rag_analytics')
    )

def execute_sql_file(cursor, filepath):
    """Execute SQL file"""
    try:
        with open(filepath, 'r') as file:
            sql_content = file.read()
            cursor.execute(sql_content)
            logger.info(f"Successfully executed {filepath}")
    except Exception as e:
        logger.error(f"Error executing {filepath}: {e}")
        raise

def initialize_database():
    """Initialize database with schemas"""
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create schemas
        schema_files = [
            'schemas/commercial_data.sql',
            'schemas/n8n_schema.sql'
        ]
        
        for schema_file in schema_files:
            filepath = os.path.join(os.path.dirname(__file__), '..', schema_file)
            execute_sql_file(cursor, filepath)
        
        # Insert initial data if needed
        cursor.execute("""
            INSERT INTO system_metrics (metric_name, metric_value) 
            VALUES ('db_initialized', 1.0) 
            ON CONFLICT DO NOTHING
        """)
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        sys.exit(1)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    initialize_database()