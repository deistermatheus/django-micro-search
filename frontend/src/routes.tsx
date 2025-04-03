import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

import About from './pages/about'
import Home from './pages/home';
import Documents from './pages/documents';
import Images from './pages/images';


const AppRoutes: React.FC = () => {
  return (
    <Router>
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
            <Link to="/documents">Documents</Link>
            <Link to="/images">Images</Link>
            <Link to="/about">About</Link>
          </li>
        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/images" element={<Images />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;