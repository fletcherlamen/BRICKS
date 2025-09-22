import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  HeartIcon,
  CpuChipIcon,
  ServerIcon,
  GlobeAltIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';

const Health = () => {
  const [healthData, setHealthData] = useState({});
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetchHealthData();
    const interval = setInterval(fetchHealthData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchHealthData = async () => {
    try {
      // Mock health data - in production this would fetch from API
      const mockHealthData = {
        overall_status: 'healthy',
        services: {
          database: {
            status: 'healthy',
            response_time_ms: 15,
            last_check: new Date().toISOString()
          },
          redis: {
            status: 'healthy',
            response_time_ms: 5,
            last_check: new Date().toISOString()
          },
          crewai: {
            status: 'healthy',
            api_configured: true,
            agents_available: 5,
            last_check: new Date().toISOString()
          },
          mem0: {
            status: 'healthy',
            api_configured: true,
            memory_count: 150,
            last_check: new Date().toISOString()
          },
          devin_ai: {
            status: 'healthy',
            api_configured: true,
            capabilities: 'Full',
            last_check: new Date().toISOString()
          },
          multi_model_router: {
            status: 'healthy',
            available_models: 6,
            last_check: new Date().toISOString()
          }
        },
        business_systems: {
          church_kit_generator: {
            status: 'healthy',
            api_accessible: true,
            last_sync: new Date().toISOString()
          },
          global_sky_ai: {
            status: 'healthy',
            api_accessible: true,
            optimization_active: true,
            last_sync: new Date().toISOString()
          },
          treasury_management: {
            status: 'healthy',
            api_accessible: true,
            yield_optimization_active: true,
            last_sync: new Date().toISOString()
          }
        },
        system_metrics: {
          uptime_seconds: 86400,
          total_requests: 1250,
          success_rate: 0.985,
          average_response_time_ms: 250,
          active_sessions: 3,
          memory_usage_percent: 65,
          cpu_usage_percent: 45
        }
      };

      setHealthData(mockHealthData);
      setLastUpdated(new Date());
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch health data:', error);
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'healthy': return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'degraded': return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />;
      case 'unhealthy': return <ExclamationTriangleIcon className="h-5 w-5 text-red-500" />;
      default: return <ClockIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy': return 'status-healthy';
      case 'degraded': return 'status-warning';
      case 'unhealthy': return 'status-danger';
      default: return 'status-unknown';
    }
  };

  const formatUptime = (seconds) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${days}d ${hours}h ${minutes}m`;
  };

  const formatResponseTime = (ms) => {
    if (ms < 100) return `${ms}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
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
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">System Health</h1>
            <p className="mt-2 text-gray-600">
              Real-time monitoring of all system components and services
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`h-3 w-3 rounded-full ${
              healthData.overall_status === 'healthy' ? 'bg-green-500' :
              healthData.overall_status === 'degraded' ? 'bg-yellow-500' :
              'bg-red-500'
            } animate-pulse`}></div>
            <span className={`status-indicator ${getStatusColor(healthData.overall_status)}`}>
              {healthData.overall_status}
            </span>
          </div>
        </div>
        {lastUpdated && (
          <p className="text-sm text-gray-500 mt-2">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </p>
        )}
      </div>

      {/* System Overview */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {[
          {
            name: 'Uptime',
            value: formatUptime(healthData.system_metrics?.uptime_seconds || 0),
            icon: ClockIcon,
            color: 'bg-blue-500'
          },
          {
            name: 'Success Rate',
            value: `${((healthData.system_metrics?.success_rate || 0) * 100).toFixed(1)}%`,
            icon: ChartBarIcon,
            color: 'bg-green-500'
          },
          {
            name: 'Active Sessions',
            value: healthData.system_metrics?.active_sessions || 0,
            icon: CpuChipIcon,
            color: 'bg-purple-500'
          },
          {
            name: 'Avg Response Time',
            value: formatResponseTime(healthData.system_metrics?.average_response_time_ms || 0),
            icon: ServerIcon,
            color: 'bg-yellow-500'
          }
        ].map((metric, index) => (
          <motion.div
            key={metric.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="card"
          >
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${metric.color} bg-opacity-10`}>
                <metric.icon className={`h-6 w-6 ${metric.color.replace('bg-', 'text-')}`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">{metric.name}</p>
                <p className="text-2xl font-bold text-gray-900">{metric.value}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* AI Systems Health */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">AI Systems</h3>
            <p className="text-sm text-gray-600">Status of AI orchestration components</p>
          </div>
          
          <div className="space-y-3">
            {Object.entries(healthData.services || {}).map(([service, data]) => (
              <div key={service} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(data.status)}
                  <div>
                    <p className="text-sm font-medium text-gray-900 capitalize">
                      {service.replace('_', ' ')}
                    </p>
                    <p className="text-xs text-gray-500">
                      {data.response_time_ms && `Response: ${data.response_time_ms}ms`}
                      {data.agents_available && ` • ${data.agents_available} agents`}
                      {data.memory_count && ` • ${data.memory_count} memories`}
                      {data.available_models && ` • ${data.available_models} models`}
                    </p>
                  </div>
                </div>
                <span className={`status-indicator ${getStatusColor(data.status)}`}>
                  {data.status}
                </span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Infrastructure Health */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Infrastructure</h3>
            <p className="text-sm text-gray-600">Core system components</p>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <ServerIcon className="h-5 w-5 text-blue-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Database</p>
                  <p className="text-xs text-gray-500">PostgreSQL</p>
                </div>
              </div>
              <span className="status-healthy">Connected</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <CpuChipIcon className="h-5 w-5 text-red-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Redis Cache</p>
                  <p className="text-xs text-gray-500">Memory store</p>
                </div>
              </div>
              <span className="status-healthy">Connected</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <GlobeAltIcon className="h-5 w-5 text-green-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">API Gateway</p>
                  <p className="text-xs text-gray-500">FastAPI</p>
                </div>
              </div>
              <span className="status-healthy">Running</span>
            </div>

            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <HeartIcon className="h-5 w-5 text-purple-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">Frontend</p>
                  <p className="text-xs text-gray-500">React Dashboard</p>
                </div>
              </div>
              <span className="status-healthy">Online</span>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Business Systems Health */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900">Business Systems</h3>
          <p className="text-sm text-gray-600">External integrations and business services</p>
        </div>
        
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Object.entries(healthData.business_systems || {}).map(([system, data]) => (
            <div key={system} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                {getStatusIcon(data.status)}
                <div>
                  <p className="text-sm font-medium text-gray-900 capitalize">
                    {system.replace('_', ' ')}
                  </p>
                  <p className="text-xs text-gray-500">
                    {data.optimization_active && 'Optimization Active'}
                    {data.yield_optimization_active && 'Yield Optimization Active'}
                    {data.last_sync && `Last sync: ${new Date(data.last_sync).toLocaleTimeString()}`}
                  </p>
                </div>
              </div>
              <span className={`status-indicator ${getStatusColor(data.status)}`}>
                {data.status}
              </span>
            </div>
          ))}
        </div>
      </motion.div>

      {/* System Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900">System Metrics</h3>
          <p className="text-sm text-gray-600">Performance and resource utilization</p>
        </div>
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {healthData.system_metrics?.memory_usage_percent || 0}%
            </div>
            <div className="text-sm text-gray-600">Memory Usage</div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
              <div
                className="bg-blue-600 h-2 rounded-full"
                style={{ width: `${healthData.system_metrics?.memory_usage_percent || 0}%` }}
              ></div>
            </div>
          </div>

          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {healthData.system_metrics?.cpu_usage_percent || 0}%
            </div>
            <div className="text-sm text-gray-600">CPU Usage</div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
              <div
                className="bg-green-600 h-2 rounded-full"
                style={{ width: `${healthData.system_metrics?.cpu_usage_percent || 0}%` }}
              ></div>
            </div>
          </div>

          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {healthData.system_metrics?.total_requests?.toLocaleString() || 0}
            </div>
            <div className="text-sm text-gray-600">Total Requests</div>
          </div>

          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {formatResponseTime(healthData.system_metrics?.average_response_time_ms || 0)}
            </div>
            <div className="text-sm text-gray-600">Avg Response Time</div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Health;
