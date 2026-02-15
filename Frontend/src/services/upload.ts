import api from './api';

export interface UploadRoomRequest {
  file: File;
  roomType?: string;
  direction?: string;
}

export interface UploadRoomResponse {
  room_id: string;
  image_url: string;
  message: string;
}

export interface Room {
  id: string;
  user_id: string;
  image_url: string;
  room_type?: string;
  direction?: string;
  created_at: string;
}

export const uploadRoom = async (data: UploadRoomRequest): Promise<UploadRoomResponse> => {
  const formData = new FormData();
  formData.append('file', data.file);
  if (data.roomType) formData.append('room_type', data.roomType);
  if (data.direction) formData.append('direction', data.direction);

  const response = await api.post('/api/room/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getRoom = async (roomId: string): Promise<Room> => {
  const response = await api.get(`/api/room/${roomId}`);
  return response.data;
};

export const getUserRooms = async (): Promise<{ rooms: Room[]; total: number }> => {
  const response = await api.get('/api/room/user/rooms');
  return response.data;
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
