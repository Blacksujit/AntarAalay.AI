import api from './api';
import { logger } from '../utils/logger';

export interface UploadRoomRequest {
  north: File;
  south: File;
  east: File;
  west: File;
}

export interface UploadRoomResponse {
  room_id: string;
  images: {
    north: string;
    south: string;
    east: string;
    west: string;
  };
  status: string;
}

export interface Room {
  room_id: string;
  user_id: string;
  images: {
    north: string;
    south: string;
    east: string;
    west: string;
  };
  room_type?: string;
  direction?: string;
  created_at: string;
}

export const uploadRoom = async (data: UploadRoomRequest | FormData): Promise<UploadRoomResponse> => {
  try {
    let formData: FormData;
    
    if (data instanceof FormData) {
      formData = data;
    } else {
      formData = new FormData();
      formData.append('north', data.north);
      formData.append('south', data.south);
      formData.append('east', data.east);
      formData.append('west', data.west);
    }

    const response = await api.post('/api/room/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    logger.info('Room upload successful', { roomId: response.data.room_id });
    return response.data;
  } catch (error) {
    logger.error('Room upload failed', {}, error as Error);
    throw error;
  }
};

export const getRoom = async (roomId: string): Promise<Room> => {
  try {
    const response = await api.get(`/api/room/${roomId}`);
    return response.data;
  } catch (error) {
    logger.error('Get room failed', { roomId }, error as Error);
    throw error;
  }
};

export const getUserRooms = async (): Promise<{ rooms: Room[]; total: number }> => {
  try {
    const response = await api.get('/api/room/user/rooms');
    return response.data;
  } catch (error) {
    logger.error('Get user rooms failed', {}, error as Error);
    throw error;
  }
};

export const validateImageFile = (file: File): { valid: boolean; error?: string } => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  const maxSize = 10 * 1024 * 1024; // 10MB

  if (!allowedTypes.includes(file.type)) {
    return { valid: false, error: 'Only JPEG, PNG, and WebP images are allowed' };
  }

  if (file.size > maxSize) {
    return { valid: false, error: 'File size must be less than 10MB' };
  }

  return { valid: true };
};
