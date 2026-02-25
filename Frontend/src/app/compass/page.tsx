'use client';

import { useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { 
  analyzeVastu, 
  getVastuRemedies, 
  getVastuScore,
  roomTypes, 
  directions, 
  getElementIcon,
  getDirectionColor,
  type VastuAnalyzeResponse
} from '../../services/vastu';
import { 
  Sparkles, 
  Compass, 
  AlertTriangle, 
  CheckCircle, 
  Lightbulb, 
  ArrowRight,
  Home,
  TrendingUp,
  Shield,
  Info
} from 'lucide-react';
import Link from 'next/link';

export default function CompassPage() {
  const [selectedRoom, setSelectedRoom] = useState('');
  const [selectedDirection, setSelectedDirection] = useState('');

  const analyzeMutation = useMutation({
    mutationFn: () => analyzeVastu({ direction: selectedDirection, room_type: selectedRoom }),
  });

  const remediesMutation = useMutation({
    mutationFn: () => getVastuRemedies(selectedDirection, selectedRoom),
  });

  const scoreQuery = useQuery({
    queryKey: ['vastu-score', selectedDirection, selectedRoom],
    queryFn: () => getVastuScore(selectedDirection, selectedRoom),
    enabled: !!selectedDirection && !!selectedRoom,
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
  const remedies = remediesMutation.data;
  const score = scoreQuery.data;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-amber-600';
    return 'text-red-600';
  };

  const getScoreBg = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-amber-100';
    return 'bg-red-100';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <header className="w-full px-6 py-4 bg-white/70 backdrop-blur-md border-b border-amber-100">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/dashboard" className="p-2 hover:bg-amber-100 rounded-lg transition-colors">
              <Home className="w-5 h-5 text-amber-700" />
            </Link>
            <div className="w-10 h-10 bg-amber-600 rounded-xl flex items-center justify-center">
              <Compass className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-amber-900">Spatial Harmony Compass</h1>
          </div>
          <Link 
            href="/upload" 
            className="flex items-center gap-2 px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-medium transition-colors"
          >
            Upload Room
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Selection Panel */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-amber-100 shadow-sm"
            >
              <h2 className="text-xl font-semibold text-amber-950 mb-6 flex items-center gap-2">
                <Compass className="w-5 h-5" />
                Room & Direction
              </h2>
              
              <div className="space-y-4">
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

                <div className="pt-4 space-y-3">
                  <button
                    onClick={handleAnalyze}
                    disabled={!selectedRoom || !selectedDirection || analyzeMutation.isPending}
                    className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-amber-600 hover:bg-amber-700 disabled:bg-amber-300 text-white rounded-xl font-semibold transition-all"
                  >
                    {analyzeMutation.isPending ? (
                      <>
                        <span className="animate-spin">⟳</span>
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-4 h-4" />
                        Analyze Vastu
                      </>
                    )}
                  </button>

                  {result && (
                    <button
                      onClick={handleGetRemedies}
                      disabled={remediesMutation.isPending}
                      className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-300 text-white rounded-xl font-semibold transition-all"
                    >
                      {remediesMutation.isPending ? (
                        <>
                          <span className="animate-spin">⟳</span>
                          Loading...
                        </>
                      ) : (
                        <>
                          <Lightbulb className="w-4 h-4" />
                          Get Remedies
                        </>
                      )}
                    </button>
                  )}
                </div>
              </div>

              {/* Quick Score */}
              {score && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`mt-6 p-4 rounded-xl ${getScoreBg(score.vastu_score)}`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Vastu Score</span>
                    <TrendingUp className="w-4 h-4" />
                  </div>
                  <div className={`text-2xl font-bold mt-1 ${getScoreColor(score.vastu_score)}`}>
                    {score.vastu_score}/100
                  </div>
                  <div className="text-xs text-gray-600 mt-1">{score.rating}</div>
                </motion.div>
              )}
            </motion.div>
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2 space-y-6">
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-amber-100 shadow-sm"
              >
                <h3 className="text-xl font-semibold text-amber-950 mb-6 flex items-center gap-2">
                  <Shield className="w-5 h-5" />
                  Analysis Results
                </h3>

                {/* Score Overview */}
                <div className="grid md:grid-cols-3 gap-4 mb-6">
                  <div className={`text-center p-4 rounded-xl ${getScoreBg(result.vastu_score)}`}>
                    <div className={`text-3xl font-bold ${getScoreColor(result.vastu_score)}`}>
                      {result.vastu_score}
                    </div>
                    <div className="text-sm text-gray-600 mt-1">Overall Score</div>
                  </div>
                  <div className="text-center p-4 bg-blue-50 rounded-xl">
                    <div className="text-2xl mb-1">{getElementIcon(result.element_balance.dominant_element)}</div>
                    <div className="text-sm font-medium text-blue-900">{result.element_balance.dominant_element}</div>
                    <div className="text-xs text-gray-600">Dominant Element</div>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-xl">
                    <div className="text-lg font-bold text-purple-900">{result.direction_rating}</div>
                    <div className="text-xs text-gray-600">Direction Rating</div>
                  </div>
                </div>

                {/* Suggestions */}
                {result.suggestions.length > 0 && (
                  <div className="mb-6">
                    <h4 className="font-medium text-green-800 mb-3 flex items-center gap-2">
                      <CheckCircle className="w-4 h-4" />
                      Positive Aspects
                    </h4>
                    <ul className="space-y-2">
                      {result.suggestions.map((suggestion, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                          <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-1.5 flex-shrink-0" />
                          {suggestion}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Warnings */}
                {result.warnings.length > 0 && (
                  <div>
                    <h4 className="font-medium text-amber-800 mb-3 flex items-center gap-2">
                      <AlertTriangle className="w-4 h-4" />
                      Areas for Improvement
                    </h4>
                    <ul className="space-y-2">
                      {result.warnings.map((warning, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                          <span className="w-1.5 h-1.5 bg-amber-500 rounded-full mt-1.5 flex-shrink-0" />
                          {warning}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </motion.div>
            )}

            {remedies && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-amber-100 shadow-sm"
              >
                <h3 className="text-xl font-semibold text-amber-950 mb-6 flex items-center gap-2">
                  <Lightbulb className="w-5 h-5" />
                  Vastu Remedies
                </h3>

                <div className="mb-4 p-4 bg-amber-50 rounded-xl">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-amber-800">Improvement Potential</span>
                    <span className="text-lg font-bold text-amber-600">+{remedies.improvement_potential}%</span>
                  </div>
                  <div className="w-full bg-amber-200 rounded-full h-2">
                    <div 
                      className="bg-amber-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${remedies.improvement_potential}%` }}
                    />
                  </div>
                </div>

                <div className="space-y-3">
                  {remedies.remedies.map((remedy, idx) => (
                    <div key={idx} className="flex items-start gap-3 p-3 bg-purple-50 rounded-lg">
                      <span className="flex items-center justify-center w-6 h-6 bg-purple-200 text-purple-800 rounded-full text-xs font-bold mt-0.5">
                        {idx + 1}
                      </span>
                      <p className="text-sm text-gray-700">{remedy}</p>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {!result && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="bg-white/40 backdrop-blur-sm rounded-2xl p-12 border border-amber-100 text-center"
              >
                <Compass className="w-16 h-16 text-amber-300 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-[#1F1F1F] mb-2">Spatial Harmony Compass</h3>
                <p className="text-sm text-gray-600">Align your space with energy and direction</p>
              </motion.div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
