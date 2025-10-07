import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  BanknotesIcon,
  RocketLaunchIcon,
  ChartBarIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
  CurrencyDollarIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

const Revenue = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);
  const [revenueConnections, setRevenueConnections] = useState(null);
  const [churchKitMetrics, setChurchKitMetrics] = useState(null);
  const [globalSkyCapabilities, setGlobalSkyCapabilities] = useState(null);
  const [financialHealth, setFinancialHealth] = useState(null);
  const [proposals, setProposals] = useState(null);
  const [generatingProposal, setGeneratingProposal] = useState(false);

  const tabs = [
    { id: 'overview', name: 'Revenue Overview', icon: ChartBarIcon },
    { id: 'church-kit', name: 'Church Kit Generator', icon: BanknotesIcon },
    { id: 'global-sky', name: 'Global Sky AI', icon: RocketLaunchIcon },
    { id: 'treasury', name: 'Treasury Optimization', icon: CurrencyDollarIcon },
    { id: 'proposals', name: 'BRICK Proposals', icon: ArrowTrendingUpIcon }
  ];

  useEffect(() => {
    if (activeTab === 'overview') {
      fetchRevenueConnections();
    } else if (activeTab === 'church-kit') {
      fetchChurchKitMetrics();
    } else if (activeTab === 'global-sky') {
      fetchGlobalSkyCapabilities();
    } else if (activeTab === 'treasury') {
      fetchFinancialHealth();
    } else if (activeTab === 'proposals') {
      fetchProposals();
    }
  }, [activeTab]);

  const fetchRevenueConnections = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/revenue/revenue-connections`);
      const data = await response.json();
      
      if (response.ok) {
        setRevenueConnections(data);
      } else {
        toast.error('Failed to fetch revenue connections');
      }
    } catch (error) {
      console.error('Error fetching revenue connections:', error);
      toast.error('Error fetching revenue connections');
    } finally {
      setLoading(false);
    }
  };

  const fetchChurchKitMetrics = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/revenue/church-kit/metrics`);
      const data = await response.json();
      
      if (response.ok) {
        setChurchKitMetrics(data);
      } else {
        toast.error('Failed to fetch Church Kit metrics');
      }
    } catch (error) {
      console.error('Error fetching Church Kit metrics:', error);
      toast.error('Error fetching Church Kit metrics');
    } finally {
      setLoading(false);
    }
  };

  const fetchGlobalSkyCapabilities = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/revenue/global-sky/capabilities`);
      const data = await response.json();
      
      if (response.ok) {
        setGlobalSkyCapabilities(data);
      } else {
        toast.error('Failed to fetch Global Sky capabilities');
      }
    } catch (error) {
      console.error('Error fetching Global Sky capabilities:', error);
      toast.error('Error fetching Global Sky capabilities');
    } finally {
      setLoading(false);
    }
  };

  const fetchFinancialHealth = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/revenue/treasury/financial-health`);
      const data = await response.json();
      
      if (response.ok) {
        setFinancialHealth(data);
      } else {
        toast.error('Failed to fetch financial health');
      }
    } catch (error) {
      console.error('Error fetching financial health:', error);
      toast.error('Error fetching financial health');
    } finally {
      setLoading(false);
    }
  };

  const fetchProposals = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/revenue/proposals`);
      const data = await response.json();
      
      if (response.ok) {
        setProposals(data);
      } else {
        toast.error('Failed to fetch proposals');
      }
    } catch (error) {
      console.error('Error fetching proposals:', error);
      toast.error('Error fetching proposals');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateProposal = async () => {
    setGeneratingProposal(true);
    toast.loading('Generating autonomous BRICK proposal...');
    
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/revenue/proposals/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      
      const data = await response.json();
      
      if (response.ok) {
        toast.dismiss();
        toast.success('BRICK proposal generated successfully!');
        fetchProposals();
      } else {
        toast.error('Failed to generate proposal');
      }
    } catch (error) {
      console.error('Error generating proposal:', error);
      toast.error('Error generating proposal');
    } finally {
      setGeneratingProposal(false);
    }
  };

  const handleApproveProposal = async (proposalId, approved) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/revenue/proposals/${proposalId}/approve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ approved, feedback: approved ? 'Approved for development' : 'Rejected' })
      });
      
      const data = await response.json();
      
      if (response.ok) {
        toast.success(approved ? 'Proposal approved!' : 'Proposal rejected');
        fetchProposals();
      } else {
        toast.error('Failed to process approval');
      }
    } catch (error) {
      console.error('Error processing approval:', error);
      toast.error('Error processing approval');
    }
  };

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Revenue Integration Loop</h1>
        <p className="mt-2 text-gray-600">
          Revenue-connected BRICK development with autonomous proposals
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

      {/* Revenue Overview Tab */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {loading ? (
            <div className="text-center py-12">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Loading revenue connections...</p>
            </div>
          ) : revenueConnections ? (
            <>
              {/* Summary Cards */}
              <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card">
                  <div className="flex items-center">
                    <div className="p-3 rounded-lg bg-green-500 bg-opacity-10">
                      <BanknotesIcon className="h-6 w-6 text-green-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Total Revenue Tracked</p>
                      <p className="text-2xl font-bold text-gray-900">${revenueConnections.total_revenue_tracked?.toLocaleString()}/mo</p>
                    </div>
                  </div>
                </motion.div>

                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="card">
                  <div className="flex items-center">
                    <div className="p-3 rounded-lg bg-blue-500 bg-opacity-10">
                      <RocketLaunchIcon className="h-6 w-6 text-blue-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Connected BRICKs</p>
                      <p className="text-2xl font-bold text-gray-900">{revenueConnections.total_connected_bricks}</p>
                    </div>
                  </div>
                </motion.div>

                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="card">
                  <div className="flex items-center">
                    <div className="p-3 rounded-lg bg-purple-500 bg-opacity-10">
                      <CheckCircleIcon className="h-6 w-6 text-purple-500" />
                    </div>
                    <div className="ml-4">
                      <p className="text-sm font-medium text-gray-600">Integration Health</p>
                      <p className="text-2xl font-bold text-gray-900 capitalize">{revenueConnections.integration_health}</p>
                    </div>
                  </div>
                </motion.div>
              </div>

              {/* Connected BRICKs */}
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="card">
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-gray-900">Revenue-Connected BRICKs</h3>
                </div>
                <div className="divide-y divide-gray-200">
                  {Object.entries(revenueConnections.connections || {}).map(([brickName, connection], index) => (
                    <div key={brickName} className="p-6">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <h4 className="text-lg font-semibold text-gray-900 capitalize">
                            {brickName.replace(/_/g, ' ')}
                          </h4>
                          <div className="mt-2 grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div>
                              <p className="text-xs text-gray-500">Connection</p>
                              <p className={`text-sm font-semibold ${connection.connected ? 'text-green-600' : 'text-red-600'}`}>
                                {connection.connected ? 'Connected' : 'Disconnected'}
                              </p>
                            </div>
                            {connection.monthly_revenue !== undefined && (
                              <div>
                                <p className="text-xs text-gray-500">Monthly Revenue</p>
                                <p className="text-sm font-semibold text-gray-900">${connection.monthly_revenue?.toLocaleString()}</p>
                              </div>
                            )}
                            <div>
                              <p className="text-xs text-gray-500">Integration Health</p>
                              <p className="text-sm font-semibold text-blue-600 capitalize">{connection.integration_health}</p>
                            </div>
                            <div>
                              <p className="text-xs text-gray-500">Tracking</p>
                              <p className="text-sm font-semibold text-purple-600">
                                {connection.revenue_tracking || connection.financial_tracking ? 'Active' : 'Inactive'}
                              </p>
                            </div>
                          </div>
                        </div>
                        <span className={`ml-4 px-3 py-1 rounded-full text-xs font-medium ${
                          connection.connected ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          {connection.connected ? 'ACTIVE' : 'PENDING'}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </motion.div>
            </>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">No revenue connection data available</p>
            </div>
          )}
        </div>
      )}

      {/* BRICK Proposals Tab */}
      {activeTab === 'proposals' && (
        <div className="space-y-6">
          {/* Generate Proposal Button */}
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card bg-gradient-to-r from-blue-50 to-purple-50">
            <div className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">Autonomous BRICK Proposals</h3>
                  <p className="mt-1 text-sm text-gray-600">
                    AI-generated development proposals connected to revenue impact
                  </p>
                </div>
                <button
                  onClick={handleGenerateProposal}
                  disabled={generatingProposal}
                  className={`btn btn-primary flex items-center ${generatingProposal ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  <RocketLaunchIcon className="h-5 w-5 mr-2" />
                  {generatingProposal ? 'Generating...' : 'Generate Proposal'}
                </button>
              </div>
            </div>
          </motion.div>

          {/* Proposals List */}
          {loading ? (
            <div className="text-center py-12">
              <div className="spinner mx-auto mb-4"></div>
              <p className="text-gray-600">Loading proposals...</p>
            </div>
          ) : proposals && proposals.proposals ? (
            <div className="space-y-6">
              {proposals.proposals.length === 0 ? (
                <div className="text-center py-12 card">
                  <RocketLaunchIcon className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                  <p className="text-gray-500">No proposals yet. Click "Generate Proposal" to create one!</p>
                </div>
              ) : (
                proposals.proposals.map((proposal, index) => (
                  <motion.div
                    key={proposal.proposal_id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="card"
                  >
                    <div className="p-6">
                      {/* Proposal Header */}
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h3 className="text-xl font-bold text-gray-900">{proposal.brick_design?.brick_name}</h3>
                            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                              proposal.status === 'pending_approval' ? 'bg-yellow-100 text-yellow-800' :
                              proposal.status === 'approved' ? 'bg-green-100 text-green-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {proposal.status?.replace('_', ' ').toUpperCase()}
                            </span>
                            <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              Confidence: {(proposal.confidence_score * 100).toFixed(0)}%
                            </span>
                          </div>
                          <p className="text-sm text-gray-600">{proposal.brick_design?.description}</p>
                        </div>
                      </div>

                      {/* Revenue Impact */}
                      <div className="bg-green-50 rounded-lg p-4 mb-4">
                        <h4 className="text-sm font-semibold text-gray-900 mb-2">Revenue Impact</h4>
                        <div className="grid grid-cols-3 gap-4">
                          <div>
                            <p className="text-xs text-gray-600">Monthly Revenue</p>
                            <p className="text-lg font-bold text-green-600">
                              ${proposal.revenue_impact?.total_revenue_impact?.toLocaleString() || 0}
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-600">ROI (12 months)</p>
                            <p className="text-lg font-bold text-blue-600">
                              {proposal.revenue_impact?.roi_12_months?.toFixed(1)}x
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-600">Payback Period</p>
                            <p className="text-lg font-bold text-purple-600">
                              {proposal.revenue_impact?.payback_period_months} months
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* Feasibility */}
                      <div className="bg-blue-50 rounded-lg p-4 mb-4">
                        <h4 className="text-sm font-semibold text-gray-900 mb-2">Feasibility Assessment</h4>
                        <div className="grid grid-cols-3 gap-4">
                          <div>
                            <p className="text-xs text-gray-600">Overall Score</p>
                            <p className="text-lg font-bold text-blue-600">
                              {(proposal.feasibility_assessment?.overall_feasibility?.score * 100).toFixed(0)}%
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-600">Rating</p>
                            <p className="text-lg font-bold text-gray-900 capitalize">
                              {proposal.feasibility_assessment?.overall_feasibility?.rating?.replace('_', ' ')}
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-600">Recommendation</p>
                            <p className="text-lg font-bold text-green-600">
                              {proposal.feasibility_assessment?.overall_feasibility?.recommendation}
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* Implementation Plan */}
                      <div className="mb-4">
                        <h4 className="text-sm font-semibold text-gray-900 mb-2">Implementation Plan</h4>
                        <div className="grid grid-cols-3 gap-4 text-sm">
                          <div>
                            <p className="text-xs text-gray-500">Timeline</p>
                            <p className="font-semibold text-gray-900">
                              {proposal.implementation_plan?.total_timeline_weeks} weeks
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500">Total Cost</p>
                            <p className="font-semibold text-gray-900">
                              ${proposal.implementation_plan?.total_cost?.toLocaleString()}
                            </p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500">Phases</p>
                            <p className="font-semibold text-gray-900">
                              {proposal.implementation_plan?.phases?.length} phases
                            </p>
                          </div>
                        </div>
                      </div>

                      {/* Approval Actions */}
                      {proposal.status === 'pending_approval' && (
                        <div className="flex items-center space-x-4 pt-4 border-t border-gray-200">
                          <button
                            onClick={() => handleApproveProposal(proposal.proposal_id, true)}
                            className="btn btn-primary flex items-center"
                          >
                            <CheckCircleIcon className="h-5 w-5 mr-2" />
                            Approve
                          </button>
                          <button
                            onClick={() => handleApproveProposal(proposal.proposal_id, false)}
                            className="btn btn-secondary flex items-center"
                          >
                            <XCircleIcon className="h-5 w-5 mr-2" />
                            Reject
                          </button>
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))
              )}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-500">Loading proposals...</p>
            </div>
          )}
        </div>
      )}

      {/* Church Kit Tab */}
      {activeTab === 'church-kit' && churchKitMetrics && (
        <div className="space-y-6">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-gray-900">Church Kit Generator Metrics</h3>
            </div>
            <div className="p-6 grid grid-cols-2 md:grid-cols-4 gap-6">
              {Object.entries(churchKitMetrics.metrics || {}).map(([key, value]) => (
                <div key={key}>
                  <p className="text-xs text-gray-500 capitalize">{key.replace(/_/g, ' ')}</p>
                  <p className="text-xl font-bold text-gray-900">
                    {typeof value === 'number' && key.includes('revenue') ? `$${value.toLocaleString()}` :
                     typeof value === 'number' && value < 1 ? (value * 100).toFixed(1) + '%' :
                     value}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default Revenue;
