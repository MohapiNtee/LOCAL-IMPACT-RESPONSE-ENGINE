import React from 'react';
import './IncidentTable.css';

const IncidentTable = ({ incidents }) => {
  const getStatusBadge = (status) => {
    const statusClasses = {
      active: 'badge-danger',
      in_progress: 'badge-warning',
      resolved: 'badge-success',
      cancelled: 'badge-secondary'
    };
    return statusClasses[status] || 'badge-secondary';
  };

  return (
    <div className="incident-table">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
            <th>Location</th>
            <th>Status</th>
            <th>Severity</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          {incidents && incidents.length > 0 ? (
            incidents.map((incident) => (
              <tr key={incident.id}>
                <td>{incident.id.substring(0, 8)}</td>
                <td>{incident.incident_type}</td>
                <td>{incident.location}</td>
                <td>
                  <span className={`badge ${getStatusBadge(incident.status)}`}>
                    {incident.status}
                  </span>
                </td>
                <td>{incident.severity}/10</td>
                <td>{new Date(incident.created_at).toLocaleDateString()}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="6" className="no-data">No incidents found</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default IncidentTable;
