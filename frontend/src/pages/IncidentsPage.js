import React, { useState } from 'react';
import './IncidentsPage.css';
import IncidentTable from '../components/IncidentTable';

const IncidentsPage = ({ incidents, onRefresh }) => {
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterType, setFilterType] = useState('all');

  const filteredIncidents = incidents?.filter((incident) => {
    const statusMatch = filterStatus === 'all' || incident.status === filterStatus;
    const typeMatch = filterType === 'all' || incident.incident_type === filterType;
    return statusMatch && typeMatch;
  }) || [];

  return (
    <div className="incidents-page">
      <div className="page-header">
        <h1>Incidents Management</h1>
        <button className="btn-primary" onClick={onRefresh}>
          <i className="fas fa-sync"></i> Refresh
        </button>
      </div>

      <div className="filters">
        <div className="filter-group">
          <label>Status:</label>
          <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>

        <div className="filter-group">
          <label>Type:</label>
          <select value={filterType} onChange={(e) => setFilterType(e.target.value)}>
            <option value="all">All</option>
            <option value="accident">Accident</option>
            <option value="hijacking">Hijacking</option>
            <option value="medical">Medical</option>
            <option value="fire">Fire</option>
            <option value="crime">Crime</option>
          </select>
        </div>
      </div>

      <IncidentTable incidents={filteredIncidents} />
    </div>
  );
};

export default IncidentsPage;
