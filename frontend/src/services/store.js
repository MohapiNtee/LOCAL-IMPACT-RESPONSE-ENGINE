import { create } from 'zustand';

export const useStore = create((set) => ({
  // Incidents
  incidents: [],
  setIncidents: (incidents) => set({ incidents }),
  addIncident: (incident) => set((state) => ({ incidents: [...state.incidents, incident] })),
  updateIncident: (id, updatedIncident) =>
    set((state) => ({
      incidents: state.incidents.map((i) => (i.id === id ? updatedIncident : i)),
    })),

  // Responders
  responders: [],
  setResponders: (responders) => set({ responders }),
  addResponder: (responder) => set((state) => ({ responders: [...state.responders, responder] })),

  // Nodes
  nodes: [],
  setNodes: (nodes) => set({ nodes }),
  addNode: (node) => set((state) => ({ nodes: [...state.nodes, node] })),

  // UI State
  loading: false,
  setLoading: (loading) => set({ loading }),
  error: null,
  setError: (error) => set({ error }),
}));
