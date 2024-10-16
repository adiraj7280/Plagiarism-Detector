import React from 'react';
import { Link } from 'react-router-dom';
import { FileCheck, Upload, Bot } from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul>
        <NavItem to="/" icon={<FileCheck size={18} />} text="1 v 1 Check" />
        <NavItem to="/batch-upload" icon={<Upload size={18} />} text="Batch Upload" />
        <NavItem to="/ai-check" icon={<Bot size={18} />} text="AI Check" />
      </ul>
    </nav>
  );
};

const NavItem = ({ to, icon, text }) => (
  <li>
    <Link to={to}>
      {icon}
      <span>{text}</span>
    </Link>
  </li>
);

export default Navbar;