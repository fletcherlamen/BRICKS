import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  ChatBubbleLeftRightIcon,
  PaperAirplaneIcon,
  UserIcon,
  CpuChipIcon,
  ClockIcon,
  ServerStackIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [currentUser, setCurrentUser] = useState('james@fullpotential.com');
  const [contextInfo, setContextInfo] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Generate a new session ID for this chat
    const newSessionId = `chat_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(newSessionId);
    
    // Load conversation history from I MEMORY if available
    loadConversationHistory(currentUser, newSessionId);
  }, [currentUser]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversationHistory = async (userId, sessionIdToLoad) => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/chat/history/${userId}?limit=20`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        
        if (data.conversations && data.conversations.length > 0) {
          // Add welcome message with context indicator
          setMessages([{
            id: 'welcome',
            type: 'system',
            content: `Welcome back! I remember our previous conversations. I have ${data.count} conversation exchanges in memory. How can I help you today?`,
            timestamp: new Date().toISOString(),
            hasContext: true
          }]);
          
          setContextInfo({
            conversationCount: data.count,
            hasHistory: true
          });
        } else {
          // New conversation
          setMessages([{
            id: 'welcome',
            type: 'system',
            content: 'Hello! I\'m I CHAT, your conversational AI assistant. I have access to persistent memory and can remember our conversations. What would you like to talk about?',
            timestamp: new Date().toISOString()
          }]);
        }
      }
    } catch (error) {
      console.error('Failed to load conversation history:', error);
      setMessages([{
        id: 'welcome',
        type: 'system',
        content: 'Hello! I\'m I CHAT, your conversational AI assistant. How can I help you today?',
        timestamp: new Date().toISOString()
      }]);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: `user_${Date.now()}`,
      type: 'user',
      content: inputMessage.trim(),
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Send to I CHAT backend with I MEMORY integration
      const response = await fetch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/api/v1/chat/message`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: inputMessage.trim(),
            user_id: currentUser,
            session_id: sessionId,
            context: {
              chat_interface: true,
              timestamp: new Date().toISOString()
            }
          })
        }
      );

      const data = await response.json();
      
      const systemMessage = {
        id: `system_${Date.now()}`,
        type: 'system',
        content: data.response || 'I understand your request.',
        timestamp: data.timestamp || new Date().toISOString(),
        metadata: data.metadata || {},
        contextUsed: data.context_used || false,
        memoryCount: data.memory_count || 0
      };

      setMessages(prev => [...prev, systemMessage]);
      
      // Update context info
      if (data.context_used) {
        setContextInfo({
          conversationCount: (contextInfo?.conversationCount || 0) + 1,
          hasHistory: true,
          lastMemoryCount: data.memory_count
        });
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: `error_${Date.now()}`,
        type: 'system',
        content: 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const getMessageIcon = (type) => {
    switch (type) {
      case 'user': return <UserIcon className="h-5 w-5" />;
      case 'system': return <CpuChipIcon className="h-5 w-5" />;
      default: return <ChatBubbleLeftRightIcon className="h-5 w-5" />;
    }
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <ChatBubbleLeftRightIcon className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-900">I CHAT</h1>
              <p className="text-sm text-gray-600">
                Trinity BRICKS Conversational AI
              </p>
            </div>
          </div>
          
          {/* User Selector */}
          <div className="flex items-center space-x-3">
            {contextInfo && contextInfo.hasHistory && (
              <div className="flex items-center space-x-2 px-3 py-1 bg-purple-50 rounded-lg border border-purple-200">
                <ServerStackIcon className="h-4 w-4 text-purple-600" />
                <span className="text-xs font-medium text-purple-700">
                  {contextInfo.conversationCount} memories
                </span>
              </div>
            )}
            
            <select
              value={currentUser}
              onChange={(e) => setCurrentUser(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="james@fullpotential.com">James</option>
              <option value="vahit@company.com">Vahit</option>
              <option value="fletcher@dev.com">Fletcher</option>
              <option value="alice@company.com">Alice</option>
              <option value="bob@company.com">Bob</option>
            </select>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <motion.div
            key={message.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`flex items-start space-x-3 max-w-3xl ${message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
              {/* Avatar */}
              <div className={`flex-shrink-0 p-2 rounded-lg ${
                message.type === 'user' 
                  ? 'bg-purple-100 text-purple-600' 
                  : message.isError 
                    ? 'bg-red-100 text-red-600'
                    : 'bg-gray-100 text-gray-600'
              }`}>
                {getMessageIcon(message.type)}
              </div>

              {/* Message Content */}
              <div className={`flex flex-col space-y-1 ${message.type === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`px-4 py-3 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-purple-600 text-white'
                    : message.isError
                      ? 'bg-red-50 text-red-800 border border-red-200'
                      : 'bg-gray-50 text-gray-900 border border-gray-200'
                }`}>
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  
                  {/* Context indicator */}
                  {message.contextUsed && (
                    <div className="mt-2 pt-2 border-t border-gray-200 flex items-center space-x-2 text-xs text-gray-600">
                      <SparklesIcon className="h-3 w-3" />
                      <span>Used {message.memoryCount} context memories</span>
                    </div>
                  )}
                  
                  {message.hasContext && (
                    <div className="mt-2 pt-2 border-t border-gray-200 flex items-center space-x-2 text-xs text-gray-600">
                      <ServerStackIcon className="h-3 w-3" />
                      <span>Loaded from I MEMORY</span>
                    </div>
                  )}
                </div>
                
                <div className="flex items-center space-x-2 text-xs text-gray-500">
                  <ClockIcon className="h-3 w-3" />
                  <span>{formatTime(message.timestamp)}</span>
                  {message.metadata?.claude_enabled && (
                    <span className="px-2 py-0.5 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                      Claude
                    </span>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div className="flex items-start space-x-3 max-w-3xl">
              <div className="flex-shrink-0 p-2 rounded-lg bg-gray-100 text-gray-600">
                <CpuChipIcon className="h-5 w-5" />
              </div>
              <div className="px-4 py-3 rounded-lg bg-gray-50 text-gray-600 border border-gray-200">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm">Thinking...</span>
                </div>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex space-x-3">
          <div className="flex-1">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything... I'll remember our conversation."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              rows={2}
              disabled={isLoading}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <PaperAirplaneIcon className="h-5 w-5" />
          </button>
        </div>
        
        <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
          <span>Press Enter to send, Shift+Enter for new line</span>
          <div className="flex items-center space-x-2">
            <ServerStackIcon className="h-3 w-3" />
            <span>Powered by I MEMORY + Claude</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
