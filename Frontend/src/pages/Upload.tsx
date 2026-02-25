import { useState, useCallback, type ChangeEvent, type DragEvent } from 'react';
import { useRouter } from 'next/router';
import { useMutation } from '@tanstack/react-query';
import { Upload as UploadIcon, Compass, ArrowUp, ArrowDown, ArrowLeft, ArrowRight, X, Loader2 } from 'lucide-react';
import { uploadRoom } from '../services/upload';
import { logger } from '../utils/logger';

interface ImageFile {
  file: File;
  preview: string;
  direction: 'north' | 'south' | 'east' | 'west';
}

type Direction = ImageFile['direction'];

const DIRECTIONS = [
  { key: 'north', label: 'North', icon: ArrowUp, description: 'Facing North' },
  { key: 'south', label: 'South', icon: ArrowDown, description: 'Facing South' },
  { key: 'east', label: 'East', icon: ArrowRight, description: 'Facing East' },
  { key: 'west', label: 'West', icon: ArrowLeft, description: 'Facing West' },
] as const;

export default function Upload() {
  const router = useRouter();
  const [images, setImages] = useState<Record<Direction, ImageFile | undefined>>({} as Record<Direction, ImageFile | undefined>);
  const [activeDirection, setActiveDirection] = useState<Direction>('north');

  const uploadMutation = useMutation({
    mutationFn: uploadRoom,
    onSuccess: (data) => {
      logger.info('Upload successful', { roomId: data.room_id });
      router.push(`/customize/${data.room_id}`);
    },
    onError: (error) => {
      logger.error('Upload failed', {}, error as Error);
    },
  });

  const acceptFiles = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    const direction = activeDirection;

    setImages((prev) => {
      const existing = prev[direction];
      if (existing) {
        URL.revokeObjectURL(existing.preview);
      }

      return {
        ...prev,
        [direction]: {
          file,
          preview: URL.createObjectURL(file),
          direction,
        },
      };
    });

    const currentIndex = DIRECTIONS.findIndex((d) => d.key === direction);
    if (currentIndex < DIRECTIONS.length - 1) {
      setActiveDirection(DIRECTIONS[currentIndex + 1].key);
    }
  }, [activeDirection]);

  const [isDragActive, setIsDragActive] = useState(false);

  const onFileInputChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;
    acceptFiles([files[0]]);
    e.target.value = '';
  }, [acceptFiles]);

  const onDropZoneDrop = useCallback((e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragActive(false);
    const files = Array.from(e.dataTransfer.files || []);
    acceptFiles(files);
  }, [acceptFiles]);

  const removeImage = (direction: Direction) => {
    setImages(prev => {
      const newImages = { ...prev };
      if (newImages[direction]) {
        URL.revokeObjectURL(newImages[direction]!.preview);
        delete newImages[direction];
      }
      return newImages;
    });
    setActiveDirection(direction);
  };

  const handleSubmit = () => {
    if (Object.keys(images).length !== 4) {
      logger.warn('Attempted upload without all 4 images');
      return;
    }

    const formData = new FormData();
    formData.append('north', images.north!.file);
    formData.append('south', images.south!.file);
    formData.append('east', images.east!.file);
    formData.append('west', images.west!.file);

    uploadMutation.mutate(formData);
  };

  const allImagesUploaded = Object.keys(images).length === 4;

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <header className="w-full px-6 py-4 bg-white/70 backdrop-blur-md border-b border-amber-100">
        <div className="max-w-7xl mx-auto flex items-center gap-2">
          <div className="w-10 h-10 bg-amber-600 rounded-xl flex items-center justify-center">
            <Compass className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-amber-900">Upload Room Photos</h1>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Panel - Drop Zone */}
          <div className="space-y-6">
            <div className="bg-white/80 rounded-2xl p-6 border border-amber-100">
              <h2 className="text-lg font-semibold text-amber-950 mb-4">
                Upload {DIRECTIONS.find(d => d.key === activeDirection)?.label} Image
              </h2>
              
              <div
                className={`aspect-square border-2 border-dashed rounded-2xl flex flex-col items-center justify-center cursor-pointer transition-all ${
                  isDragActive 
                    ? 'border-amber-500 bg-amber-50' 
                    : 'border-amber-300 bg-white/50 hover:bg-amber-50'
                }`}
                onDragEnter={(e) => {
                  e.preventDefault();
                  setIsDragActive(true);
                }}
                onDragOver={(e) => {
                  e.preventDefault();
                  setIsDragActive(true);
                }}
                onDragLeave={(e) => {
                  e.preventDefault();
                  setIsDragActive(false);
                }}
                onDrop={onDropZoneDrop}
                onClick={() => {
                  const input = document.getElementById('room-upload-input') as HTMLInputElement | null;
                  input?.click();
                }}
              >
                <input
                  id="room-upload-input"
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  className="hidden"
                  onChange={onFileInputChange}
                />
                
                {images[activeDirection] ? (
                  <div className="relative w-full h-full p-4">
                    <img
                      src={images[activeDirection]!.preview}
                      alt={activeDirection}
                      className="w-full h-full object-cover rounded-xl"
                    />
                    <div className="absolute inset-0 bg-black/20 rounded-xl" />
                    <div className="absolute top-2 right-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                      <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        removeImage(activeDirection);
                      }}
                      className="absolute top-6 right-6 p-2 bg-white/90 rounded-full text-amber-700 hover:text-red-600 shadow-lg"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="w-20 h-20 bg-amber-100 rounded-full flex items-center justify-center mb-4">
                      {(() => {
                        const Icon = DIRECTIONS.find(d => d.key === activeDirection)?.icon || UploadIcon;
                        return <Icon className="w-10 h-10 text-amber-600" />;
                      })()}
                    </div>
                    <p className="text-amber-700 font-medium mb-2">
                      {isDragActive ? 'Drop image here' : 'Drag & drop an image'}
                    </p>
                    <p className="text-amber-500 text-sm">or click to browse</p>
                    <p className="text-amber-400 text-xs mt-2">
                      {DIRECTIONS.find(d => d.key === activeDirection)?.description}
                    </p>
                  </>
                )}
              </div>
            </div>

            {/* Instructions */}
            <div className="bg-white/60 rounded-xl p-4 border border-amber-100">
              <h3 className="text-sm font-medium text-amber-800 mb-2">Instructions:</h3>
              <ul className="text-sm text-amber-600 space-y-1">
                <li>• Upload 4 photos from each direction</li>
                <li>Stand in the center of the room</li>
                <li>Take clear, well-lit photos</li>
                <li>Max file size: 10MB per image</li>
              </ul>
            </div>
          </div>

          {/* Right Panel - Direction Grid */}
          <div className="space-y-6">
            <div className="bg-white/80 rounded-2xl p-6 border border-amber-100">
              <h2 className="text-lg font-semibold text-amber-950 mb-4">Room Overview</h2>
              
              <div className="grid grid-cols-2 gap-4">
                {DIRECTIONS.map(({ key, label, icon: Icon }) => {
                  const hasImage = !!images[key];
                  const isActive = activeDirection === key;
                  
                  return (
                    <button
                      key={key}
                      onClick={() => setActiveDirection(key)}
                      className={`relative aspect-square rounded-xl border-2 transition-all ${
                        isActive 
                          ? 'border-amber-500 bg-amber-50' 
                          : hasImage
                            ? 'border-green-400 bg-green-50'
                            : 'border-amber-200 bg-white/50 hover:bg-amber-50'
                      }`}
                    >
                      {hasImage ? (
                        <>
                          <img
                            src={images[key]!.preview}
                            alt={label}
                            className="absolute inset-0 w-full h-full object-cover rounded-xl"
                          />
                          <div className="absolute inset-0 bg-black/20 rounded-xl" />
                          <div className="absolute top-2 right-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                            <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                            </svg>
                          </div>
                        </>
                      ) : (
                        <div className="flex flex-col items-center justify-center h-full">
                          <Icon className={`w-8 h-8 mb-2 ${isActive ? 'text-amber-600' : 'text-amber-400'}`} />
                          <span className={`text-sm font-medium ${isActive ? 'text-amber-700' : 'text-amber-500'}`}>
                            {label}
                          </span>
                        </div>
                      )}
                      
                      <div className="absolute bottom-2 left-2 px-2 py-1 bg-white/90 rounded text-xs font-medium text-amber-700">
                        {label}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmit}
              disabled={!allImagesUploaded || uploadMutation.isPending}
              className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-amber-600 hover:bg-amber-700 disabled:bg-amber-300 text-white rounded-xl font-semibold transition-all"
            >
              {uploadMutation.isPending ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Uploading...
                </>
              ) : (
                <>
                  <UploadIcon className="w-5 h-5" />
                  {allImagesUploaded ? 'Upload & Continue' : `Upload ${Object.keys(images).length}/4 Images`}
                </>
              )}
            </button>

            {uploadMutation.isError && (
              <p className="text-red-600 text-sm text-center">
                Upload failed. Please try again.
              </p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export async function getServerSideProps() {
  return { props: {} };
}
