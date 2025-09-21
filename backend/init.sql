-- I PROACTIVE BRICK Orchestration Intelligence Database Initialization

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create database user for application
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'brick_app') THEN
        CREATE ROLE brick_app WITH LOGIN PASSWORD 'brick_app_password';
    END IF;
END
$$;

-- Grant permissions
GRANT CONNECT ON DATABASE brick_orchestration TO brick_app;
GRANT USAGE ON SCHEMA public TO brick_app;
GRANT CREATE ON SCHEMA public TO brick_app;

-- Indexes will be created after tables are created by the application
-- CREATE INDEX IF NOT EXISTS idx_orchestration_sessions_status ON orchestration_sessions(status);
-- CREATE INDEX IF NOT EXISTS idx_orchestration_sessions_created_at ON orchestration_sessions(created_at);
-- CREATE INDEX IF NOT EXISTS idx_orchestration_tasks_session_id ON orchestration_tasks(session_id);
-- CREATE INDEX IF NOT EXISTS idx_ai_collaborations_session_id ON ai_collaborations(session_id);
-- CREATE INDEX IF NOT EXISTS idx_ai_collaborations_timestamp ON ai_collaborations(timestamp);
-- CREATE INDEX IF NOT EXISTS idx_performance_metrics_system_name ON performance_metrics(system_name);
-- CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(timestamp);
-- CREATE INDEX IF NOT EXISTS idx_revenue_opportunities_status ON revenue_opportunities(status);

-- Initial data will be inserted after tables are created by the application
-- INSERT INTO system_health (system_name, status, response_time, error_rate, last_successful_call, timestamp)
-- VALUES 
--     ('crewai', 'healthy', 0.5, 0.0, NOW(), NOW()),
--     ('mem0', 'healthy', 0.3, 0.0, NOW(), NOW()),
--     ('orchestrator', 'healthy', 0.2, 0.0, NOW(), NOW()),
--     ('database', 'healthy', 0.1, 0.0, NOW(), NOW())
-- ON CONFLICT DO NOTHING;

-- INSERT INTO strategic_analyses (analysis_type, title, content, recommendations, priority_score, revenue_impact, status)
-- VALUES 
--     ('bricks_roadmap', 'Q1 2024 Strategic Analysis', 
--      'Comprehensive analysis of BRICKS development roadmap for Q1 2024, identifying key opportunities and strategic priorities.',
--      '["Implement Church Kit Generator integration", "Enhance Global Sky AI capabilities", "Develop Treasury optimization system"]',
--      85, 50000, 'draft')
-- ON CONFLICT DO NOTHING;

-- INSERT INTO revenue_opportunities (opportunity_name, description, estimated_revenue, confidence_score, brick_related, status)
-- VALUES 
--     ('Church Kit Generator Integration', 'Automated legal formation services with AI-powered document generation', 15000.00, 0.85, 'Legal Automation BRICK', 'identified'),
--     ('Global Sky AI Performance Enhancement', 'Advanced business optimization algorithms for enterprise clients', 8500.00, 0.75, 'AI Optimization BRICK', 'identified'),
--     ('Treasury Management System', 'Automated yield optimization and risk management platform', 12000.00, 0.90, 'Financial Intelligence BRICK', 'identified')
-- ON CONFLICT DO NOTHING;

-- Materialized view and functions will be created after tables are created by the application
-- CREATE MATERIALIZED VIEW IF NOT EXISTS dashboard_metrics AS
-- SELECT 
--     DATE_TRUNC('hour', created_at) as hour,
--     COUNT(*) as sessions_count,
--     COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_sessions,
--     COUNT(CASE WHEN status = 'active' THEN 1 END) as active_sessions,
--     AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) as avg_duration_seconds
-- FROM orchestration_sessions
-- WHERE created_at >= NOW() - INTERVAL '24 hours'
-- GROUP BY DATE_TRUNC('hour', created_at)
-- ORDER BY hour DESC;

-- CREATE OR REPLACE FUNCTION refresh_dashboard_metrics()
-- RETURNS void AS $$
-- BEGIN
--     REFRESH MATERIALIZED VIEW dashboard_metrics;
-- END;
-- $$ LANGUAGE plpgsql;

-- GRANT SELECT ON dashboard_metrics TO brick_app;
-- GRANT EXECUTE ON FUNCTION refresh_dashboard_metrics() TO brick_app;
