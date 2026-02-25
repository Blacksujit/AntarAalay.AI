'use client';

import { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  UploadIcon, 
  CompassIcon, 
  ArrowLeftIcon,
  ImageIcon,
  XIcon,
  CheckIcon
} from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { uploadService } from '../../services/apiService';
import { useAuthStore } from '../../store/authStore';
import { CompassErrorBoundary, useCompassStore, VastuCompass, type Cardinal } from '../../features/vastuCompass';

export default function UploadPage() {
  const { isAuthenticated, initializeAuth } = useAuthStore();
  const [files, setFiles] = useState<{ north?: File; south?: File; east?: File; west?: File }>({});
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const compass = useCompassStore();

  useEffect(() => {
    void initializeAuth();
  }, [initializeAuth]);

  const setDirectionalFile = (direction: 'north' | 'south' | 'east' | 'west', file?: File) => {
    compass.reset();
    setFiles((prev) => ({ ...prev, [direction]: file }));
  };

  const requiredSlots = useMemo(() => (['north', 'east', 'south', 'west'] as const), []);
  const mappedLabelForSlot = useMemo(() => {
    const map = compass.mappedDirections;
    return (slot: Cardinal) => map[slot];
  }, [compass.mappedDirections]);

  const labelText = useMemo(() => {
    const labels: Record<Cardinal, string> = {
      north: 'North',
      east: 'East',
      south: 'South',
      west: 'West',
    };
    return (c: Cardinal) => labels[c];
  }, []);

  const handleUpload = async () => {
    setError(null);
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }
    if (!files.north || !files.south || !files.east || !files.west) {
      setError('Please upload all 4 directional images (North, South, East, West).');
      return;
    }

    if (!compass.confirmed) {
      setError('Please lock the compass orientation before uploading.');
      return;
    }

    try {
      setIsUploading(true);
      setUploadProgress(0);
      const resp = await uploadService.uploadRoomImages(
        {
          north: files.north,
          south: files.south,
          east: files.east,
          west: files.west,
        },
        (p) => setUploadProgress(p),
        {
          orientation_degree: Math.round(compass.angle),
          compass_confirmed: compass.confirmed,
        }
      );

      if (typeof window !== 'undefined') {
        window.sessionStorage.setItem('latest_room_id', resp.room_id);
      }

      router.push('/generate');
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const directions = [
    { id: 'north' as const, label: labelText(mappedLabelForSlot('north')), icon: '↑', color: '#3B82F6' },
    { id: 'east' as const, label: labelText(mappedLabelForSlot('east')), icon: '→', color: '#10B981' },
    { id: 'south' as const, label: labelText(mappedLabelForSlot('south')), icon: '↓', color: '#EF4444' },
    { id: 'west' as const, label: labelText(mappedLabelForSlot('west')), icon: '←', color: '#F59E0B' },
  ];

  return (
    <div className="min-h-screen bg-[#F4EFE6]">
      {/* Header */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-[#C6A75E]/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link href="/dashboard" className="flex items-center space-x-2">
              <CompassIcon className="w-8 h-8 text-[#C6A75E]" />
              <span className="text-xl font-bold text-[#1F1F1F]">AntarAalay.ai</span>
            </Link>
            <Link href="/dashboard" className="flex items-center text-gray-600 hover:text-[#1F1F1F] transition-colors">
              <ArrowLeftIcon className="w-5 h-5 mr-2" />
              Back to Dashboard
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-24 pb-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-8"
          >
            <h1 className="text-3xl font-bold text-[#1F1F1F] mb-2">Upload Your Room</h1>
            <p className="text-gray-600">Upload photos of your space and specify the direction for Vastu analysis</p>
          </motion.div>

          <CompassErrorBoundary>
            <VastuCompass />
          </CompassErrorBoundary>

          {/* Directional Upload Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-8"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {directions.map((dir) => (
                <div key={dir.id} className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center text-white font-bold" style={{ backgroundColor: dir.color }}>
                        {dir.icon}
                      </div>
                      <div>
                        <p className="font-semibold text-[#1F1F1F]">{dir.label} View</p>
                        <p className="text-sm text-gray-500">Upload the {dir.label.toLowerCase()} facing photo</p>
                      </div>
                    </div>

                    {files[dir.id] ? (
                      <button
                        onClick={() => setDirectionalFile(dir.id, undefined)}
                        className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                        title="Remove"
                      >
                        <XIcon className="w-5 h-5" />
                      </button>
                    ) : (
                      <CheckIcon className="w-5 h-5 text-gray-200" />
                    )}
                  </div>

                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => {
                      const f = e.target.files?.[0];
                      if (f) setDirectionalFile(dir.id, f);
                    }}
                    className="hidden"
                    id={`file-${dir.id}`}
                  />
                  <label
                    htmlFor={`file-${dir.id}`}
                    className="flex items-center justify-center gap-2 w-full px-4 py-3 border-2 border-dashed rounded-xl cursor-pointer hover:border-[#C6A75E]/60 transition-colors"
                  >
                    <ImageIcon className="w-5 h-5 text-gray-400" />
                    <span className="text-sm text-gray-600">
                      {files[dir.id] ? files[dir.id]!.name : 'Choose image'}
                    </span>
                  </label>
                </div>
              ))}
            </div>
          </motion.div>

          {error && (
            <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <div className="text-center">
            <button
              onClick={handleUpload}
              disabled={isUploading || !compass.confirmed || requiredSlots.some((s) => !files[s])}
              className="px-8 py-4 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {isUploading ? `Uploading... ${uploadProgress}%` : 'Upload & Continue'}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
