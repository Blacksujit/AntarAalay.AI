import { describe, it, expect, vi, beforeEach } from 'vitest';
import { uploadRoom, validateImageFile } from '../../services/upload';
import api from '../../services/api';

// Mock the API module
vi.mock('../../services/api', () => ({
  default: {
    post: vi.fn(),
  },
}));

describe('UploadService', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('validateImageFile', () => {
    it('should accept valid image types (JPEG, PNG, WebP)', () => {
      const validFile = new File(['test'], 'test.jpg', { type: 'image/jpeg' });
      const result = validateImageFile(validFile);
      expect(result.valid).toBe(true);
      expect(result.error).toBeUndefined();
    });

    it('should reject invalid image types', () => {
      const invalidFile = new File(['test'], 'test.gif', { type: 'image/gif' });
      const result = validateImageFile(invalidFile);
      expect(result.valid).toBe(false);
      expect(result.error).toContain('Only JPEG, PNG, and WebP');
    });

    it('should reject files larger than 10MB', () => {
      // Create a large file using Uint8Array instead of ArrayBuffer
      const largeContent = new Uint8Array(11 * 1024 * 1024);
      const largeFile = new File([largeContent], 'large.jpg', { type: 'image/jpeg' });
      const result = validateImageFile(largeFile);
      expect(result.valid).toBe(false);
      expect(result.error).toContain('less than 10MB');
    });
  });

  describe('uploadRoom', () => {
    it('should upload room with correct form data', async () => {
      const mockResponse = {
        data: {
          room_id: 'room-123',
          image_url: 'https://firebase.com/room.jpg',
          message: 'Upload successful'
        }
      };

      (api.post as any).mockResolvedValue(mockResponse);

      const file = new File(['test'], 'room.jpg', { type: 'image/jpeg' });
      const result = await uploadRoom({
        file,
        roomType: 'bedroom',
        direction: 'north'
      });

      expect(api.post).toHaveBeenCalledWith(
        '/api/room/upload',
        expect.any(FormData),
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      expect(result.room_id).toBe('room-123');
    });
  });
});
