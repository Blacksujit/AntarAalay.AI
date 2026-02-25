/**
 * Magical AI Generation Experience
 * AntarAalay.ai - Premium Design Generation with Cinematic UX
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
  PlayIcon,
  HeartIcon,
  ShareIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';
import { useMutation } from '@tanstack/react-query';
import { designService } from '../../services/apiService';
import { Button, Card, ProgressRing } from '../../components/ui';

interface GenerationStep {
  id: string;
  title: string;
  description: string;
  duration: number;
  icon: React.ElementType;
  particleEffect?: boolean;
}

const generationSteps: GenerationStep[] = [
  {
    id: 'analyzing',
    title: 'Analyzing Room Geometry',
    description: 'Understanding your space dimensions and architectural elements',
    duration: 15,
    icon: Cog6ToothIcon,
    particleEffect: true,
  },
  {
    id: 'vastu',
    title: 'Applying Vastu Principles',
    description: 'Ensuring harmony and positive energy flow throughout the space',
    duration: 10,
    icon: SparklesIcon,
    particleEffect: true,
  },
  {
    id: 'designing',
    title: 'Creating Interior Designs',
    description: 'Generating beautiful design variations tailored to your preferences',
    duration: 20,
    icon: EyeIcon,
    particleEffect: true,
  },
  {
    id: 'finalizing',
    title: 'Finalizing Details',
    description: 'Adding finishing touches, lighting, and cost estimates',
    duration: 10,
    icon: CheckCircleIcon,
    particleEffect: false,
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
  materials: string[];
  timeline: string;
}

export const PremiumGeneration: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { roomId } = location.state || {};
  
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(55);
  const [showResults, setShowResults] = useState(false);
  const [selectedDesign, setSelectedDesign] = useState<string | null>(null);
  const [expandedDesign, setExpandedDesign] = useState<string | null>(null);

  // Mock design variations
  const [designs] = useState<DesignVariation[]>([
    {
      id: '1',
      title: 'Modern Elegance',
      style: 'Contemporary Luxury',
      imageUrl: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop',
      cost: '$45,000',
      vastuScore: 92,
      features: ['Open concept living', 'Smart home integration', 'Natural lighting optimization'],
      materials: ['Italian marble', 'Oak wood flooring', 'Custom cabinetry'],
      timeline: '8-10 weeks',
    },
    {
      id: '2',
      title: 'Scandinavian Serenity',
      style: 'Minimalist Comfort',
      imageUrl: 'https://images.unsplash.com/photo-1560185007-c5ca9d2c014d?w=800&h=600&fit=crop',
      cost: '$38,000',
      vastuScore: 88,
      features: ['Hygge atmosphere', 'Sustainable materials', 'Functional minimalism'],
      materials: ['Bamboo flooring', 'Recycled wood', 'Organic textiles'],
      timeline: '6-8 weeks',
    },
    {
      id: '3',
      title: 'Luxury Living',
      style: 'High-End Modern',
      imageUrl: 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=600&fit=crop',
      cost: '$62,000',
      vastuScore: 95,
      features: ['Premium finishes', 'Home automation', 'Custom furniture pieces'],
      materials: ['Travertine stone', 'Walnut wood', 'Brass accents'],
      timeline: '10-12 weeks',
    },
  ]);

  // Generation mutation
  const generateMutation = useMutation({
    mutationFn: (request: any) => designService.generateDesign(request),
    onSuccess: () => {
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
          if (currentStep < generationSteps.length - 1) {
            setCurrentStep((step) => step + 1);
            return 0;
          } else {
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
    
    generateMutation.mutate({ room_id: roomId });
  }, [roomId, navigate, generateMutation]);

  const currentStepData = generationSteps[currentStep];
  const overallProgress = ((currentStep * 100) + progress) / generationSteps.length;

  if (!roomId) {
    return null;
  }

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
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate('/upload')}
                leftIcon={<ArrowLeftIcon className="w-4 h-4" />}
              >
                Back
              </Button>
              <div>
                <h1 className="font-serif text-2xl font-bold text-charcoal">AI Design Generation</h1>
                <p className="text-text-secondary">Creating your perfect interior design</p>
              </div>
            </div>
            
            {!showResults && (
              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <p className="text-sm text-text-secondary">Time Remaining</p>
                  <p className="text-lg font-semibold text-charcoal">{timeRemaining}s</p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  leftIcon={isPaused ? <PlayIcon className="w-4 h-4" /> : <PauseIcon className="w-4 h-4" />}
                  onClick={() => setIsPaused(!isPaused)}
                >
                  {isPaused ? 'Resume' : 'Pause'}
                </Button>
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
              <div className="mb-16">
                <div className="relative inline-block">
                  <ProgressRing progress={Math.round(overallProgress)} size={200} />
                  
                  {/* Particle Effects */}
                  {currentStepData.particleEffect && (
                    <div className="absolute inset-0 pointer-events-none">
                      {[...Array(6)].map((_, i) => (
                        <motion.div
                          key={i}
                          className="absolute w-2 h-2 bg-gold rounded-full opacity-60"
                          animate={{
                            x: [0, Math.cos((i * 60) * Math.PI / 180) * 150],
                            y: [0, Math.sin((i * 60) * Math.PI / 180) * 150],
                            opacity: [0, 1, 0],
                          }}
                          transition={{
                            duration: 2,
                            repeat: Infinity,
                            delay: i * 0.3,
                            ease: 'easeOut',
                          }}
                          style={{
                            left: '50%',
                            top: '50%',
                            marginLeft: '-4px',
                            marginTop: '-4px',
                          }}
                        />
                      ))}
                    </div>
                  )}
                </div>
                
                <motion.div
                  key={currentStep}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                  className="mt-8"
                >
                  <div className="w-16 h-16 bg-gradient-to-br from-gold to-amber-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-glow">
                    <currentStepData.icon className="w-8 h-8 text-white" />
                  </div>
                  <h2 className="font-serif text-4xl font-bold text-charcoal mb-4">
                    {currentStepData.title}
                  </h2>
                  <p className="text-xl text-text-secondary max-w-2xl mx-auto leading-relaxed">
                    {currentStepData.description}
                  </p>
                </motion.div>
              </div>

              {/* Step Progress */}
              <div className="max-w-3xl mx-auto mb-16">
                <div className="flex items-center justify-between mb-6">
                  {generationSteps.map((step, index) => (
                    <div key={step.id} className="flex items-center flex-1">
                      <motion.div
                        className={`w-12 h-12 rounded-full flex items-center justify-center transition-all duration-500 ${
                          index < currentStep
                            ? 'bg-success text-white shadow-lg'
                            : index === currentStep
                            ? 'bg-gold text-white shadow-glow'
                            : 'bg-neutral-grey text-text-tertiary'
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
                          className={`flex-1 h-1 mx-2 transition-all duration-500 ${
                            index < currentStep ? 'bg-success' : 'bg-neutral-grey'
                          }`}
                        />
                      )}
                    </div>
                  ))}
                </div>
                
                <div className="flex justify-between text-sm text-text-secondary">
                  {generationSteps.map((step) => (
                    <span key={step.id} className="hidden sm:block">
                      {step.title.split(' ')[0]}
                    </span>
                  ))}
                </div>
              </div>

              {/* Ambient Background Animation */}
              <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
                {[...Array(8)].map((_, i) => (
                  <motion.div
                    key={i}
                    className="absolute w-3 h-3 bg-gold/20 rounded-full"
                    animate={{
                      x: [0, 200, 0],
                      y: [0, -150, 0],
                      scale: [1, 1.5, 1],
                    }}
                    transition={{
                      duration: 4 + i,
                      repeat: Infinity,
                      ease: 'easeInOut',
                      delay: i * 0.5,
                    }}
                    style={{
                      left: `${10 + i * 12}%`,
                      top: `${20 + i * 8}%`,
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
              <div className="text-center mb-16">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', damping: 10, stiffness: 100 }}
                  className="w-20 h-20 bg-gradient-to-br from-success to-green-600 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-glow"
                >
                  <CheckCircleIcon className="w-10 h-10 text-white" />
                </motion.div>
                <h2 className="font-serif text-5xl font-bold text-charcoal mb-6">
                  Your Designs Are Ready!
                </h2>
                <p className="text-xl text-text-secondary max-w-3xl mx-auto leading-relaxed">
                  We've created 3 stunning design variations for your space. 
                  Each one follows Vastu principles and includes detailed cost estimates and timelines.
                </p>
              </div>

              {/* Design Variations */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-16">
                {designs.map((design, index) => (
                  <motion.div
                    key={design.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.2 }}
                  >
                    <Card 
                      variant={selectedDesign === design.id ? "elevated" : "default"}
                      className={`cursor-pointer transition-all duration-300 overflow-hidden ${
                        selectedDesign === design.id ? 'ring-2 ring-gold shadow-xl' : 'hover:shadow-lg'
                      }`}
                      onClick={() => setSelectedDesign(design.id)}
                    >
                      {/* Image */}
                      <div className="aspect-[4/3] overflow-hidden relative">
                        <motion.img
                          src={design.imageUrl}
                          alt={design.title}
                          className="w-full h-full object-cover"
                          whileHover={{ scale: 1.05 }}
                          transition={{ duration: 0.6 }}
                        />
                        
                        {/* Quick Actions */}
                        <div className="absolute top-4 right-4 flex space-x-2">
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className="w-10 h-10 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-lg"
                          >
                            <HeartIcon className="w-5 h-5 text-charcoal" />
                          </motion.button>
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.9 }}
                            className="w-10 h-10 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-lg"
                          >
                            <ShareIcon className="w-5 h-5 text-charcoal" />
                          </motion.button>
                        </div>
                      </div>
                      
                      {/* Content */}
                      <div className="p-6">
                        <h3 className="font-serif text-xl font-bold text-charcoal mb-2">
                          {design.title}
                        </h3>
                        <div className="flex items-center justify-between mb-4">
                          <span className="text-sm font-medium text-gold">{design.style}</span>
                          <span className="text-lg font-bold text-charcoal">{design.cost}</span>
                        </div>
                        
                        {/* Vastu Score */}
                        <div className="flex items-center justify-between mb-4">
                          <span className="text-sm text-text-secondary">Vastu Score</span>
                          <div className="flex items-center space-x-2">
                            <div className="w-20 h-2 bg-neutral-grey rounded-full overflow-hidden">
                              <motion.div
                                className="h-full bg-gradient-to-r from-gold to-amber-600"
                                initial={{ width: 0 }}
                                animate={{ width: `${design.vastuScore}%` }}
                                transition={{ duration: 1, delay: 0.5 + index * 0.2 }}
                              />
                            </div>
                            <span className="text-sm font-semibold text-charcoal">
                              {design.vastuScore}%
                            </span>
                          </div>
                        </div>
                        
                        {/* Features */}
                        <div className="space-y-2 mb-4">
                          {design.features.slice(0, expandedDesign === design.id ? undefined : 2).map((feature, i) => (
                            <div key={i} className="flex items-center space-x-2">
                              <CheckCircleIcon className="w-4 h-4 text-success flex-shrink-0" />
                              <span className="text-sm text-text-secondary">{feature}</span>
                            </div>
                          ))}
                        </div>
                        
                        {/* Expand Button */}
                        {design.features.length > 2 && (
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setExpandedDesign(expandedDesign === design.id ? null : design.id);
                            }}
                            className="text-sm text-gold font-medium hover:text-amber-600 transition-colors"
                          >
                            {expandedDesign === design.id ? 'Show less' : 'Show more'}
                          </button>
                        )}
                        
                        {/* Action Buttons */}
                        <div className="flex space-x-3 mt-6">
                          <Button
                            fullWidth
                            variant={selectedDesign === design.id ? 'primary' : 'outline'}
                            size="sm"
                            onClick={() => navigate(`/design/${design.id}`)}
                          >
                            {selectedDesign === design.id ? 'Selected' : 'View Details'}
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            leftIcon={<ArrowDownTrayIcon className="w-4 h-4" />}
                          >
                            Save
                          </Button>
                        </div>
                      </div>
                    </Card>
                  </motion.div>
                ))}
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button
                  size="xl"
                  onClick={() => {
                    setShowResults(false);
                    setCurrentStep(0);
                    setProgress(0);
                    setTimeRemaining(55);
                    generateMutation.mutate({ room_id: roomId });
                  }}
                  leftIcon={<ArrowPathIcon className="w-6 h-6" />}
                >
                  Generate More Designs
                </Button>
                
                <Button
                  variant="outline"
                  size="xl"
                  onClick={() => navigate('/dashboard')}
                >
                  Back to Dashboard
                </Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default PremiumGeneration;
