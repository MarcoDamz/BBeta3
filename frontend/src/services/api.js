import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
});

// Intercepteur pour logger les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      url: error.config?.url,
    });
    return Promise.reject(error);
  },
);

// Agents
export const agentsAPI = {
  list: () => api.get("/agents/"),
  get: (id) => api.get(`/agents/${id}/`),
  create: (data) => api.post("/agents/", data),
  update: (id, data) => api.put(`/agents/${id}/`, data),
  delete: (id) => api.delete(`/agents/${id}/`),
  duplicate: (id) => api.post(`/agents/${id}/duplicate/`),
};

// Conversations
export const conversationsAPI = {
  list: () => api.get("/chat/conversations/"),
  get: (id) => api.get(`/chat/conversations/${id}/`),
  create: (data) => api.post("/chat/conversations/", data),
  delete: (id) => api.delete(`/chat/conversations/${id}/`),
  sendMessage: (data) => api.post("/chat/conversations/send_message/", data),
  autoChat: (data) => api.post("/chat/conversations/auto_chat/", data),
};

// LLM Models
export const llmAPI = {
  getModels: () => api.get("/agents/available-models/"),
};

export default api;
