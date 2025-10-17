import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Orchestration from './pages/Orchestration';
import Bricks from './pages/Bricks';
import Memory from './pages/Memory';
import Chat from './pages/Chat';
import Assess from './pages/Assess';
import UbicHealth from './pages/UbicHealth';
import Strategic from './pages/Strategic';
import Revenue from './pages/Revenue';
import NotFound from './pages/NotFound';

function App() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen bg-gray-50"
    >
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/orchestration" element={<Orchestration />} />
          <Route path="/bricks" element={<Bricks />} />
          <Route path="/memory" element={<Memory />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/assess" element={<Assess />} />
          <Route path="/strategic" element={<Strategic />} />
          <Route path="/revenue" element={<Revenue />} />
          <Route path="/health" element={<UbicHealth />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Layout>
    </motion.div>
  );
}

export default App;