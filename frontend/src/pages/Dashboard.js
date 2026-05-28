import React from 'react';
import StatCard from '../components/StatCard';
import IncidentTable from '../components/IncidentTable';
import './Dashboard.css';

const Dashboard = ({ incidents, responders, nodes, loading }) => {
  const activeIncidents = incidents?.filter(i => i.status === 'active').length || 0;
  const resolvedIncidents = incidents?.filter(i => i.status === 'resolved').length || 0;
  const availableResponders = responders?.filter(r => r.available).length || 0;
  const onlineNodes = nodes?.filter(n => n.status === 'online').length || 0;

  return (
    <div className="dashboard">
      <h1>System Dashboard</h1>

      <div className="stats-grid">
        <StatCard
          title="Total Incidents"
          value={incidents?.length || 0}
          icon="fa-exclamation-circle"
          color="primary"
        />
        <StatCard
          title="Active Incidents"
          value={activeIncidents}
          icon="fa-fire"
          color="danger"
        />
        <StatCard
          title="Resolved"
          value={resolvedIncidents}
          icon="fa-check-circle"
          color="success"
        />
        <StatCard
          title="Available Responders"
          value={availableResponders}
          icon="fa-user-shield"
          color="warning"
        />
        <StatCard
          title="Online Nodes"
          value={onlineNodes}
          icon="fa-network-wired"
          color="primary"
        />
        <StatCard
          title="Total Network Nodes"
          value={nodes?.length || 0}
          icon="fa-sitemap"
          color="success"
        />
      </div>

      <div className="recent-incidents">
        <h2>Recent Incidents</h2>
        <IncidentTable incidents={incidents?.slice(0, 10)} />
      </div>
    </div>
  );
};

export default Dashboard;
