import api from './api';

export interface VastuAnalyzeRequest {
  direction: string;
  room_type: string;
}

export interface VastuAnalyzeResponse {
  vastu_score: number;
  suggestions: string[];
  warnings: string[];
  direction_rating: string;
  element_balance: {
    dominant_element: string;
    ruling_planet: string;
    balance_status: string;
  };
}

export interface VastuDirectionInfo {
  direction: string;
  ruling_element: string;
  suitable_rooms: string[];
  colors: string[];
  tips: string[];
}

export const analyzeVastu = async (data: VastuAnalyzeRequest): Promise<VastuAnalyzeResponse> => {
  const response = await api.post('/api/vastu/analyze', data);
  return response.data;
};

export const getDirectionInfo = async (direction: string): Promise<VastuDirectionInfo> => {
  const response = await api.get(`/api/vastu/direction/${direction}`);
  return response.data;
};

export const getVastuScore = async (direction: string, roomType: string): Promise<{
  direction: string;
  room_type: string;
  vastu_score: number;
  rating: string;
  element: string;
}> => {
  const response = await api.get(`/api/vastu/score/${direction}/${roomType}`);
  return response.data;
};

export const getVastuRemedies = async (direction: string, roomType: string): Promise<{
  direction: string;
  room_type: string;
  current_score: number;
  remedies: string[];
  improvement_potential: number;
}> => {
  const response = await api.get(`/api/vastu/remedies/${direction}/${roomType}`);
  return response.data;
};

export const getAllDirections = async (): Promise<{ directions: {
  direction: string;
  element: string;
  suitable_rooms: string[];
  colors: string[];
}[] }> => {
  const response = await api.get('/api/vastu/directions');
  return response.data;
};

export const roomTypes = [
  { value: 'bedroom', label: 'Bedroom' },
  { value: 'living', label: 'Living Room' },
  { value: 'kitchen', label: 'Kitchen' },
  { value: 'dining', label: 'Dining Room' },
  { value: 'study', label: 'Study/Office' },
  { value: 'bathroom', label: 'Bathroom' },
];

export const directions = [
  { value: 'north', label: 'North', element: 'Water' },
  { value: 'south', label: 'South', element: 'Fire' },
  { value: 'east', label: 'East', element: 'Air' },
  { value: 'west', label: 'West', element: 'Space' },
  { value: 'northeast', label: 'Northeast', element: 'Water' },
  { value: 'northwest', label: 'Northwest', element: 'Air' },
  { value: 'southeast', label: 'Southeast', element: 'Fire' },
  { value: 'southwest', label: 'Southwest', element: 'Earth' },
];

export const getDirectionColor = (direction: string): string => {
  const colors: Record<string, string> = {
    north: 'bg-blue-500',
    south: 'bg-red-500',
    east: 'bg-green-500',
    west: 'bg-purple-500',
    northeast: 'bg-cyan-400',
    northwest: 'bg-sky-400',
    southeast: 'bg-orange-500',
    southwest: 'bg-amber-600',
  };
  return colors[direction] || 'bg-gray-500';
};

export const getElementIcon = (element: string): string => {
  const icons: Record<string, string> = {
    Water: '💧',
    Fire: '🔥',
    Air: '💨',
    Space: '🌌',
    Earth: '🌍',
  };
  return icons[element] || '⬜';
};
