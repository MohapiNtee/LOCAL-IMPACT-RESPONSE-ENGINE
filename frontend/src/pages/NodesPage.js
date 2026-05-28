import React from 'react';
import './NodesPage.css';

const NodesPage = ({ nodes, onRefresh }) => {
  return (
    <div className="nodes-page">
      <div className="page-header">
        <h1>Network Nodes</h1>
        <button className="btn-primary" onClick={onRefresh}>
          <i className="fas fa-sync"></i> Refresh
        </button>
      </div>

      <div className="nodes-grid">
        {nodes && nodes.length > 0 ? (
          nodes.map((node) => (
            <div key={node.id} className="node-card">
              <div className="node-header">
                <h3>{node.name}</h3>
                <span className={`node-status ${node.status}`}>
                  <i className="fas fa-circle"></i> {node.status}
                </span>
              </div>
              <div className="node-info">
                <p><strong>Type:</strong> {node.node_type}</p>
                <p><strong>IP:</strong> {node.ip_address || 'N/A'}</p>
                <p><strong>Location:</strong> {node.location || 'N/A'}</p>
              </div>
              <div className="node-metrics">
                <div className="metric">
                  <label>CPU</label>
                  <div className="metric-bar">
                    <div className="metric-fill" style={{ width: `${node.cpu_usage}%` }}></div>
                  </div>
                  <span>{node.cpu_usage}%</span>
                </div>
                <div className="metric">
                  <label>Memory</label>
                  <div className="metric-bar">
                    <div className="metric-fill" style={{ width: `${node.memory_usage}%` }}></div>
                  </div>
                  <span>{node.memory_usage}%</span>
                </div>
              </div>
              <div className="node-load">
                <p>Load: {node.current_load}/{node.capacity}</p>
              </div>
            </div>
          ))
        ) : (
          <div className="no-nodes">No network nodes found</div>
        )}
      </div>
    </div>
  );
};

export default NodesPage;
