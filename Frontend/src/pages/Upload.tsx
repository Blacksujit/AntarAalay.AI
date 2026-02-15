import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { uploadRoom } from '../services/upload';
import { directions, roomTypes } from '../services/vastu';
import { Upload, X, Image as ImageIcon, Sparkles } from 'lucide-react';

export default function UploadPage() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [roomType, setRoomType] = useState('');
  const [direction, setDirection] = useState('');
  const [budget, setBudget] = useState(50000);

  const uploadMutation = useMutation({
    mutationFn: uploadRoom,
    onSuccess: (data) => {
      navigate(`/designs/${data.room_id}`);
    },
  });

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
  };

  const handleSubmit = () => {
    if (!selectedFile) return;
    
    uploadMutation.mutate({
      file: selectedFile,
      roomType: roomType || undefined,
      direction: direction || undefined,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <header className="w-full px-6 py-4 bg-white/70 backdrop-blur-md border-b border-amber-100">
        <div className="max-w-7xl mx-auto flex items-center gap-2">
          <div className="w-10 h-10 bg-amber-600 rounded-xl flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-amber-900">Upload Room</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-12">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Image Upload */}
          <div>
            <h2 className="text-xl font-semibold text-amber-950 mb-4">Room Photo</h2>
            
            {!previewUrl ? (
              <div
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                className="aspect-square border-2 border-dashed border-amber-300 rounded-2xl flex flex-col items-center justify-center bg-white/50 hover:bg-white/80 transition-all cursor-pointer"
                onClick={() => document.getElementById('file-input')?.click()}
              >
                <ImageIcon className="w-16 h-16 text-amber-300 mb-4" />
                <p className="text-amber-700 font-medium mb-2">Drag & drop an image</p>
                <p className="text-amber-500 text-sm">or click to browse</p>
                <input
                  id="file-input"
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  className="hidden"
                />
              </div>
            ) : (
              <div className="relative aspect-square rounded-2xl overflow-hidden">
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="w-full h-full object-cover"
                />
                <button
                  onClick={clearSelection}
                  className="absolute top-4 right-4 p-2 bg-white/90 rounded-full text-amber-700 hover:text-red-600 shadow-lg"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            )}
          </div>

          {/* Form */}
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-amber-800 mb-2">Room Type</label>
              <select
                value={roomType}
                onChange={(e) => setRoomType(e.target.value)}
                className="w-full px-4 py-3 bg-white/80 border border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
              >
                <option value="">Select room type</option>
                {roomTypes.map((type) => (
                  <option key={type.value} value={type.value}>{type.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-amber-800 mb-2">Direction</label>
              <select
                value={direction}
                onChange={(e) => setDirection(e.target.value)}
                className="w-full px-4 py-3 bg-white/80 border border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
              >
                <option value="">Select direction</option>
                {directions.map((dir) => (
                  <option key={dir.value} value={dir.value}>{dir.label}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-amber-800 mb-2">
                Budget: ₹{budget.toLocaleString()}
              </label>
              <input
                type="range"
                min="10000"
                max="500000"
                step="5000"
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full h-2 bg-amber-200 rounded-lg appearance-none cursor-pointer accent-amber-600"
              />
              <div className="flex justify-between text-xs text-amber-600 mt-1">
                <span>₹10K</span>
                <span>₹5L</span>
              </div>
            </div>

            <button
              onClick={handleSubmit}
              disabled={!selectedFile || uploadMutation.isPending}
              className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-amber-600 hover:bg-amber-700 disabled:bg-amber-300 text-white rounded-xl font-semibold transition-all"
            >
              {uploadMutation.isPending ? (
                <>
                  <span className="animate-spin">⟳</span>
                  Uploading...
                </>
              ) : (
                <>
                  <Upload className="w-5 h-5" />
                  Upload & Generate
                </>
              )}
            </button>

            {uploadMutation.isError && (
              <p className="text-red-600 text-sm">
                Upload failed. Please try again.
              </p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
