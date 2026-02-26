'use client';

import { useEffect, useRef, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  CameraIcon, 
  Move3DIcon, 
  Maximize2Icon,
  SaveIcon,
  CompassIcon
} from 'lucide-react';

// WebXR type declarations
declare global {
  interface Navigator {
    xr?: {
      isSessionSupported(mode: string): Promise<boolean>;
      requestSession(mode: string, options?: XRSessionInit): Promise<XRSession>;
    };
  }
}

interface XRSessionInit {
  requiredFeatures?: string[];
  optionalFeatures?: string[];
}

interface XRSession extends EventTarget {
  updateRenderState(state: XRRenderState): void;
  requestAnimationFrame(callback: XRFrameRequestCallback): number;
  addEventListener(type: string, listener: EventListener): void;
}

interface XRRenderState {
  baseLayer?: XRWebGLLayer;
}

interface XRWebGLLayer {
  framebuffer: WebGLFramebuffer;
}

interface XRFrameRequestCallback {
  (time: number, frame: XRFrame): void;
}

interface XRFrame {
  session: XRSession;
}

interface WebGLRenderingContext {
  bindFramebuffer(target: number, framebuffer: WebGLFramebuffer | null): void;
  clearColor(r: number, g: number, b: number, a: number): void;
  clear(mask: number): void;
  COLOR_BUFFER_BIT: number;
  DEPTH_BUFFER_BIT: number;
  FRAMEBUFFER: number;
}

// XRWebGLLayer constructor interface
interface XRWebGLLayerConstructor {
  new(session: XRSession, context: WebGLRenderingContext): XRWebGLLayer;
}

declare const XRWebGLLayer: XRWebGLLayerConstructor;

interface ARViewerProps {
  sessionId: string;
  onSessionComplete: (screenshot: string, transform: any) => void;
}

export default function ARViewer({ sessionId, onSessionComplete }: ARViewerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isARSupported, setIsARSupported] = useState(false);
  const [isARActive, setIsARActive] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [compassDirection, setCompassDirection] = useState(0);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      // Stop camera stream
      const stream = (window as any).cameraStream;
      if (stream) {
        stream.getTracks().forEach((track: MediaStreamTrack) => track.stop());
        delete (window as any).cameraStream;
      }
    };
  }, []);

  // Check AR support on mount
  useEffect(() => {
    checkARSupport();
    setupCompass();
  }, []);

  const checkARSupport = async () => {
    try {
      if (navigator.xr) {
        const supported = await navigator.xr.isSessionSupported('immersive-ar');
        setIsARSupported(supported);
      } else {
        setIsARSupported(false);
      }
    } catch (err) {
      console.error('AR support check failed:', err);
      setIsARSupported(false);
    } finally {
      setIsLoading(false);
    }
  };

  const setupCompass = () => {
    if (window.DeviceOrientationEvent) {
      const handleOrientation = (event: DeviceOrientationEvent) => {
        if (event.alpha !== null) {
          setCompassDirection(event.alpha);
        }
      };

      // Request permission for iOS 13+
      if (typeof (DeviceOrientationEvent as any).requestPermission === 'function') {
        (DeviceOrientationEvent as any).requestPermission()
          .then((response: string) => {
            if (response === 'granted') {
              window.addEventListener('deviceorientation', handleOrientation);
            }
          })
          .catch(console.error);
      } else {
        window.addEventListener('deviceorientation', handleOrientation);
      }

      return () => {
        window.removeEventListener('deviceorientation', handleOrientation);
      };
    }
  };

  const startARExperience = async () => {
    if (!isARSupported) return;
    
    setIsLoading(true);
    try {
      // Check for WebXR support
      if (navigator.xr) {
        const isSupported = await navigator.xr.isSessionSupported('immersive-ar');
        if (isSupported) {
          // Try to start WebXR session
          const xrSession = await navigator.xr.requestSession('immersive-ar', {
            requiredFeatures: ['local', 'hit-test'],
            optionalFeatures: ['dom-overlay', 'light-estimation']
          });
          
          await setupARScene(xrSession);
          setIsARActive(true);
          return;
        }
      }
      
      // Fallback to camera-based AR
      await startCameraAR();
      
    } catch (error) {
      console.error('Failed to start AR:', error);
      setError('AR not supported on this device');
    } finally {
      setIsLoading(false);
    }
  };

  const startCameraAR = async () => {
    try {
      // Request camera access
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      });
      
      // Create video element for camera feed
      const video = document.createElement('video');
      video.srcObject = stream;
      video.autoplay = true;
      video.playsInline = true;
      
      // Wait for video to be ready
      await new Promise((resolve) => {
        video.onloadedmetadata = resolve;
      });
      
      // Set video to canvas
      const canvas = canvasRef.current;
      if (canvas) {
        const ctx = canvas.getContext('2d');
        if (ctx) {
          // Start rendering camera feed with AR overlay
          const renderCamera = () => {
            if (video.readyState === video.HAVE_ENOUGH_DATA) {
              ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
              
              // Add AR overlay elements
              drawAROverlay(ctx, canvas.width, canvas.height);
            }
            
            if (isARActive) {
              requestAnimationFrame(renderCamera);
            }
          };
          
          setIsARActive(true);
          renderCamera();
        }
      }
      
      // Store stream for cleanup
      (window as any).cameraStream = stream;
      
    } catch (error) {
      console.error('Camera AR failed:', error);
      throw new Error('Camera access denied or not available');
    }
  };

  const drawAROverlay = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
    // Draw Vastu compass overlay
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = 80;
    
    // Draw compass circle
    ctx.strokeStyle = '#C6A75E';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.stroke();
    
    // Draw direction indicators
    const directions = ['N', 'E', 'S', 'W'];
    const angles = [0, Math.PI/2, Math.PI, 3*Math.PI/2];
    
    ctx.fillStyle = '#C6A75E';
    ctx.font = 'bold 16px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    directions.forEach((dir, i) => {
      const x = centerX + Math.cos(angles[i] - compassDirection * Math.PI/180) * (radius + 20);
      const y = centerY + Math.sin(angles[i] - compassDirection * Math.PI/180) * (radius + 20);
      ctx.fillText(dir, x, y);
    });
    
    // Draw center point
    ctx.fillStyle = '#C6A75E';
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI);
    ctx.fill();
  };

  const setupARScene = async (xrSession: XRSession) => {
    // Simplified AR scene setup
    const canvas = canvasRef.current;
    if (!canvas) return;

    const gl = canvas.getContext('webgl', { xrCompatible: true }) as WebGLRenderingContext | null;
    if (!gl) throw new Error('WebGL not supported');

    const xrLayer = new XRWebGLLayer(xrSession, gl);
    xrSession.updateRenderState({ baseLayer: xrLayer });

    const render = (time: number, frame: XRFrame) => {
      // Simple render loop
      gl.bindFramebuffer(gl.FRAMEBUFFER, xrLayer.framebuffer);
      
      // Clear with transparent background
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      
      frame.session.requestAnimationFrame(render);
    };

    xrSession.requestAnimationFrame(render);

    // Handle session end
    xrSession.addEventListener('end', () => {
      setIsARActive(false);
    });
  };

  const captureScreenshot = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const screenshot = canvas.toDataURL('image/jpeg', 0.8);
    const transform = {
      position: { x: 0, y: 0, z: 0 },
      rotation: { x: 0, y: 0, z: 0, w: 1 },
      scale: { x: 1, y: 1, z: 1 }
    };

    onSessionComplete(screenshot, transform);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#C6A75E]"></div>
      </div>
    );
  }

  if (!isARSupported) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 text-center">
        <Move3DIcon className="w-12 h-12 text-yellow-600 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-yellow-800 mb-2">AR Not Supported</h3>
        <p className="text-yellow-700">
          Your device doesn't support WebXR. Please use a compatible mobile device.
        </p>
      </div>
    );
  }

  if (isARActive) {
    return (
      <div className="relative w-full h-full bg-black">
        {/* Hidden canvas for AR rendering */}
        <canvas
          ref={canvasRef}
          className="absolute inset-0 w-full h-full"
          style={{ display: 'none' }}
        />

        {/* AR UI Overlay */}
        <div className="absolute inset-0 pointer-events-none">
          {/* Vastu Compass */}
          <div className="absolute top-4 right-4 pointer-events-auto">
            <div 
              className="w-16 h-16 bg-white/90 backdrop-blur-sm rounded-full shadow-lg flex items-center justify-center"
              style={{ transform: `rotate(${-compassDirection}deg)` }}
            >
              <div className="relative">
                <CompassIcon className="w-8 h-8 text-[#C6A75E]" />
                <span className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1 text-xs font-bold text-[#C6A75E]">
                  N
                </span>
              </div>
            </div>
          </div>

          {/* Instructions */}
          <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-sm rounded-lg p-3 max-w-xs">
            <p className="text-sm text-gray-800">
              Point at a flat surface and tap to place Vastu-aligned furniture
            </p>
          </div>

          {/* Controls */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-4 pointer-events-auto">
            <button
              onClick={captureScreenshot}
              className="bg-white/90 backdrop-blur-sm p-4 rounded-full shadow-lg hover:bg-white transition-colors"
            >
              <CameraIcon className="w-6 h-6 text-gray-800" />
            </button>
            <button
              onClick={() => {
                // Try to close window, fallback to navigation
                try {
                  window.close();
                } catch {
                  window.location.href = '/dashboard';
                }
              }}
              className="bg-red-500/90 backdrop-blur-sm p-4 rounded-full shadow-lg hover:bg-red-500 transition-colors"
            >
              <Maximize2Icon className="w-6 h-6 text-white" />
            </button>
          </div>

          {/* Vastu Zones Indicator */}
          <div className="absolute bottom-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg p-2">
            <div className="grid grid-cols-2 gap-1 text-xs">
              <div className="w-8 h-8 bg-green-200 rounded flex items-center justify-center">NE</div>
              <div className="w-8 h-8 bg-red-200 rounded flex items-center justify-center">SE</div>
              <div className="w-8 h-8 bg-yellow-200 rounded flex items-center justify-center">SW</div>
              <div className="w-8 h-8 bg-blue-200 rounded flex items-center justify-center">NW</div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      <div className="bg-gradient-to-br from-[#C6A75E]/10 to-[#F4EFE6] rounded-xl p-8 text-center">
        <Move3DIcon className="w-16 h-16 text-[#C6A75E] mx-auto mb-4" />
        <h3 className="text-xl font-bold text-gray-900 mb-2">Ready for AR Experience</h3>
        <p className="text-gray-600 mb-6">
          Experience your Vastu-aligned design in augmented reality
        </p>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={startARExperience}
          className="bg-[#C6A75E] text-white px-8 py-3 rounded-xl font-semibold hover:bg-[#B89A4F] transition-colors shadow-lg"
        >
          Start AR Experience
        </motion.button>
      </div>

      <div className="bg-gray-50 rounded-xl p-4">
        <h4 className="font-semibold text-gray-900 mb-2">Before you start:</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• Ensure you're in a well-lit area</li>
          <li>• Grant camera permissions when prompted</li>
          <li>• Point your device at a flat surface</li>
          <li>• Tap to place furniture items</li>
          <li>• Capture screenshot when ready</li>
        </ul>
      </div>
    </div>
  );
}
