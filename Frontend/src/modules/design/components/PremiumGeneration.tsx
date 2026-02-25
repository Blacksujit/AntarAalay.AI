/**
 * Premium Design Generation Page
 * AntarAalay.ai - Luxury AI Design Generation Experience
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  ArrowLeftIcon,
  SparklesIcon,
  CheckCircleIcon,
  Cog6ToothIcon,
  EyeIcon,
  ArrowPathIcon,
  PauseIcon,
  PlayIcon
} from '@heroicons/react/24/outline';
import { useMutation } from '@tanstack/react-query';
import { designService } from '../../../services/apiService';
import { PremiumButton, GlassCard, ProgressRing } from '../../../components/ui/PremiumComponents';

interface GenerationStep {
  id: string;
  title: string;
  description: string;
  duration: number; // in seconds
  icon: React.ElementType;
}

const generationSteps: GenerationStep[] = [
  {
    id: 'analyzing',
    title: 'Analyzing Room Geometry',
    description: 'Understanding your space dimensions and layout',
    duration: 15,
    icon: Cog6ToothIcon,
  },
  {
    id: 'vastu',
    title: 'Applying Vastu Principles',
    description: 'Ensuring harmony and positive energy flow',
    duration: 10,
    icon: SparklesIcon,
  },
  {
    id: 'designing',
    title: 'Creating Interior Designs',
    description: 'Generating beautiful design variations',
    duration: 20,
    icon: EyeIcon,
  },
  {
    id: 'finalizing',
    title: 'Finalizing Details',
    description: 'Adding finishing touches and cost estimates',
    duration: 10,
    icon: CheckCircleIcon,
  },
];

interface DesignVariation {
  id: string;
  title: string;
  style: string;
  imageUrl: string;
  cost: string;
  vastuScore: number;
  features: string[];
}

export const PremiumGeneration: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { roomId } = location.state || {};
  
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(60);
  const [showResults, setShowResults] = useState(false);
  const [selectedDesign, setSelectedDesign] = useState<string | null>(null);

  // Mock design variations
  const [designs] = useState<DesignVariation[]>([
    {
      id: '1',
      title: 'Modern Elegance',
      style: 'Contemporary',
      imageUrl: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop',
      cost: '$45,000',
      vastuScore: 92,
      features: ['Open layout', 'Natural lighting', 'Minimalist furniture'],
    },
    {
      id: '2',
      title: 'Classic Comfort',
      style: 'Traditional',
      imageUrl: 'https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?w=600&h=400&fit=crop',
      cost: '$38,000',
      vastuScore: 88,
      features: ['Warm colors', 'Wood finishes', 'Cozy ambiance'],
    },
    {
      id: '3',
      title: 'Luxury Living',
      style: 'High-End',
      imageUrl: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&h=400&fit=crop',
      cost: '$62,000',
      vastuScore: 95,
      features: ['Premium materials', 'Smart home', 'Custom furniture'],
    },
  ]);

  // Generation mutation
  const generateMutation = useMutation({
    mutationFn: (request: any) => designService.generateDesign(request),
    onSuccess: () => {
      // In real app, use the returned data
      setTimeout(() => {
        setShowResults(true);
      }, 2000);
    },
    onError: (error: Error) => {
      console.error('Generation failed:', error);
    },
  });

  // Progress simulation
  useEffect(() => {
    if (isPaused || showResults) return;

    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          // Move to next step or finish
          if (currentStep < generationSteps.length - 1) {
            setCurrentStep((step) => step + 1);
            return 0;
          } else {
            // Generation complete
            generateMutation.mutate({ room_id: roomId });
            return 100;
          }
        }
        return prev + (100 / generationSteps[currentStep].duration);
      });
      
      setTimeRemaining((prev) => Math.max(0, prev - 1));
    }, 1000);

    return () => clearInterval(interval);
  }, [currentStep, isPaused, showResults, generateMutation, roomId]);

  // Start generation on mount
  useEffect(() => {
    if (!roomId) {
      navigate('/upload');
      return;
    }
    
    // Start generation
    generateMutation.mutate({ room_id: roomId });
  }, [roomId, navigate, generateMutation]);

  const currentStepData = generationSteps[currentStep];
  const overallProgress = ((currentStep * 100) + progress) / generationSteps.length;

  if (!roomId) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/80 backdrop-blur-lg border-b border-amber-100 sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <PremiumButton
                variant="ghost"
                size="sm"
                leftIcon={<ArrowLeftIcon className="w-4 h-4" />}
                onClick={() => navigate('/upload')}
              >
                Back
              </PremiumButton>
              <div>
                <h1 className="text-2xl font-serif font-bold text-gray-900">AI Design Generation</h1>
                <p className="text-gray-600">Creating your perfect interior design</p>
              </div>
            </div>
            
            {!showResults && (
              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <p className="text-sm text-gray-500">Time Remaining</p>
                  <p className="text-lg font-semibold text-gray-900">{timeRemaining}s</p>
                </div>
                <PremiumButton
                  variant="outline"
                  size="sm"
                  leftIcon={isPaused ? <PlayIcon className="w-4 h-4" /> : <PauseIcon className="w-4 h-4" />}
                  onClick={() => setIsPaused(!isPaused)}
                >
                  {isPaused ? 'Resume' : 'Pause'}
                </PremiumButton>
              </div>
            )}
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <AnimatePresence mode="wait">
          {!showResults ? (
            // Generation Progress
            <motion.div
              key="generation"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 1.05 }}
              transition={{ duration: 0.5 }}
              className="text-center"
            >
              {/* Main Progress Circle */}
              <div className="mb-12">
                <ProgressRing progress={Math.round(overallProgress)} size={200} />
                
                <motion.div
                  key={currentStep}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="mt-8"
                >
                  <div className="w-16 h-16 bg-gradient-to-br from-amber-400 to-amber-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-glow">
                    <currentStepData.icon className="w-8 h-8 text-white" />
                  </div>
                  <h2 className="text-3xl font-serif font-bold text-gray-900 mb-2">
                    {currentStepData.title}
                  </h2>
                  <p className="text-lg text-gray-600 max-w-md mx-auto">
                    {currentStepData.description}
                  </p>
                </motion.div>
              </div>

              {/* Step Progress */}
              <div className="max-w-2xl mx-auto mb-12">
                <div className="flex items-center justify-between mb-4">
                  {generationSteps.map((step, index) => (
                    <div key={step.id} className="flex items-center">
                      <motion.div
                        className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-300 ${
                          index < currentStep
                            ? 'bg-green-500 text-white'
                            : index === currentStep
                            ? 'bg-amber-500 text-white'
                            : 'bg-gray-200 text-gray-400'
                        }`}
                        whileHover={{ scale: 1.1 }}
                      >
                        {index < currentStep ? (
                          <CheckCircleIcon className="w-6 h-6" />
                        ) : (
                          <step.icon className="w-6 h-6" />
                        )}
                      </motion.div>
                      {index < generationSteps.length - 1 && (
                        <div
                          className={`w-24 h-1 mx-2 transition-all duration-300 ${
                            index < currentStep ? 'bg-green-500' : 'bg-gray-200'
                          }`}
                        />
                      )}
                    </div>
                  ))}
                </div>
                
                <div className="flex justify-between text-sm text-gray-500">
                  {generationSteps.map((step) => (
                    <span key={step.id} className="hidden sm:block">
                      {step.title.split(' ')[0]}
                    </span>
                  ))}
                </div>
              </div>

              {/* Animated Background Elements */}
              <div className="fixed inset-0 pointer-events-none overflow-hidden">
                {[...Array(6)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-2 h-2 bg-amber-400 rounded-full opacity-20"
                    animate={{
                      x: [0, 100, 0],
                      y: [0, -100, 0],
                    }}
                    transition={{
                      duration: 3 + i,
                      repeat: Infinity,
                      ease: 'easeInOut',
                      delay: i * 0.5,
                    }}
                    style={{
                      left: `${20 + i * 15}%`,
                      top: `${30 + i * 10}%`,
                    }}
                  />
                ))}
              </div>
            </motion.div>
          ) : (
            // Results
            <motion.div
              key="results"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <div className="text-center mb-12">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', damping: 10 }}
                  className="w-20 h-20 bg-gradient-to-br from-green-400 to-green-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-glow"
                >
                  <CheckCircleIcon className="w-10 h-10 text-white" />
                </motion.div>
                <h2 className="text-4xl font-serif font-bold text-gray-900 mb-4">
                  Your Designs Are Ready!
                </h2>
                <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                  We've created 3 stunning design variations for your space. 
                  Each one follows Vastu principles and includes detailed cost estimates.
                </p>
              </div>

              {/* Design Variations */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
                {designs.map((design, index) => (
                  <motion.div
                    key={design.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.2 }}
                  >
                    <GlassCard className={`cursor-pointer transition-all duration-300 ${
                      selectedDesign === design.id ? 'ring-2 ring-amber-400' : ''
                    }`}
                    onClick={() => setSelectedDesign(design.id)}
                    >
                      <div className="aspect-[4/3] overflow-hidden rounded-xl mb-4">
                        <motion.img
                          src={design.imageUrl}
                          alt={design.title}
                          className="w-full h-full object-cover"
                          whileHover={{ scale: 1.05 }}
                          transition={{ duration: 0.6 }}
                        />
                      </div>
                      
                      <div className="mb-4">
                        <h3 className="text-xl font-serif font-bold text-gray-900 mb-2">
                          {design.title}
                        </h3>
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-sm font-medium text-amber-600">{design.style}</span>
                          <span className="text-lg font-bold text-gray-900">{design.cost}</span>
                        </div>
                        
                        <div className="flex items-center justify-between mb-3">
                          <span className="text-sm text-gray-600">Vastu Score</span>
                          <div className="flex items-center space-x-2">
                            <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
                              <motion.div
                                className="h-full bg-gradient-to-r from-amber-400 to-amber-600"
                                initial={{ width: 0 }}
                                animate={{ width: `${design.vastuScore}%` }}
                                transition={{ duration: 1, delay: 0.5 + index * 0.2 }}
                              />
                            </div>
                            <span className="text-sm font-semibold text-gray-900">
                              {design.vastuScore}%
                            </span>
                          </div>
                        </div>
                        
                        <div className="space-y-2">
                          {design.features.map((feature, i) => (
                            <div key={i} className="flex items-center space-x-2">
                              <CheckCircleIcon className="w-4 h-4 text-green-500" />
                              <span className="text-sm text-gray-600">{feature}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                      
                      <PremiumButton
                        fullWidth
                        variant={selectedDesign === design.id ? 'primary' : 'outline'}
                        size="sm"
                        onClick={() => navigate(`/design/${design.id}`)}
                      >
                        {selectedDesign === design.id ? 'Selected' : 'View Details'}
                      </PremiumButton>
                    </GlassCard>
                  </motion.div>
                ))}
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <PremiumButton
                  size="lg"
                  leftIcon={<ArrowPathIcon className="w-5 h-5" />}
                  onClick={() => {
                    setShowResults(false);
                    setCurrentStep(0);
                    setProgress(0);
                    setTimeRemaining(60);
                    generateMutation.mutate({ room_id: roomId });
                  }}
                >
                  Generate More
                </PremiumButton>
                
                <PremiumButton
                  variant="outline"
                  size="lg"
                  onClick={() => navigate('/dashboard')}
                >
                  Back to Dashboard
                </PremiumButton>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default PremiumGeneration;
