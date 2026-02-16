import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from '@tanstack/react-query';
import { getRoomDesignsWithDetails, regenerateDesign } from '../services/design';
import type { FurnitureItem } from '../services/design';
import { getDirectionColor } from '../services/vastu';
import { Sparkles, ArrowLeft, CheckCircle, AlertTriangle, IndianRupee, Home, RefreshCw, Palette } from 'lucide-react';

export default function Designs() {
  const { roomId } = useParams<{ roomId: string }>();
  const navigate = useNavigate();
  const [showCustomize, setShowCustomize] = useState(false);
  const [customization, setCustomization] = useState({
    wall_color: '',
    flooring: '',
    furniture_style: '',
    style: 'modern'
  });

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['roomDesigns', roomId],
    queryFn: () => getRoomDesignsWithDetails(roomId!),
    enabled: !!roomId,
  });

  const regenerateMutation = useMutation({
    mutationFn: (designId: string) => regenerateDesign(designId, customization),
    onSuccess: () => {
      refetch();
      setShowCustomize(false);
    }
  });

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-amber-200 border-t-amber-600 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-amber-700">Loading your designs...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">Failed to load designs</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 bg-amber-600 text-white rounded-lg"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const { designs, room } = data;
  const latestDesign = designs[0]?.design;

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <header className="w-full px-6 py-4 bg-white/70 backdrop-blur-md border-b border-amber-100 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto flex items-center gap-4">
          <button
            onClick={() => navigate('/dashboard')}
            className="p-2 hover:bg-amber-100 rounded-lg transition-all"
          >
            <ArrowLeft className="w-6 h-6 text-amber-700" />
          </button>
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-amber-600 rounded-xl flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-amber-900">Your Designs</h1>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {designs.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-amber-700 mb-4">No designs generated yet.</p>
            <button
              onClick={() => navigate('/upload')}
              className="px-6 py-3 bg-amber-600 text-white rounded-xl font-medium"
            >
              Create New Design
            </button>
          </div>
        ) : (
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Original Room */}
            <div className="lg:col-span-1">
              <h2 className="text-xl font-semibold text-amber-950 mb-4">Original Room</h2>
              <div className="bg-white/80 rounded-2xl overflow-hidden border border-amber-100 shadow-sm">
                <img
                  src={room.image_url}
                  alt="Original room"
                  className="w-full aspect-square object-cover"
                />
                <div className="p-4">
                  <div className="flex items-center gap-2 mb-2">
                    <Home className="w-4 h-4 text-amber-600" />
                    <span className="capitalize text-amber-800 font-medium">
                      {room.room_type || 'Room'}
                    </span>
                  </div>
                  {room.direction && (
                    <div className="flex items-center gap-2">
                      <span className={`w-3 h-3 rounded-full ${getDirectionColor(room.direction)}`} />
                      <span className="capitalize text-amber-600 text-sm">
                        {room.direction} direction
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Generated Designs */}
            <div className="lg:col-span-2">
              <h2 className="text-xl font-semibold text-amber-950 mb-4">AI Generated Designs</h2>
              
              {latestDesign?.status === 'pending' ? (
                <div className="bg-white/80 rounded-2xl p-12 text-center border border-amber-100">
                  <div className="w-16 h-16 border-4 border-amber-200 border-t-amber-600 rounded-full animate-spin mx-auto mb-4" />
                  <p className="text-amber-700">Generating your designs...</p>
                  <p className="text-amber-500 text-sm mt-2">This may take a minute</p>
                </div>
              ) : (
                <div className="space-y-6">
                  {/* Design Variations */}
                  <div className="grid md:grid-cols-3 gap-4">
                    {[latestDesign?.image_1_url, latestDesign?.image_2_url, latestDesign?.image_3_url]
                      .filter(Boolean)
                      .map((url, idx) => (
                        <div
                          key={idx}
                          className="bg-white/80 rounded-2xl overflow-hidden border border-amber-100 shadow-sm"
                        >
                          <img
                            src={url}
                            alt={`Design ${idx + 1}`}
                            className="w-full aspect-square object-cover"
                          />
                          <div className="p-3 text-center">
                            <span className="text-sm text-amber-600 font-medium">
                              Variation {idx + 1}
                            </span>
                          </div>
                        </div>
                      ))}
                  </div>

                  {/* Customization & Regenerate */}
                  {latestDesign?.status === 'completed' && (
                    <div className="bg-white/80 rounded-2xl p-6 border border-amber-100">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="font-semibold text-amber-950 flex items-center gap-2">
                          <Palette className="w-5 h-5 text-amber-600" />
                          Customize & Regenerate
                        </h3>
                        <button
                          onClick={() => setShowCustomize(!showCustomize)}
                          className="text-amber-600 hover:text-amber-700 font-medium text-sm"
                        >
                          {showCustomize ? 'Hide' : 'Show'} Options
                        </button>
                      </div>
                      
                      {showCustomize && (
                        <div className="space-y-4">
                          <div className="grid md:grid-cols-2 gap-4">
                            <div>
                              <label className="block text-sm font-medium text-amber-800 mb-1">
                                Wall Color
                              </label>
                              <input
                                type="text"
                                value={customization.wall_color}
                                onChange={(e) => setCustomization({...customization, wall_color: e.target.value})}
                                placeholder="e.g., warm beige, sky blue"
                                className="w-full px-3 py-2 border border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
                              />
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-amber-800 mb-1">
                                Flooring
                              </label>
                              <input
                                type="text"
                                value={customization.flooring}
                                onChange={(e) => setCustomization({...customization, flooring: e.target.value})}
                                placeholder="e.g., hardwood, marble tiles"
                                className="w-full px-3 py-2 border border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
                              />
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-amber-800 mb-1">
                                Furniture Style
                              </label>
                              <input
                                type="text"
                                value={customization.furniture_style}
                                onChange={(e) => setCustomization({...customization, furniture_style: e.target.value})}
                                placeholder="e.g., modern, traditional Indian"
                                className="w-full px-3 py-2 border border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
                              />
                            </div>
                            <div>
                              <label className="block text-sm font-medium text-amber-800 mb-1">
                                Overall Style
                              </label>
                              <select
                                value={customization.style}
                                onChange={(e) => setCustomization({...customization, style: e.target.value})}
                                className="w-full px-3 py-2 border border-amber-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
                              >
                                <option value="modern">Modern</option>
                                <option value="traditional">Traditional Indian</option>
                                <option value="contemporary">Contemporary</option>
                                <option value="minimalist">Minimalist</option>
                                <option value="luxury">Luxury</option>
                              </select>
                            </div>
                          </div>
                          
                          <button
                            onClick={() => regenerateMutation.mutate(latestDesign.id)}
                            disabled={regenerateMutation.isPending}
                            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-amber-600 text-white rounded-xl font-medium hover:bg-amber-700 disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {regenerateMutation.isPending ? (
                              <>
                                <RefreshCw className="w-5 h-5 animate-spin" />
                                Regenerating...
                              </>
                            ) : (
                              <>
                                <RefreshCw className="w-5 h-5" />
                                Regenerate with Customizations
                              </>
                            )}
                          </button>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Budget & Vastu Summary */}
                  {latestDesign?.status === 'completed' && (
                    <div className="grid md:grid-cols-2 gap-6">
                      {/* Budget Breakdown */}
                      {latestDesign.estimated_cost && (
                        <div className="bg-white/80 rounded-2xl p-6 border border-amber-100">
                          <div className="flex items-center gap-2 mb-4">
                            <IndianRupee className="w-5 h-5 text-amber-600" />
                            <h3 className="font-semibold text-amber-950">Budget Breakdown</h3>
                          </div>
                          <div className="space-y-3">
                            <div className="flex justify-between">
                              <span className="text-amber-700">Estimated Cost:</span>
                              <span className="font-semibold text-amber-900">
                                ₹{latestDesign.estimated_cost.toLocaleString()}
                              </span>
                            </div>
                            {latestDesign.budget && (
                              <div className="flex justify-between">
                                <span className="text-amber-700">Your Budget:</span>
                                <span className="font-semibold text-amber-900">
                                  ₹{latestDesign.budget.toLocaleString()}
                                </span>
                              </div>
                            )}
                            {latestDesign.budget_match_percentage && (
                              <div className="flex justify-between">
                                <span className="text-amber-700">Budget Match:</span>
                                <span className={`font-semibold ${
                                  latestDesign.budget_match_percentage <= 100 
                                    ? 'text-green-600' 
                                    : 'text-orange-600'
                                }`}>
                                  {latestDesign.budget_match_percentage}%
                                </span>
                              </div>
                            )}
                          </div>
                          
                          {latestDesign.furniture_breakdown && (
                            <div className="mt-4 pt-4 border-t border-amber-100">
                              <h4 className="text-sm font-medium text-amber-800 mb-3">Furniture Items:</h4>
                              <div className="space-y-2">
                                {Object.entries(latestDesign.furniture_breakdown).map(([item, details]) => (
                                  <div key={item} className="flex justify-between text-sm">
                                    <span className="capitalize text-amber-600">{item}</span>
                                    <span className="text-amber-800">
                                      ₹{(details as FurnitureItem).adjusted_price.toLocaleString()}
                                    </span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Vastu Score */}
                      {latestDesign.vastu_score !== undefined && (
                        <div className="bg-white/80 rounded-2xl p-6 border border-amber-100">
                          <div className="flex items-center gap-2 mb-4">
                            <Sparkles className="w-5 h-5 text-amber-600" />
                            <h3 className="font-semibold text-amber-950">Vastu Analysis</h3>
                          </div>
                          
                          <div className="text-center mb-4">
                            <div className={`text-4xl font-bold mb-1 ${
                              latestDesign.vastu_score >= 80 ? 'text-green-600' :
                              latestDesign.vastu_score >= 60 ? 'text-amber-600' :
                              latestDesign.vastu_score >= 40 ? 'text-orange-500' :
                              'text-red-500'
                            }`}>
                              {latestDesign.vastu_score}%
                            </div>
                            <span className="text-sm text-amber-600">Vastu Score</span>
                          </div>

                          {latestDesign.vastu_suggestions && latestDesign.vastu_suggestions.length > 0 && (
                            <div className="mb-4">
                              <h4 className="text-sm font-medium text-green-700 mb-2 flex items-center gap-1">
                                <CheckCircle className="w-4 h-4" /> Suggestions
                              </h4>
                              <ul className="space-y-1">
                                {latestDesign.vastu_suggestions.slice(0, 3).map((suggestion, idx) => (
                                  <li key={idx} className="text-sm text-amber-700">{suggestion}</li>
                                ))}
                              </ul>
                            </div>
                          )}

                          {latestDesign.vastu_warnings && latestDesign.vastu_warnings.length > 0 && (
                            <div>
                              <h4 className="text-sm font-medium text-orange-700 mb-2 flex items-center gap-1">
                                <AlertTriangle className="w-4 h-4" /> Warnings
                              </h4>
                              <ul className="space-y-1">
                                {latestDesign.vastu_warnings.slice(0, 3).map((warning, idx) => (
                                  <li key={idx} className="text-sm text-amber-700">{warning}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
