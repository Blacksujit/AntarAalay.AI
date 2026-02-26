'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  SmartphoneIcon, 
  AlertTriangleIcon, 
  Loader2Icon,
  CheckCircleIcon
} from 'lucide-react';
import { arService } from '../../../services/arService';
import ARViewer from '../../../components/ar/ARViewer';

export default function ARSessionPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = (params?.sessionId as string) || '';

  const [sessionStatus, setSessionStatus] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCompleted, setIsCompleted] = useState(false);

  // Validate session on mount
  useEffect(() => {
    validateSession();
  }, [sessionId]);

  const validateSession = async () => {
    if (!sessionId) return;

    try {
      const status = await arService.getSessionStatus(sessionId);
      setSessionStatus(status);

      if (status.status === 'expired') {
        setError('This AR session has expired. Please create a new session.');
      } else if (status.status === 'completed') {
        setIsCompleted(true);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Invalid session');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSessionComplete = async (screenshot: string, transform: any) => {
    try {
      await arService.completeSession({
        session_id: sessionId,
        screenshot_data: screenshot,
        anchor_transform: transform
      });

      setIsCompleted(true);
      
      // Show success message and close
      setTimeout(() => {
        try {
          window.close();
        } catch {
          window.location.href = '/dashboard';
        }
      }, 3000);
    } catch (err) {
      setError('Failed to save AR session. Please try again.');
    }
  };

  if (isCompleted) {
    return (
      <div className="min-h-screen bg-[#F4EFE6] flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg p-6 max-w-md w-full text-center">
          <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-full mx-auto mb-4">
            <CheckCircleIcon className="w-6 h-6 text-green-600" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">AR Session Completed!</h2>
          <p className="text-gray-600 mb-6">
            Your AR experience has been saved successfully. This window will close automatically.
          </p>
          <div className="animate-pulse">
            <p className="text-sm text-gray-500">Closing...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#F4EFE6] flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg p-6 max-w-md w-full">
          <div className="flex items-center justify-center w-12 h-12 bg-red-100 rounded-full mx-auto mb-4">
            <AlertTriangleIcon className="w-6 h-6 text-red-600" />
          </div>
          <h2 className="text-xl font-bold text-center text-gray-900 mb-2">AR Session Error</h2>
          <p className="text-gray-600 text-center mb-6">{error}</p>
          <button
            onClick={() => {
              try {
                window.close();
              } catch {
                window.location.href = '/dashboard';
              }
            }}
            className="w-full bg-[#C6A75E] text-white py-2 px-4 rounded-lg hover:bg-[#B89A4F] transition-colors"
          >
            Close Window
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F4EFE6]">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-md mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <SmartphoneIcon className="w-6 h-6 text-[#C6A75E]" />
              <div>
                <h1 className="text-lg font-bold text-gray-900">AR Vastu Experience</h1>
                <p className="text-sm text-gray-600">Session: {sessionId?.slice(0, 8)}...</p>
              </div>
            </div>
            <button
              onClick={() => {
                try {
                  window.close();
                } catch {
                  window.location.href = '/dashboard';
                }
              }}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              ×
            </button>
          </div>
        </div>
      </div>

      {/* AR Viewer */}
      <div className="max-w-md mx-auto p-4">
        <ARViewer 
          sessionId={sessionId} 
          onSessionComplete={handleSessionComplete}
        />
      </div>
    </div>
  );
}
