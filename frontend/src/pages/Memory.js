import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  CircleStackIcon,
  PlusIcon,
  MagnifyingGlassIcon,
  UserIcon,
  TrashIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

const TrinityMemory = () => {
  const [memories, setMemories] = useState([]);
  const [currentUser, setCurrentUser] = useState('james@fullpotential.com');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  
  // Add memory form
  const [showAddForm, setShowAddForm] = useState(false);
  const [newMemory, setNewMemory] = useState({
    content: {}
  });
  const [contentKey, setContentKey] = useState('');
  const [contentValue, setContentValue] = useState('');
  const [contentPairs, setContentPairs] = useState([]);

  useEffect(() => {
    if (currentUser) {
      fetchUserMemories();
      fetchUserStats();
    }
  }, [currentUser]);

  const fetchUserMemories = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/get-all?user_id=${encodeURIComponent(currentUser)}&limit=100`
      );
      const data = await response.json();
      
      if (data.status === 'success') {
        setMemories(data.memories || []);
      }
    } catch (error) {
      console.error('Error fetching memories:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserStats = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/stats?user_id=${encodeURIComponent(currentUser)}`
      );
      const data = await response.json();
      
      if (data.status === 'success') {
        setStats(data.stats);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      fetchUserMemories();
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/search?user_id=${encodeURIComponent(currentUser)}&query=${encodeURIComponent(searchQuery)}&limit=50`
      );
      const data = await response.json();
      
      if (data.status === 'success') {
        setMemories(data.results || []);
      }
    } catch (error) {
      console.error('Error searching memories:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddMemory = async () => {
    try {
      // Build content object from key-value pairs
      const content = {};
      contentPairs.forEach(pair => {
        content[pair.key] = pair.value;
      });

      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/add`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            user_id: currentUser,
            content: content,
            metadata: { added_via: 'ui' }
          })
        }
      );

      const result = await response.json();
      
      if (result.status === 'success') {
        alert('Memory added successfully!');
        setShowAddForm(false);
        setContentPairs([]);
        fetchUserMemories();
        fetchUserStats();
      } else {
        alert('Error adding memory: ' + result.detail);
      }
    } catch (error) {
      console.error('Error adding memory:', error);
      alert('Error adding memory');
    }
  };

  const handleDeleteMemory = async (memoryId) => {
    if (!window.confirm('Are you sure you want to delete this memory?')) {
      return;
    }

    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/delete?memory_id=${encodeURIComponent(memoryId)}&user_id=${encodeURIComponent(currentUser)}`,
        { method: 'DELETE' }
      );

      const result = await response.json();
      
      if (result.status === 'success') {
        alert('Memory deleted successfully!');
        fetchUserMemories();
        fetchUserStats();
      } else {
        alert('Error deleting memory: ' + result.detail);
      }
    } catch (error) {
      console.error('Error deleting memory:', error);
      alert('Error deleting memory');
    }
  };

  const addContentPair = () => {
    if (contentKey && contentValue) {
      setContentPairs([...contentPairs, { key: contentKey, value: contentValue }]);
      setContentKey('');
      setContentValue('');
    }
  };

  const removeContentPair = (index) => {
    setContentPairs(contentPairs.filter((_, i) => i !== index));
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4">
        <h1 className="text-3xl font-bold text-gray-900">Trinity BRICKS I MEMORY</h1>
        <p className="mt-2 text-gray-600">
          Persistent memory with multi-user isolation and semantic search
        </p>
      </div>

      {/* User Selection & Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* User Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <div className="flex items-center mb-4">
            <UserIcon className="h-6 w-6 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Current User</h3>
          </div>
          <select
            value={currentUser}
            onChange={(e) => setCurrentUser(e.target.value)}
            className="input w-full"
          >
            <option value="james@fullpotential.com">James (james@fullpotential.com)</option>
            <option value="vahit@company.com">Vahit (vahit@company.com)</option>
            <option value="fletcher@developer.com">Fletcher (fletcher@developer.com)</option>
            <option value="alice@example.com">Alice (alice@example.com)</option>
            <option value="bob@example.com">Bob (bob@example.com)</option>
          </select>
          <p className="text-xs text-gray-500 mt-2">
            Each user has isolated memory space
          </p>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <div className="flex items-center mb-4">
            <CircleStackIcon className="h-6 w-6 text-green-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Your Memories</h3>
          </div>
          {stats && stats.user_stats ? (
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Total:</span>
                <span className="text-sm font-semibold">{stats.user_stats.total_memories || 0}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Cache:</span>
                <span className="text-sm font-semibold">
                  {stats.user_stats.cache_enabled ? '✅ Enabled' : '❌ Disabled'}
                </span>
              </div>
            </div>
          ) : (
            <p className="text-sm text-gray-500">Loading stats...</p>
          )}
        </motion.div>

        {/* Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center mb-4">
            <PlusIcon className="h-6 w-6 text-purple-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Actions</h3>
          </div>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="btn-primary w-full"
          >
            {showAddForm ? 'Cancel' : 'Add New Memory'}
          </button>
        </motion.div>
      </div>

      {/* Add Memory Form */}
      {showAddForm && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Memory</h3>
          
          <div className="space-y-4">
            {/* Content Key-Value Pairs */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Memory Content (Key-Value Pairs)
              </label>
              
              <div className="space-y-2">
                {contentPairs.map((pair, index) => (
                  <div key={index} className="flex items-center gap-2 p-2 bg-gray-50 rounded">
                    <span className="text-sm font-medium text-gray-700">{pair.key}:</span>
                    <span className="text-sm text-gray-600">{pair.value}</span>
                    <button
                      onClick={() => removeContentPair(index)}
                      className="ml-auto text-red-500 hover:text-red-700"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>

              <div className="flex gap-2 mt-2">
                <input
                  type="text"
                  placeholder="Key (e.g., developer)"
                  value={contentKey}
                  onChange={(e) => setContentKey(e.target.value)}
                  className="input flex-1"
                />
                <input
                  type="text"
                  placeholder="Value (e.g., Fletcher)"
                  value={contentValue}
                  onChange={(e) => setContentValue(e.target.value)}
                  className="input flex-1"
                />
                <button
                  onClick={addContentPair}
                  disabled={!contentKey || !contentValue}
                  className="btn-outline disabled:opacity-50"
                >
                  Add
                </button>
              </div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={handleAddMemory}
                disabled={contentPairs.length === 0}
                className="btn-primary flex-1 disabled:opacity-50"
              >
                Save Memory
              </button>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setContentPairs([]);
                  setContentKey('');
                  setContentValue('');
                }}
                className="btn-outline flex-1"
              >
                Cancel
              </button>
            </div>
          </div>
        </motion.div>
      )}

      {/* Search */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card"
      >
        <div className="flex items-center gap-4">
          <div className="relative flex-1">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Semantic search: 'What's Fletcher's status?' or 'developer assessments'"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="input pl-10 w-full"
            />
          </div>
          <button
            onClick={handleSearch}
            className="btn-primary"
          >
            Search
          </button>
          {searchQuery && (
            <button
              onClick={() => {
                setSearchQuery('');
                fetchUserMemories();
              }}
              className="btn-outline"
            >
              Clear
            </button>
          )}
        </div>
      </motion.div>

      {/* Memories List */}
      <div className="space-y-4">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="spinner"></div>
          </div>
        ) : memories.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card text-center py-12"
          >
            <CircleStackIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No memories found</h3>
            <p className="text-gray-600 mb-4">
              {searchQuery
                ? 'Try a different search query'
                : 'Add your first memory to get started'
              }
            </p>
            <button
              onClick={() => setShowAddForm(true)}
              className="btn-primary"
            >
              Add Memory
            </button>
          </motion.div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {searchQuery ? `Search Results (${memories.length})` : `All Memories (${memories.length})`}
              </h3>
              <span className="text-sm text-gray-500">
                User: {currentUser}
              </span>
            </div>

            {memories.map((memory, index) => (
              <motion.div
                key={memory.memory_id || index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.05 }}
                className="card hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <CircleStackIcon className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <span className="text-xs text-gray-500">
                        Memory ID: {memory.memory_id?.substring(0, 20)}...
                      </span>
                      {memory.relevance_score && (
                        <span className="ml-2 text-xs text-green-600 font-semibold">
                          Relevance: {(memory.relevance_score * 100).toFixed(0)}%
                        </span>
                      )}
                    </div>
                  </div>
                  <button
                    onClick={() => handleDeleteMemory(memory.memory_id)}
                    className="text-red-500 hover:text-red-700 transition-colors p-1 rounded"
                    title="Delete memory"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>

                {/* Memory Content */}
                <div className="bg-gray-50 rounded-lg p-4 mb-3">
                  {typeof memory.content === 'object' ? (
                    <div className="space-y-2">
                      {Object.entries(memory.content).map(([key, value]) => (
                        <div key={key} className="flex">
                          <span className="text-sm font-semibold text-gray-700 min-w-[120px]">
                            {key}:
                          </span>
                          <span className="text-sm text-gray-900">
                            {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-900">{String(memory.content)}</p>
                  )}
                </div>

                {/* Metadata */}
                {memory.metadata && Object.keys(memory.metadata).length > 0 && (
                  <div className="mb-3">
                    <p className="text-xs text-gray-500 mb-1">Metadata:</p>
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(memory.metadata).map(([key, value]) => (
                        <span
                          key={key}
                          className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-800"
                        >
                          {key}: {String(value)}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Footer */}
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <div className="flex items-center">
                    <ClockIcon className="h-4 w-4 mr-1" />
                    {formatDate(memory.timestamp)}
                  </div>
                  <span className="badge badge-outline">
                    {memory.source || 'mem0'}
                  </span>
                </div>
              </motion.div>
            ))}
          </>
        )}
      </div>

      {/* Trinity BRICKS Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card bg-gradient-to-r from-blue-50 to-purple-50"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          🧠 Trinity BRICKS I MEMORY
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <p className="font-semibold text-gray-700">Multi-User Isolation</p>
            <p className="text-gray-600">Each user has private memory namespace</p>
          </div>
          <div>
            <p className="font-semibold text-gray-700">Semantic Search</p>
            <p className="text-gray-600">Natural language queries with AI</p>
          </div>
          <div>
            <p className="font-semibold text-gray-700">Persistent Storage</p>
            <p className="text-gray-600">Memories survive container restarts</p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default TrinityMemory;
