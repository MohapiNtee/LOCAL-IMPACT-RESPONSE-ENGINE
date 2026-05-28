import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Incidents API
export const incidentsApi = {
  getAll: () => apiClient.get('/incidents/'),
  getById: (id) => apiClient.get(`/incidents/${id}/`),
  create: (data) => apiClient.post('/incidents/', data),
  update: (id, data) => apiClient.patch(`/incidents/${id}/`, data),
  resolve: (id) => apiClient.post(`/incidents/${id}/resolve/`),
  getStatistics: () => apiClient.get('/incidents/statistics/'),
};

// Responders API
export const respondersApi = {
  getAll: () => apiClient.get('/responders/'),
  getById: (id) => apiClient.get(`/responders/${id}/`),
  create: (data) => apiClient.post('/responders/', data),
  update: (id, data) => apiClient.patch(`/responders/${id}/`, data),
  getAvailable: () => apiClient.get('/responders/available/'),
  assignToIncident: (responderId, incidentId) =>
    apiClient.post(`/responders/${responderId}/assign_to_incident/`, { incident_id: incidentId }),
};

// Nodes API
export const nodesApi = {
  getAll: () => apiClient.get('/nodes/'),
  getById: (id) => apiClient.get(`/nodes/${id}/`),
  create: (data) => apiClient.post('/nodes/', data),
  sendHeartbeat: (id, metrics) => apiClient.post(`/nodes/${id}/heartbeat/`, metrics),
  getHealthyNodes: () => apiClient.get('/nodes/healthy_nodes/'),
  getNetworkStatus: () => apiClient.get('/nodes/network_status/'),
};

export default apiClient;
