import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  CubeIcon,
  PlusIcon,
  ChartBarIcon,
  CurrencyDollarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';

const Bricks = () => {
  const [bricks, setBricks] = useState([]);
  const [opportunities, setOpportunities] = useState([]);
  const [gaps, setGaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('bricks');

  useEffect(() => {
    fetchBrickData();
  }, []);

  const fetchBrickData = async () => {
    try {
      // Fetch real BRICK development data from orchestration sessions
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/orchestration/sessions`);
      const data = await response.json();
      
      // Process orchestration sessions to show BRICK development progress
      const brickSessions = data.sessions.filter(session => session.task_type === 'brick_development');
      
      const processedBricks = brickSessions.map((session, index) => {
        const developmentPlan = session.results?.development_plan || {};
        const generatedArtifacts = session.results?.generated_artifacts || {};
        
        return {
          id: session.run_id,
          name: developmentPlan.brick_name || `BRICK ${index + 1}`,
          description: `Generated from: ${session.goal}`,
          category: 'ai_generated',
          status: 'completed',
          priority: developmentPlan.priority === 'critical' ? 9 : developmentPlan.priority === 'high' ? 7 : 5,
          revenue_potential: developmentPlan.estimated_hours * 150, // $150/hour estimate
          complexity: Math.min(10, Math.floor(developmentPlan.estimated_hours / 20)),
          estimated_hours: developmentPlan.estimated_hours || 100,
          actual_hours: developmentPlan.estimated_hours || 100, // Completed
          generated_files: generatedArtifacts.total_files || 0,
          generated_size: generatedArtifacts.total_size_bytes || 0,
          components: developmentPlan.components || [],
          created_at: session.created_at,
          session_id: session.session_id
        };
      });
      
      // Add default BRICKS if no real sessions exist
      if (processedBricks.length === 0) {
        processedBricks.push(
          {
            id: 'brick_001',
            name: 'Church Kit Generator API',
            description: 'Automated legal formation services for churches and religious organizations',
            category: 'automation',
            status: 'production',
            priority: 8,
            revenue_potential: 15000,
            complexity: 7,
            estimated_hours: 120,
            actual_hours: 115,
            generated_files: 0,
            generated_size: 0,
            components: ['API endpoints', 'Database integration', 'Payment processing'],
            created_at: new Date().toISOString(),
            session_id: 'default'
          }
        );
      }
      
      setBricks(processedBricks);

      setOpportunities([
        {
          id: 'opp_001',
          title: 'Mobile App Development',
          description: 'Create mobile applications for all BRICK services',
          estimated_revenue: 100000,
          confidence_level: 0.85,
          effort_required: 'high',
          time_to_implement: 180
        },
        {
          id: 'opp_002',
          title: 'API Marketplace',
          description: 'Create marketplace for BRICK API integrations',
          estimated_revenue: 75000,
          confidence_level: 0.92,
          effort_required: 'medium',
          time_to_implement: 120
        }
      ]);

      setGaps([
        {
          id: 'gap_001',
          title: 'Mobile Application Platform',
          description: 'Lack of mobile applications for key services',
          gap_type: 'capability',
          severity: 'high'
        },
        {
          id: 'gap_002',
          title: 'Advanced Analytics Integration',
          description: 'Missing advanced analytics capabilities',
          gap_type: 'integration',
          severity: 'medium'
        }
      ]);

      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch BRICK data:', error);
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'production': return 'badge-success';
      case 'development': return 'badge-primary';
      case 'testing': return 'badge-warning';
      default: return 'badge-secondary';
    }
  };

  const getPriorityColor = (priority) => {
    if (priority >= 8) return 'text-red-600';
    if (priority >= 6) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high': return 'badge-danger';
      case 'medium': return 'badge-warning';
      case 'low': return 'badge-success';
      default: return 'badge-secondary';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <h1 className="text-3xl font-bold text-gray-900">BRICKS</h1>
        <p className="mt-2 text-gray-600">
          Business Resource Intelligence & Capability Kits - Strategic Business Components
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'bricks', name: 'BRICKS', count: bricks.length },
            { id: 'opportunities', name: 'Revenue Opportunities', count: opportunities.length },
            { id: 'gaps', name: 'Strategic Gaps', count: gaps.length }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.name} ({tab.count})
            </button>
          ))}
        </nav>
      </div>

      {/* BRICKS Tab */}
      {activeTab === 'bricks' && (
        <div className="space-y-6">
          {/* Add New BRICK Button */}
          <div className="flex justify-end">
            <button className="btn-primary">
              <PlusIcon className="h-4 w-4 mr-2" />
              Add New BRICK
            </button>
          </div>

          {/* BRICKS Grid */}
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-3">
            {bricks.map((brick, index) => (
              <motion.div
                key={brick.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card hover:shadow-md transition-shadow cursor-pointer"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center">
                    <div className="p-2 bg-primary-100 rounded-lg">
                      <CubeIcon className="h-6 w-6 text-primary-600" />
                    </div>
                    <div className="ml-3">
                      <h3 className="text-lg font-semibold text-gray-900">{brick.name}</h3>
                      <span className={`badge ${getStatusColor(brick.status)}`}>
                        {brick.status}
                      </span>
                    </div>
                  </div>
                  <span className={`text-sm font-medium ${getPriorityColor(brick.priority)}`}>
                    Priority {brick.priority}
                  </span>
                </div>

                <p className="text-sm text-gray-600 mb-4">{brick.description}</p>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Category:</span>
                    <span className="text-gray-900 capitalize">{brick.category}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Complexity:</span>
                    <span className="text-gray-900">{brick.complexity}/10</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Revenue Potential:</span>
                    <span className="text-green-600 font-medium">${brick.revenue_potential.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Progress:</span>
                    <span className="text-gray-900">{Math.round((brick.actual_hours / brick.estimated_hours) * 100)}%</span>
                  </div>
                  {brick.generated_files > 0 && (
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Generated Files:</span>
                      <span className="text-blue-600 font-medium">{brick.generated_files} files ({(brick.generated_size / 1024).toFixed(1)}KB)</span>
                    </div>
                  )}
                </div>

                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-primary-600 h-2 rounded-full"
                    style={{ width: `${Math.round((brick.actual_hours / brick.estimated_hours) * 100)}%` }}
                  ></div>
                </div>
                
                {brick.generated_files > 0 && (
                  <div className="mt-3">
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-500">Generated Code Artifacts:</span>
                      <span className="text-xs text-blue-600">Ready for deployment</span>
                    </div>
                    <div className="mt-1 text-xs text-gray-600">
                      Python code, Docker config, JSON config, Requirements file
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Revenue Opportunities Tab */}
      {activeTab === 'opportunities' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {opportunities.map((opportunity, index) => (
              <motion.div
                key={opportunity.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center">
                    <div className="p-2 bg-green-100 rounded-lg">
                      <CurrencyDollarIcon className="h-6 w-6 text-green-600" />
                    </div>
                    <div className="ml-3">
                      <h3 className="text-lg font-semibold text-gray-900">{opportunity.title}</h3>
                      <span className={`badge ${
                        opportunity.effort_required === 'high' ? 'badge-danger' :
                        opportunity.effort_required === 'medium' ? 'badge-warning' :
                        'badge-success'
                      }`}>
                        {opportunity.effort_required} effort
                      </span>
                    </div>
                  </div>
                  <span className="text-2xl font-bold text-green-600">
                    ${opportunity.estimated_revenue.toLocaleString()}
                  </span>
                </div>

                <p className="text-sm text-gray-600 mb-4">{opportunity.description}</p>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Confidence Level:</span>
                    <span className="text-gray-900">{(opportunity.confidence_level * 100).toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Time to Implement:</span>
                    <span className="text-gray-900">{opportunity.time_to_implement} days</span>
                  </div>
                </div>

                <div className="flex space-x-2">
                  <button className="btn-primary flex-1">
                    <CheckCircleIcon className="h-4 w-4 mr-2" />
                    Implement
                  </button>
                  <button className="btn-outline">
                    Analyze
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Strategic Gaps Tab */}
      {activeTab === 'gaps' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            {gaps.map((gap, index) => (
              <motion.div
                key={gap.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center">
                    <div className="p-2 bg-yellow-100 rounded-lg">
                      <ExclamationTriangleIcon className="h-6 w-6 text-yellow-600" />
                    </div>
                    <div className="ml-3">
                      <h3 className="text-lg font-semibold text-gray-900">{gap.title}</h3>
                      <span className={`badge ${getSeverityColor(gap.severity)}`}>
                        {gap.severity} severity
                      </span>
                    </div>
                  </div>
                  <span className="text-sm text-gray-500 capitalize">{gap.gap_type}</span>
                </div>

                <p className="text-sm text-gray-600 mb-4">{gap.description}</p>

                <div className="flex space-x-2">
                  <button className="btn-primary flex-1">
                    <CubeIcon className="h-4 w-4 mr-2" />
                    Create BRICK
                  </button>
                  <button className="btn-outline">
                    Analyze Impact
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Bricks;
