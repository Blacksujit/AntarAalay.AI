import api from './api';
import { logger } from '../utils/logger';

export interface Room {
  room_id: string;
  images: {
    north: string;
    south: string;
    east: string;
    west: string;
  };
  status: string;
  created_at: string;
}

export const getRoom = async (roomId: string): Promise<Room> => {
  try {
    const response = await api.get(`/api/room/${roomId}`);
    return response.data;
  } catch (error) {
    logger.error('Failed to fetch room', { roomId }, error as Error);
    throw error;
  }
};
