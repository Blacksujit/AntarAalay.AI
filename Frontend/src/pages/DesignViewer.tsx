import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import { 
  Eye, 
  ArrowLeft, 
  Download, 
  Share2, 
  Heart, 
  Settings, 
  Loader2,
  RefreshCw,
  Sparkles,
} from 'lucide-react';
import { getRoomDesigns, regenerateDesign } from '../services/design';
import type { Design as DesignModel, CustomizationOptions } from '../services/design';
import { logger } from '../utils/logger';

const getDesignImages = (design: DesignModel | undefined): string[] => {
  if (!design) return [];
  return [design.image_1_url, design.image_2_url, design.image_3_url].filter(
    (u): u is string => typeof u === 'string' && u.length > 0
  );
};

export default function DesignViewer() {
  const { roomId } = useParams<{ roomId: string }>();
  const navigate = useNavigate();
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [showCustomization, setShowCustomization] = useState(false);

  // Fetch all designs for this room
  const { 
    data: designsData, 
    isLoading: designsLoading,
    refetch: refetchDesigns
  } = useQuery({
    queryKey: ['room-designs', roomId],
    queryFn: () => getRoomDesigns(roomId!),
    enabled: !!roomId,
  });

  // Get the latest design (first in array)
  const currentDesign = designsData?.designs?.[0];
  const generatedImages = getDesignImages(currentDesign);

  // Regenerate mutation
  const regenerateMutation = useMutation({
    mutationFn: (customization: CustomizationOptions) => {
      if (!currentDesign) {
        throw new Error('No current design to regenerate');
      }
      return regenerateDesign(currentDesign.id, customization);
    },
    onSuccess: (data) => {
      logger.info('Design regenerated', { designId: (data as { design_id?: string }).design_id });
      refetchDesigns();
    },
    onError: (error) => {
      logger.error('Design regeneration failed', {}, error as Error);
    },
  });

  if (designsLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-indigo-600 mx-auto mb-4" />
          <p className="text-indigo-700">Loading your designs...</p>
        </div>
      </div>
    );
  }

  if (!currentDesign) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">No designs found for this room</p>
          <button
            onClick={() => navigate(`/customize/${roomId}`)}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            Generate Designs
          </button>
        </div>
      </div>
    );
  }

  const handleRegenerate = (newCustomization: CustomizationOptions) => {
    regenerateMutation.mutate(newCustomization);
  };

  const handleDownload = (imageUrl: string, index: number) => {
    const link = document.createElement('a');
    link.href = imageUrl;
    link.download = `design-${currentDesign.id}-variant-${index + 1}.jpg`;
    link.click();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="w-full px-6 py-4 bg-white/70 backdrop-blur-md border-b border-indigo-100">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate(-1)}
              className="p-2 hover:bg-indigo-100 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5 text-indigo-700" />
            </button>
            <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center">
              <Eye className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-indigo-900">Your AI Designs</h1>
              <p className="text-indigo-600 text-sm">
                {currentDesign.style}
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowCustomization(!showCustomization)}
              className="p-2 hover:bg-indigo-100 rounded-lg transition-colors"
            >
              <Settings className="w-5 h-5 text-indigo-700" />
            </button>
            <button
              onClick={() => handleDownload(generatedImages[selectedImageIndex], selectedImageIndex)}
              className="p-2 hover:bg-indigo-100 rounded-lg transition-colors"
            >
              <Download className="w-5 h-5 text-indigo-700" />
            </button>
            <button className="p-2 hover:bg-indigo-100 rounded-lg transition-colors">
              <Share2 className="w-5 h-5 text-indigo-700" />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Image Display */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white/80 rounded-2xl p-6 border border-indigo-100">
              <div className="relative aspect-square rounded-xl overflow-hidden bg-gray-100">
                {generatedImages[selectedImageIndex] ? (
                  <img
                    src={generatedImages[selectedImageIndex]}
                    alt={`Design variant ${selectedImageIndex + 1}`}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <Loader2 className="w-8 h-8 animate-spin text-indigo-400" />
                  </div>
                )}
                
                {/* Image Navigation */}
                {generatedImages.length > 1 && (
                  <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2">
                    {generatedImages.map((_: string, index: number) => (
                      <button
                        key={index}
                        onClick={() => setSelectedImageIndex(index)}
                        className={`w-2 h-2 rounded-full transition-all ${
                          selectedImageIndex === index
                            ? 'bg-white w-8'
                            : 'bg-white/50'
                        }`}
                      />
                    ))}
                  </div>
                )}
              </div>
              
              {/* Image Thumbnails */}
              {generatedImages.length > 1 && (
                <div className="flex gap-2 mt-4">
                  {generatedImages.map((image: string, index: number) => (
                    <button
                      key={index}
                      onClick={() => setSelectedImageIndex(index)}
                      className={`relative aspect-square w-20 rounded-lg overflow-hidden border-2 transition-all ${
                        selectedImageIndex === index
                          ? 'border-indigo-500 scale-105'
                          : 'border-indigo-200 hover:border-indigo-300'
                      }`}
                    >
                      <img
                        src={image}
                        alt={`Variant ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Design Details */}
            <div className="bg-white/80 rounded-2xl p-6 border border-indigo-100">
              <h3 className="text-lg font-semibold text-indigo-950 mb-4">Design Details</h3>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-indigo-600">Style:</span>
                  <span className="ml-2 font-medium text-indigo-900 capitalize">
                    {currentDesign.style}
                  </span>
                </div>
                <div>
                  <span className="text-indigo-600">Wall Color:</span>
                  <span className="ml-2 font-medium text-indigo-900">
                    {'Default'}
                  </span>
                </div>
                <div>
                  <span className="text-indigo-600">Flooring:</span>
                  <span className="ml-2 font-medium text-indigo-900">
                    {'Default'}
                  </span>
                </div>
                <div>
                  <span className="text-indigo-600">Furniture:</span>
                  <span className="ml-2 font-medium text-indigo-900">
                    {'Default'}
                  </span>
                </div>
              </div>
              
              <div className="mt-4" />
            </div>
          </div>

          {/* Right Panel - Actions & Customization */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white/80 rounded-2xl p-6 border border-indigo-100">
              <h3 className="text-lg font-semibold text-indigo-950 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button
                  onClick={() => handleDownload(generatedImages[selectedImageIndex], selectedImageIndex)}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-medium transition-colors"
                >
                  <Download className="w-4 h-4" />
                  Download This Design
                </button>
                
                <button className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-white border-2 border-indigo-200 hover:bg-indigo-50 text-indigo-700 rounded-xl font-medium transition-colors">
                  <Heart className="w-4 h-4" />
                  Save to Favorites
                </button>
                
                <button className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-white border-2 border-indigo-200 hover:bg-indigo-50 text-indigo-700 rounded-xl font-medium transition-colors">
                  <Share2 className="w-4 h-4" />
                  Share Design
                </button>
              </div>
            </div>

            {/* Regenerate Options */}
            {showCustomization && (
              <div className="bg-white/80 rounded-2xl p-6 border border-indigo-100">
                <h3 className="text-lg font-semibold text-indigo-950 mb-4 flex items-center gap-2">
                  <RefreshCw className="w-5 h-5 text-indigo-600" />
                  Regenerate Design
                </h3>
                
                <div className="space-y-4">
                  <div>
                    <label className="text-sm font-medium text-indigo-700">Change Style</label>
                    <select 
                      className="w-full mt-1 px-3 py-2 border border-indigo-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      defaultValue={currentDesign.style}
                    >
                      <option value="modern">Modern</option>
                      <option value="traditional">Traditional</option>
                      <option value="contemporary">Contemporary</option>
                      <option value="minimalist">Minimalist</option>
                      <option value="luxury">Luxury</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium text-indigo-700">Wall Color</label>
                    <select 
                      className="w-full mt-1 px-3 py-2 border border-indigo-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      defaultValue={''}
                    >
                      <option value="warm beige">Warm Beige</option>
                      <option value="soft white">Soft White</option>
                      <option value="sage green">Sage Green</option>
                      <option value="sky blue">Sky Blue</option>
                      <option value="terracotta">Terracotta</option>
                    </select>
                  </div>
                  
                  <button
                    onClick={() => handleRegenerate({
                      style: 'modern', // These would come from the form
                      wall_color: 'warm beige',
                      flooring: 'hardwood',
                      furniture_style: 'modern',
                    })}
                    disabled={regenerateMutation.isPending}
                    className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 disabled:from-indigo-400 disabled:to-purple-400 text-white rounded-xl font-medium transition-all"
                  >
                    {regenerateMutation.isPending ? (
                      <>
                        <Loader2 className="w-4 h-4 animate-spin" />
                        Regenerating...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4" />
                        Regenerate with Changes
                      </>
                    )}
                  </button>
                </div>
              </div>
            )}

            {/* Design History */}
            {designsData?.designs && designsData.designs.length > 1 && (
              <div className="bg-white/80 rounded-2xl p-6 border border-indigo-100">
                <h3 className="text-lg font-semibold text-indigo-950 mb-4">Design History</h3>
                <div className="space-y-2">
                  {designsData.designs.slice(0, 5).map((design: DesignModel) => (
                    <button
                      key={design.id}
                      className={`w-full p-3 rounded-lg border-2 text-left transition-all ${
                        design.id === currentDesign.id
                          ? 'border-indigo-500 bg-indigo-50'
                          : 'border-indigo-200 hover:bg-indigo-50'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-indigo-900 capitalize">
                            {design.style}
                          </div>
                          <div className="text-xs text-indigo-600">
                            {new Date(design.created_at).toLocaleDateString()}
                          </div>
                        </div>
                        {design.id === currentDesign.id && (
                          <div className="w-2 h-2 bg-indigo-500 rounded-full" />
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
