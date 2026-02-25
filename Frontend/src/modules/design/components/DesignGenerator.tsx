/**
 * Enterprise Design Generation Module
 * Split-screen interface with real-time preview
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowPathIcon,
  SparklesIcon,
  PhotoIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { cn } from '../../../utils/logger';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { useGlobalStore, selectCanGenerate, selectIsGenerating } from '../../../store/globalStore';
import { designService } from '../../../services/apiService';

const STYLE_OPTIONS = [
  { id: 'modern', label: 'Modern Minimalist', icon: '✨' },
  { id: 'luxury', label: 'Luxury Elegant', icon: '💎' },
  { id: 'traditional', label: 'Classic Traditional', icon: '🏛️' },
  { id: 'scandinavian', label: 'Scandinavian', icon: '🌿' },
  { id: 'industrial', label: 'Industrial Chic', icon: '⚙️' },
  { id: 'bohemian', label: 'Bohemian', icon: '🎨' },
];

const WALL_COLOR_OPTIONS = [
  { id: 'white', label: 'Pure White', color: '#FFFFFF' },
  { id: 'cream', label: 'Warm Cream', color: '#F5F5DC' },
  { id: 'beige', label: 'Soft Beige', color: '#F5F5DC' },
  { id: 'gray', label: 'Light Gray', color: '#D3D3D3' },
  { id: 'sage', label: 'Sage Green', color: '#9DC183' },
  { id: 'navy', label: 'Navy Blue', color: '#000080' },
  { id: 'terracotta', label: 'Terracotta', color: '#E2725B' },
];

const FLOORING_OPTIONS = [
  { id: 'hardwood', label: 'Hardwood', icon: '🪵' },
  { id: 'marble', label: 'Marble', icon: '🏛️' },
  { id: 'tiles', label: 'Ceramic Tiles', icon: '🔲' },
  { id: 'carpet', label: 'Plush Carpet', icon: '🛋️' },
  { id: 'vinyl', label: 'Luxury Vinyl', icon: '💎' },
  { id: 'concrete', label: 'Polished Concrete', icon: '🏗️' },
];

export const DesignGenerator = () => {
  const navigate = useNavigate();
  const roomId = useGlobalStore((state) => state.roomId);
  const selectedCustomization = useGlobalStore((state) => state.selectedCustomization);
  const setSelectedCustomization = useGlobalStore((state) => state.setSelectedCustomization);
  const startGeneration = useGlobalStore((state) => state.startGeneration);
  const completeGeneration = useGlobalStore((state) => state.completeGeneration);
  const failGeneration = useGlobalStore((state) => state.failGeneration);
  const incrementUsage = useGlobalStore((state) => state.incrementUsage);
  
  const canGenerate = useGlobalStore(selectCanGenerate);
  const isGenerating = useGlobalStore(selectIsGenerating);
  
  const [activeTab, setActiveTab] = useState<'style' | 'color' | 'flooring'>('style');

  const handleGenerate = async () => {
    if (!roomId || !canGenerate) return;

    startGeneration();

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        const progress = Math.min(95, Math.random() * 30 + 20);
        // Update progress in store
      }, 5000);

      const response = await designService.generateDesign({
        room_id: roomId,
        style: selectedCustomization.style,
        wall_color: selectedCustomization.wall_color,
        flooring_material: selectedCustomization.flooring_material,
        budget: selectedCustomization.budget,
      });

      clearInterval(progressInterval);

      // Fetch the generated designs
      const designs = await designService.getUserDesigns();
      const latestDesign = designs[0];
      
      completeGeneration(designs);
      incrementUsage();
      
      // Navigate to design view
      navigate(`/design/${response.design_id}`);
    } catch (error: any) {
      failGeneration(error.message || 'Generation failed. Please try again.');
    }
  };

  // Redirect if no room uploaded
  if (!roomId) {
    return (
      <div className="text-center py-20">
        <PhotoIcon className="w-16 h-16 mx-auto text-neutral-300 mb-4" />
        <h2 className="text-2xl font-display font-bold text-brand-charcoal mb-2">
          No Room Uploaded
        </h2>
        <p className="text-neutral-600 mb-6">
          Please upload your room images first to generate designs
        </p>
        <Button onClick={() => navigate('/upload')}>
          Upload Room
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-10"
      >
        <h1 className="text-4xl font-display font-bold text-brand-charcoal mb-4">
          Design Your Space
        </h1>
        <p className="text-lg text-neutral-600 max-w-2xl mx-auto">
          Customize your interior design preferences and let our AI create stunning 
          3 variations of your dream room.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Panel - Customization Controls */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-4 space-y-6"
        >
          <Card className="sticky top-24">
            <div className="p-6">
              {/* Tabs */}
              <div className="flex gap-2 mb-6">
                {[
                  { id: 'style', label: 'Style', icon: SparklesIcon },
                  { id: 'color', label: 'Walls', icon: '🎨' },
                  { id: 'flooring', label: 'Floor', icon: '🏠' },
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={cn(
                      'flex-1 py-3 px-4 rounded-xl text-sm font-medium transition-all duration-300',
                      activeTab === tab.id
                        ? 'bg-brand-gold text-white shadow-glow'
                        : 'bg-neutral-100 text-neutral-600 hover:bg-neutral-200'
                    )}
                  >
                    {typeof tab.icon === 'string' ? tab.icon : <tab.icon className="w-4 h-4 mx-auto" />}
                    <span className="block mt-1">{tab.label}</span>
                  </button>
                ))}
              </div>

              {/* Style Selection */}
              {activeTab === 'style' && (
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-brand-charcoal mb-4">
                    Select Interior Style
                  </h3>
                  {STYLE_OPTIONS.map((style) => (
                    <motion.button
                      key={style.id}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setSelectedCustomization({ style: style.id })}
                      className={cn(
                        'w-full flex items-center gap-3 p-4 rounded-xl border-2 transition-all duration-300',
                        selectedCustomization.style === style.id
                          ? 'border-brand-gold bg-brand-gold/10'
                          : 'border-neutral-200 hover:border-brand-gold/50'
                      )}
                    >
                      <span className="text-2xl">{style.icon}</span>
                      <span className="font-medium text-brand-charcoal">
                        {style.label}
                      </span>
                      {selectedCustomization.style === style.id && (
                        <CheckCircleIcon className="w-5 h-5 text-brand-gold ml-auto" />
                      )}
                    </motion.button>
                  ))}
                </div>
              )}

              {/* Wall Color Selection */}
              {activeTab === 'color' && (
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-brand-charcoal mb-4">
                    Choose Wall Color
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    {WALL_COLOR_OPTIONS.map((color) => (
                      <motion.button
                        key={color.id}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setSelectedCustomization({ wall_color: color.id })}
                        className={cn(
                          'p-4 rounded-xl border-2 transition-all duration-300 text-left',
                          selectedCustomization.wall_color === color.id
                            ? 'border-brand-gold shadow-glow'
                            : 'border-neutral-200 hover:border-brand-gold/50'
                        )}
                      >
                        <div
                          className="w-full h-12 rounded-lg mb-2 border border-neutral-200"
                          style={{ backgroundColor: color.color }}
                        />
                        <span className="text-sm font-medium text-brand-charcoal">
                          {color.label}
                        </span>
                      </motion.button>
                    ))}
                  </div>
                </div>
              )}

              {/* Flooring Selection */}
              {activeTab === 'flooring' && (
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold text-brand-charcoal mb-4">
                    Select Flooring
                  </h3>
                  {FLOORING_OPTIONS.map((floor) => (
                    <motion.button
                      key={floor.id}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setSelectedCustomization({ flooring_material: floor.id })}
                      className={cn(
                        'w-full flex items-center gap-3 p-4 rounded-xl border-2 transition-all duration-300',
                        selectedCustomization.flooring_material === floor.id
                          ? 'border-brand-gold bg-brand-gold/10'
                          : 'border-neutral-200 hover:border-brand-gold/50'
                      )}
                    >
                      <span className="text-2xl">{floor.icon}</span>
                      <span className="font-medium text-brand-charcoal">
                        {floor.label}
                      </span>
                      {selectedCustomization.flooring_material === floor.id && (
                        <CheckCircleIcon className="w-5 h-5 text-brand-gold ml-auto" />
                      )}
                    </motion.button>
                  ))}
                </div>
              )}
            </div>
          </Card>

          {/* Generate Button */}
          <Button
            size="lg"
            fullWidth
            isLoading={isGenerating}
            disabled={!canGenerate || isGenerating}
            onClick={handleGenerate}
            leftIcon={<SparklesIcon className="w-5 h-5" />}
            className="py-4 text-lg shadow-luxury"
          >
            {!canGenerate 
              ? 'Daily Limit Reached'
              : isGenerating 
                ? 'Generating Designs...'
                : 'Generate 3 Designs'
            }
          </Button>
        </motion.div>

        {/* Right Panel - Preview Area */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-8"
        >
          <Card variant="glass" className="h-full min-h-[600px]">
            <div className="p-8 h-full flex flex-col items-center justify-center text-center">
              {/* Preview Placeholder */}
              <motion.div
                animate={{ 
                  y: [0, -10, 0],
                  rotate: [0, 2, -2, 0]
                }}
                transition={{ 
                  duration: 4, 
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
                className="mb-8"
              >
                <div className="w-48 h-48 mx-auto bg-gradient-to-br from-brand-gold/20 to-brand-gold/5 rounded-3xl flex items-center justify-center border-2 border-dashed border-brand-gold/30">
                  <SparklesIcon className="w-20 h-20 text-brand-gold/50" />
                </div>
              </motion.div>

              <h3 className="text-2xl font-display font-bold text-brand-charcoal mb-4">
                Your Design Preview
              </h3>
              
              <p className="text-neutral-600 max-w-md mb-8">
                Select your preferences on the left and click "Generate" to create 
                3 unique AI-powered interior design variations of your room.
              </p>

              {/* Selected Preferences Summary */}
              <div className="grid grid-cols-3 gap-4 w-full max-w-lg">
                <div className="bg-brand-beige/50 rounded-xl p-4">
                  <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Style</p>
                  <p className="font-semibold text-brand-char capitalize">
                    {STYLE_OPTIONS.find(s => s.id === selectedCustomization.style)?.label}
                  </p>
                </div>
                <div className="bg-brand-beige/50 rounded-xl p-4">
                  <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Walls</p>
                  <p className="font-semibold text-brand-char capitalize">
                    {WALL_COLOR_OPTIONS.find(c => c.id === selectedCustomization.wall_color)?.label}
                  </p>
                </div>
                <div className="bg-brand-beige/50 rounded-xl p-4">
                  <p className="text-xs text-neutral-500 uppercase tracking-wider mb-1">Floor</p>
                  <p className="font-semibold text-brand-char capitalize">
                    {FLOORING_OPTIONS.find(f => f.id === selectedCustomization.flooring_material)?.label}
                  </p>
                </div>
              </div>

              {/* Features List */}
              <div className="mt-8 flex flex-wrap justify-center gap-4">
                {[
                  { icon: '✨', text: '3 Unique Variations' },
                  { icon: '🏠', text: 'Vastu Compliant' },
                  { icon: '💰', text: 'Cost Estimation' },
                  { icon: '⚡', text: '45-60 Seconds' },
                ].map((feature, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className="flex items-center gap-2 px-4 py-2 bg-white/50 rounded-full"
                  >
                    <span>{feature.icon}</span>
                    <span className="text-sm font-medium text-brand-charcoal">
                      {feature.text}
                    </span>
                  </motion.div>
                ))}
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  );
};

export default DesignGenerator;
