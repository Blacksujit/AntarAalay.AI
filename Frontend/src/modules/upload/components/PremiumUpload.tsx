/**
 * Premium Upload Page
 * AntarAalay.ai - Luxury Room Image Upload Experience
 */

import { useState, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowUpIcon, 
  ArrowDownIcon, 
  ArrowLeftIcon, 
  ArrowRightIcon,
  CameraIcon,
  CheckCircleIcon,
  XMarkIcon,
  CloudArrowUpIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { useMutation } from '@tanstack/react-query';
import { uploadService } from '../../../services/apiService';
import { PremiumButton, GlassCard, ProgressRing, LoadingDots } from '../../../components/ui/PremiumComponents';

interface UploadedFile {
  file: File;
  preview: string;
  direction: 'north' | 'south' | 'east' | 'west';
}

interface DirectionConfig {
  direction: 'north' | 'south' | 'east' | 'west';
  label: string;
  icon: React.ElementType;
  description: string;
  color: string;
}

const directions: DirectionConfig[] = [
  { 
    direction: 'north', 
    label: 'North', 
    icon: ArrowUpIcon,
    description: 'Face the main entrance or largest window',
    color: 'from-blue-400 to-blue-600'
  },
  { 
    direction: 'south', 
    label: 'South', 
    icon: ArrowDownIcon,
    description: 'Opposite to North, towards the back',
    color: 'from-green-400 to-green-600'
  },
  { 
    direction: 'east', 
    label: 'East', 
    icon: ArrowRightIcon,
    description: 'To your right when facing North',
    color: 'from-orange-400 to-orange-600'
  },
  { 
    direction: 'west', 
    label: 'West', 
    icon: ArrowLeftIcon,
    description: 'To your left when facing North',
    color: 'from-purple-400 to-purple-600'
  },
];

export const PremiumUpload: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRefs = useRef<{ [key: string]: HTMLInputElement | null }>({});
  
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [draggedDirection, setDraggedDirection] = useState<string | null>(null);

  // Upload mutation
  const uploadMutation = useMutation({
    mutationFn: ({ files, onProgress }: { 
      files: { north: File; south: File; east: File; west: File };
      onProgress: (progress: number) => void;
    }) => uploadService.uploadRoomImages(files, onProgress),
    onSuccess: (data: any) => {
      // Navigate to design generation with room data
      navigate('/design', { state: { roomId: data.room_id, images: data.images } });
    },
    onError: (error: Error) => {
      console.error('Upload failed:', error);
      // Handle error display
    },
  });

  const handleFileSelect = useCallback((direction: 'north' | 'south' | 'east' | 'west', file: File) => {
    if (!file) return;
    
    // Validate file
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      alert('Please select a valid image file (JPEG, PNG, or WebP)');
      return;
    }
    
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      alert('Image size must be less than 10MB');
      return;
    }
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const preview = e.target?.result as string;
      setUploadedFiles(prev => {
        const filtered = prev.filter(f => f.direction !== direction);
        return [...filtered, { file, preview, direction }];
      });
    };
    reader.readAsDataURL(file);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent, direction: string) => {
    e.preventDefault();
    setDraggedDirection(null);
    
    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleFileSelect(direction as any, files[0]);
    }
  }, [handleFileSelect]);

  const handleDragOver = useCallback((e: React.DragEvent, direction: string) => {
    e.preventDefault();
    setDraggedDirection(direction);
  }, []);

  const handleDragLeave = useCallback(() => {
    setDraggedDirection(null);
  }, []);

  const removeFile = useCallback((direction: 'north' | 'south' | 'east' | 'west') => {
    setUploadedFiles(prev => prev.filter(f => f.direction !== direction));
  }, []);

  const handleUpload = useCallback(() => {
    if (uploadedFiles.length !== 4) {
      alert('Please upload all 4 directional images');
      return;
    }
    
    const files = uploadedFiles.reduce((acc, uploaded) => {
      acc[uploaded.direction] = uploaded.file;
      return acc;
    }, {} as { north: File; south: File; east: File; west: File });
    
    uploadMutation.mutate({ 
      files,
      onProgress: setUploadProgress 
    });
  }, [uploadedFiles, uploadMutation]);

  const allFilesUploaded = uploadedFiles.length === 4;

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/80 backdrop-blur-lg border-b border-amber-100 sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-amber-400 to-amber-600 rounded-xl flex items-center justify-center shadow-glow">
                <CameraIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-serif font-bold text-gray-900">Capture Your Space</h1>
                <p className="text-gray-600">Upload 4 directional images to begin your design journey</p>
              </div>
            </div>
            <PremiumButton
              variant="outline"
              onClick={() => navigate('/dashboard')}
            >
              Back to Dashboard
            </PremiumButton>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Instructions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-center mb-12"
        >
          <div className="inline-flex items-center space-x-2 bg-amber-100 text-amber-800 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <SparklesIcon className="w-4 h-4" />
            <span>Professional Tip: Stand in the center of your room for best results</span>
          </div>
          <h2 className="text-3xl font-serif text-gray-900 mb-4">
            Photograph Each Direction
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Capture your room from all four cardinal directions. Our AI will analyze the space 
            and create stunning designs that respect Vastu principles.
          </p>
        </motion.div>

        {/* Upload Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {directions.map((dir, index) => {
            const uploadedFile = uploadedFiles.find(f => f.direction === dir.direction);
            const isDraggedOver = draggedDirection === dir.direction;
            
            return (
              <motion.div
                key={dir.direction}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
              >
                <GlassCard className={`h-full transition-all duration-300 ${
                  isDraggedOver ? 'ring-2 ring-amber-400 scale-105' : ''
                }`}>
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 bg-gradient-to-br ${dir.color} rounded-lg flex items-center justify-center`}>
                        <dir.icon className="w-5 h-5 text-white" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-900">{dir.label} Direction</h3>
                        <p className="text-sm text-gray-600">{dir.description}</p>
                      </div>
                    </div>
                    {uploadedFile && (
                      <CheckCircleIcon className="w-6 h-6 text-green-500" />
                    )}
                  </div>
                  
                  {/* Upload Area */}
                  <div
                    className={`relative border-2 border-dashed rounded-xl transition-all duration-300 ${
                      uploadedFile 
                        ? 'border-green-400 bg-green-50' 
                        : isDraggedOver
                        ? 'border-amber-400 bg-amber-50'
                        : 'border-gray-300 hover:border-amber-400 hover:bg-amber-50'
                    }`}
                    onDrop={(e) => handleDrop(e, dir.direction)}
                    onDragOver={(e) => handleDragOver(e, dir.direction)}
                    onDragLeave={handleDragLeave}
                    onClick={() => fileInputRefs.current[dir.direction]?.click()}
                  >
                    <input
                      ref={(el) => {
                        fileInputRefs.current[dir.direction] = el;
                      }}
                      type="file"
                      accept="image/jpeg,image/png,image/webp"
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) handleFileSelect(dir.direction, file);
                      }}
                    />
                    
                    {uploadedFile ? (
                      <div className="relative aspect-[4/3]">
                        <img
                          src={uploadedFile.preview}
                          alt={`${dir.label} view`}
                          className="w-full h-full object-cover rounded-lg"
                        />
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            removeFile(dir.direction);
                          }}
                          className="absolute top-2 right-2 w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
                        >
                          <XMarkIcon className="w-4 h-4" />
                        </button>
                      </div>
                    ) : (
                      <div className="aspect-[4/3] flex flex-col items-center justify-center p-8 cursor-pointer">
                        <CloudArrowUpIcon className="w-12 h-12 text-gray-400 mb-4" />
                        <p className="text-gray-600 font-medium mb-2">
                          {isDraggedOver ? 'Drop image here' : 'Click or drag image here'}
                        </p>
                        <p className="text-sm text-gray-500">
                          JPEG, PNG, or WebP (max 10MB)
                        </p>
                      </div>
                    )}
                  </div>
                </GlassCard>
              </motion.div>
            );
          })}
        </div>

        {/* Upload Progress */}
        <AnimatePresence>
          {uploadMutation.isPending && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50"
            >
              <GlassCard variant="light" className="max-w-md w-full mx-4">
                <div className="text-center">
                  <ProgressRing progress={uploadProgress} size={120} className="mx-auto mb-6" />
                  <h3 className="text-xl font-serif font-bold text-gray-900 mb-2">
                    Uploading Your Space
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Processing your room images... {uploadProgress}%
                  </p>
                  <div className="flex justify-center">
                    <LoadingDots />
                  </div>
                </div>
              </GlassCard>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Action Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="text-center"
        >
          <PremiumButton
            size="xl"
            onClick={handleUpload}
            disabled={!allFilesUploaded || uploadMutation.isPending}
            loading={uploadMutation.isPending}
            className="px-12 py-4 text-lg"
          >
            {uploadMutation.isPending ? 'Uploading...' : 'Generate Designs'}
          </PremiumButton>
          
          {!allFilesUploaded && (
            <p className="text-sm text-gray-500 mt-3">
              Please upload all 4 directional images to continue
            </p>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default PremiumUpload;
