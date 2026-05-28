import React from 'react';
import './StatCard.css';

const StatCard = ({ title, value, icon, color }) => {
  return (
    <div className={`stat-card ${color}`}>
      <div className="stat-icon">
        <i className={`fas ${icon}`}></i>
      </div>
      <div className="stat-content">
        <h3>{title}</h3>
        <p className="stat-value">{value}</p>
      </div>
    </div>
  );
};

export default StatCard;
