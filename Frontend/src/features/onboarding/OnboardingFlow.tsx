/**
 * Cinematic Onboarding Flow
 * AntarAalay.ai - Premium AI Interior Studio Experience
 */

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowRightIcon,
  HomeIcon,
  SparklesIcon,
  BuildingOfficeIcon,
  ArrowLeftIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { Button } from '../../components/ui';

interface OnboardingStep {
  id: string;
  title: string;
  subtitle: string;
  component: React.ComponentType<{ onNext: () => void; onPrev?: () => void }>;
}

// Step 1: Welcome
const WelcomeStep: React.FC<{ onNext: () => void; onPrev?: () => void }> = ({ onNext }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 1.1 }}
      transition={{ duration: 0.8, ease: 'easeOut' }}
      className="text-center max-w-4xl mx-auto"
    >
      <div className="mb-12">
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.6 }}
          className="inline-flex items-center space-x-2 bg-gold/10 text-gold px-4 py-2 rounded-full text-sm font-medium mb-8"
        >
          <SparklesIcon className="w-4 h-4" />
          <span>AI-Powered Interior Design</span>
        </motion.div>
        
        <motion.h1
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="font-serif text-6xl md:text-8xl font-bold text-charcoal mb-6 leading-tight"
        >
          Welcome to Your
          <span className="text-gold"> AI Interior</span>
          <br />
          Studio
        </motion.h1>
        
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.6 }}
          className="text-xl md:text-2xl text-text-secondary max-w-2xl mx-auto leading-relaxed"
        >
          Transform your spaces with AI-generated interior designs that blend 
          aesthetics with Vastu principles for perfect harmony.
        </motion.p>
      </div>
      
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.5, duration: 0.6 }}
        className="relative aspect-video max-w-4xl mx-auto mb-12 rounded-3xl overflow-hidden shadow-2xl"
      >
        <img
          src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=1200&h=600&fit=crop"
          alt="Luxury Interior"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-charcoal/50 to-transparent" />
      </motion.div>
      
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.6, duration: 0.6 }}
      >
        <Button
          size="xl"
          onClick={onNext}
          rightIcon={<ArrowRightIcon className="w-6 h-6" />}
          className="px-12 py-6 text-xl"
        >
          Begin Your Journey
        </Button>
      </motion.div>
    </motion.div>
  );
};

// Step 2: User Type Selection
const UserTypeStep: React.FC<{ onNext: () => void; onPrev?: () => void }> = ({ onNext, onPrev }) => {
  const [selectedType, setSelectedType] = useState<string | null>(null);
  
  const userTypes = [
    {
      id: 'homeowner',
      title: 'Homeowner',
      description: 'Design your dream living spaces',
      icon: HomeIcon,
      color: 'from-blue-500 to-blue-600',
    },
    {
      id: 'designer',
      title: 'Designer',
      description: 'Create designs for clients',
      icon: SparklesIcon,
      color: 'from-purple-500 to-purple-600',
    },
    {
      id: 'agency',
      title: 'Agency',
      description: 'Manage multiple projects',
      icon: BuildingOfficeIcon,
      color: 'from-emerald-500 to-emerald-600',
    },
  ];
  
  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="max-w-4xl mx-auto"
    >
      <div className="text-center mb-12">
        <motion.h2
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="font-serif text-5xl font-bold text-charcoal mb-4"
        >
          How will you use our studio?
        </motion.h2>
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="text-xl text-text-secondary"
        >
          Select your role to personalize your experience
        </motion.p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {userTypes.map((type, index) => (
          <motion.div
            key={type.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + index * 0.1 }}
            onClick={() => setSelectedType(type.id)}
            className={`cursor-pointer transition-all duration-300 ${
              selectedType === type.id 
                ? 'ring-2 ring-gold shadow-xl' 
                : 'hover:shadow-lg'
            }`}
          >
            <div className="bg-white rounded-3xl p-8 text-center">
              <div className={`w-16 h-16 bg-gradient-to-br ${type.color} rounded-2xl flex items-center justify-center mx-auto mb-4`}>
                <type.icon className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-serif text-xl font-bold text-charcoal mb-2">{type.title}</h3>
              <p className="text-text-secondary">{type.description}</p>
              {selectedType === type.id && (
                <CheckCircleIcon className="w-6 h-6 text-gold mx-auto mt-4" />
              )}
            </div>
          </motion.div>
        ))}
      </div>
      
      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={onPrev}
          leftIcon={<ArrowLeftIcon className="w-5 h-5" />}
        >
          Back
        </Button>
        <Button
          size="lg"
          onClick={onNext}
          disabled={!selectedType}
          rightIcon={<ArrowRightIcon className="w-5 h-5" />}
        >
          Continue
        </Button>
      </div>
    </motion.div>
  );
};

// Step 3: Design Preferences
const DesignPreferencesStep: React.FC<{ onNext: () => void; onPrev?: () => void }> = ({ onNext, onPrev }) => {
  const [selectedStyles, setSelectedStyles] = useState<string[]>([]);
  
  const designStyles = [
    { id: 'modern', name: 'Modern', description: 'Clean lines and minimalism' },
    { id: 'luxury', name: 'Luxury', description: 'Elegant and sophisticated' },
    { id: 'minimal', name: 'Minimal', description: 'Simple and functional' },
    { id: 'scandinavian', name: 'Scandinavian', description: 'Cozy and natural' },
    { id: 'traditional', name: 'Traditional', description: 'Classic and timeless' },
  ];
  
  const toggleStyle = (styleId: string) => {
    setSelectedStyles(prev => 
      prev.includes(styleId) 
        ? prev.filter(id => id !== styleId)
        : [...prev, styleId]
    );
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="max-w-4xl mx-auto"
    >
      <div className="text-center mb-12">
        <motion.h2
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="font-serif text-5xl font-bold text-charcoal mb-4"
        >
          What's your design style?
        </motion.h2>
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="text-xl text-text-secondary"
        >
          Choose the styles that inspire you (select multiple)
        </motion.p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-12">
        {designStyles.map((style, index) => (
          <motion.div
            key={style.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + index * 0.1 }}
            onClick={() => toggleStyle(style.id)}
            className={`cursor-pointer transition-all duration-300 ${
              selectedStyles.includes(style.id)
                ? 'ring-2 ring-gold bg-gold/10'
                : 'hover:shadow-md bg-white'
            }`}
          >
            <div className="rounded-2xl p-6 text-center">
              <h3 className="font-semibold text-charcoal mb-2">{style.name}</h3>
              <p className="text-sm text-text-secondary">{style.description}</p>
              {selectedStyles.includes(style.id) && (
                <CheckCircleIcon className="w-5 h-5 text-gold mx-auto mt-3" />
              )}
            </div>
          </motion.div>
        ))}
      </div>
      
      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={onPrev}
          leftIcon={<ArrowLeftIcon className="w-5 h-5" />}
        >
          Back
        </Button>
        <Button
          size="lg"
          onClick={onNext}
          disabled={selectedStyles.length === 0}
          rightIcon={<ArrowRightIcon className="w-5 h-5" />}
        >
          Continue
        </Button>
      </div>
    </motion.div>
  );
};

// Step 4: Demo Animation
const DemoStep: React.FC<{ onNext: () => void; onPrev?: () => void }> = ({ onNext, onPrev }) => {
  const [isTransforming, setIsTransforming] = useState(false);
  const [showAfter, setShowAfter] = useState(false);
  
  const handleTransform = () => {
    setIsTransforming(true);
    setTimeout(() => {
      setShowAfter(true);
      setIsTransforming(false);
    }, 2000);
  };
  
  return (
    <motion.div
      initial={{ opacity: 0, x: 100 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -100 }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
      className="max-w-6xl mx-auto"
    >
      <div className="text-center mb-12">
        <motion.h2
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="font-serif text-5xl font-bold text-charcoal mb-4"
        >
          See the Magic
        </motion.h2>
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="text-xl text-text-secondary"
        >
          Watch how AI transforms ordinary spaces into extraordinary designs
        </motion.p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="relative"
        >
          <div className="bg-white rounded-3xl p-6 shadow-large">
            <h3 className="font-serif text-xl font-bold text-charcoal mb-4">Before</h3>
            <div className="aspect-video rounded-2xl overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=600&h=400&fit=crop"
                alt="Before"
                className="w-full h-full object-cover"
              />
            </div>
            <div className="mt-4 space-y-2">
              <div className="flex items-center text-sm text-text-secondary">
                <span className="w-2 h-2 bg-red-500 rounded-full mr-2"></span>
                Poor lighting
              </div>
              <div className="flex items-center text-sm text-text-secondary">
                <span className="w-2 h-2 bg-red-500 rounded-full mr-2"></span>
                Inefficient layout
              </div>
              <div className="flex items-center text-sm text-text-secondary">
                <span className="w-2 h-2 bg-red-500 rounded-full mr-2"></span>
                Basic furniture
              </div>
            </div>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="relative"
        >
          <div className="bg-white rounded-3xl p-6 shadow-large">
            <h3 className="font-serif text-xl font-bold text-charcoal mb-4">After</h3>
            <div className="aspect-video rounded-2xl overflow-hidden relative">
              <AnimatePresence mode="wait">
                {!showAfter ? (
                  <motion.div
                    key="placeholder"
                    initial={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="absolute inset-0 bg-gray-200 flex items-center justify-center"
                  >
                    {isTransforming ? (
                      <div className="text-center">
                        <motion.div
                          animate={{ rotate: 360 }}
                          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                          className="w-12 h-12 border-4 border-gold border-t-transparent rounded-full mx-auto mb-4"
                        />
                        <p className="text-charcoal font-medium">AI is working...</p>
                      </div>
                    ) : (
                      <div className="text-center">
                        <SparklesIcon className="w-12 h-12 text-gold mx-auto mb-4" />
                        <p className="text-charcoal font-medium">Click to transform</p>
                      </div>
                    )}
                  </motion.div>
                ) : (
                  <motion.img
                    key="after"
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.6 }}
                    src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?w=600&h=400&fit=crop"
                    alt="After"
                    className="w-full h-full object-cover"
                  />
                )}
              </AnimatePresence>
            </div>
            <div className="mt-4 space-y-2">
              <div className="flex items-center text-sm text-text-secondary">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Optimized lighting
              </div>
              <div className="flex items-center text-sm text-text-secondary">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Perfect layout
              </div>
              <div className="flex items-center text-sm text-text-secondary">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Premium furniture
              </div>
            </div>
          </div>
        </motion.div>
      </div>
      
      {!showAfter && (
        <div className="text-center mb-8">
          <Button
            size="lg"
            onClick={handleTransform}
            disabled={isTransforming}
            loading={isTransforming}
            className="px-8"
          >
            Transform with AI
          </Button>
        </div>
      )}
      
      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={onPrev}
          leftIcon={<ArrowLeftIcon className="w-5 h-5" />}
        >
          Back
        </Button>
        {showAfter && (
          <Button
            size="lg"
            onClick={onNext}
            rightIcon={<ArrowRightIcon className="w-5 h-5" />}
          >
            Start Designing
          </Button>
        )}
      </div>
    </motion.div>
  );
};

export const OnboardingFlow: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const navigate = useNavigate();
  
  const steps: OnboardingStep[] = [
    {
      id: 'welcome',
      title: 'Welcome',
      subtitle: 'Introduction to AI Interior Studio',
      component: WelcomeStep,
    },
    {
      id: 'user-type',
      title: 'User Type',
      subtitle: 'Select your role',
      component: UserTypeStep,
    },
    {
      id: 'preferences',
      title: 'Design Preferences',
      subtitle: 'Choose your style',
      component: DesignPreferencesStep,
    },
    {
      id: 'demo',
      title: 'Demo',
      subtitle: 'See the transformation',
      component: DemoStep,
    },
  ];
  
  const CurrentStepComponent = steps[currentStep].component;
  
  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      // Onboarding complete - navigate to dashboard
      navigate('/dashboard');
    }
  };
  
  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };
  
  return (
    <div className="min-h-screen bg-stone flex items-center justify-center px-6 py-12">
      {/* Progress Indicator */}
      <div className="absolute top-8 left-1/2 transform -translate-x-1/2">
        <div className="flex items-center space-x-2">
          {steps.map((step, index) => (
            <div
              key={step.id}
              className={`w-2 h-2 rounded-full transition-all duration-300 ${
                index <= currentStep ? 'bg-gold' : 'bg-neutral-grey'
              }`}
            />
          ))}
        </div>
        <p className="text-center text-sm text-text-secondary mt-2">
          Step {currentStep + 1} of {steps.length}
        </p>
      </div>
      
      {/* Step Content */}
      <AnimatePresence mode="wait">
        <CurrentStepComponent
          key={currentStep}
          onNext={handleNext}
          onPrev={handlePrev}
        />
      </AnimatePresence>
    </div>
  );
};

export default OnboardingFlow;
