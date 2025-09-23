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
  WrenchScrewdriverIcon,
  ExclamationCircleIcon,
  InformationCircleIcon,
} from '@heroicons/react/24/outline';

const UbicHealth = () => {
  const [healthData, setHealthData] = useState({});
  const [capabilities, setCapabilities] = useState({});
  const [dependencies, setDependencies] = useState([]);
  const [stateMetrics, setStateMetrics] = useState({});
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    fetchUbicData();
    const interval = setInterval(fetchUbicData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchUbicData = async () => {
    try {
      // Fetch UBIC v1.5 endpoints
      const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const [healthResponse, capabilitiesResponse, dependenciesResponse, stateResponse] = await Promise.all([
        fetch(`${baseUrl}/api/v1/health/`),
        fetch(`${baseUrl}/api/v1/health/capabilities`),
        fetch(`${baseUrl}/api/v1/health/dependencies`),
        fetch(`${baseUrl}/api/v1/health/state`)
      ]);

      const [healthData, capabilitiesData, dependenciesData, stateData] = await Promise.all([
        healthResponse.json(),
        capabilitiesResponse.json(),
        dependenciesResponse.json(),
        stateResponse.json()
      ]);

      setHealthData(healthData.details);
      setCapabilities(capabilitiesData.details);
      setDependencies(dependenciesData.details.dependencies || []);
      setStateMetrics(stateData.details);
      setLastUpdated(new Date());
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch UBIC data:', error);
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'healthy': return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'warning': return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />;
      case 'critical': return <ExclamationCircleIcon className="h-5 w-5 text-red-500" />;
      case 'info': return <InformationCircleIcon className="h-5 w-5 text-blue-500" />;
      default: return <ClockIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'healthy': return 'status-healthy';
      case 'warning': return 'status-warning';
      case 'critical': return 'status-danger';
      case 'info': return 'status-info';
      default: return 'status-unknown';
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'text-red-600 bg-red-100';
      case 'warning': return 'text-yellow-600 bg-yellow-100';
      case 'info': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const formatUptime = (seconds) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${days}d ${hours}h ${minutes}m`;
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
            <h1 className="text-3xl font-bold text-gray-900">UBIC v1.5 Health Monitor</h1>
            <p className="mt-2 text-gray-600">
              Universal Brick Interface Contract compliance monitoring
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`h-3 w-3 rounded-full ${
              healthData.status === 'healthy' ? 'bg-green-500' :
              healthData.status === 'warning' ? 'bg-yellow-500' :
              'bg-red-500'
            } animate-pulse`}></div>
            <span className={`status-indicator ${getStatusColor(healthData.status)}`}>
              {healthData.status}
            </span>
          </div>
        </div>
        {lastUpdated && (
          <p className="text-sm text-gray-500 mt-2">
            Last updated: {lastUpdated.toLocaleTimeString()}
          </p>
        )}
      </div>

      {/* UBIC Overview */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {[
          {
            name: 'UBIC Version',
            value: capabilities.api_version || '1.5',
            icon: WrenchScrewdriverIcon,
            color: 'bg-purple-500'
          },
          {
            name: 'Uptime',
            value: formatUptime(healthData.uptime_seconds || 0),
            icon: ClockIcon,
            color: 'bg-blue-500'
          },
          {
            name: 'Success Rate',
            value: `${((stateMetrics.requests_total > 0 ? stateMetrics.requests_success / stateMetrics.requests_total : 0) * 100).toFixed(1)}%`,
            icon: ChartBarIcon,
            color: 'bg-green-500'
          },
          {
            name: 'Active Connections',
            value: stateMetrics.active_connections || 0,
            icon: CpuChipIcon,
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
        {/* Dependencies Health */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Dependencies</h3>
            <p className="text-sm text-gray-600">UBIC v1.5 dependency monitoring</p>
          </div>
          
          <div className="space-y-3">
            {dependencies.map((dep, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(dep.status)}
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {dep.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {dep.type} • {dep.details?.host && `${dep.details.host}:${dep.details.port}`}
                      {dep.details?.version && ` • v${dep.details.version}`}
                      {dep.details?.models_available && ` • ${dep.details.models_available.length} models`}
                    </p>
                  </div>
                </div>
                <div className="flex flex-col items-end space-y-1">
                  <span className={`status-indicator ${getStatusColor(dep.status)}`}>
                    {dep.status}
                  </span>
                  <span className={`text-xs px-2 py-1 rounded-full ${getSeverityColor(dep.severity)}`}>
                    {dep.severity}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Capabilities */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Capabilities</h3>
            <p className="text-sm text-gray-600">Available brick capabilities</p>
          </div>
          
          <div className="space-y-3">
            {capabilities.capabilities?.map((cap, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <div className={`h-3 w-3 rounded-full ${cap.enabled ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {cap.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {cap.description} • v{cap.version}
                    </p>
                  </div>
                </div>
                <span className={`status-indicator ${cap.enabled ? 'status-healthy' : 'status-unknown'}`}>
                  {cap.enabled ? 'Enabled' : 'Disabled'}
                </span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Feature Flags */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card"
      >
        <div className="card-header">
          <h3 className="text-lg font-semibold text-gray-900">Feature Flags</h3>
          <p className="text-sm text-gray-600">UBIC v1.5 feature flag status</p>
        </div>
        
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {capabilities.feature_flags?.map((flag, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className={`h-3 w-3 rounded-full ${
                  flag.enabled ? 'bg-green-500' : 
                  flag.supported ? 'bg-yellow-500' : 'bg-red-500'
                }`}></div>
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {flag.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {flag.description}
                  </p>
                </div>
              </div>
              <div className="flex flex-col items-end space-y-1">
                <span className={`text-xs px-2 py-1 rounded-full ${
                  flag.enabled ? 'bg-green-100 text-green-800' :
                  flag.supported ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {flag.enabled ? 'Enabled' : flag.supported ? 'Supported' : 'Unsupported'}
                </span>
              </div>
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
          <p className="text-sm text-gray-600">UBIC v1.5 operational metrics</p>
        </div>
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {stateMetrics.memory_usage_percent?.toFixed(1) || 0}%
            </div>
            <div className="text-sm text-gray-600">Memory Usage</div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
              <div
                className="bg-blue-600 h-2 rounded-full"
                style={{ width: `${stateMetrics.memory_usage_percent || 0}%` }}
              ></div>
            </div>
          </div>

          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {stateMetrics.cpu_usage_percent?.toFixed(1) || 0}%
            </div>
            <div className="text-sm text-gray-600">CPU Usage</div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
              <div
                className="bg-green-600 h-2 rounded-full"
                style={{ width: `${stateMetrics.cpu_usage_percent || 0}%` }}
              ></div>
            </div>
          </div>

          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {stateMetrics.requests_total?.toLocaleString() || 0}
            </div>
            <div className="text-sm text-gray-600">Total Requests</div>
          </div>

          <div className="text-center">
            <div className="text-3xl font-bold text-gray-900">
              {stateMetrics.average_response_time_ms?.toFixed(0) || 0}ms
            </div>
            <div className="text-sm text-gray-600">Avg Response Time</div>
          </div>
        </div>
      </motion.div>

      {/* Resource Specification */}
      {capabilities.resource_spec && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="card"
        >
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Resource Specification</h3>
            <p className="text-sm text-gray-600">UBIC v1.5 resource requirements</p>
          </div>
          
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {capabilities.resource_spec.cpu_min} - {capabilities.resource_spec.cpu_max}
              </div>
              <div className="text-sm text-gray-600">CPU Cores</div>
              <div className="text-xs text-gray-500 mt-1">
                Recommended: {capabilities.resource_spec.cpu_recommended}
              </div>
            </div>

            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {capabilities.resource_spec.memory_min} - {capabilities.resource_spec.memory_max}
              </div>
              <div className="text-sm text-gray-600">Memory</div>
              <div className="text-xs text-gray-500 mt-1">
                Recommended: {capabilities.resource_spec.memory_recommended}
              </div>
            </div>

            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {capabilities.resource_spec.storage_min} - {capabilities.resource_spec.storage_max}
              </div>
              <div className="text-sm text-gray-600">Storage</div>
              <div className="text-xs text-gray-500 mt-1">
                Recommended: {capabilities.resource_spec.storage_recommended}
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default UbicHealth;
