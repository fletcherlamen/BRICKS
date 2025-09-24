import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  CircleStackIcon,
  PlusIcon,
  MagnifyingGlassIcon,
  ClockIcon,
  TagIcon,
  DocumentTextIcon,
  DocumentIcon,
  CloudArrowUpIcon,
  FolderIcon,
  XMarkIcon,
  CheckIcon,
  TrashIcon
} from '@heroicons/react/24/outline';

const EnhancedMemory = () => {
  const [memories, setMemories] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedTags, setSelectedTags] = useState([]);
  const [categories, setCategories] = useState({});
  const [availableTags, setAvailableTags] = useState({});
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({});
  const [showAddForm, setShowAddForm] = useState(false);
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [largeText, setLargeText] = useState('');
  const [uploading, setUploading] = useState(false);
  const [newMemory, setNewMemory] = useState({
    content: '',
    memory_type: 'fact',
    category: 'general',
    importance_score: 0.5,
    tags: [],
    source_type: 'text'
  });

  useEffect(() => {
    fetchMemoryData();
    fetchCategories();
    fetchTags();
    fetchStats();
  }, []);

  const fetchMemoryData = async () => {
    try {
      // Always fetch all memories without filters - filtering will be done client-side
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/`);
      const data = await response.json();
      setMemories(data.memories || []);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching memories:', error);
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/categories`);
      const data = await response.json();
      setCategories(data.categories || {});
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/tags`);
      const data = await response.json();
      setAvailableTags(data.tags || {});
    } catch (error) {
      console.error('Error fetching tags:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/stats`);
      const data = await response.json();
      setStats(data.statistics || {});
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploadedFile(file);
    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('category', 'documents');
      formData.append('tags', JSON.stringify(['uploaded', 'document']));
      formData.append('importance_score', '0.7');
      formData.append('auto_extract', 'true');

      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/upload`, {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      
      if (response.ok) {
        // Refresh memories
        fetchMemoryData();
        setUploadedFile(null);
        setShowFileUpload(false);
        alert('File uploaded successfully!');
      } else {
        alert('Error uploading file: ' + result.detail);
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    } finally {
      setUploading(false);
    }
  };

  const handleLargeTextUpload = async () => {
    if (!largeText.trim()) return;

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('content', largeText);
      formData.append('category', 'general');
      formData.append('tags', JSON.stringify(['text', 'large-content']));
      formData.append('importance_score', '0.6');

      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/upload-text`, {
        method: 'POST',
        body: formData
      });

      const result = await response.json();
      
      if (response.ok) {
        // Refresh memories
        fetchMemoryData();
        setLargeText('');
        setShowAddForm(false);
        alert('Large text uploaded successfully!');
      } else {
        alert('Error uploading text: ' + result.detail);
      }
    } catch (error) {
      console.error('Error uploading text:', error);
      alert('Error uploading text');
    } finally {
      setUploading(false);
    }
  };

  const handleAddMemory = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newMemory)
      });

      const result = await response.json();
      
      if (response.ok) {
        fetchMemoryData();
        setNewMemory({
          content: '',
          memory_type: 'fact',
          category: 'general',
          importance_score: 0.5,
          tags: [],
          source_type: 'text'
        });
        setShowAddForm(false);
        alert('Memory added successfully!');
      } else {
        alert('Error adding memory: ' + result.detail);
      }
    } catch (error) {
      console.error('Error adding memory:', error);
      alert('Error adding memory');
    }
  };

  const handleDeleteMemory = async (memoryId) => {
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/memory/${memoryId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        fetchMemoryData();
        alert('Memory deleted successfully!');
      } else {
        const result = await response.json();
        alert('Error deleting memory: ' + (result.detail || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error deleting memory:', error);
      alert('Error deleting memory');
    }
  };

  const getMemoryTypeColor = (type) => {
    switch (type) {
      case 'strategy': return 'badge-primary';
      case 'gap': return 'badge-danger';
      case 'opportunity': return 'badge-success';
      case 'fact': return 'badge-secondary';
      case 'experience': return 'badge-warning';
      case 'document': return 'badge-info';
      case 'text': return 'badge-accent';
      default: return 'badge-secondary';
    }
  };

  const getSourceTypeIcon = (sourceType) => {
    switch (sourceType) {
      case 'pdf': return DocumentIcon;
      case 'markdown': return DocumentTextIcon;
      case 'text': return DocumentTextIcon;
      default: return CircleStackIcon;
    }
  };

  const filteredMemories = memories.filter(memory => {
    // Filter by search query (content or tags)
    const matchesSearch = searchQuery === '' || 
                         memory.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         (memory.tags && memory.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase())));
    
    // Filter by category (exact match)
    const matchesCategory = selectedCategory === '' || memory.category === selectedCategory;
    
    // Filter by tags (any selected tag must be present in memory tags)
    const matchesTags = selectedTags.length === 0 || 
                       (memory.tags && selectedTags.some(selectedTag => 
                         memory.tags.some(memoryTag => memoryTag.toLowerCase() === selectedTag.toLowerCase())
                       ));
    
    return matchesSearch && matchesCategory && matchesTags;
  });

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const clearFilters = () => {
    setSearchQuery('');
    setSelectedCategory('');
    setSelectedTags([]);
  };

  const hasActiveFilters = searchQuery || selectedCategory || selectedTags.length > 0;

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
        <h1 className="text-3xl font-bold text-gray-900">Enhanced Memory System</h1>
        <p className="mt-2 text-gray-600">
          Upload files (PDF, .md, .txt), paste large text, and organize with categories and tags
        </p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { name: 'Total Memories', value: stats.total_memories || memories.length, icon: CircleStackIcon, color: 'bg-blue-500' },
          { name: 'Categories', value: Object.keys(stats.categories || categories).length, icon: FolderIcon, color: 'bg-green-500' },
          { name: 'Available Tags', value: Object.keys(stats.top_tags || availableTags).length, icon: TagIcon, color: 'bg-purple-500' },
          { name: 'Recent Memories', value: stats.recent_memories || memories.filter(m => {
            const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
            return new Date(m.timestamp || m.created_at) > oneDayAgo;
          }).length, icon: DocumentIcon, color: 'bg-yellow-500' }
        ].map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="card"
          >
            <div className="flex items-center">
              <div className={`p-3 rounded-lg ${stat.color} bg-opacity-10`}>
                <stat.icon className={`h-6 w-6 ${stat.color.replace('bg-', 'text-')}`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Upload and Add Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* File Upload */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="card"
        >
          <div className="flex items-center mb-4">
            <CloudArrowUpIcon className="h-6 w-6 text-blue-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Upload Files</h3>
          </div>
          <p className="text-sm text-gray-600 mb-4">
            Upload PDF, .md, or .txt files for automatic text extraction
          </p>
          
          <div className="space-y-3">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <DocumentIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p className="text-sm text-gray-600 mb-2">Drop files here or click to browse</p>
              <input
                type="file"
                accept=".pdf,.md,.txt,.markdown"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
                disabled={uploading}
              />
              <label
                htmlFor="file-upload"
                className="btn-primary cursor-pointer"
              >
                {uploading ? 'Uploading...' : 'Choose Files'}
              </label>
            </div>
            
            {uploadedFile && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                <div className="flex items-center">
                  <CheckIcon className="h-5 w-5 text-green-600 mr-2" />
                  <span className="text-sm text-green-800">
                    {uploadedFile.name} ({formatFileSize(uploadedFile.size)})
                  </span>
                </div>
              </div>
            )}
          </div>
        </motion.div>

        {/* Large Text Upload */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="card"
        >
          <div className="flex items-center mb-4">
            <DocumentTextIcon className="h-6 w-6 text-green-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Large Text</h3>
          </div>
          <p className="text-sm text-gray-600 mb-4">
            Paste large amounts of text content (up to 100KB)
          </p>
          
          <div className="space-y-3">
            <textarea
              value={largeText}
              onChange={(e) => setLargeText(e.target.value)}
              placeholder="Paste your large text content here..."
              className="w-full p-3 border border-gray-300 rounded-lg resize-none"
              rows={6}
              disabled={uploading}
            />
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-500">
                {largeText.length}/100,000 characters
              </span>
              <button
                onClick={handleLargeTextUpload}
                disabled={!largeText.trim() || uploading}
                className="btn-primary disabled:opacity-50"
              >
                {uploading ? 'Uploading...' : 'Upload Text'}
              </button>
            </div>
          </div>
        </motion.div>

        {/* Quick Add Memory */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="card"
        >
          <div className="flex items-center mb-4">
            <PlusIcon className="h-6 w-6 text-purple-600 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Quick Add</h3>
          </div>
          <p className="text-sm text-gray-600 mb-4">
            Add a simple memory with category and tags
          </p>
          
          <div className="space-y-3">
            <textarea
              value={newMemory.content}
              onChange={(e) => setNewMemory({...newMemory, content: e.target.value})}
              placeholder="Enter memory content..."
              className="w-full p-3 border border-gray-300 rounded-lg resize-none"
              rows={3}
            />
            
            <div className="grid grid-cols-2 gap-2">
              <select
                value={newMemory.category}
                onChange={(e) => setNewMemory({...newMemory, category: e.target.value})}
                className="input text-sm"
              >
                <option value="general">General</option>
                <option value="business">Business</option>
                <option value="technical">Technical</option>
                <option value="documents">Documents</option>
                <option value="research">Research</option>
              </select>
              
              <select
                value={newMemory.memory_type}
                onChange={(e) => setNewMemory({...newMemory, memory_type: e.target.value})}
                className="input text-sm"
              >
                <option value="fact">Fact</option>
                <option value="strategy">Strategy</option>
                <option value="gap">Gap</option>
                <option value="opportunity">Opportunity</option>
                <option value="experience">Experience</option>
              </select>
            </div>
            
            <input
              type="text"
              value={newMemory.tags.join(', ')}
              onChange={(e) => setNewMemory({...newMemory, tags: e.target.value.split(',').map(t => t.trim()).filter(t => t)})}
              placeholder="Tags (comma-separated)"
              className="input text-sm"
            />
            
            <button
              onClick={handleAddMemory}
              disabled={!newMemory.content.trim()}
              className="btn-primary w-full disabled:opacity-50"
            >
              Add Memory
            </button>
          </div>
        </motion.div>
      </div>

      {/* Search and Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search memories by content or tags..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="input pl-10"
              />
            </div>
          </div>
          <div className="flex gap-2">
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="input"
            >
              <option value="">All Categories</option>
              {Object.entries(categories).map(([key, category]) => (
                <option key={key} value={key}>
                  {typeof category === 'string' ? category : category.name || key}
                </option>
              ))}
              {/* Add common categories if not in API response */}
              {Object.keys(categories).length === 0 && (
                <>
                  <option value="general">General</option>
                  <option value="business">Business</option>
                  <option value="technical">Technical</option>
                  <option value="documents">Documents</option>
                  <option value="development">Development</option>
                </>
              )}
            </select>
            <select
              value={selectedTags.join(',')}
              onChange={(e) => setSelectedTags(e.target.value ? e.target.value.split(',') : [])}
              className="input"
            >
              <option value="">All Tags</option>
              {Object.entries(availableTags).map(([tag, info]) => (
                <option key={tag} value={tag}>
                  {tag}
                </option>
              ))}
              {/* Add common tags if not in API response */}
              {Object.keys(availableTags).length === 0 && (
                <>
                  <option value="strategy">Strategy</option>
                  <option value="development">Development</option>
                  <option value="business">Business</option>
                  <option value="technical">Technical</option>
                  <option value="research">Research</option>
                  <option value="document">Document</option>
                  <option value="uploaded">Uploaded</option>
                </>
              )}
            </select>
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="btn-outline text-sm px-3 py-2 whitespace-nowrap"
                title="Clear all filters"
              >
                Clear Filters
              </button>
            )}
          </div>
        </div>
        
        {/* Active Filters Display */}
        {hasActiveFilters && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex flex-wrap gap-2 items-center">
              <span className="text-sm text-gray-600">Active filters:</span>
              {searchQuery && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                  Search: "{searchQuery}"
                  <button
                    onClick={() => setSearchQuery('')}
                    className="ml-1 text-blue-600 hover:text-blue-800"
                  >
                    <XMarkIcon className="h-3 w-3" />
                  </button>
                </span>
              )}
              {selectedCategory && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                  Category: {selectedCategory}
                  <button
                    onClick={() => setSelectedCategory('')}
                    className="ml-1 text-green-600 hover:text-green-800"
                  >
                    <XMarkIcon className="h-3 w-3" />
                  </button>
                </span>
              )}
              {selectedTags.map((tag) => (
                <span key={tag} className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-800">
                  Tag: {tag}
                  <button
                    onClick={() => setSelectedTags(selectedTags.filter(t => t !== tag))}
                    className="ml-1 text-purple-600 hover:text-purple-800"
                  >
                    <XMarkIcon className="h-3 w-3" />
                  </button>
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Memory List */}
      <div className="space-y-4">
        {filteredMemories.length === 0 ? (
          <div className="card text-center py-12">
            <CircleStackIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No memories found</h3>
            <p className="text-gray-600 mb-4">
              {hasActiveFilters
                ? 'Try adjusting your search criteria or clear filters'
                : 'Upload files or add memories to get started'
              }
            </p>
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="btn-primary"
              >
                Clear All Filters
              </button>
            )}
          </div>
        ) : (
          filteredMemories.map((memory, index) => {
            const SourceIcon = getSourceTypeIcon(memory.source_type);
            return (
              <motion.div
                key={memory.memory_id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.05 }}
                className="card hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-purple-100 rounded-lg">
                      <SourceIcon className="h-5 w-5 text-purple-600" />
                    </div>
                    <div>
                      <span className={`badge ${getMemoryTypeColor(memory.memory_type)}`}>
                        {memory.memory_type}
                      </span>
                      <span className="badge badge-outline ml-2">
                        {memory.category}
                      </span>
                      {memory.file_name && (
                        <span className="text-xs text-gray-500 ml-2">
                          {memory.file_name} ({formatFileSize(memory.file_size || 0)})
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-medium text-gray-600">
                      {(memory.importance_score * 100).toFixed(0)}%
                    </span>
                    <span className="text-xs text-gray-500">
                      {memory.source_type}
                    </span>
                    <button
                      onClick={() => handleDeleteMemory(memory.memory_id)}
                      className="text-red-500 hover:text-red-700 transition-colors p-1 rounded"
                      title="Delete memory"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <p className="text-gray-900 mb-3 line-clamp-3">{memory.content}</p>

                <div className="flex items-center justify-between">
                  <div className="flex flex-wrap gap-1">
                    {memory.tags.map((tag, tagIndex) => (
                      <span
                        key={tagIndex}
                        className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-800"
                      >
                        <TagIcon className="h-3 w-3 mr-1" />
                        {tag}
                      </span>
                    ))}
                  </div>
                  <span className="text-xs text-gray-500">
                    {formatDate(memory.timestamp || memory.created_at)}
                  </span>
                </div>
              </motion.div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default EnhancedMemory;
