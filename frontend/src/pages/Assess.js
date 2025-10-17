import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  CodeBracketIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  BeakerIcon,
  ShieldCheckIcon,
  CurrencyDollarIcon,
  DocumentMagnifyingGlassIcon,
  ArrowPathIcon,
  ChatBubbleLeftRightIcon
} from '@heroicons/react/24/outline';

function Assess() {
  const [audits, setAudits] = useState([]);
  const [selectedAudit, setSelectedAudit] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentUser, setCurrentUser] = useState('james@fullpotential.com');
  
  // Start new audit form
  const [showStartForm, setShowStartForm] = useState(false);
  const [repositoryUrl, setRepositoryUrl] = useState('');
  const [starting, setStarting] = useState(false);
  
  // Explain audit
  const [explainQuestion, setExplainQuestion] = useState('');
  const [explainAnswer, setExplainAnswer] = useState('');
  const [explaining, setExplaining] = useState(false);

  useEffect(() => {
    fetchUserAudits();
    const interval = setInterval(fetchUserAudits, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, [currentUser]);

  const fetchUserAudits = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/audit/user/${encodeURIComponent(currentUser)}?limit=20`
      );
      const data = await response.json();
      
      if (data.status === 'success') {
        setAudits(data.audits || []);
      }
    } catch (error) {
      console.error('Error fetching audits:', error);
    }
  };

  const startAudit = async () => {
    if (!repositoryUrl.trim()) return;
    
    setStarting(true);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/audit/start`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            repository: repositoryUrl,
            user_id: currentUser,
            criteria: ['UBIC_compliance', 'test_coverage', 'code_quality']
          })
        }
      );
      
      const data = await response.json();
      
      if (data.status === 'success') {
        alert(`Audit started! ID: ${data.audit_id}`);
        setRepositoryUrl('');
        setShowStartForm(false);
        fetchUserAudits();
      } else {
        alert('Failed to start audit');
      }
    } catch (error) {
      console.error('Error starting audit:', error);
      alert('Error starting audit');
    } finally {
      setStarting(false);
    }
  };

  const selectAudit = async (auditId) => {
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/audit/${auditId}`
      );
      const data = await response.json();
      
      if (data.status === 'success') {
        setSelectedAudit(data.audit);
      }
    } catch (error) {
      console.error('Error fetching audit details:', error);
    } finally {
      setLoading(false);
    }
  };

  const explainAudit = async () => {
    if (!explainQuestion.trim() || !selectedAudit) return;
    
    setExplaining(true);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/audit/${selectedAudit.audit_id}/explain`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: explainQuestion })
        }
      );
      
      const data = await response.json();
      
      if (data.status === 'success') {
        setExplainAnswer(data.answer);
      }
    } catch (error) {
      console.error('Error explaining audit:', error);
      setExplainAnswer('Error getting explanation');
    } finally {
      setExplaining(false);
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      completed: { color: 'bg-green-100 text-green-700', icon: CheckCircleIcon, text: 'Completed' },
      running: { color: 'bg-blue-100 text-blue-700', icon: ClockIcon, text: 'Running' },
      analyzing: { color: 'bg-yellow-100 text-yellow-700', icon: CodeBracketIcon, text: 'Analyzing' },
      cloning: { color: 'bg-purple-100 text-purple-700', icon: ArrowPathIcon, text: 'Cloning' },
      queued: { color: 'bg-gray-100 text-gray-700', icon: ClockIcon, text: 'Queued' },
      failed: { color: 'bg-red-100 text-red-700', icon: XCircleIcon, text: 'Failed' }
    };
    
    const badge = badges[status] || badges.queued;
    const Icon = badge.icon;
    
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${badge.color}`}>
        <Icon className="h-4 w-4 mr-1" />
        {badge.text}
      </span>
    );
  };

  const getRecommendationBadge = (recommendation) => {
    const badges = {
      APPROVE_FULL_PAYMENT: { color: 'bg-green-500 text-white', text: '✅ Approve Full Payment' },
      APPROVE_PARTIAL_PAYMENT: { color: 'bg-yellow-500 text-white', text: '⚠️ Approve Partial' },
      REQUEST_FIXES_FIRST: { color: 'bg-orange-500 text-white', text: '🔧 Request Fixes' },
      REJECT_DO_NOT_PAY: { color: 'bg-red-500 text-white', text: '❌ Do Not Pay' }
    };
    
    const badge = badges[recommendation] || { color: 'bg-gray-500 text-white', text: recommendation };
    
    return (
      <span className={`inline-flex items-center px-4 py-2 rounded-lg text-sm font-bold ${badge.color}`}>
        {badge.text}
      </span>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">I ASSESS</h1>
          <p className="text-gray-600 mt-1">Automated Code Quality Auditing with Payment Recommendations</p>
        </div>
        <button
          onClick={() => setShowStartForm(!showStartForm)}
          className="btn btn-primary"
        >
          <CodeBracketIcon className="h-5 w-5 mr-2" />
          New Audit
        </button>
      </div>

      {/* User Selection */}
      <div className="card">
        <div className="flex items-center gap-4">
          <label className="font-medium text-gray-700">User:</label>
          <select
            value={currentUser}
            onChange={(e) => setCurrentUser(e.target.value)}
            className="input w-64"
          >
            <option value="james@fullpotential.com">James (james@fullpotential.com)</option>
            <option value="vahit@company.com">Vahit (vahit@company.com)</option>
          </select>
        </div>
      </div>

      {/* Start Audit Form */}
      {showStartForm && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card bg-blue-50 border-blue-200"
        >
          <h3 className="text-lg font-semibold mb-4">Start New Audit</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Repository URL
              </label>
              <input
                type="text"
                value={repositoryUrl}
                onChange={(e) => setRepositoryUrl(e.target.value)}
                placeholder="https://github.com/username/repository"
                className="input w-full"
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={startAudit}
                disabled={starting || !repositoryUrl.trim()}
                className="btn btn-primary"
              >
                {starting ? 'Starting...' : 'Start Audit'}
              </button>
              <button
                onClick={() => setShowStartForm(false)}
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </div>
        </motion.div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Audit History */}
        <div className="lg:col-span-1 space-y-3">
          <h2 className="text-xl font-semibold">Audit History ({audits.length})</h2>
          
          {audits.length === 0 ? (
            <div className="card text-center py-8 text-gray-500">
              <DocumentMagnifyingGlassIcon className="h-12 w-12 mx-auto mb-2 text-gray-400" />
              <p>No audits yet</p>
              <p className="text-sm mt-1">Start your first code audit!</p>
            </div>
          ) : (
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {audits.map((audit) => (
                <motion.div
                  key={audit.audit_id}
                  whileHover={{ scale: 1.02 }}
                  onClick={() => selectAudit(audit.audit_id)}
                  className={`card cursor-pointer transition-all ${
                    selectedAudit?.audit_id === audit.audit_id
                      ? 'ring-2 ring-blue-500 bg-blue-50'
                      : 'hover:shadow-md'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <p className="text-xs text-gray-500 truncate">
                        {audit.repository}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(audit.started_at).toLocaleString()}
                      </p>
                    </div>
                  </div>
                  <div className="mt-2">
                    {getStatusBadge(audit.status)}
                  </div>
                  {audit.payment_recommendation && (
                    <div className="mt-2 text-sm font-bold">
                      Score: {audit.payment_recommendation.total_score}/100
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          )}
        </div>

        {/* Audit Details */}
        <div className="lg:col-span-2">
          {!selectedAudit ? (
            <div className="card text-center py-16 text-gray-500">
              <CodeBracketIcon className="h-16 w-16 mx-auto mb-4 text-gray-400" />
              <p className="text-lg">Select an audit to view details</p>
            </div>
          ) : loading ? (
            <div className="card text-center py-16">
              <div className="spinner h-12 w-12 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading audit details...</p>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Header */}
              <div className="card">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold mb-2">Audit Details</h2>
                    <p className="text-sm text-gray-600">{selectedAudit.repository}</p>
                    <p className="text-xs text-gray-400 mt-1">
                      Started: {new Date(selectedAudit.started_at).toLocaleString()}
                    </p>
                  </div>
                  {getStatusBadge(selectedAudit.status)}
                </div>
              </div>

              {selectedAudit.status === 'completed' && (
                <>
                  {/* Payment Recommendation */}
                  {selectedAudit.payment_recommendation && (
                    <div className="card bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200">
                      <h3 className="text-xl font-bold mb-4 flex items-center">
                        <CurrencyDollarIcon className="h-6 w-6 mr-2 text-blue-600" />
                        Payment Recommendation
                      </h3>
                      
                      <div className="text-center mb-6">
                        <div className="text-6xl font-bold text-blue-600 mb-2">
                          {selectedAudit.payment_recommendation.total_score}
                          <span className="text-3xl text-gray-500">/100</span>
                        </div>
                        {getRecommendationBadge(selectedAudit.payment_recommendation.recommendation)}
                        <p className="mt-4 text-lg font-medium text-gray-700">
                          {selectedAudit.payment_recommendation.action}
                        </p>
                      </div>

                      <div className="bg-white rounded-lg p-4 space-y-2">
                        <h4 className="font-semibold mb-2">Score Breakdown:</h4>
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <p className="text-sm text-gray-600">UBIC Compliance</p>
                            <p className="text-lg font-bold">{selectedAudit.payment_recommendation.score_breakdown.ubic}/30</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">Test Coverage</p>
                            <p className="text-lg font-bold">{selectedAudit.payment_recommendation.score_breakdown.coverage}/30</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">Tests Passing</p>
                            <p className="text-lg font-bold">{selectedAudit.payment_recommendation.score_breakdown.tests_pass}/20</p>
                          </div>
                          <div>
                            <p className="text-sm text-gray-600">Code Quality</p>
                            <p className="text-lg font-bold">{selectedAudit.payment_recommendation.score_breakdown.ai_quality}/20</p>
                          </div>
                        </div>
                        <div className="mt-4 pt-4 border-t">
                          <p className="text-sm text-gray-700">{selectedAudit.payment_recommendation.reasoning}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* UBIC Compliance */}
                  {selectedAudit.ubic_compliance && (
                    <div className="card">
                      <h3 className="text-lg font-bold mb-4 flex items-center">
                        <ShieldCheckIcon className="h-6 w-6 mr-2 text-purple-600" />
                        UBIC v1.5 Compliance
                      </h3>
                      
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <p className="text-3xl font-bold text-purple-600">
                            {selectedAudit.ubic_compliance.found}/{selectedAudit.ubic_compliance.total_required}
                          </p>
                          <p className="text-sm text-gray-600">Endpoints Found</p>
                        </div>
                        <div className="text-right">
                          <p className="text-3xl font-bold text-purple-600">
                            {selectedAudit.ubic_compliance.compliance_percent.toFixed(0)}%
                          </p>
                          <p className="text-sm text-gray-600">Compliance</p>
                        </div>
                      </div>

                      {selectedAudit.ubic_compliance.missing.length > 0 && (
                        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                          <p className="font-semibold text-red-700 mb-2">Missing Endpoints:</p>
                          <ul className="list-disc list-inside text-sm text-red-600">
                            {selectedAudit.ubic_compliance.missing.map((ep, i) => (
                              <li key={i}>{ep}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Test Results */}
                  {selectedAudit.test_results && (
                    <div className="card">
                      <h3 className="text-lg font-bold mb-4 flex items-center">
                        <BeakerIcon className="h-6 w-6 mr-2 text-green-600" />
                        Test Results
                      </h3>
                      
                      <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-3xl font-bold text-green-600">
                            {selectedAudit.test_results.coverage_percent.toFixed(1)}%
                          </p>
                          <p className="text-sm text-gray-600">Test Coverage</p>
                        </div>
                        <div>
                          <p className="text-3xl font-bold">
                            {selectedAudit.test_results.tests_passed ? '✅' : '❌'}
                          </p>
                          <p className="text-sm text-gray-600">Tests Status</p>
                        </div>
                      </div>

                      {selectedAudit.test_results.meets_80_threshold ? (
                        <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-green-700">
                          ✅ Meets 80% coverage threshold
                        </div>
                      ) : (
                        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-yellow-700">
                          ⚠️ Below 80% coverage threshold (needs improvement)
                        </div>
                      )}
                    </div>
                  )}

                  {/* AI Code Review */}
                  {selectedAudit.ai_review && (
                    <div className="card">
                      <h3 className="text-lg font-bold mb-4 flex items-center">
                        <CodeBracketIcon className="h-6 w-6 mr-2 text-blue-600" />
                        AI Code Review
                      </h3>
                      
                      <div className="mb-4">
                        <p className="text-3xl font-bold text-blue-600">
                          {selectedAudit.ai_review.quality_score}/10
                        </p>
                        <p className="text-sm text-gray-600">Code Quality Score</p>
                      </div>

                      {selectedAudit.ai_review.ai_analysis && (
                        <div className="bg-gray-50 rounded-lg p-4 whitespace-pre-wrap text-sm">
                          {selectedAudit.ai_review.ai_analysis}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Ask Question */}
                  <div className="card bg-purple-50 border-purple-200">
                    <h3 className="text-lg font-bold mb-4 flex items-center">
                      <ChatBubbleLeftRightIcon className="h-6 w-6 mr-2 text-purple-600" />
                      Ask About This Audit
                    </h3>
                    
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={explainQuestion}
                        onChange={(e) => setExplainQuestion(e.target.value)}
                        placeholder="e.g., Should I pay the developer for this work?"
                        className="input w-full"
                      />
                      <button
                        onClick={explainAudit}
                        disabled={explaining || !explainQuestion.trim()}
                        className="btn btn-primary"
                      >
                        {explaining ? 'Getting Answer...' : 'Ask AI'}
                      </button>
                      
                      {explainAnswer && (
                        <div className="bg-white rounded-lg p-4 mt-4 border border-purple-300">
                          <p className="font-semibold text-purple-700 mb-2">AI Answer:</p>
                          <p className="text-gray-700 whitespace-pre-wrap">{explainAnswer}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </>
              )}

              {selectedAudit.status === 'failed' && selectedAudit.error && (
                <div className="card bg-red-50 border-red-200">
                  <h3 className="text-lg font-bold text-red-700 mb-2">Audit Failed</h3>
                  <p className="text-red-600">{selectedAudit.error}</p>
                </div>
              )}

              {['queued', 'cloning', 'analyzing', 'running'].includes(selectedAudit.status) && (
                <div className="card text-center py-8">
                  <div className="spinner h-12 w-12 mx-auto mb-4"></div>
                  <p className="text-lg font-medium">Audit in progress...</p>
                  <p className="text-sm text-gray-600 mt-2">Status: {selectedAudit.status}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Assess;

