import axios from 'axios';

const api = axios.create({
    baseURL: '/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        // Handle 503 Service Unavailable (Database not initialized)
        if (error.response?.status === 503) {
            console.error('Database connection error:', error.response?.data?.detail);
            // Show user-friendly error message
            if (error.response?.data?.detail?.includes('Database not initialized')) {
                alert('Database connection error. Please check if MongoDB is running and restart the backend server.');
            }
        }
        return Promise.reject(error);
    }
);

export default api;
