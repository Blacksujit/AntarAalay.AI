/**
 * Premium Design Generation Page
 * AI-powered interior design with real-time preview
 */

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  SparklesIcon, 
  ArrowPathIcon, 
  PhotoIcon,
  Cog6ToothIcon,
  EyeIcon
} from '@heroicons/react/24/outline';
import { cn } from '../utils/logger';

interface DesignGenerationProps {
  roomId: string;
  initialImages?: {
    north: string;
    south: string;
    east: string;
    west: string;
  };
}

const DesignGeneration = ({ roomId, initialImages }: DesignGenerationProps) => {
  const [style, setStyle] = useState('modern');
  const [wallColor, setWallColor] = useState('white');
  const [flooring, setFlooring] = useState('hardwood');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImages, setGeneratedImages] = useState<string[]>([]);
  const [currentStep, setCurrentStep] = useState(1);

  const styles = [
    { value: 'modern', label: 'Modern', description: 'Clean lines, neutral colors' },
    { value: 'minimalist', label: 'Minimalist', description: 'Simple, uncluttered spaces' },
    { value: 'luxury', label: 'Luxury', description: 'Premium materials, elegant details' },
    { value: 'traditional', label: 'Traditional', description: 'Classic, timeless designs' },
    { value: 'scandinavian', label: 'Scandinavian', description: 'Light woods, cozy atmosphere' },
    { value: 'industrial', label: 'Industrial', description: 'Raw materials, urban style' },
  ];

  const wallColors = [
    { value: 'white', label: 'White', color: '#FFFFFF' },
    { value: 'beige', label: 'Beige', color: '#F5F1E8' },
    { value: 'gray', label: 'Gray', color: '#9CA3AF' },
    { value: 'blue', label: 'Blue', color: '#3B82F6' },
    { value: 'green', label: 'Green', color: '#10B981' },
  ];

  const flooringOptions = [
    { value: 'hardwood', label: 'Hardwood' },
    { value: 'laminate', label: 'Laminate' },
    { value: 'tile', label: 'Ceramic Tile' },
    { value: 'carpet', label: 'Carpet' },
    { value: 'vinyl', label: 'Vinyl' },
  ];

  const handleGenerate = async () => {
    setIsGenerating(true);
    setCurrentStep(2);
    
    try {
      // Simulate API call to backend
      const response = await fetch('/api/design/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
        },
        body: JSON.stringify({
          room_id: roomId,
          style,
          wall_color: wallColor,
          flooring_material: flooring,
        }),
      });

      const result = await response.json();
      
      if (result.status === 'success') {
        setGeneratedImages(result.images || []);
        setCurrentStep(3);
      }
    } catch (error) {
      console.error('Generation failed:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-beige via-white to-brand-white">
      <div className="max-w-7xl mx-auto p-8">
        {/* Progress Steps */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-8"
        >
          <div className="flex items-center justify-center space-x-8">
            {[1, 2, 3].map((step) => (
              <div
                key={step}
                className={cn(
                  "flex items-center justify-center w-10 h-10 rounded-full font-medium text-sm",
                  step === currentStep
                    ? "bg-brand-gold text-white shadow-glow"
                    : step < currentStep
                      ? "bg-brand-charcoal text-white"
                      : "bg-neutral-200 text-neutral-500"
                )}
              >
                {step === 1 && "Customize"}
                {step === 2 && "Generating"}
                {step === 3 && "Complete"}
              </div>
            ))}
          </div>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Panel - Customization */}
          <motion.div
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="bg-white rounded-3xl shadow-luxury p-8"
          >
            <h2 className="text-2xl font-display font-bold text-brand-charcoal mb-6">
              Design Customization
            </h2>

            {/* Style Selection */}
            <div className="mb-8">
              <label className="block text-sm font-semibold text-brand-charcoal mb-3">
                Furniture Style
              </label>
              <div className="grid grid-cols-2 gap-3">
                {styles.map((styleOption) => (
                  <motion.button
                    key={styleOption.value}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => setStyle(styleOption.value)}
                    className={cn(
                      "p-4 rounded-xl border-2 transition-all duration-200",
                      style === styleOption.value
                        ? "border-brand-gold bg-brand-gold/10 shadow-soft"
                        : "border-neutral-200 hover:border-neutral-300 hover:bg-neutral-50"
                    )}
                  >
                    <div className="text-left">
                      <div className="font-semibold text-brand-charcoal mb-1">
                        {styleOption.label}
                      </div>
                      <div className="text-xs text-neutral-500">
                        {styleOption.description}
                      </div>
                    </div>
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Wall Color */}
            <div className="mb-8">
              <label className="block text-sm font-semibold text-brand-charcoal mb-3">
                Wall Color
              </label>
              <div className="grid grid-cols-3 gap-3">
                {wallColors.map((color) => (
                  <motion.button
                    key={color.value}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setWallColor(color.value)}
                    className={cn(
                      "p-4 rounded-xl border-2 transition-all duration-200",
                      wallColor === color.value
                        ? "border-brand-gold bg-brand-gold/10 shadow-soft"
                        : "border-neutral-200 hover:border-neutral-300 hover:bg-neutral-50"
                    )}
                  >
                    <div className="flex items-center space-x-3">
                      <div
                        className="w-6 h-6 rounded-full border-2 border-neutral-300"
                        style={{ backgroundColor: color.color }}
                      />
                      <span className="text-sm font-medium text-brand-charcoal">
                        {color.label}
                      </span>
                    </div>
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Flooring Material */}
            <div className="mb-8">
              <label className="block text-sm font-semibold text-brand-charcoal mb-3">
                Flooring Material
              </label>
              <select
                value={flooring}
                onChange={(e) => setFlooring(e.target.value)}
                className={cn(
                  "w-full px-4 py-3 rounded-xl border-2 font-medium",
                  "border-neutral-200 bg-white focus:border-brand-gold focus:ring-2 focus:ring-brand-gold/20",
                  "transition-all duration-200"
                )}
              >
                {flooringOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Generate Button */}
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(198, 167, 94, 0.4)" }}
              whileTap={{ scale: 0.95 }}
              onClick={handleGenerate}
              disabled={isGenerating}
              className={cn(
                "w-full py-4 text-lg font-semibold text-brand-white",
                "bg-gradient-to-r from-brand-gold to-brand-gold/600",
                "rounded-xl shadow-luxury hover:shadow-glow",
                "transition-all duration-300 ease-out",
                "disabled:opacity-50 disabled:cursor-not-allowed"
              )}
            >
              <span className="relative z-10 flex items-center justify-center">
                {isGenerating ? (
                  <>
                    <motion.div
                      animate={{ rotate: 360 }}
                      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                      className="w-5 h-5 border-2 border-white/30 border-t-transparent rounded-full mr-3"
                    />
                    Designing your space...
                  </>
                ) : (
                  <>
                    <SparklesIcon className="w-5 h-5 mr-3" />
                    Generate Designs
                  </>
                )}
              </span>
              
              {/* Button shimmer effect */}
              <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-transparent via-white/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-500" />
            </motion.button>
          </motion.div>

          {/* Right Panel - Preview */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="bg-white rounded-3xl shadow-luxury p-8"
          >
            <h2 className="text-2xl font-display font-bold text-brand-charcoal mb-6">
              Design Preview
            </h2>

            {isGenerating ? (
              <div className="flex flex-col items-center justify-center h-96">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  className="w-16 h-16 border-4 border-brand-gold/30 border-t-transparent rounded-full"
                />
                <p className="mt-6 text-brand-charcoal font-medium">
                  AI is creating your custom designs...
                </p>
                <p className="text-sm text-neutral-500">
                  This usually takes 30-60 seconds
                </p>
              </div>
            ) : generatedImages.length > 0 ? (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-brand-charcoal mb-4">
                  Generated Designs
                </h3>
                <div className="grid grid-cols-1 gap-4">
                  {generatedImages.map((image, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, scale: 0.8 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: index * 0.2, duration: 0.6 }}
                      whileHover={{ scale: 1.05, boxShadow: "0 10px 30px rgba(0, 0, 0, 0.2)" }}
                      className="relative group cursor-pointer rounded-xl overflow-hidden shadow-soft"
                    >
                      <img
                        src={image}
                        alt={`Generated design ${index + 1}`}
                        className="w-full h-64 object-cover"
                      />
                      
                      {/* Overlay on hover */}
                      <div className="absolute inset-0 bg-gradient-to-t from-brand-charcoal/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                        <EyeIcon className="w-8 h-8 text-white" />
                      </div>
                      
                      {/* Image info */}
                      <div className="absolute bottom-2 left-2 bg-brand-charcoal/90 text-white px-3 py-2 rounded-lg text-xs">
                        Design {index + 1}
                      </div>
                    </motion.div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-96 text-neutral-400">
                <PhotoIcon className="w-16 h-16 mb-4 text-neutral-300" />
                <p className="text-lg font-medium mb-2">
                  Your designs will appear here
                </p>
                <p className="text-sm">
                  Customize your preferences and click Generate to begin
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default DesignGeneration;

export async function getServerSideProps() {
  return { props: {} };
}
