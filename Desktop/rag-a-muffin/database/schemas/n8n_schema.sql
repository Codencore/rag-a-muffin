-- n8n Database Schema
-- Extended schema for n8n workflow management

-- Workflow execution history
CREATE TABLE IF NOT EXISTS workflow_executions (
    id SERIAL PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL,
    workflow_name VARCHAR(255) NOT NULL,
    execution_status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    finished_at TIMESTAMP,
    execution_time_ms INTEGER,
    error_message TEXT,
    input_data JSON,
    output_data JSON,
    
    INDEX idx_workflow_id (workflow_id),
    INDEX idx_status (execution_status),
    INDEX idx_started_at (started_at)
);

-- Workflow performance metrics
CREATE TABLE IF NOT EXISTS workflow_metrics (
    id SERIAL PRIMARY KEY,
    workflow_id VARCHAR(255) NOT NULL,
    metric_date DATE NOT NULL,
    total_executions INTEGER DEFAULT 0,
    successful_executions INTEGER DEFAULT 0,
    failed_executions INTEGER DEFAULT 0,
    avg_execution_time_ms DECIMAL(10,2) DEFAULT 0,
    
    UNIQUE KEY unique_workflow_date (workflow_id, metric_date),
    INDEX idx_workflow_id (workflow_id),
    INDEX idx_metric_date (metric_date)
);

-- Agent workflow states
CREATE TABLE IF NOT EXISTS agent_states (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100) NOT NULL,
    workflow_id VARCHAR(255) NOT NULL,
    state_data JSON NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_agent_workflow (agent_id, workflow_id),
    INDEX idx_agent_id (agent_id),
    INDEX idx_workflow_id (workflow_id)
);

-- Data quality checks
CREATE TABLE IF NOT EXISTS data_quality_checks (
    id SERIAL PRIMARY KEY,
    check_name VARCHAR(100) NOT NULL,
    check_type VARCHAR(50) NOT NULL,
    data_source VARCHAR(100) NOT NULL,
    check_result BOOLEAN NOT NULL,
    check_details JSON,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_check_name (check_name),
    INDEX idx_data_source (data_source),
    INDEX idx_checked_at (checked_at)
);