import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <i className="fas fa-broadcast-tower"></i>
          LIRE
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/" className="nav-links">Dashboard</Link>
          </li>
          <li className="nav-item">
            <Link to="/incidents" className="nav-links">Incidents</Link>
          </li>
          <li className="nav-item">
            <Link to="/responders" className="nav-links">Responders</Link>
          </li>
          <li className="nav-item">
            <Link to="/nodes" className="nav-links">Network</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
