-- I PROACTIVE BRICK Orchestration Intelligence Database Initialization
-- PostgreSQL database setup script

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database if not exists (handled by Docker)
-- CREATE DATABASE brick_orchestration;

-- Set timezone
SET timezone = 'UTC';

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    full_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create orchestration sessions table
CREATE TABLE IF NOT EXISTS orchestration_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'active',
    goal TEXT,
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Create orchestration tasks table
CREATE TABLE IF NOT EXISTS orchestration_tasks (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(100) UNIQUE NOT NULL,
    session_id INTEGER REFERENCES orchestration_sessions(id),
    ai_system VARCHAR(50) NOT NULL,
    task_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    execution_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Create task logs table
CREATE TABLE IF NOT EXISTS task_logs (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES orchestration_tasks(id),
    log_level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create AI interactions table
CREATE TABLE IF NOT EXISTS ai_interactions (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES orchestration_sessions(id),
    from_ai_system VARCHAR(50) NOT NULL,
    to_ai_system VARCHAR(50) NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create memories table
CREATE TABLE IF NOT EXISTS memories (
    id SERIAL PRIMARY KEY,
    memory_id VARCHAR(100) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    memory_type VARCHAR(50) NOT NULL,
    importance_score FLOAT DEFAULT 0.5,
    tags JSONB,
    source_system VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_accessed TIMESTAMP WITH TIME ZONE,
    access_count INTEGER DEFAULT 0
);

-- Create contexts table
CREATE TABLE IF NOT EXISTS contexts (
    id SERIAL PRIMARY KEY,
    context_id VARCHAR(100) UNIQUE NOT NULL,
    session_id VARCHAR(100),
    context_type VARCHAR(50) NOT NULL,
    content JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create knowledge graph table
CREATE TABLE IF NOT EXISTS knowledge_graph (
    id SERIAL PRIMARY KEY,
    source_entity VARCHAR(200) NOT NULL,
    relationship VARCHAR(100) NOT NULL,
    target_entity VARCHAR(200) NOT NULL,
    strength FLOAT DEFAULT 1.0,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create bricks table
CREATE TABLE IF NOT EXISTS bricks (
    id SERIAL PRIMARY KEY,
    brick_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'development',
    priority INTEGER DEFAULT 5,
    complexity INTEGER DEFAULT 5,
    estimated_development_hours INTEGER,
    actual_development_hours INTEGER,
    revenue_potential FLOAT,
    dependencies JSONB,
    capabilities JSONB,
    integration_points JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deployed_at TIMESTAMP WITH TIME ZONE
);

-- Create brick developments table
CREATE TABLE IF NOT EXISTS brick_developments (
    id SERIAL PRIMARY KEY,
    brick_id INTEGER REFERENCES bricks(id),
    development_type VARCHAR(50) NOT NULL,
    description TEXT,
    progress_percentage INTEGER DEFAULT 0,
    ai_system_used VARCHAR(50),
    output JSONB,
    time_spent_minutes INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create brick analyses table
CREATE TABLE IF NOT EXISTS brick_analyses (
    id SERIAL PRIMARY KEY,
    brick_id INTEGER REFERENCES bricks(id),
    analysis_type VARCHAR(50) NOT NULL,
    ai_system_used VARCHAR(50),
    findings TEXT,
    recommendations TEXT,
    confidence_score FLOAT,
    impact_assessment JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create revenue opportunities table
CREATE TABLE IF NOT EXISTS revenue_opportunities (
    id SERIAL PRIMARY KEY,
    opportunity_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    estimated_revenue FLOAT,
    confidence_level FLOAT,
    effort_required VARCHAR(50),
    time_to_implement INTEGER,
    related_bricks JSONB,
    ai_system_identified VARCHAR(50),
    status VARCHAR(50) DEFAULT 'identified',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create strategic gaps table
CREATE TABLE IF NOT EXISTS strategic_gaps (
    id SERIAL PRIMARY KEY,
    gap_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    gap_type VARCHAR(100),
    severity VARCHAR(20),
    impact_assessment JSONB,
    suggested_solutions JSONB,
    ai_system_identified VARCHAR(50),
    status VARCHAR(50) DEFAULT 'identified',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_orchestration_sessions_session_id ON orchestration_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_orchestration_sessions_user_id ON orchestration_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_orchestration_sessions_status ON orchestration_sessions(status);
CREATE INDEX IF NOT EXISTS idx_orchestration_sessions_created_at ON orchestration_sessions(created_at);

CREATE INDEX IF NOT EXISTS idx_orchestration_tasks_session_id ON orchestration_tasks(session_id);
CREATE INDEX IF NOT EXISTS idx_orchestration_tasks_ai_system ON orchestration_tasks(ai_system);
CREATE INDEX IF NOT EXISTS idx_orchestration_tasks_status ON orchestration_tasks(status);
CREATE INDEX IF NOT EXISTS idx_orchestration_tasks_task_type ON orchestration_tasks(task_type);

CREATE INDEX IF NOT EXISTS idx_task_logs_task_id ON task_logs(task_id);
CREATE INDEX IF NOT EXISTS idx_task_logs_log_level ON task_logs(log_level);
CREATE INDEX IF NOT EXISTS idx_task_logs_timestamp ON task_logs(timestamp);

CREATE INDEX IF NOT EXISTS idx_ai_interactions_session_id ON ai_interactions(session_id);
CREATE INDEX IF NOT EXISTS idx_ai_interactions_from_system ON ai_interactions(from_ai_system);
CREATE INDEX IF NOT EXISTS idx_ai_interactions_to_system ON ai_interactions(to_ai_system);
CREATE INDEX IF NOT EXISTS idx_ai_interactions_timestamp ON ai_interactions(timestamp);

CREATE INDEX IF NOT EXISTS idx_memories_memory_id ON memories(memory_id);
CREATE INDEX IF NOT EXISTS idx_memories_memory_type ON memories(memory_type);
CREATE INDEX IF NOT EXISTS idx_memories_importance_score ON memories(importance_score);
CREATE INDEX IF NOT EXISTS idx_memories_source_system ON memories(source_system);
CREATE INDEX IF NOT EXISTS idx_memories_tags ON memories USING GIN(tags);

CREATE INDEX IF NOT EXISTS idx_contexts_context_id ON contexts(context_id);
CREATE INDEX IF NOT EXISTS idx_contexts_session_id ON contexts(session_id);
CREATE INDEX IF NOT EXISTS idx_contexts_context_type ON contexts(context_type);
CREATE INDEX IF NOT EXISTS idx_contexts_is_active ON contexts(is_active);

CREATE INDEX IF NOT EXISTS idx_knowledge_graph_source ON knowledge_graph(source_entity);
CREATE INDEX IF NOT EXISTS idx_knowledge_graph_target ON knowledge_graph(target_entity);
CREATE INDEX IF NOT EXISTS idx_knowledge_graph_relationship ON knowledge_graph(relationship);

CREATE INDEX IF NOT EXISTS idx_bricks_brick_id ON bricks(brick_id);
CREATE INDEX IF NOT EXISTS idx_bricks_category ON bricks(category);
CREATE INDEX IF NOT EXISTS idx_bricks_status ON bricks(status);
CREATE INDEX IF NOT EXISTS idx_bricks_priority ON bricks(priority);

CREATE INDEX IF NOT EXISTS idx_brick_developments_brick_id ON brick_developments(brick_id);
CREATE INDEX IF NOT EXISTS idx_brick_developments_type ON brick_developments(development_type);

CREATE INDEX IF NOT EXISTS idx_brick_analyses_brick_id ON brick_analyses(brick_id);
CREATE INDEX IF NOT EXISTS idx_brick_analyses_type ON brick_analyses(analysis_type);

CREATE INDEX IF NOT EXISTS idx_revenue_opportunities_opportunity_id ON revenue_opportunities(opportunity_id);
CREATE INDEX IF NOT EXISTS idx_revenue_opportunities_category ON revenue_opportunities(category);
CREATE INDEX IF NOT EXISTS idx_revenue_opportunities_status ON revenue_opportunities(status);

CREATE INDEX IF NOT EXISTS idx_strategic_gaps_gap_id ON strategic_gaps(gap_id);
CREATE INDEX IF NOT EXISTS idx_strategic_gaps_gap_type ON strategic_gaps(gap_type);
CREATE INDEX IF NOT EXISTS idx_strategic_gaps_severity ON strategic_gaps(severity);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orchestration_sessions_updated_at BEFORE UPDATE ON orchestration_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orchestration_tasks_updated_at BEFORE UPDATE ON orchestration_tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_memories_updated_at BEFORE UPDATE ON memories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_contexts_updated_at BEFORE UPDATE ON contexts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_knowledge_graph_updated_at BEFORE UPDATE ON knowledge_graph FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_bricks_updated_at BEFORE UPDATE ON bricks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_revenue_opportunities_updated_at BEFORE UPDATE ON revenue_opportunities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_strategic_gaps_updated_at BEFORE UPDATE ON strategic_gaps FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO users (username, email, hashed_password, is_admin, full_name) VALUES
('admin', 'admin@brickorchestration.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeXZ4Ql7X7wXK7sK2', TRUE, 'System Administrator'),
('demo_user', 'demo@brickorchestration.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeXZ4Ql7X7wXK7sK2', FALSE, 'Demo User')
ON CONFLICT (username) DO NOTHING;

INSERT INTO bricks (brick_id, name, description, category, status, priority, complexity, estimated_development_hours, revenue_potential) VALUES
('brick_001', 'Church Kit Generator API', 'Automated legal formation services for churches and religious organizations', 'automation', 'production', 8, 7, 120, 15000),
('brick_002', 'Global Sky AI Optimizer', 'Business performance optimization and analytics platform', 'analysis', 'development', 7, 8, 160, 25000),
('brick_003', 'Treasury Management System', 'Automated yield optimization and financial management', 'automation', 'testing', 6, 6, 80, 20000),
('brick_004', 'Dream Big Masks E-commerce', 'Automated e-commerce platform for custom mask sales', 'ecommerce', 'production', 5, 5, 60, 10000)
ON CONFLICT (brick_id) DO NOTHING;

INSERT INTO revenue_opportunities (opportunity_id, title, description, category, estimated_revenue, confidence_level, effort_required, time_to_implement, ai_system_identified, status) VALUES
('opp_001', 'Mobile App Development', 'Create mobile applications for all BRICK services', 'expansion', 100000, 0.85, 'high', 180, 'crewai', 'identified'),
('opp_002', 'API Marketplace', 'Create marketplace for BRICK API integrations', 'new_service', 75000, 0.92, 'medium', 120, 'multi_model_router', 'identified'),
('opp_003', 'Advanced Analytics Dashboard', 'Real-time business intelligence dashboard', 'optimization', 50000, 0.88, 'medium', 90, 'crewai', 'evaluating')
ON CONFLICT (opportunity_id) DO NOTHING;

INSERT INTO strategic_gaps (gap_id, title, description, gap_type, severity, ai_system_identified, status) VALUES
('gap_001', 'Mobile Application Platform', 'Lack of mobile applications for key services', 'capability', 'high', 'crewai', 'identified'),
('gap_002', 'Advanced Analytics Integration', 'Missing advanced analytics capabilities', 'integration', 'medium', 'multi_model_router', 'identified'),
('gap_003', 'Automated Testing Framework', 'Need comprehensive automated testing', 'development', 'medium', 'devin_ai', 'analyzing')
ON CONFLICT (gap_id) DO NOTHING;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO brick_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO brick_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO brick_user;

-- Log completion
INSERT INTO task_logs (task_id, log_level, message, metadata) VALUES
(0, 'info', 'Database initialization completed successfully', '{"script": "init.sql", "version": "1.0.0"}');
