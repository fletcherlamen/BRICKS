import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  CpuChipIcon,
  CubeIcon,
  CircleStackIcon,
  HeartIcon,
  ChartBarIcon,
  CurrencyDollarIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    activeSessions: 0,
    totalBricks: 0,
    revenueOpportunities: 0,
    systemHealth: 'healthy'
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Mock data for now - in production this would fetch from API
      setStats({
        activeSessions: 3,
        totalBricks: 15,
        revenueOpportunities: 8,
        systemHealth: 'healthy'
      });
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      setLoading(false);
    }
  };

  const statCards = [
    {
      name: 'Active Sessions',
      value: stats.activeSessions,
      icon: CpuChipIcon,
      color: 'bg-blue-500',
      change: '+12%',
      changeType: 'positive'
    },
    {
      name: 'Total BRICKS',
      value: stats.totalBricks,
      icon: CubeIcon,
      color: 'bg-green-500',
      change: '+3',
      changeType: 'positive'
    },
    {
      name: 'Revenue Opportunities',
      value: stats.revenueOpportunities,
      icon: CurrencyDollarIcon,
      color: 'bg-yellow-500',
      change: '+2',
      changeType: 'positive'
    },
    {
      name: 'System Health',
      value: stats.systemHealth,
      icon: HeartIcon,
      color: 'bg-green-500',
      change: '100%',
      changeType: 'positive'
    }
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'orchestration',
      title: 'Strategic Analysis Completed',
      description: 'AI systems analyzed Church Kit Generator optimization opportunities',
      timestamp: '2 minutes ago',
      status: 'completed'
    },
    {
      id: 2,
      type: 'brick',
      title: 'New BRICK Identified',
      description: 'Mobile App Platform gap identified with high priority',
      timestamp: '15 minutes ago',
      status: 'pending'
    },
    {
      id: 3,
      type: 'revenue',
      title: 'Revenue Opportunity Found',
      description: 'API Marketplace opportunity estimated at $75K revenue',
      timestamp: '1 hour ago',
      status: 'evaluating'
    },
    {
      id: 4,
      type: 'memory',
      title: 'Memory Updated',
      description: 'Strategic insights stored in persistent memory',
      timestamp: '2 hours ago',
      status: 'completed'
    }
  ];

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
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">
          I PROACTIVE BRICK Orchestration Intelligence - Real-time System Overview
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="card hover:shadow-md transition-shadow"
          >
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${stat.color} bg-opacity-10`}>
                <stat.icon className={`h-6 w-6 ${stat.color.replace('bg-', 'text-')}`} />
              </div>
              <div className="ml-4 flex-1">
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                <p className={`text-sm ${stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'}`}>
                  {stat.change} from last week
                </p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Recent Activities */}
        <div className="lg:col-span-2">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="card"
          >
            <div className="card-header">
              <h3 className="text-lg font-semibold text-gray-900">Recent Activities</h3>
              <p className="text-sm text-gray-600">Latest orchestration and analysis activities</p>
            </div>
            <div className="space-y-4">
              {recentActivities.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50">
                  <div className={`p-2 rounded-full ${
                    activity.type === 'orchestration' ? 'bg-blue-100' :
                    activity.type === 'brick' ? 'bg-green-100' :
                    activity.type === 'revenue' ? 'bg-yellow-100' :
                    'bg-purple-100'
                  }`}>
                    {activity.type === 'orchestration' && <CpuChipIcon className="h-4 w-4 text-blue-600" />}
                    {activity.type === 'brick' && <CubeIcon className="h-4 w-4 text-green-600" />}
                    {activity.type === 'revenue' && <CurrencyDollarIcon className="h-4 w-4 text-yellow-600" />}
                    {activity.type === 'memory' && <CircleStackIcon className="h-4 w-4 text-purple-600" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium text-gray-900">{activity.title}</p>
                      <span className={`badge ${
                        activity.status === 'completed' ? 'badge-success' :
                        activity.status === 'pending' ? 'badge-warning' :
                        'badge-primary'
                      }`}>
                        {activity.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{activity.description}</p>
                    <p className="text-xs text-gray-500 mt-1">{activity.timestamp}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* System Status */}
        <div className="space-y-6">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="card"
          >
            <div className="card-header">
              <h3 className="text-lg font-semibold text-gray-900">System Status</h3>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">AI Orchestrator</span>
                <span className="status-healthy">Healthy</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">CrewAI</span>
                <span className="status-healthy">Healthy</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Mem0.ai</span>
                <span className="status-healthy">Healthy</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Multi-Model Router</span>
                <span className="status-healthy">Healthy</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Database</span>
                <span className="status-healthy">Connected</span>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="card"
          >
            <div className="card-header">
              <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
            </div>
            <div className="space-y-3">
              <button className="btn-primary w-full">
                Start New Analysis
              </button>
              <button className="btn-outline w-full">
                View BRICKS
              </button>
              <button className="btn-outline w-full">
                Check Memory
              </button>
              <button className="btn-outline w-full">
                System Health
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
