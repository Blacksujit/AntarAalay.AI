import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { analyzeVastu, getVastuRemedies, roomTypes, directions, getDirectionColor, getElementIcon } from '../services/vastu';
import { Sparkles, Compass, AlertTriangle, CheckCircle, Lightbulb, ArrowRight } from 'lucide-react';

export default function Vastu() {
  const [selectedRoom, setSelectedRoom] = useState('');
  const [selectedDirection, setSelectedDirection] = useState('');

  const analyzeMutation = useMutation({
    mutationFn: () => analyzeVastu({ direction: selectedDirection, room_type: selectedRoom }),
    enabled: selectedRoom && selectedDirection,
  });

  const remediesMutation = useMutation({
    mutationFn: () => getVastuRemedies(selectedDirection, selectedRoom),
    enabled: selectedRoom && selectedDirection,
  });

  const handleAnalyze = () => {
    if (selectedRoom && selectedDirection) {
      analyzeMutation.mutate();
    }
  };

  const handleGetRemedies = () => {
    if (selectedRoom && selectedDirection) {
      remediesMutation.mutate();
    }
  };

  const result = analyzeMutation.data;

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <header className="w-full px-6 py-4 bg-white/70 backdrop-blur-md border-b border-amber-100">
        <div className="max-w-7xl mx-auto flex items-center gap-2">
          <div className="w-10 h-10 bg-amber-600 rounded-xl flex items-center justify-center">
            <Compass className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-amber-900">Vastu Analysis</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-12">
        {/* Selection Form */}
        <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-amber-100 shadow-sm mb-8">
          <h2 className="text-xl font-semibold text-amber-950 mb-6">Select Room & Direction</h2>
          
          <div className="grid md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium text-amber-800 mb-2">Room Type</label>
              <select
                value={selectedRoom}
                onChange={(e) => {
                  setSelectedRoom(e.target.value);
                  analyzeMutation.reset();
                  remediesMutation.reset();
                }}
                className="w-full px-4 py-3 bg-white border border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
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
                value={selectedDirection}
                onChange={(e) => {
                  setSelectedDirection(e.target.value);
                  analyzeMutation.reset();
                  remediesMutation.reset();
                }}
                className="w-full px-4 py-3 bg-white border border-amber-200 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent"
              >
                <option value="">Select direction</option>
                {directions.map((dir) => (
                  <option key={dir.value} value={dir.value}>
                    {dir.label} ({dir.element})
                  </option>
                ))}
              </select>
            </div>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={!selectedRoom || !selectedDirection || analyzeMutation.isPending}
            className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-amber-600 hover:bg-amber-700 disabled:bg-amber-300 text-white rounded-xl font-semibold transition-all"
          >
            {analyzeMutation.isPending ? (
              <>
                <span className="animate-spin">⟳</span>
                Analyzing...
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                Analyze Vastu
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {result && (
          <div className="space-y-6">
            {/* Score Card */}
            <div className="bg-white/80 backdrop-blur-sm rounded-2xl p-8 border border-amber-100 shadow-sm">
              <div className="text-center mb-6">
                <div className={`inline-flex items-center justify-center w-24 h-24 rounded-full mb-4 ${
                  result.vastu_score >= 80 ? 'bg-green-100' :
                  result.vastu_score >= 60 ? 'bg-amber-100' :
                  result.vastu_score >= 40 ? 'bg-orange-100' :
                  'bg-red-100'
                }`}>
                  <span className={`text-4xl font-bold ${
                    result.vastu_score >= 80 ? 'text-green-600' :
                    result.vastu_score >= 60 ? 'text-amber-600' :
                    result.vastu_score >= 40 ? 'text-orange-500' :
                    'text-red-500'
                  }`}>
                    {result.vastu_score}%
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-amber-950 mb-1">
                  {result.direction_rating === 'excellent' ? 'Excellent Alignment!' :
                   result.direction_rating === 'good' ? 'Good Alignment' :
                   result.direction_rating === 'neutral' ? 'Neutral Alignment' :
                   'Needs Improvement'}
                </h3>
                <p className="text-amber-600 capitalize">{selectedRoom.replace('_', ' ')} in {selectedDirection}</p>
              </div>

              {/* Element Info */}
              {result.element_balance && (
                <div className="flex justify-center gap-8 mb-6 pb-6 border-b border-amber-100">
                  <div className="text-center">
                    <div className="text-3xl mb-1">{getElementIcon(result.element_balance.dominant_element)}</div>
                    <p className="text-sm text-amber-600">{result.element_balance.dominant_element}</p>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl mb-1">🪐</div>
                    <p className="text-sm text-amber-600">{result.element_balance.ruling_planet}</p>
                  </div>
                </div>
              )}

              {/* Suggestions */}
              {result.suggestions.length > 0 && (
                <div className="mb-6">
                  <h4 className="flex items-center gap-2 text-lg font-semibold text-green-700 mb-4">
                    <CheckCircle className="w-5 h-5" />
                    Vastu Suggestions
                  </h4>
                  <ul className="space-y-3">
                    {result.suggestions.map((suggestion: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
                        <span className="text-green-600 mt-0.5">✓</span>
                        <span className="text-green-800">{suggestion}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Warnings */}
              {result.warnings.length > 0 && (
                <div>
                  <h4 className="flex items-center gap-2 text-lg font-semibold text-orange-700 mb-4">
                    <AlertTriangle className="w-5 h-5" />
                    Areas to Watch
                  </h4>
                  <ul className="space-y-3">
                    {result.warnings.map((warning: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-3 p-3 bg-orange-50 rounded-lg">
                        <span className="text-orange-600 mt-0.5">!</span>
                        <span className="text-orange-800">{warning}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Remedies Section */}
            {result.vastu_score < 70 && (
              <div className="bg-gradient-to-r from-amber-600 to-orange-600 rounded-2xl p-8 text-white">
                <div className="flex items-center gap-3 mb-4">
                  <Lightbulb className="w-6 h-6" />
                  <h3 className="text-xl font-semibold">Vastu Remedies Available</h3>
                </div>
                <p className="text-amber-100 mb-6">
                  Get personalized remedies to improve the Vastu score of your space.
                </p>
                <button
                  onClick={handleGetRemedies}
                  disabled={remediesMutation.isPending}
                  className="flex items-center gap-2 px-6 py-3 bg-white text-amber-600 rounded-xl font-semibold hover:bg-amber-50 transition-all disabled:opacity-70"
                >
                  {remediesMutation.isPending ? (
                    <>
                      <span className="animate-spin">⟳</span>
                      Loading...
                    </>
                  ) : (
                    <>
                      Get Remedies
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>

                {remediesMutation.data && (
                  <div className="mt-6 p-6 bg-white/10 backdrop-blur-sm rounded-xl">
                    <h4 className="font-semibold mb-4">Recommended Remedies:</h4>
                    <ul className="space-y-2">
                      {remediesMutation.data.remedies.map((remedy: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2">
                          <span className="text-amber-200">•</span>
                          <span className="text-amber-100">{remedy}</span>
                        </li>
                      ))}
                    </ul>
                    <div className="mt-4 pt-4 border-t border-white/20">
                      <p className="text-sm text-amber-200">
                        Improvement Potential: Up to {remediesMutation.data.improvement_potential}%
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
