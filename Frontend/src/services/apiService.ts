/**
 * Enterprise API Service Layer
 * AntarAalay.ai - API Integration with Error Handling
 */

import axios, { AxiosError, type AxiosInstance } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for AI generation
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = window.localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      if (typeof window !== 'undefined') {
        window.localStorage.removeItem('auth_token');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Types
export interface UploadResponse {
  room_id: string;
  message: string;
  images: {
    north: string;
    south: string;
    east: string;
    west: string;
  };
}

export interface GenerateRequest {
  room_id: string;
  style: string;
  room_type?: string;
  budget?: number;
  wall_color?: string;
  flooring_material?: string;
}

export interface GenerateResponse {
  design_id: string;
  status: string;
  message: string;
}

export interface Design {
  id: string;
  room_id: string;
  user_id: string;
  style: string;
  budget?: number;
  wall_color?: string;
  flooring_material?: string;
  image_1_url?: string;
  image_2_url?: string;
  image_3_url?: string;
  estimated_cost?: number;
  budget_match_percentage?: number;
  vastu_score?: number;
  vastu_suggestions?: string[];
  vastu_warnings?: string[];
  status: string;
  created_at: string;
}

export interface DashboardStats {
  totalDesigns: number;
  thisMonth: number;
  avgGenerationTime: number;
  favoriteStyle: string;
}

export interface DashboardResponse {
  status: string;
  stats: DashboardStats;
  recentDesigns: Design[];
}

export interface VastuAnalyzeRequest {
  direction: string;
  room_type: string;
}

export interface VastuAnalyzeResponse {
  vastu_score: number;
  suggestions: string[];
  warnings: string[];
  direction_rating: string;
  element_balance?: {
    dominant_element: string;
  };
}

export interface UploadOrientationMetadata {
  orientation_degree: number;
  compass_confirmed?: boolean;
}

// Upload Service
export const uploadService = {
  async uploadRoomImages(
    files: {
      north: File;
      south: File;
      east: File;
      west: File;
    },
    onProgress?: (progress: number) => void,
    orientation?: UploadOrientationMetadata
  ): Promise<UploadResponse> {
    // Validate files
    const requiredFiles = ['north', 'south', 'east', 'west'] as const;
    for (const direction of requiredFiles) {
      const file = files[direction];
      if (!file) {
        throw new Error(`${direction} image is required`);
      }
      
      // Check file type
      const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
      if (!allowedTypes.includes(file.type)) {
        throw new Error(`${direction} image must be JPEG, PNG, or WebP format`);
      }
      
      // Check file size (10MB limit)
      const maxSize = 10 * 1024 * 1024; // 10MB
      if (file.size > maxSize) {
        throw new Error(`${direction} image must be smaller than 10MB`);
      }
    }

    const formData = new FormData();
    formData.append('north', files.north);
    formData.append('south', files.south);
    formData.append('east', files.east);
    formData.append('west', files.west);

    if (orientation) {
      formData.append('orientation_degree', String(orientation.orientation_degree));
      if (typeof orientation.compass_confirmed !== 'undefined') {
        formData.append('compass_confirmed', String(orientation.compass_confirmed));
      }
    }

    const postUpload = async (data: FormData) => {
      return apiClient.post<UploadResponse>('/api/room/upload', data, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            onProgress(progress);
          }
        },
      });
    };

    try {
      const response = await postUpload(formData);
      
      return response.data;
    } catch (error: any) {
      const status = error.response?.status;
      const hasOrientation = !!orientation;

      if (hasOrientation && (status === 400 || status === 401 || status === 403 || status === 404 || status === 413 || status === 422)) {
        const retryFormData = new FormData();
        retryFormData.append('north', files.north);
        retryFormData.append('south', files.south);
        retryFormData.append('east', files.east);
        retryFormData.append('west', files.west);

        try {
          const response = await postUpload(retryFormData);
          return response.data;
        } catch (retryError: any) {
          error = retryError;
        }
      }

      // Enhanced error handling
      if (error.response?.data?.detail) {
        throw new Error(error.response.data.detail);
      } else if (error.response?.status === 413) {
        throw new Error('Files are too large. Please ensure each image is under 10MB.');
      } else if (error.response?.status === 400) {
        throw new Error('Invalid file format. Please use JPEG, PNG, or WebP images.');
      } else if (error.response?.status === 401) {
        throw new Error('Please log in to upload images.');
      } else {
        throw new Error('Upload failed. Please try again.');
      }
    }
  },
};

// Design Service
export const designService = {
  async generateDesign(request: GenerateRequest): Promise<GenerateResponse> {
    const response = await apiClient.post<GenerateResponse>('/api/design/generate', request);
    return response.data;
  },

  async regenerateDesign(
    designId: string,
    customizations: Partial<GenerateRequest>
  ): Promise<GenerateResponse> {
    const response = await apiClient.post<GenerateResponse>(
      `/api/design/${designId}/regenerate`,
      customizations
    );
    return response.data;
  },

  async getUserDesigns(): Promise<Design[]> {
    const response = await apiClient.get<{ designs: Design[] }>('/api/design/user');
    return response.data.designs;
  },

  async getDesignById(id: string): Promise<Design> {
    const response = await apiClient.get<Design>(`/api/design/${id}`);
    return response.data;
  },
};

// Dashboard Service
export const dashboardService = {
  async getStats(): Promise<DashboardResponse> {
    const response = await apiClient.get<DashboardResponse>('/api/dashboard/stats');
    return response.data;
  },
};

// Vastu Service
export const vastuService = {
  async analyzeVastu(request: VastuAnalyzeRequest): Promise<VastuAnalyzeResponse> {
    const response = await apiClient.post<VastuAnalyzeResponse>('/api/vastu/analyze', request);
    return response.data;
  },

  async getVastuScore(direction: string, roomType: string): Promise<{
    direction: string;
    room_type: string;
    vastu_score: number;
    rating: string;
    element: string;
  }> {
    const response = await apiClient.get(
      `/api/vastu/score/${direction}/${roomType}`
    );
    return response.data;
  },

  async getVastuRemedies(direction: string, roomType: string): Promise<{
    direction: string;
    room_type: string;
    current_score: number;
    remedies: string[];
    improvement_potential: number;
  }> {
    const response = await apiClient.get(
      `/api/vastu/remedies/${direction}/${roomType}`
    );
    return response.data;
  },
};

// Error Handler Helper
export const handleApiError = (error: AxiosError): string => {
  if (error.response) {
    // Server returned an error response
    const status = error.response.status;
    const data = error.response.data as any;

    switch (status) {
      case 400:
        return data.detail || 'Invalid request. Please check your input.';
      case 401:
        return 'Session expired. Please log in again.';
      case 403:
        return 'You do not have permission to perform this action.';
      case 404:
        return 'Resource not found.';
      case 429:
        return 'Rate limit exceeded. Please try again later.';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return data.detail || 'An unexpected error occurred.';
    }
  } else if (error.request) {
    // Request was made but no response received
    return 'Network error. Please check your internet connection.';
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred.';
  }
};

export default apiClient;
