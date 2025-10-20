import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  ChartBarIcon,
  LightBulbIcon,
  ExclamationTriangleIcon,
  QueueListIcon,
  ShieldCheckIcon,
  CpuChipIcon,
  ArrowTrendingUpIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const Strategic = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [strategicDashboard, setStrategicDashboard] = useState(null);
  const [ecosystem, setEcosystem] = useState(null);
  const [revenueOpportunities, setRevenueOpportunities] = useState(null);
  const [strategicGaps, setStrategicGaps] = useState(null);
  const [priorityQueue, setPriorityQueue] = useState(null);

  const tabs = [
    { id: 'dashboard', name: 'Strategic Dashboard', icon: ChartBarIcon },
    { id: 'ecosystem', name: 'BRICKS Ecosystem', icon: CpuChipIcon },
    { id: 'revenue', name: 'Revenue Opportunities', icon: ArrowTrendingUpIcon },
    { id: 'gaps', name: 'Strategic Gaps', icon: ExclamationTriangleIcon },
    { id: 'priority', name: 'Priority Queue', icon: QueueListIcon }
  ];

  useEffect(() => {
    if (activeTab === 'dashboard') {
      fetchStrategicDashboard();
    } else if (activeTab === 'ecosystem') {
      fetchEcosystem();
    } else if (activeTab === 'revenue') {
      fetchRevenueOpportunities();
    } else if (activeTab === 'gaps') {
      fetchStrategicGaps();
    } else if (activeTab === 'priority') {
      fetchPriorityQueue();
    }
  }, [activeTab]);

  const fetchStrategicDashboard = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/strategic/dashboard`);
      const data = await response.json();
      
      if (response.ok) {
        setStrategicDashboard(data);
      } else {
        toast.error('Failed to fetch strategic dashboard');
      }
    } catch (error) {
      console.error('Error fetching strategic dashboard:', error);
      toast.error('Error fetching strategic dashboard');
    } finally {
      setLoading(false);
    }
  };

  const fetchEcosystem = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/strategic/ecosystem`);
      const data = await response.json();
      
      if (response.ok) {
        setEcosystem(data);
      } else {
        toast.error('Failed to fetch BRICKS ecosystem');
      }
    } catch (error) {
      console.error('Error fetching ecosystem:', error);
      toast.error('Error fetching ecosystem');
    } finally {
      setLoading(false);
    }
  };

  const fetchRevenueOpportunities = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/strategic/revenue-opportunities`);
      const data = await response.json();
      
      if (response.ok) {
        setRevenueOpportunities(data);
      } else {
        toast.error('Failed to fetch revenue opportunities');
      }
    } catch (error) {
      console.error('Error fetching revenue opportunities:', error);
      toast.error('Error fetching revenue opportunities');
    } finally {
      setLoading(false);
    }
  };

  const fetchStrategicGaps = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/strategic/strategic-gaps`);
      const data = await response.json();
      
      if (response.ok) {
        setStrategicGaps(data);
      } else {
        toast.error('Failed to fetch strategic gaps');
      }
    } catch (error) {
      console.error('Error fetching strategic gaps:', error);
      toast.error('Error fetching strategic gaps');
    } finally {
      setLoading(false);
    }
  };

  const fetchPriorityQueue = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/strategic/priority-queue`);
      const data = await response.json();
      
      if (response.ok) {
        setPriorityQueue(data);
      } else {
        toast.error('Failed to fetch priority queue');
      }
    } catch (error) {
      console.error('Error fetching priority queue:', error);
      toast.error('Error fetching priority queue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Strategic Intelligence</h1>
        <p className="mt-2 text-gray-600">
          STRATEGIC Framework - Comprehensive strategic analysis and planning
        </p>
      </div>

      {/* Tabs */}
      <div className="mb-6 border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex items-center py-4 px-1 border-b-2 font-medium text-sm
                  ${activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <Icon className="h-5 w-5 mr-2" />
                {tab.name}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Strategic Dashboard Tab */}
      {activeTab === 'dashboard' && (
        <div className="space-y-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Loading strategic dashboard...</p>
            </div>
          ) : strategicDashboard ? (
            <>
              {/* Strategic Health Score */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="card"
              >
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-gray-900">Strategic Health Score</h3>
                </div>
                <div className="p-6">
                  <div className="flex items-center justify-center">
                    <div className="text-center">
                      <div className="text-6xl font-bold text-blue-600">
                        {strategicDashboard.strategic_health_score?.toFixed(1) || '0.0'}
                      </div>
                      <div className="mt-2 text-xl text-gray-600">
                        Status: <span className="font-semibold capitalize">{strategicDashboard.strategic_status}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Quick Stats */}
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card">
                  <div className="flex items-center">
                    <div className="p-3 rounded-lg bg-blue-500 bg-opacity-10">
                      <CpuChipIcon className="h-6 w-6 text-blue-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Total BRICKs</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {(strategicDashboard.dashboard_data?.ecosystem_overview?.total_existing_bricks || 0) +
                         (strategicDashboard.dashboard_data?.ecosystem_overview?.total_potential_bricks || 0)}
                      </p>
                    </div>
                  </div>
                </motion.div>

                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="card">
                  <div className="flex items-center">
                    <div className="p-3 rounded-lg bg-green-500 bg-opacity-10">
                      <ArrowTrendingUpIcon className="h-6 w-6 text-green-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Revenue Opportunities</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {strategicDashboard.dashboard_data?.revenue_opportunities?.total_opportunities || 0}
                      </p>
                    </div>
                  </div>
                </motion.div>

                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="card">
                  <div className="flex items-center">
                    <div className="p-3 rounded-lg bg-yellow-500 bg-opacity-10">
                      <ExclamationTriangleIcon className="h-6 w-6 text-yellow-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Strategic Gaps</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {strategicDashboard.dashboard_data?.strategic_gaps?.total_gaps || 0}
                      </p>
                    </div>
                  </div>
                </motion.div>

                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="card">
                  <div className="flex items-center">
                    <div className="p-3 rounded-lg bg-purple-500 bg-opacity-10">
                      <QueueListIcon className="h-6 w-6 text-purple-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">BRICKs in Queue</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {strategicDashboard.dashboard_data?.priority_queue?.total_bricks_analyzed || 0}
                      </p>
                    </div>
                  </div>
                </motion.div>
              </div>
            </>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No strategic dashboard data available</p>
            </div>
          )}
        </div>
      )}

      {/* BRICKS Ecosystem Tab */}
      {activeTab === 'ecosystem' && (
        <div className="space-y-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Loading BRICKS ecosystem...</p>
            </div>
          ) : ecosystem ? (
            <>
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card">
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-gray-900">Ecosystem Overview</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Existing BRICKs</p>
                    <p className="text-3xl font-bold text-blue-600">{ecosystem.total_existing_bricks || 0}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Potential BRICKs</p>
                    <p className="text-3xl font-bold text-green-600">{ecosystem.total_potential_bricks || 0}</p>
                  </div>
                  <div className="text-center">
                    <p className="text-sm text-gray-600">Monthly Revenue</p>
                    <p className="text-3xl font-bold text-purple-600">${ecosystem.total_monthly_revenue?.toLocaleString() || 0}</p>
                  </div>
                </div>
              </motion.div>

              {/* Existing BRICKs */}
              {ecosystem.ecosystem?.existing_bricks && (
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="card">
                  <div className="card-header">
                    <h3 className="text-lg font-semibold text-gray-900">Existing BRICKs</h3>
                  </div>
                  <div className="divide-y divide-gray-200">
                    {Object.entries(ecosystem.ecosystem.existing_bricks).map(([key, brick], index) => (
                      <div key={key} className="p-6">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="text-lg font-semibold text-gray-900">{brick.name}</h4>
                            <p className="mt-1 text-sm text-gray-600">Status: <span className="font-medium capitalize">{brick.status}</span></p>
                            <div className="mt-2 flex items-center space-x-4 text-sm">
                              <span className="text-gray-600">Revenue: <span className="font-semibold">${brick.monthly_revenue}/mo</span></span>
                              <span className="text-gray-600">Users: <span className="font-semibold">{brick.user_base}</span></span>
                              <span className="text-gray-600">Type: <span className="font-semibold capitalize">{brick.revenue_stream?.replace('_', ' ')}</span></span>
                            </div>
                            <div className="mt-2">
                              <p className="text-xs text-gray-500">Tech Stack: {brick.technology_stack?.join(', ')}</p>
                            </div>
                          </div>
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                            brick.expansion_potential === 'very_high' ? 'bg-green-100 text-green-800' :
                            brick.expansion_potential === 'high' ? 'bg-blue-100 text-blue-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {brick.expansion_potential?.replace('_', ' ').toUpperCase()}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )}
            </>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No ecosystem data available</p>
            </div>
          )}
        </div>
      )}

      {/* Revenue Opportunities Tab */}
      {activeTab === 'revenue' && (
        <div className="space-y-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Analyzing revenue opportunities...</p>
            </div>
          ) : revenueOpportunities ? (
            <>
              {/* Summary Card */}
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card bg-gradient-to-r from-green-50 to-blue-50">
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Revenue Opportunity Summary</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <p className="text-sm text-gray-600">Total Opportunities</p>
                      <p className="text-3xl font-bold text-blue-600">{revenueOpportunities.total_opportunities}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Total Potential Revenue</p>
                      <p className="text-3xl font-bold text-green-600">${revenueOpportunities.total_potential_revenue?.toLocaleString() || 0}/mo</p>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Opportunities List */}
              <div className="grid grid-cols-1 gap-6">
                {revenueOpportunities.opportunities?.map((opp, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="card"
                  >
                    <div className="p-6">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3">
                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                              index === 0 ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'
                            }`}>
                              {index === 0 ? 'TOP OPPORTUNITY' : `#${index + 1}`}
                            </span>
                            <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 capitalize">
                              {opp.type?.replace('_', ' ')}
                            </span>
                          </div>
                          <h4 className="mt-3 text-lg font-semibold text-gray-900">{opp.name}</h4>
                          <p className="mt-2 text-sm text-gray-600">{opp.description}</p>
                          
                          <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div>
                              <p className="text-xs text-gray-500">Potential Revenue</p>
                              <p className="text-lg font-semibold text-green-600">${opp.potential_revenue?.toLocaleString() || 0}/mo</p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-500">Probability</p>
                              <p className="text-lg font-semibold text-blue-600">{(opp.probability * 100).toFixed(0)}%</p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-500">Effort Level</p>
                              <p className="text-lg font-semibold text-gray-700 capitalize">{opp.effort_level}</p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-500">Timeline</p>
                              <p className="text-lg font-semibold text-purple-600">{opp.time_to_revenue}</p>
                            </div>
                          </div>

                          {/* Action Items */}
                          <div className="mt-4">
                            <p className="text-sm font-medium text-gray-700 mb-2">Action Items:</p>
                            <ul className="space-y-1">
                              {opp.action_items?.map((action, idx) => (
                                <li key={idx} className="flex items-start text-sm text-gray-600">
                                  <CheckCircleIcon className="h-4 w-4 mt-0.5 mr-2 text-green-500" />
                                  {action}
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No revenue opportunities data available</p>
            </div>
          )}
        </div>
      )}

      {/* Strategic Gaps Tab */}
      {activeTab === 'gaps' && (
        <div className="space-y-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Detecting strategic gaps...</p>
            </div>
          ) : strategicGaps ? (
            <>
              {/* Gap Summary */}
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card">
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-gray-900">Gap Analysis Summary</h3>
                </div>
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                      <p className="text-sm text-gray-600">Total Gaps Detected</p>
                      <p className="text-3xl font-bold text-gray-900">{strategicGaps.total_gaps}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">High Priority</p>
                      <p className="text-3xl font-bold text-red-600">{strategicGaps.high_priority_gaps}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Gap Severity</p>
                      <p className={`text-3xl font-bold capitalize ${
                        strategicGaps.gap_severity === 'critical' ? 'text-red-600' :
                        strategicGaps.gap_severity === 'high' ? 'text-orange-600' :
                        strategicGaps.gap_severity === 'medium' ? 'text-yellow-600' :
                        'text-green-600'
                      }`}>
                        {strategicGaps.gap_severity}
                      </p>
                    </div>
                  </div>

                  {/* Recommendations */}
                  <div className="mt-6">
                    <h4 className="text-md font-semibold text-gray-900 mb-3">Strategic Recommendations</h4>
                    <ul className="space-y-2">
                      {strategicGaps.strategic_recommendations?.map((rec, idx) => (
                        <li key={idx} className="flex items-start text-sm text-gray-700">
                          <LightBulbIcon className="h-5 w-5 mt-0.5 mr-2 text-yellow-500" />
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </motion.div>

              {/* Gap Categories */}
              {Object.entries(strategicGaps.detected_gaps || {}).map(([category, gaps], catIndex) => (
                gaps.length > 0 && (
                  <motion.div
                    key={category}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: catIndex * 0.1 }}
                    className="card"
                  >
                    <div className="card-header">
                      <h3 className="text-lg font-semibold text-gray-900 capitalize">
                        {category.replace('_', ' ')} ({gaps.length})
                      </h3>
                    </div>
                    <div className="divide-y divide-gray-200">
                      {gaps.map((gap, gapIndex) => (
                        <div key={gapIndex} className="p-4">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h5 className="font-medium text-gray-900">
                                {gap.gap_name || gap.gap_type || gap.market_segment || gap.gap || 'Gap'}
                              </h5>
                              <p className="mt-1 text-sm text-gray-600">
                                {gap.description || gap.reason || 'Strategic gap identified'}
                              </p>
                              {gap.missing_capabilities && (
                                <div className="mt-2">
                                  <p className="text-xs text-gray-500">Missing: {gap.missing_capabilities.join(', ')}</p>
                                </div>
                              )}
                            </div>
                            <span className={`ml-4 px-3 py-1 rounded-full text-xs font-medium ${
                              gap.priority === 'high' ? 'bg-red-100 text-red-800' :
                              gap.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {gap.priority?.toUpperCase() || gap.importance?.toUpperCase() || 'MEDIUM'}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )
              ))}
            </>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No strategic gaps data available</p>
            </div>
          )}
        </div>
      )}

      {/* Priority Queue Tab */}
      {activeTab === 'priority' && (
        <div className="space-y-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Generating priority queue...</p>
            </div>
          ) : priorityQueue ? (
            <>
              {/* Next BRICK Recommendation */}
              {priorityQueue.next_brick_recommendation && (
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200">
                  <div className="p-6">
                    <div className="flex items-center mb-4">
                      <div className="p-2 bg-blue-500 rounded-lg">
                        <QueueListIcon className="h-6 w-6 text-white" />
                      </div>
                      <h3 className="ml-3 text-xl font-bold text-gray-900">Next BRICK Recommendation</h3>
                    </div>
                    <h4 className="text-2xl font-bold text-blue-600 mb-2">
                      {priorityQueue.next_brick_recommendation.brick_data?.name}
                    </h4>
                    <p className="text-gray-700 mb-4">{priorityQueue.next_brick_recommendation.recommendation}</p>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div>
                        <p className="text-xs text-gray-600">Priority Score</p>
                        <p className="text-xl font-bold text-blue-600">{priorityQueue.next_brick_recommendation.priority_score?.toFixed(1)}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Priority Level</p>
                        <p className="text-xl font-bold text-red-600 capitalize">{priorityQueue.next_brick_recommendation.priority_level}</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Timeline</p>
                        <p className="text-xl font-bold text-purple-600">{priorityQueue.next_brick_recommendation.estimated_timeline?.weeks} weeks</p>
                      </div>
                      <div>
                        <p className="text-xs text-gray-600">Dependencies</p>
                        <p className="text-xl font-bold text-green-600">{priorityQueue.next_brick_recommendation.dependencies_met ? 'Met' : 'Pending'}</p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Full Priority Queue */}
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="card">
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-gray-900">BRICK Development Priority Queue</h3>
                </div>
                <div className="divide-y divide-gray-200">
                  {priorityQueue.priority_queue?.map((brick, index) => (
                    <div key={index} className="p-4 hover:bg-gray-50">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-4 flex-1">
                          <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center font-bold ${
                            index === 0 ? 'bg-yellow-400 text-white' :
                            index === 1 ? 'bg-gray-300 text-gray-700' :
                            index === 2 ? 'bg-orange-300 text-gray-700' :
                            'bg-gray-200 text-gray-600'
                          }`}>
                            {index + 1}
                          </div>
                          <div className="flex-1">
                            <h5 className="font-semibold text-gray-900">{brick.brick_data?.name || brick.brick_name}</h5>
                            <p className="mt-1 text-sm text-gray-600">{brick.brick_data?.value_proposition}</p>
                            <div className="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                              <span>Score: <span className="font-semibold">{brick.priority_score?.toFixed(1)}</span></span>
                              <span>Timeline: <span className="font-semibold">{brick.estimated_timeline?.weeks} weeks</span></span>
                              <span>Complexity: <span className="font-semibold capitalize">{brick.estimated_timeline?.complexity}</span></span>
                            </div>
                          </div>
                        </div>
                        <span className={`ml-4 px-3 py-1 rounded-full text-xs font-medium ${
                          brick.priority_level === 'critical' ? 'bg-red-100 text-red-800' :
                          brick.priority_level === 'high' ? 'bg-orange-100 text-orange-800' :
                          brick.priority_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {brick.priority_level?.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            </>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No priority queue data available</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Strategic;
