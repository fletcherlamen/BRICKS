import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  PlayIcon,
  StopIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  CpuChipIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const Orchestration = () => {
  const [activeTab, setActiveTab] = useState('execute');
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResults, setExecutionResults] = useState(null);
  const [formData, setFormData] = useState({
    taskType: 'strategic_analysis',
    goal: '',
    context: ''
  });

  const taskTypes = [
    { value: 'strategic_analysis', label: 'Strategic Analysis' },
    { value: 'brick_development', label: 'BRICK Development' },
    { value: 'revenue_optimization', label: 'Revenue Optimization' },
    { value: 'gap_analysis', label: 'Gap Analysis' }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.goal.trim()) {
      toast.error('Please enter a goal');
      return;
    }

    setIsExecuting(true);
    toast.loading('Executing orchestration...');

    try {
      // Mock execution - in production this would call the API
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const mockResult = {
        sessionId: `session_${Date.now()}`,
        taskType: formData.taskType,
        status: 'completed',
        results: {
          analysis: {
            crewai: 'Strategic analysis completed using CrewAI multi-agent system',
            multi_model: 'Multiple AI models provided diverse perspectives',
            historical: 'Relevant historical context retrieved from memory'
          },
          recommendations: [
            'Implement mobile application platform',
            'Focus on API marketplace development',
            'Optimize Church Kit Generator workflows'
          ],
          confidence: 0.92
        },
        timestamp: new Date().toISOString()
      };

      setExecutionResults(mockResult);
      toast.success('Orchestration completed successfully!');
    } catch (error) {
      toast.error('Orchestration failed');
      console.error('Orchestration error:', error);
    } finally {
      setIsExecuting(false);
    }
  };

  const recentSessions = [
    {
      id: 'session_001',
      goal: 'Analyze Church Kit Generator optimization',
      status: 'completed',
      timestamp: '2 minutes ago',
      duration: '2m 34s'
    },
    {
      id: 'session_002',
      goal: 'Identify revenue opportunities',
      status: 'completed',
      timestamp: '15 minutes ago',
      duration: '1m 45s'
    },
    {
      id: 'session_003',
      goal: 'Strategic gap analysis',
      status: 'running',
      timestamp: '1 hour ago',
      duration: '5m 12s'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <h1 className="text-3xl font-bold text-gray-900">AI Orchestration</h1>
        <p className="mt-2 text-gray-600">
          Coordinate multiple AI systems for strategic business intelligence
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'execute', name: 'Execute Task' },
            { id: 'sessions', name: 'Recent Sessions' },
            { id: 'status', name: 'System Status' }
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
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Execute Task Tab */}
      {activeTab === 'execute' && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="card"
          >
            <div className="card-header">
              <h3 className="text-lg font-semibold text-gray-900">Execute Orchestration</h3>
              <p className="text-sm text-gray-600">Configure and run AI orchestration tasks</p>
            </div>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="label">Task Type</label>
                <select
                  value={formData.taskType}
                  onChange={(e) => setFormData({ ...formData, taskType: e.target.value })}
                  className="input"
                >
                  {taskTypes.map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="label">Goal</label>
                <textarea
                  value={formData.goal}
                  onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
                  placeholder="Describe the goal or objective for this orchestration..."
                  className="input"
                  rows={3}
                />
              </div>

              <div>
                <label className="label">Context (Optional)</label>
                <textarea
                  value={formData.context}
                  onChange={(e) => setFormData({ ...formData, context: e.target.value })}
                  placeholder="Provide additional context or constraints..."
                  className="input"
                  rows={2}
                />
              </div>

              <button
                type="submit"
                disabled={isExecuting}
                className={`btn-primary w-full ${isExecuting ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {isExecuting ? (
                  <>
                    <div className="spinner mr-2"></div>
                    Executing...
                  </>
                ) : (
                  <>
                    <PlayIcon className="h-4 w-4 mr-2" />
                    Execute Orchestration
                  </>
                )}
              </button>
            </form>
          </motion.div>

          {/* Results Panel */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="card"
          >
            <div className="card-header">
              <h3 className="text-lg font-semibold text-gray-900">Execution Results</h3>
            </div>
            
            {executionResults ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-600">Session ID:</span>
                  <span className="text-sm text-gray-900 font-mono">{executionResults.sessionId}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-600">Status:</span>
                  <span className="status-healthy">Completed</span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-600">Confidence:</span>
                  <span className="text-sm text-gray-900">{(executionResults.results.confidence * 100).toFixed(1)}%</span>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Recommendations:</h4>
                  <ul className="space-y-1">
                    {executionResults.results.recommendations.map((rec, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <CpuChipIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No execution results yet</p>
                <p className="text-sm text-gray-400">Run an orchestration task to see results here</p>
              </div>
            )}
          </motion.div>
        </div>
      )}

      {/* Recent Sessions Tab */}
      {activeTab === 'sessions' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Recent Orchestration Sessions</h3>
            <p className="text-sm text-gray-600">History of AI orchestration executions</p>
          </div>
          
          <div className="overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Session ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Goal
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Duration
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Timestamp
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {recentSessions.map((session) => (
                  <tr key={session.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">
                      {session.id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {session.goal}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`status-indicator ${
                        session.status === 'completed' ? 'status-healthy' :
                        session.status === 'running' ? 'status-warning' :
                        'status-danger'
                      }`}>
                        {session.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {session.duration}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {session.timestamp}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}

      {/* System Status Tab */}
      {activeTab === 'status' && (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="card"
          >
            <div className="card-header">
              <h3 className="text-lg font-semibold text-gray-900">AI Systems Status</h3>
            </div>
            
            <div className="space-y-4">
              {[
                { name: 'CrewAI', status: 'healthy', agents: 5 },
                { name: 'Mem0.ai', status: 'healthy', memories: 150 },
                { name: 'Devin AI', status: 'healthy', capabilities: 'Full' },
                { name: 'Multi-Model Router', status: 'healthy', models: 6 },
                { name: 'Copilot Studio', status: 'healthy', workflows: 3 }
              ].map((system) => (
                <div key={system.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-900">{system.name}</p>
                    <p className="text-xs text-gray-500">
                      {system.agents && `${system.agents} agents`}
                      {system.memories && `${system.memories} memories`}
                      {system.capabilities && system.capabilities}
                      {system.models && `${system.models} models`}
                      {system.workflows && `${system.workflows} workflows`}
                    </p>
                  </div>
                  <span className="status-healthy">{system.status}</span>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="card"
          >
            <div className="card-header">
              <h3 className="text-lg font-semibold text-gray-900">Performance Metrics</h3>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Average Response Time</span>
                <span className="text-sm font-medium text-gray-900">250ms</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Success Rate</span>
                <span className="text-sm font-medium text-gray-900">98.5%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Active Sessions</span>
                <span className="text-sm font-medium text-gray-900">3</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Total Executions</span>
                <span className="text-sm font-medium text-gray-900">1,247</span>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default Orchestration;
