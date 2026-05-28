import React from 'react';
import './RespondersPage.css';

const RespondersPage = ({ responders, onRefresh }) => {
  return (
    <div className="responders-page">
      <div className="page-header">
        <h1>Responders Management</h1>
        <button className="btn-primary" onClick={onRefresh}>
          <i className="fas fa-sync"></i> Refresh
        </button>
      </div>

      <div className="responders-grid">
        {responders && responders.length > 0 ? (
          responders.map((responder) => (
            <div key={responder.id} className="responder-card">
              <div className="responder-header">
                <h3>{responder.name}</h3>
                <span className={`status-badge ${responder.status}`}>
                  {responder.status}
                </span>
              </div>
              <div className="responder-info">
                <p><strong>Type:</strong> {responder.responder_type}</p>
                <p><strong>Phone:</strong> {responder.phone || 'N/A'}</p>
                <p><strong>Location:</strong> {responder.location || 'N/A'}</p>
                <p><strong>Available:</strong> {responder.available ? '✓ Yes' : '✗ No'}</p>
              </div>
            </div>
          ))
        ) : (
          <div className="no-responders">No responders found</div>
        )}
      </div>
    </div>
  );
};

export default RespondersPage;
