/**
 * Enterprise 4-Directional Upload Module
 * Marvel-quality drag-drop interface for room images
 */

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowUpIcon, 
  ArrowDownIcon, 
  ArrowLeftIcon, 
  ArrowRightIcon,
  CloudArrowUpIcon,
  XMarkIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { cn } from '../../../utils/logger';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { useGlobalStore, selectAllImagesUploaded, selectCanGenerate } from '../../../store/globalStore';
import { uploadService } from '../../../services/apiService';

interface DirectionalUpload {
  direction: 'north' | 'south' | 'east' | 'west';
  label: string;
  icon: React.ElementType;
  description: string;
}

const directions: DirectionalUpload[] = [
  { 
    direction: 'north', 
    label: 'North', 
    icon: ArrowUpIcon,
    description: 'Face the main entrance or largest window'
  },
  { 
    direction: 'south', 
    label: 'South', 
    icon: ArrowDownIcon,
    description: 'Opposite to North, towards the back'
  },
  { 
    direction: 'east', 
    label: 'East', 
    icon: ArrowRightIcon,
    description: 'To your right when facing North'
  },
  { 
    direction: 'west', 
    label: 'West', 
    icon: ArrowLeftIcon,
    description: 'To your left when facing North'
  },
];

export const RoomUpload = () => {
  const navigate = useNavigate();
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  
  const uploadedImages = useGlobalStore((state) => state.uploadedImages);
  const setUploadedImages = useGlobalStore((state) => state.setUploadedImages);
  const setRoomId = useGlobalStore((state) => state.setRoomId);
  const allUploaded = useGlobalStore(selectAllImagesUploaded);
  const canGenerate = useGlobalStore(selectCanGenerate);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent, direction: string) => {
    e.preventDefault();
    e.stopPropagation();
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0], direction);
    }
  }, []);

  const handleFileSelect = (file: File, direction: string) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setUploadError('Please upload an image file (JPEG, PNG, WebP)');
      return;
    }
    
    // Validate file size (10MB max)
    if (file.size > 10 * 1024 * 1024) {
      setUploadError('File size must be less than 10MB');
      return;
    }

    setUploadError(null);
    setUploadedImages({
      ...uploadedImages,
      [direction]: file,
    });
  };

  const handleRemoveImage = (direction: string) => {
    setUploadedImages({
      ...uploadedImages,
      [direction]: null,
    });
  };

  const handleProceed = async () => {
    if (!allUploaded || !canGenerate) return;

    setIsUploading(true);
    setUploadError(null);

    try {
      const response = await uploadService.uploadRoomImages({
        north: uploadedImages.north!,
        south: uploadedImages.south!,
        east: uploadedImages.east!,
        west: uploadedImages.west!,
      });

      setRoomId(response.room_id);
      navigate('/design/generate');
    } catch (error: any) {
      setUploadError(error.message || 'Failed to upload images. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-10"
      >
        <h1 className="text-4xl font-display font-bold text-brand-charcoal mb-4">
          Upload Your Room
        </h1>
        <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
          Capture your room from all four directions to help our AI understand your space. 
          Stand in the center of your room and take photos facing each direction.
        </p>
      </motion.div>

      {/* Error Message */}
      <AnimatePresence>
        {uploadError && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-600 text-center"
          >
            {uploadError}
          </motion.div>
        )}
      </AnimatePresence>

      {/* 2x2 Grid Upload Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
        {directions.map((dir, index) => {
          const uploadedFile = uploadedImages[dir.direction];
          const previewUrl = uploadedFile ? URL.createObjectURL(uploadedFile) : null;

          return (
            <motion.div
              key={dir.direction}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1, duration: 0.4 }}
            >
              <Card 
                variant={uploadedFile ? 'elevated' : 'default'}
                className={cn(
                  'relative overflow-hidden transition-all duration-300',
                  !uploadedFile && 'border-2 border-dashed border-neutral-300 hover:border-brand-gold'
                )}
              >
                <div
                  onDragOver={handleDragOver}
                  onDrop={(e) => handleDrop(e, dir.direction)}
                  className="p-6"
                >
                  {/* Direction Header */}
                  <div className="flex items-center gap-3 mb-4">
                    <div className={cn(
                      'w-12 h-12 rounded-xl flex items-center justify-center transition-colors duration-300',
                      uploadedFile ? 'bg-brand-gold text-white' : 'bg-brand-beige text-brand-charcoal'
                    )}>
                      <dir.icon className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-brand-charcoal">
                        {dir.label}
                      </h3>
                      <p className="text-sm text-neutral-500">{dir.description}</p>
                    </div>
                    
                    {uploadedFile && (
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        className="ml-auto"
                      >
                        <CheckCircleIcon className="w-6 h-6 text-green-500" />
                      </motion.div>
                    )}
                  </div>

                  {/* Upload Area */}
                  {uploadedFile ? (
                    <div className="relative">
                      <img
                        src={previewUrl!}
                        alt={`${dir.label} view`}
                        className="w-full h-48 object-cover rounded-xl"
                      />
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        onClick={() => handleRemoveImage(dir.direction)}
                        className="absolute top-2 right-2 p-1.5 bg-white/90 rounded-full shadow-soft hover:bg-white transition-colors"
                      >
                        <XMarkIcon className="w-5 h-5 text-red-500" />
                      </motion.button>
                      
                      <div className="mt-3 flex items-center justify-between text-sm text-neutral-600">
                        <span>{uploadedFile.name}</span>
                        <span>{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</span>
                      </div>
                    </div>
                  ) : (
                    <label className="block cursor-pointer">
                      <input
                        type="file"
                        accept="image/*"
                        className="hidden"
                        onChange={(e) => {
                          if (e.target.files?.[0]) {
                            handleFileSelect(e.target.files[0], dir.direction);
                          }
                        }}
                      />
                      <div className="flex flex-col items-center justify-center h-48 bg-brand-beige/50 rounded-xl border-2 border-dashed border-neutral-300 hover:border-brand-gold hover:bg-brand-beige transition-all duration-300">
                        <CloudArrowUpIcon className="w-12 h-12 text-neutral-400 mb-3" />
                        <p className="text-neutral-600 font-medium">Drop image here or click</p>
                        <p className="text-sm text-neutral-400 mt-1">JPEG, PNG, WebP up to 10MB</p>
                      </div>
                    </label>
                  )}
                </div>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Progress Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-neutral-600">
            Upload Progress
          </span>
          <span className="text-sm font-bold text-brand-gold">
            {Object.values(uploadedImages).filter(Boolean).length} / 4
          </span>
        </div>
        <div className="h-2 bg-neutral-200 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ 
              width: `${(Object.values(uploadedImages).filter(Boolean).length / 4) * 100}%` 
            }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
            className="h-full bg-brand-gold rounded-full"
          />
        </div>
      </motion.div>

      {/* Action Button */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-center"
      >
        <Button
          size="lg"
          isLoading={isUploading}
          disabled={!allUploaded || !canGenerate}
          onClick={handleProceed}
          leftIcon={!allUploaded ? undefined : <CloudArrowUpIcon className="w-5 h-5" />}
          className={cn(
            'px-12 py-4 text-lg shadow-luxury',
            !allUploaded && 'opacity-50'
          )}
        >
          {!canGenerate 
            ? 'Daily Limit Reached'
            : !allUploaded 
              ? `Upload All 4 Images (${Object.values(uploadedImages).filter(Boolean).length}/4)`
              : isUploading 
                ? 'Uploading...'
                : 'Proceed to Design'
          }
        </Button>
      </motion.div>

      {/* Help Text */}
      {!allUploaded && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center mt-4 text-sm text-neutral-500"
        >
          Upload all 4 directional images to proceed with AI design generation
        </motion.p>
      )}
    </div>
  );
};

export default RoomUpload;
