import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { HomeIcon } from '@heroicons/react/24/outline';

const NotFound = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-center"
      >
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-primary-600">404</h1>
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Page Not Found</h2>
          <p className="text-lg text-gray-600 mb-8">
            The page you're looking for doesn't exist in the I PROACTIVE BRICK system.
          </p>
        </div>

        <div className="space-y-4">
          <Link
            to="/"
            className="btn-primary inline-flex items-center"
          >
            <HomeIcon className="h-5 w-5 mr-2" />
            Return to Dashboard
          </Link>
          
          <div className="text-sm text-gray-500">
            <p>Available pages:</p>
            <div className="mt-2 space-x-4">
              <Link to="/orchestration" className="text-primary-600 hover:text-primary-700">
                Orchestration
              </Link>
              <Link to="/bricks" className="text-primary-600 hover:text-primary-700">
                BRICKS
              </Link>
              <Link to="/memory" className="text-primary-600 hover:text-primary-700">
                Memory
              </Link>
              <Link to="/health" className="text-primary-600 hover:text-primary-700">
                Health
              </Link>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default NotFound;
