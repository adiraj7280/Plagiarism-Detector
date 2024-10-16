import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import OneVsOneCheck from './pages/OneVsOneCheck';
import AIBasedCheck from './pages/AIBasedCheck';
import BatchUpload from './pages/BatchUpload';

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<OneVsOneCheck />} />
        <Route path="/batch-upload" element={<BatchUpload />} />
        <Route path="/ai-check" element={<AIBasedCheck />} />
      </Routes>
    </Router>
  );
};

export default App;