'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  X as XIcon,
  QrCode as QrCodeIcon,
  Smartphone as SmartphoneIcon,
  CheckCircle as CheckCircleIcon,
  AlertTriangle as AlertTriangleIcon,
  Clock as ClockIcon
} from 'lucide-react';
import { QRCodeCanvas } from 'qrcode.react';
import { arService, type ARSessionStatus } from '../../services/arService';

interface QRModalProps {
  isOpen: boolean;
  onClose: () => void;
  designId: string;
  roomId: string;
  userId: string;
}

export default function QRModal({ isOpen, onClose, designId, roomId, userId }: QRModalProps) {
  const [sessionData, setSessionData] = useState<any>(null);
  const [sessionStatus, setSessionStatus] = useState<ARSessionStatus | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);
  const isCreatingSession = useRef(false); // Add ref to prevent duplicates

  // Create AR session when modal opens
  useEffect(() => {
    if (isOpen && designId && roomId && userId && !sessionData && !isLoading && !isCreatingSession.current) {
      createARSession();
    }

    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [isOpen, designId, roomId, userId]); // Remove sessionData from dependencies

  // Reset session when modal closes
  useEffect(() => {
    if (!isOpen) {
      setSessionData(null);
      setSessionStatus(null);
      setError(null);
      setIsLoading(false);
      isCreatingSession.current = false; // Reset ref
    }
  }, [isOpen]);

  // Poll session status
  useEffect(() => {
    if (sessionData?.session_id && sessionStatus?.status === 'pending') {
      // Skip polling for demo sessions
      if (sessionData.session_id.startsWith('demo-session-')) {
        console.log('Skipping status polling for demo session');
        return;
      }

      const interval = setInterval(async () => {
        try {
          const status = await arService.getSessionStatus(sessionData.session_id);
          setSessionStatus(status);

          // Close modal if session is completed
          if (status.status === 'completed') {
            clearInterval(interval);
            setTimeout(() => {
              onClose();
              // Show success notification or update UI
            }, 2000);
          }
        } catch (err) {
          console.error('Error polling session status:', err);
        }
      }, 2000); // Poll every 2 seconds

      setPollingInterval(interval);
    }
  }, [sessionData?.session_id, sessionStatus?.status, onClose]);

  const createARSession = async () => {
    if (isCreatingSession.current) return; // Prevent duplicate calls
    
    isCreatingSession.current = true;
    setIsLoading(true);
    setError(null);

    console.log('Creating AR session with:', { userId, designId, roomId });

    try {
      const response = await arService.createSession({
        user_id: userId,
        design_id: designId,
        room_id: roomId,
      });

      console.log('AR session created:', response);
      setSessionData(response);
      
      // Set proper initial status with all required properties
      setSessionStatus({
        success: true,
        session_id: response.session_id,
        status: 'pending',
        expires_at: response.expires_at,
        created_at: new Date().toISOString()
      });
    } catch (err) {
      console.error('Failed to create AR session:', err);
      setError(err instanceof Error ? err.message : 'Failed to create AR session');
    } finally {
      setIsLoading(false);
      isCreatingSession.current = false; // Reset ref
    }
  };

  const formatTimeRemaining = (expiresAt: string) => {
    // For demo sessions, always show a long time
    if (sessionData?.session_id?.startsWith('demo-session-')) {
      return '60:00';
    }

    try {
      const now = new Date();
      const expires = new Date(expiresAt);
      
      // Check if date is valid
      if (isNaN(expires.getTime())) {
        console.warn('Invalid expiration date:', expiresAt);
        return '60:00'; // Default to 60 minutes
      }
      
      const diff = expires.getTime() - now.getTime();
      
      if (diff <= 0) return 'Expired';
      
      const minutes = Math.floor(diff / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);
      
      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    } catch (error) {
      console.error('Error formatting time:', error);
      return '60:00'; // Default to 60 minutes on error
    }
  };

  const getStatusIcon = () => {
    if (error) return <AlertTriangleIcon className="w-5 h-5 text-red-500" />;
    if (sessionStatus?.status === 'completed') return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
    return <ClockIcon className="w-5 h-5 text-blue-500" />;
  };

  const getStatusText = () => {
    if (error) return 'Error';
    if (sessionStatus?.status === 'completed') return 'Completed';
    if (sessionStatus?.status === 'active') return 'Active';
    return 'Waiting for mobile...';
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="relative bg-white rounded-2xl shadow-2xl max-w-md w-full p-6"
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-[#C6A75E]/10 rounded-xl flex items-center justify-center">
                  <SmartphoneIcon className="w-5 h-5 text-[#C6A75E]" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-[#1F1F1F]">AR Vastu Experience</h2>
                  <p className="text-sm text-gray-600">Scan to experience in AR</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <XIcon className="w-5 h-5 text-gray-500" />
              </button>
            </div>

            {/* Content */}
            <div className="space-y-6">
              {isLoading && (
                <div className="flex flex-col items-center justify-center py-8">
                  <div className="w-12 h-12 border-4 border-[#C6A75E] border-t-transparent rounded-full animate-spin mb-4"></div>
                  <p className="text-gray-600">Creating AR session...</p>
                </div>
              )}

              {error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                  <div className="flex items-start space-x-3">
                    <AlertTriangleIcon className="w-5 h-5 text-red-500 mt-0.5" />
                    <div>
                      <p className="text-red-800 font-medium">Failed to create AR session</p>
                      <p className="text-red-600 text-sm mt-1">{error}</p>
                    </div>
                  </div>
                </div>
              )}

              {sessionData && !isLoading && !error && (
                <>
                  {/* QR Code */}
                  <div className="flex flex-col items-center">
                    <div className="bg-white p-4 rounded-xl border-2 border-gray-200 shadow-sm">
                      <QRCodeCanvas
                        value={sessionData.qr_code_data}
                        size={200}
                        level="M"
                        includeMargin={true}
                        bgColor="#FFFFFF"
                        fgColor="#1F1F1F"
                      />
                    </div>
                    <p className="text-sm text-gray-600 mt-3 text-center">
                      Scan this QR code with your mobile device
                    </p>
                  </div>

                  {/* Instructions */}
                  <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                    <h3 className="font-medium text-blue-900 mb-2">How to use:</h3>
                    <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
                      <li>Open camera on your mobile device</li>
                      <li>Scan the QR code above</li>
                      <li>Wait for AR experience to load</li>
                      <li>Tap to place furniture in your space</li>
                      <li>Capture screenshot when done</li>
                    </ol>
                  </div>

                  {/* Status */}
                  <div className="flex items-center justify-between bg-gray-50 rounded-xl p-3">
                    <div className="flex items-center space-x-2">
                      {getStatusIcon()}
                      <span className="text-sm font-medium text-gray-700">{getStatusText()}</span>
                    </div>
                    {sessionData.expires_at && (
                      <div className="flex items-center space-x-1 text-sm text-gray-500">
                        <ClockIcon className="w-4 h-4" />
                        <span>{formatTimeRemaining(sessionData.expires_at)}</span>
                      </div>
                    )}
                  </div>

                  {/* Success Message */}
                  {sessionStatus?.status === 'completed' && (
                    <div className="bg-green-50 border border-green-200 rounded-xl p-4">
                      <div className="flex items-center space-x-3">
                        <CheckCircleIcon className="w-5 h-5 text-green-500" />
                        <div>
                          <p className="text-green-800 font-medium">AR Session Completed!</p>
                          <p className="text-green-600 text-sm mt-1">
                            Your AR experience has been saved. Check your designs.
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </>
              )}
            </div>

            {/* Footer */}
            <div className="mt-6 pt-4 border-t border-gray-200">
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Session expires in 15 minutes</span>
                <span>Powered by AntarAalay.ai</span>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
