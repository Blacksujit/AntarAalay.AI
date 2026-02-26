/**
 * AR Service API for managing mobile AR visualization sessions
 */

export interface ARSessionCreateRequest {
  user_id: string;
  design_id: string;
  room_id: string;
}

export interface ARSessionCreateResponse {
  success: boolean;
  session_id: string;
  mobile_url: string;
  qr_code_data: string;
  expires_at: string;
}

export interface ARSessionStatus {
  success: boolean;
  session_id: string;
  status: 'pending' | 'active' | 'completed' | 'expired';
  screenshot_url?: string;
  expires_at: string;
  created_at: string;
}

export interface ARSessionCompleteRequest {
  session_id: string;
  screenshot_data: string;
  anchor_transform?: Record<string, any>;
}

export interface ARSessionCompleteResponse {
  success: boolean;
  message: string;
  session_id: string;
  screenshot_url?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const arService = {
  /**
   * Create AR session - SIMPLIFIED DIRECT URL
   */
  async createSession(request: ARSessionCreateRequest): Promise<ARSessionCreateResponse> {
    console.log(' Creating direct AR URL - No sessions needed!');
    
    // Create direct AR URL without backend session
    const arUrl = `https://blacksujit.github.io/AntarAalay.AI?designId=${request.design_id}&roomId=${request.room_id}&userId=${request.user_id}&style=modern`;
    
    return {
      success: true,
      session_id: 'direct-ar-' + Date.now(),
      mobile_url: arUrl,
      qr_code_data: arUrl,
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours
    };
  },

  /**
   * Get AR session status - NOT NEEDED FOR DIRECT AR
   */
  async getSessionStatus(sessionId: string): Promise<ARSessionStatus> {
    // Return active status for direct AR
    return {
      success: true,
      session_id: sessionId,
      status: 'active' as any,
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
      created_at: new Date().toISOString()
    };
  },

  /**
   * Complete AR session - NOT NEEDED FOR DIRECT AR
   */
  async completeSession(request: ARSessionCompleteRequest): Promise<ARSessionCompleteResponse> {
    return {
      success: true,
      session_id: request.session_id,
      screenshot_url: null,
      message: 'Direct AR session completed'
    };
  },

  /**
   * Delete an AR session
   */
  async deleteSession(sessionId: string): Promise<{ success: boolean; message: string }> {
    const response = await fetch(`${API_BASE_URL}/api/ar/session/${sessionId}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to delete AR session');
    }

    return response.json();
  },

  /**
   * Get user's AR sessions
   */
  async getUserSessions(userId: string, limit: number = 10): Promise<{
    success: boolean;
    sessions: any[];
    total: number;
  }> {
    const response = await fetch(`${API_BASE_URL}/api/ar/sessions/user/${userId}?limit=${limit}`);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get user sessions');
    }

    return response.json();
  },
};
