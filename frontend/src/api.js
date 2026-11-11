import axios from 'axios';

// Demo guest token for seamless access without login
const DEFAULT_DEMO_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIn0.b-VqnmI7m0ex6Da0AwSKlLPW3ejoX0Vy-tNCZoHAufs";

if (!localStorage.getItem('token')) {
  localStorage.setItem('token', DEFAULT_DEMO_TOKEN);
}

// Read main server IP from .env file or default to current browser location hostname
const mainServerIp = import.meta.env.VITE_MAIN_SERVER_IP || window.location.hostname || 'localhost';
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || `http://${mainServerIp}:8005/api`;

const api = axios.create({
  baseURL: apiBaseUrl,
});

// Interceptor to attach the JWT token to every request
api.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem('token');
    if (!token) {
      token = DEFAULT_DEMO_TOKEN;
      localStorage.setItem('token', DEFAULT_DEMO_TOKEN);
    }
    config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // If token expired, renew with default demo token
    if (error.response && error.response.status === 401) {
      localStorage.setItem('token', DEFAULT_DEMO_TOKEN);
    }
    return Promise.reject(error);
  }
);

export default api;
