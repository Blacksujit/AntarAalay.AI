/**
 * Premium Upload Experience
 * AntarAalay.ai - Luxury Room Image Upload with React Dropzone
 */

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { 
  ArrowUpIcon, 
  ArrowDownIcon, 
  ArrowLeftIcon, 
  ArrowRightIcon,
  CameraIcon,
  CheckCircleIcon,
  XMarkIcon,
  CloudArrowUpIcon,
  SparklesIcon,
  ArrowPathIcon
} from '@heroicons/react/24/outline';
import { useMutation } from '@tanstack/react-query';
import { uploadService } from '../../services/apiService';
import { Button, Card, ProgressRing, LoadingDots } from '../../components/ui';

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
  bgGradient: string;
}

const directions: DirectionConfig[] = [
  { 
    direction: 'north', 
    label: 'North', 
    icon: ArrowUpIcon,
    description: 'Face the main entrance or largest window',
    color: 'text-blue-600',
    bgGradient: 'from-blue-400 to-blue-600',
  },
  { 
    direction: 'south', 
    label: 'South', 
    icon: ArrowDownIcon,
    description: 'Opposite to North, towards the back',
    color: 'text-green-600',
    bgGradient: 'from-green-400 to-green-600',
  },
  { 
    direction: 'east', 
    label: 'East', 
    icon: ArrowRightIcon,
    description: 'To your right when facing North',
    color: 'text-orange-600',
    bgGradient: 'from-orange-400 to-orange-600',
  },
  { 
    direction: 'west', 
    label: 'West', 
    icon: ArrowLeftIcon,
    description: 'To your left when facing North',
    color: 'text-purple-600',
    bgGradient: 'from-purple-400 to-purple-600',
  },
];

export const PremiumUpload: React.FC = () => {
  const navigate = useNavigate();
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

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
      setError(error.message);
      console.error('Upload failed:', error);
    },
  });

  const handleFileSelect = useCallback((direction: 'north' | 'south' | 'east' | 'west', file: File) => {
    if (!file) return;
    
    // Validate file
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      setError('Please select a valid image file (JPEG, PNG, or WebP)');
      return;
    }
    
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      setError('Image size must be less than 10MB');
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
      setError(null);
    };
    reader.readAsDataURL(file);
  }, []);

  const removeFile = useCallback((direction: 'north' | 'south' | 'east' | 'west') => {
    setUploadedFiles(prev => prev.filter(f => f.direction !== direction));
    setError(null);
  }, []);

  const handleUpload = useCallback(() => {
    if (uploadedFiles.length !== 4) {
      setError('Please upload all 4 directional images');
      return;
    }
    
    const files = uploadedFiles.reduce((acc, uploaded) => {
      acc[uploaded.direction] = uploaded.file;
      return acc;
    }, {} as { north: File; south: File; east: File; west: File });
    
    setError(null);
    uploadMutation.mutate({ 
      files,
      onProgress: setUploadProgress 
    });
  }, [uploadedFiles, uploadMutation]);

  const retryUpload = useCallback(() => {
    setError(null);
    handleUpload();
  }, [handleUpload]);

  const allFilesUploaded = uploadedFiles.length === 4;

  return (
    <div className="min-h-screen bg-stone">
      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white shadow-sm sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-gold to-amber-600 rounded-2xl flex items-center justify-center shadow-glow">
                <CameraIcon className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="font-serif text-2xl font-bold text-charcoal">Capture Your Space</h1>
                <p className="text-text-secondary">Upload 4 directional images to begin your design journey</p>
              </div>
            </div>
            <Button
              variant="outline"
              onClick={() => navigate('/dashboard')}
              leftIcon={<ArrowLeftIcon className="w-4 h-4" />}
            >
              Back to Dashboard
            </Button>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Instructions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-center mb-12"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
            className="inline-flex items-center space-x-2 bg-gold/10 text-gold px-4 py-2 rounded-full text-sm font-medium mb-6"
          >
            <SparklesIcon className="w-4 h-4" />
            <span>Professional Tip: Stand in the center of your room for best results</span>
          </motion.div>
          <h2 className="font-serif text-4xl font-bold text-charcoal mb-4">
            Photograph Each Direction
          </h2>
          <p className="text-xl text-text-secondary max-w-2xl mx-auto leading-relaxed">
            Capture your room from all four cardinal directions. Our AI will analyze the space 
            and create stunning designs that respect Vastu principles.
          </p>
        </motion.div>

        {/* Upload Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {directions.map((dir, index) => {
            const uploadedFile = uploadedFiles.find(f => f.direction === dir.direction);
            
            return (
              <motion.div
                key={dir.direction}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 + index * 0.1 }}
              >
                <DropzoneCard
                  direction={dir}
                  uploadedFile={uploadedFile}
                  onFileSelect={handleFileSelect}
                  onRemoveFile={removeFile}
                />
              </motion.div>
            );
          })}
        </div>

        {/* Error Display */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-8"
            >
              <Card className="bg-red-50 border border-red-200">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-red-800 mb-1">Upload Error</h3>
                    <p className="text-red-600">{error}</p>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={retryUpload}
                    leftIcon={<ArrowPathIcon className="w-4 h-4" />}
                    className="border-red-300 text-red-600 hover:bg-red-50"
                  >
                    Retry
                  </Button>
                </div>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Upload Progress */}
        <AnimatePresence>
          {uploadMutation.isPending && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="fixed inset-0 bg-overlay backdrop-blur-sm flex items-center justify-center z-50"
            >
              <Card variant="glass" className="max-w-md w-full mx-4">
                <div className="text-center">
                  <ProgressRing progress={uploadProgress} size={120} className="mx-auto mb-6" />
                  <h3 className="font-serif text-xl font-bold text-charcoal mb-2">
                    Uploading Your Space
                  </h3>
                  <p className="text-text-secondary mb-4">
                    Processing your room images... {uploadProgress}%
                  </p>
                  <LoadingDots />
                </div>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Action Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="text-center"
        >
          <Button
            size="xl"
            onClick={handleUpload}
            disabled={!allFilesUploaded || uploadMutation.isPending}
            loading={uploadMutation.isPending}
            className="px-12 py-6 text-xl"
          >
            {uploadMutation.isPending ? 'Uploading...' : 'Generate Designs'}
          </Button>
          
          {!allFilesUploaded && (
            <p className="text-sm text-text-secondary mt-3">
              Please upload all 4 directional images to continue
            </p>
          )}
        </motion.div>
      </div>
    </div>
  );
};

// Dropzone Card Component
interface DropzoneCardProps {
  direction: DirectionConfig;
  uploadedFile: UploadedFile | undefined;
  onFileSelect: (direction: 'north' | 'south' | 'east' | 'west', file: File) => void;
  onRemoveFile: (direction: 'north' | 'south' | 'east' | 'west') => void;
}

const DropzoneCard: React.FC<DropzoneCardProps> = ({
  direction,
  uploadedFile,
  onFileSelect,
  onRemoveFile,
}) => {
  const [isDragActive, setIsDragActive] = useState(false);
  
  const onDrop = useCallback((acceptedFiles: File[]) => {
    setIsDragActive(false);
    if (acceptedFiles.length > 0) {
      onFileSelect(direction.direction, acceptedFiles[0]);
    }
  }, [direction.direction, onFileSelect]);

  const { getRootProps, getInputProps, isDragActive: dropzoneActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/webp': ['.webp'],
    },
    maxFiles: 1,
    multiple: false,
    onDragEnter: () => setIsDragActive(true),
    onDragLeave: () => setIsDragActive(false),
  });

  return (
    <Card 
      variant={isDragActive || dropzoneActive ? "elevated" : "default"}
      className={`transition-all duration-300 ${
        isDragActive || dropzoneActive 
          ? 'ring-2 ring-gold shadow-xl scale-105' 
          : 'hover:shadow-lg'
      }`}
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`w-10 h-10 bg-gradient-to-br ${direction.bgGradient} rounded-xl flex items-center justify-center`}>
            <direction.icon className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-charcoal">{direction.label} Direction</h3>
            <p className="text-sm text-text-secondary">{direction.description}</p>
          </div>
        </div>
        {uploadedFile && (
          <CheckCircleIcon className="w-6 h-6 text-success" />
        )}
      </div>
      
      {/* Upload Area */}
      <div
        {...getRootProps()}
        className={`relative border-2 border-dashed rounded-2xl transition-all duration-300 cursor-pointer ${
          uploadedFile 
            ? 'border-success bg-success/5' 
            : isDragActive || dropzoneActive
            ? 'border-gold bg-gold/5'
            : 'border-neutral-grey hover:border-gold hover:bg-stone'
        }`}
      >
        <input {...getInputProps()} />
        
        {uploadedFile ? (
          <div className="relative aspect-[4/3]">
            <img
              src={uploadedFile.preview}
              alt={`${direction.label} view`}
              className="w-full h-full object-cover rounded-xl"
            />
            <button
              onClick={(e) => {
                e.stopPropagation();
                onRemoveFile(direction.direction);
              }}
              className="absolute top-2 right-2 w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors shadow-lg"
            >
              <XMarkIcon className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <div className="aspect-[4/3] flex flex-col items-center justify-center p-8">
            <CloudArrowUpIcon className={`w-12 h-12 mb-4 transition-colors ${
              isDragActive || dropzoneActive ? 'text-gold' : 'text-text-tertiary'
            }`} />
            <p className={`font-medium mb-2 transition-colors ${
              isDragActive || dropzoneActive ? 'text-gold' : 'text-charcoal'
            }`}>
              {isDragActive || dropzoneActive ? 'Drop image here' : 'Click or drag image here'}
            </p>
            <p className="text-sm text-text-secondary">
              JPEG, PNG, or WebP (max 10MB)
            </p>
          </div>
        )}
      </div>
    </Card>
  );
};

export default PremiumUpload;
