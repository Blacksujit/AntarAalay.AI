'use client';

import { useEffect, useMemo, useState } from 'react';
import { motion } from 'framer-motion';
import { 
  CompassIcon, 
  ArrowLeftIcon,
  SparklesIcon,
  HomeIcon,
  PaletteIcon,
  Wand2Icon,
  CheckIcon
} from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { designService, vastuService, type VastuAnalyzeResponse } from '../../services/apiService';
import { useAuthStore } from '../../store/authStore';

export default function GeneratePage() {
  const [selectedStyle, setSelectedStyle] = useState<string>('');
  const [selectedRoom, setSelectedRoom] = useState<string>('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationComplete, setGenerationComplete] = useState(false);
  const [roomId, setRoomId] = useState<string | null>(null);
  const [vastu, setVastu] = useState<VastuAnalyzeResponse | null>(null);
  const [designId, setDesignId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { isAuthenticated, initializeAuth } = useAuthStore();

  useEffect(() => {
    void initializeAuth();
  }, [initializeAuth]);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const rid = window.sessionStorage.getItem('latest_room_id');
      setRoomId(rid);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated === false) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  const roomTypes = [
    { id: 'living', label: 'Living Room', icon: HomeIcon },
    { id: 'bedroom', label: 'Bedroom', icon: HomeIcon },
    { id: 'kitchen', label: 'Kitchen', icon: HomeIcon },
    { id: 'office', label: 'Home Office', icon: HomeIcon },
    { id: 'dining', label: 'Dining Room', icon: HomeIcon },
    { id: 'bathroom', label: 'Bathroom', icon: HomeIcon },
  ];

  const designStyles = [
    { id: 'modern', label: 'Modern Minimalist', color: '#1F1F1F' },
    { id: 'traditional', label: 'Traditional Indian', color: '#C6A75E' },
    { id: 'scandinavian', label: 'Scandinavian', color: '#3B82F6' },
    { id: 'bohemian', label: 'Bohemian', color: '#F59E0B' },
    { id: 'industrial', label: 'Industrial', color: '#6B7280' },
    { id: 'coastal', label: 'Coastal', color: '#10B981' },
  ];

  const directionForVastu = useMemo(() => 'north', []);

  const handleGenerate = async () => {
    setError(null);
    if (!roomId) {
      setError('No uploaded room found. Please upload your directional images first.');
      router.push('/upload');
      return;
    }
    if (!selectedRoom || !selectedStyle) return;

    try {
      setIsGenerating(true);

      const vastuResp = await vastuService.analyzeVastu({
        direction: directionForVastu,
        room_type: selectedRoom,
      });
      setVastu(vastuResp);

      const genResp = await designService.generateDesign({
        room_id: roomId,
        style: selectedStyle,
        room_type: selectedRoom,
        wall_color: 'white',
        flooring_material: 'hardwood',
      });

      setDesignId(genResp.design_id);
      setGenerationComplete(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Generation failed');
    } finally {
      setIsGenerating(false);
    }
  };

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
          {!generationComplete ? (
            <>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-8"
              >
                <h1 className="text-3xl font-bold text-[#1F1F1F] mb-2">Generate Vastu Design</h1>
                <p className="text-gray-600">Choose your room type and design style for AI-powered Vastu-optimized designs</p>
              </motion.div>

              {error && (
                <div className="mb-6 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                  {error}
                </div>
              )}

              {/* Room Type Selection */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="mb-8"
              >
                <h3 className="text-lg font-semibold text-[#1F1F1F] mb-4">Select Room Type</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {roomTypes.map((room) => (
                    <button
                      key={room.id}
                      onClick={() => setSelectedRoom(room.id)}
                      className={`p-4 rounded-xl border-2 transition-all text-left ${
                        selectedRoom === room.id
                          ? 'border-[#C6A75E] bg-[#C6A75E]/5'
                          : 'border-gray-200 hover:border-[#C6A75E]/50'
                      }`}
                    >
                      <room.icon className={`w-6 h-6 mb-2 ${selectedRoom === room.id ? 'text-[#C6A75E]' : 'text-gray-400'}`} />
                      <span className={`font-medium ${selectedRoom === room.id ? 'text-[#C6A75E]' : 'text-[#1F1F1F]'}`}>
                        {room.label}
                      </span>
                    </button>
                  ))}
                </div>
              </motion.div>

              {/* Design Style Selection */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="mb-8"
              >
                <h3 className="text-lg font-semibold text-[#1F1F1F] mb-4">Select Design Style</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {designStyles.map((style) => (
                    <button
                      key={style.id}
                      onClick={() => setSelectedStyle(style.id)}
                      className={`p-4 rounded-xl border-2 transition-all text-left ${
                        selectedStyle === style.id
                          ? 'border-[#C6A75E] bg-[#C6A75E]/5'
                          : 'border-gray-200 hover:border-[#C6A75E]/50'
                      }`}
                    >
                      <PaletteIcon className={`w-6 h-6 mb-2 ${selectedStyle === style.id ? 'text-[#C6A75E]' : 'text-gray-400'}`} />
                      <span className={`font-medium ${selectedStyle === style.id ? 'text-[#C6A75E]' : 'text-[#1F1F1F]'}`}>
                        {style.label}
                      </span>
                    </button>
                  ))}
                </div>
              </motion.div>

              {/* Generate Button */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-center"
              >
                <button
                  onClick={handleGenerate}
                  disabled={!selectedRoom || !selectedStyle || isGenerating}
                  className="px-8 py-4 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center mx-auto"
                >
                  {isGenerating ? (
                    <>
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                        className="w-5 h-5 border-2 border-white border-t-transparent rounded-full mr-3"
                      />
                      Generating Design...
                    </>
                  ) : (
                    <>
                      <Wand2Icon className="w-5 h-5 mr-2" />
                      Generate Vastu Design
                    </>
                  )}
                </button>
              </motion.div>
            </>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center py-16"
            >
              <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-8">
                <CheckIcon className="w-12 h-12 text-green-600" />
              </div>
              <h2 className="text-3xl font-bold text-[#1F1F1F] mb-4">
                Design Generated!
              </h2>
              <p className="text-xl text-gray-600 mb-8 max-w-lg mx-auto">
                Your design is ready. We balanced orientation, flow, and material logic to keep the space feeling calm and intentional.
              </p>
              
              {/* Result Summary */}
              <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 max-w-2xl mx-auto">
                <div className="aspect-video bg-gradient-to-br from-[#C6A75E]/20 to-[#F4EFE6] rounded-xl flex items-center justify-center mb-4">
                  <SparklesIcon className="w-16 h-16 text-[#C6A75E]" />
                </div>
                <div className="text-left">
                  <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">
                    {selectedStyle.charAt(0).toUpperCase() + selectedStyle.slice(1)} {selectedRoom.charAt(0).toUpperCase() + selectedRoom.slice(1)}
                  </h3>
                  {designId && (
                    <p className="text-sm text-gray-500 mb-3">Design ID: {designId}</p>
                  )}
                  <div className="flex items-center space-x-2 mb-4">
                    <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                      Vastu Optimized ✓
                    </span>
                    <span className="px-3 py-1 bg-[#C6A75E]/10 text-[#C6A75E] rounded-full text-sm font-medium">
                      AI Generated
                    </span>
                  </div>
                  {vastu && (
                    <div className="mb-4">
                      <p className="text-sm text-gray-600">Vastu score: <span className="font-semibold">{vastu.vastu_score}</span> ({vastu.direction_rating})</p>
                    </div>
                  )}
                  <div className="space-y-2 text-sm text-gray-600">
                    <p>• Furniture placement optimized for energy flow</p>
                    <p>• Color scheme based on directional principles</p>
                    <p>• Lighting arrangement for harmony</p>
                    <p>• Decor suggestions for prosperity</p>
                  </div>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                {designId && (
                  <Link
                    href={`/designs/${designId}`}
                    className="px-8 py-4 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl text-center"
                  >
                    View Design
                  </Link>
                )}
                <button
                  onClick={() => router.push('/dashboard')}
                  className="px-8 py-4 border-2 border-[#C6A75E] text-[#C6A75E] rounded-xl font-semibold hover:bg-[#C6A75E] hover:text-white transition-all"
                >
                  Go to Dashboard
                </button>
                <button
                  onClick={() => {
                    setGenerationComplete(false);
                    setSelectedRoom('');
                    setSelectedStyle('');
                  }}
                  className="px-8 py-4 border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:bg-gray-50 transition-all"
                >
                  Generate Another
                </button>
              </div>
            </motion.div>
          )}
        </div>
      </main>
    </div>
  );
}
