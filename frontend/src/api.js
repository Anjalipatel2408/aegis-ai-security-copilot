import axios from "axios";

const API_BASE = "http://localhost:8000";

export const uploadLog = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return axios.post(`${API_BASE}/upload-log`, formData);
};

export const getLogs = () => axios.get(`${API_BASE}/logs`);
export const parseLog = (logId) => axios.post(`${API_BASE}/parse-log/${logId}`);
export const detectAnomalies = (logId) => axios.post(`${API_BASE}/detect-anomalies/${logId}`);
export const classifyAttacks = (logId) => axios.post(`${API_BASE}/classify-attacks/${logId}`);
export const getAttackSummary = (logId) => axios.get(`${API_BASE}/attack-summary/${logId}`);
export const getRemediation = (entryId) => axios.get(`${API_BASE}/remediation/${entryId}`);