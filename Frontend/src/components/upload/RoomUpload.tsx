/**
 * Premium Room Upload Component
 * Professional 4-directional room image upload
 */

import { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CameraIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { cn } from '../../utils/logger';

interface RoomUploadProps {
  onUpload: (images: { north: File; south: File; east: File; west: File }) => void;
  loading?: boolean;
}

const RoomUpload = ({ onUpload, loading = false }: RoomUploadProps) => {
  const [images, setImages] = useState<{
    north: File | null;
    south: File | null;
    east: File | null;
    west: File | null;
  }>({
    north: null,
    south: null,
    east: null,
    west: null,
  });

  const [dragOver, setDragOver] = useState<string | null>(null);

  const handleFileSelect = useCallback((direction: keyof typeof images) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setImages(prev => ({ ...prev, [direction]: file }));
    }
  }, []);

  const handleDrop = useCallback((direction: keyof typeof images) => (event: React.DragEvent) => {
    event.preventDefault();
    setDragOver(null);
    
    const file = event.dataTransfer.files?.[0];
    if (file) {
      setImages(prev => ({ ...prev, [direction]: file }));
    }
  }, []);

  const handleDragOver = useCallback((direction: string) => (event: React.DragEvent) => {
    event.preventDefault();
    setDragOver(direction);
  }, []);

  const handleDragLeave = useCallback(() => {
    setDragOver(null);
  }, []);

  const removeImage = useCallback((direction: keyof typeof images) => {
    setImages(prev => ({ ...prev, [direction]: null }));
  }, []);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const allImagesUploaded = Object.values(images).every(img => img !== null);

  const directions = [
    { key: 'north' as const, label: 'North', position: 'top-4 left-1/2 -translate-x-1/2 -translate-y-4' },
    { key: 'south' as const, label: 'South', position: 'bottom-4 left-1/2 -translate-x-1/2 translate-y-4' },
    { key: 'east' as const, label: 'East', position: 'top-1/2 right-4 translate-y-1/2 translate-x-4' },
    { key: 'west' as const, label: 'West', position: 'top-1/2 left-4 translate-y-1/2 -translate-x-4' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-beige via-white to-brand-white p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-display font-bold text-brand-charcoal mb-4">
            Upload Your Room
          </h1>
          <p className="text-xl text-neutral-600 max-w-2xl mx-auto font-body">
            Capture all four directions of your space for optimal AI design generation
          </p>
        </motion.div>

        {/* Upload Grid */}
        <div className="relative bg-white rounded-3xl shadow-luxury p-8 mb-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            {directions.map(({ key, label, position }) => (
              <motion.div
                key={key}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: directions.indexOf({ key, label, position }) * 0.1, duration: 0.6 }}
                className="relative"
              >
                <div
                  className={cn(
                    "relative aspect-square rounded-2xl border-2 border-dashed transition-all duration-300",
                    dragOver === key
                      ? "border-brand-gold bg-brand-gold/5 shadow-glow"
                      : images[key as keyof typeof images]
                      ? "border-brand-gold bg-brand-gold/10 shadow-soft"
                      : "border-neutral-300 bg-neutral-50 hover:border-neutral-400 hover:bg-neutral-100"
                  )}
                  style={{ position: position as any }}
                  onDrop={handleDrop(key)}
                  onDragOver={handleDragOver(key)}
                  onDragLeave={handleDragLeave}
                >
                  {images[key] ? (
                    <div className="relative w-full h-full">
                      <img
                        src={URL.createObjectURL(images[key]!)}
                        alt={`${label} view`}
                        className="w-full h-full object-cover rounded-xl"
                      />
                      
                      {/* Remove button */}
                      <motion.button
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => removeImage(key)}
                        className="absolute top-2 right-2 w-8 h-8 bg-brand-charcoal/80 text-white rounded-full flex items-center justify-center shadow-soft hover:bg-brand-charcoal transition-colors duration-200"
                      >
                        <XMarkIcon className="w-4 h-4" />
                      </motion.button>

                      {/* File info */}
                      <div className="absolute bottom-2 left-2 bg-brand-charcoal/90 text-white px-2 py-1 rounded-lg text-xs">
                        <div className="font-medium">{label}</div>
                        <div className="text-neutral-300">
                          {formatFileSize(images[key]!.size)}
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center w-full h-full">
                      <CameraIcon className="w-12 h-12 text-neutral-400 mb-3" />
                      <div className="text-center">
                        <div className="font-semibold text-brand-charcoal mb-1">{label}</div>
                        <div className="text-sm text-neutral-500">
                          Click or drag image
                        </div>
                      </div>
                      
                      {/* Hidden file input */}
                      <input
                        type="file"
                        accept="image/jpeg,image/png,image/webp"
                        onChange={(e) => handleFileSelect(key)(e as any)}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                      />
                    </div>
                  )}

                  {/* Drag overlay */}
                  <AnimatePresence>
                    {dragOver === key && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute inset-0 bg-brand-gold/20 rounded-2xl border-2 border-brand-gold flex items-center justify-center"
                      >
                        <div className="text-brand-gold font-semibold">
                          Drop {label} image here
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>

                {/* Direction label */}
                <div className="text-center mt-4">
                  <span className={cn(
                    "inline-flex items-center px-3 py-1 rounded-full text-sm font-medium",
                    images[key as keyof typeof images]
                      ? "bg-brand-gold text-white"
                      : "bg-neutral-200 text-neutral-600"
                  )}>
                    {label}
                  </span>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Instructions */}
          <div className="mt-8 p-6 bg-warm-50 rounded-xl">
            <h3 className="text-lg font-semibold text-brand-charcoal mb-3">
              📸 Upload Guidelines
            </h3>
            <ul className="space-y-2 text-sm text-neutral-600 font-body">
              <li className="flex items-start">
                <span className="text-brand-gold mr-2">•</span>
                High-quality images from each direction (North, South, East, West)
              </li>
              <li className="flex items-start">
                <span className="text-brand-gold mr-2">•</span>
                JPEG, PNG, or WebP format (Max 10MB per image)
              </li>
              <li className="flex items-start">
                <span className="text-brand-gold mr-2">•</span>
                Ensure good lighting and clear visibility of room features
              </li>
            </ul>
          </div>
        </div>

        {/* Action Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="text-center"
        >
          <motion.button
            whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(198, 167, 94, 0.4)" }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              if (allImagesUploaded) {
                onUpload(images as { north: File; south: File; east: File; west: File });
              }
            }}
            disabled={!allImagesUploaded || loading}
            className={cn(
              "relative px-12 py-4 text-lg font-semibold text-brand-white",
              "bg-gradient-to-r from-brand-gold to-brand-gold/600",
              "rounded-xl shadow-luxury hover:shadow-glow",
              "transition-all duration-300 ease-out",
              "disabled:opacity-50 disabled:cursor-not-allowed"
            )}
          >
            <span className="relative z-10 flex items-center">
              {loading ? (
                <>
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-5 h-5 border-2 border-white/30 border-t-transparent rounded-full mr-3"
                  />
                  Processing...
                </>
              ) : (
                <>
                  Proceed to Design
                  <motion.div
                    initial={{ x: 0 }}
                    animate={{ x: 5 }}
                    transition={{ duration: 0.3, repeat: Infinity, repeatType: "reverse", ease: "easeInOut" }}
                  >
                    →
                  </motion.div>
                </>
              )}
            </span>
            
            {/* Button shimmer effect */}
            <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-transparent via-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-500" />
          </motion.button>

          {!allImagesUploaded && (
            <p className="mt-4 text-sm text-neutral-500">
              Please upload all 4 directional images to continue
            </p>
          )}
        </motion.div>
      </div>
    </div>
  );
};

export default RoomUpload;
