-- Commercial Data Schema
-- RAG Commercial Analytics Database

-- Raw sales data table
CREATE TABLE IF NOT EXISTS raw_sales_data (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(50) NOT NULL,
    sales_amount DECIMAL(10,2) NOT NULL,
    date DATE NOT NULL,
    product_category VARCHAR(100),
    customer_id VARCHAR(50),
    region VARCHAR(50),
    channel VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_agent_id (agent_id),
    INDEX idx_date (date),
    INDEX idx_region (region)
);

-- Processed commercial metrics
CREATE TABLE IF NOT EXISTS commercial_metrics (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(50) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    metric_value DECIMAL(12,2) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_agent_metric (agent_id, metric_type),
    INDEX idx_period (period_start, period_end)
);

-- Document metadata for RAG
CREATE TABLE IF NOT EXISTS document_metadata (
    id SERIAL PRIMARY KEY,
    document_id VARCHAR(255) UNIQUE NOT NULL,
    source VARCHAR(255) NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    title VARCHAR(500),
    content_hash VARCHAR(64),
    indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_document_id (document_id),
    INDEX idx_source (source),
    INDEX idx_type (document_type)
);

-- Query logs for monitoring
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    response_time_ms INTEGER,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    user_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_timestamp (timestamp),
    INDEX idx_user_id (user_id),
    INDEX idx_success (success)
);

-- Agent performance tracking
CREATE TABLE IF NOT EXISTS agent_performance (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(50) NOT NULL,
    performance_date DATE NOT NULL,
    sales_total DECIMAL(10,2) DEFAULT 0,
    target_total DECIMAL(10,2) DEFAULT 0,
    quota_percentage DECIMAL(5,2) DEFAULT 0,
    commission_earned DECIMAL(10,2) DEFAULT 0,
    
    UNIQUE KEY unique_agent_date (agent_id, performance_date),
    INDEX idx_agent_id (agent_id),
    INDEX idx_performance_date (performance_date)
);

-- System metrics
CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(12,4) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_metric_name (metric_name),
    INDEX idx_recorded_at (recorded_at)
);