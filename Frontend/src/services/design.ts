import api from './api';
import { logger } from '../utils/logger';

export interface GenerateDesignRequest {
  room_id: string;
  style: string;
  budget?: number;
}

export interface GenerateDesignResponse {
  design_id: string;
  status: string;
  message: string;
}

export interface FurnitureItem {
  base_price: number;
  adjusted_price: number;
  quantity: number;
}

export interface Design {
  id: string;
  room_id: string;
  user_id: string;
  style: string;
  budget?: number;
  image_1_url?: string;
  image_2_url?: string;
  image_3_url?: string;
  estimated_cost?: number;
  budget_match_percentage?: number;
  furniture_breakdown?: Record<string, FurnitureItem>;
  vastu_score?: number;
  vastu_suggestions?: string[];
  vastu_warnings?: string[];
  status: string;
  created_at: string;
}

export interface DesignWithDetails {
  design: Design;
  room_image_url: string;
  budget_summary: {
    estimated_cost: number;
    budget: number;
    budget_match_percentage: number;
    furniture_breakdown: Record<string, FurnitureItem>;
  } | null;
}

export const generateDesign = async (data: GenerateDesignRequest): Promise<GenerateDesignResponse> => {
  try {
    const response = await api.post('/api/design/generate', data);
    logger.info('Design generation successful', { roomId: data.room_id, style: data.style });
    return response.data;
  } catch (error) {
    logger.error('Design generation failed', { roomId: data.room_id }, error as Error);
    throw error;
  }
};

export const getDesign = async (designId: string): Promise<Design> => {
  try {
    const response = await api.get(`/api/design/${designId}`);
    return response.data;
  } catch (error) {
    logger.error('Get design failed', { designId }, error as Error);
    throw error;
  }
};

export const getRoomDesigns = async (roomId: string): Promise<{ designs: Design[]; total: number }> => {
  try {
    const response = await api.get(`/api/design/room/${roomId}`);
    return response.data;
  } catch (error) {
    logger.error('Get room designs failed', { roomId }, error as Error);
    throw error;
  }
};

export const getRoomDesignsWithDetails = async (roomId: string): Promise<{
  designs: DesignWithDetails[];
  total: number;
  room: {
    id: string;
    image_url: string;
    room_type?: string;
    direction?: string;
  };
}> => {
  try {
    const response = await api.get(`/api/design/room/${roomId}/with-details`);
    return response.data;
  } catch (error) {
    logger.error('Get room designs with details failed', { roomId }, error as Error);
    throw error;
  }
};

export interface CustomizationOptions {
  wall_color?: string;
  flooring?: string;
  furniture_style?: string;
  style?: string;
}

export const regenerateDesign = async (
  designId: string,
  customization: CustomizationOptions
): Promise<Design> => {
  try {
    const response = await api.post(`/api/design/${designId}/regenerate`, customization);
    logger.info('Design regeneration successful', { designId, customization });
    return response.data;
  } catch (error) {
    logger.error('Design regeneration failed', { designId }, error as Error);
    throw error;
  }
};

export const designStyles = [
  { value: 'traditional', label: 'Traditional Indian', description: 'Rich colors and ethnic patterns' },
  { value: 'minimalist', label: 'Minimalist', description: 'Simple, uncluttered spaces' },
  { value: 'luxury', label: 'Luxury', description: 'Premium materials and elegant designs' },
  { value: 'bohemian', label: 'Bohemian', description: 'Eclectic and vibrant decor' },
  { value: 'scandinavian', label: 'Scandinavian', description: 'Light wood and cozy textiles' },
  { value: 'industrial', label: 'Industrial', description: 'Urban style with exposed elements' },
  { value: 'contemporary', label: 'Contemporary', description: 'Current trends and sleek designs' },
];
