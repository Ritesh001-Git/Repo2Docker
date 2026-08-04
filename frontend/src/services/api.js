import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
});

export const createBuild = (payload) => api.post("/build", payload);
export const getStatus = (buildId) => api.get(`/status/${buildId}`);
export const getLogs = (buildId) => api.get(`/logs/${buildId}`);

export default api;
