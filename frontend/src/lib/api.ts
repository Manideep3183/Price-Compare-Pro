import axios from 'axios';
import { AuthAPI } from './firebase';

// Support both VITE_API_URL (production) and VITE_API_BASE_URL (development)
const API_BASE_URL = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || 'https://price-compare-pro-1.onrender.com';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to all requests
apiClient.interceptors.request.use(
  async (config) => {
    try {
      const token = await AuthAPI.getIdToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
        console.log('🔑 Auth token attached to request:', config.url);
      } else {
        console.warn('⚠️ No auth token available for request:', config.url);
      }
    } catch (error) {
      console.error('❌ Failed to get auth token:', error);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle auth errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login if unauthorized
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// User activity logging
export const logUserActivity = async (event: string, payload?: any) => {
  try {
    await apiClient.post('/api/v1/activity', {
      event,
      payload: payload || {},
    });
  } catch (error) {
    console.error('Failed to log activity:', error);
  }
};

// Save search query
export const saveSearch = async (query: string, resultsCount: number = 0) => {
  try {
    await apiClient.post('/api/v1/searches', {
      query,
      results_count: resultsCount,
    });
  } catch (error) {
    console.error('Failed to save search:', error);
    throw error; // Re-throw so we can see the actual error
  }
};

// Get user's search history
export const getUserSearches = async (limit: number = 20) => {
  try {
    const response = await apiClient.get(`/api/v1/searches?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Failed to get searches:', error);
    return [];
  }
};

// Activity tracking
export const trackActivity = async (event: string, payload?: Record<string, any>) => {
  try {
    await apiClient.post('/api/v1/activity', {
      event,
      payload: payload || {},
    });
  } catch (error) {
    // Silent fail for analytics - don't disrupt user experience
    console.error('Failed to track activity:', error);
  }
};

// Get user's activity history
export const getUserActivity = async (limit: number = 50, eventType?: string) => {
  try {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (eventType) params.append('event_type', eventType);
    
    const response = await apiClient.get(`/api/v1/activity?${params.toString()}`);
    return response.data;
  } catch (error) {
    console.error('Failed to get activity:', error);
    return [];
  }
};

// Get user profile with stats
export const getUserProfile = async () => {
  try {
    const response = await apiClient.get('/api/v1/profile');
    return response.data;
  } catch (error) {
    console.error('Failed to get profile:', error);
    return null;
  }
};

// Create or update user profile in MongoDB
export const createOrUpdateUserProfile = async (data: {
  display_name?: string;
  phone_number?: string;
  auth_provider: 'email' | 'google';
}) => {
  try {
    const response = await apiClient.post('/api/v1/users/create-or-update', data);
    console.log('✅ User profile saved:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Failed to save user profile:', error);
    throw error;
  }
};

// Get current user's profile from MongoDB
export const getUserProfileFromDB = async () => {
  try {
    const response = await apiClient.get('/api/v1/users/me');
    return response.data;
  } catch (error) {
    console.error('Failed to get user profile from DB:', error);
    return null;
  }
};

// Check if user exists in MongoDB database
export const checkUserExists = async () => {
  try {
    const response = await apiClient.get('/api/v1/users/check-exists');
    return response.data.exists;
  } catch (error) {
    console.error('Failed to check user existence:', error);
    return false;
  }
};

// Delete current user account and all associated data
export const deleteUserAccount = async () => {
  try {
    const response = await apiClient.delete('/api/v1/users/me');
    console.log('✅ User account deleted:', response.data);
    return response.data;
  } catch (error) {
    console.error('❌ Failed to delete user account:', error);
    throw error;
  }
};
