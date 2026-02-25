/**
 * Premium Landing Page for AntarAalay.ai
 * Luxury interior design AI platform
 */

import { motion } from 'framer-motion';
import { ArrowRightIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { cn } from '../utils/logger';

const Landing = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-beige via-white to-brand-white">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background with subtle pattern */}
        <div className="absolute inset-0 bg-[url('/hero-pattern.svg')] opacity-5" />
        
        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            {/* Luxury badge */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5, duration: 0.6 }}
              className="inline-flex items-center px-4 py-2 mb-8 text-sm font-medium text-brand-charcoal bg-brand-gold/10 rounded-full"
            >
              <SparklesIcon className="w-4 h-4 mr-2 text-brand-gold" />
              AI-Powered Design Studio
            </motion.div>

            {/* Main headline */}
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.8 }}
              className="text-6xl sm:text-7xl lg:text-8xl font-display font-bold text-brand-charcoal leading-tight mb-6"
            >
              Transform Your
              <span className="text-brand-gold">Empty Space</span>
              <br />
              Into A Designed Reality
            </motion.h1>

            {/* Subheadline */}
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="text-xl sm:text-2xl text-neutral-600 max-w-3xl mx-auto mb-12 font-body"
            >
              AI-powered architectural interior styling with precision and elegance.
            </motion.p>

            {/* CTA Button */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.9, duration: 0.8 }}
              whileHover={{ scale: 1.05, boxShadow: "0 0 30px rgba(198, 167, 94, 0.4)" }}
              className="inline-block"
            >
              <button className={cn(
                "group relative px-8 py-4 text-lg font-semibold text-brand-white",
                "bg-gradient-to-r from-brand-gold to-brand-gold/600",
                "rounded-xl shadow-luxury hover:shadow-glow",
                "transition-all duration-300 ease-out"
              )}>
                <span className="relative z-10 flex items-center">
                  Start Designing
                  <ArrowRightIcon className="ml-2 w-5 h-5 transition-transform group-hover:translate-x-1" />
                </span>
                
                {/* Button shimmer effect */}
                <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-transparent via-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              </button>
            </motion.div>
          </motion.div>
        </div>

        {/* Floating design elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-brand-gold/20 rounded-full blur-xl animate-float" />
        <div className="absolute top-40 right-20 w-16 h-16 bg-brand-gold/10 rounded-full blur-lg animate-float" style={{ animationDelay: '2s' }} />
        <div className="absolute bottom-20 left-20 w-24 h-24 bg-brand-gold/5 rounded-full blur-2xl animate-float" style={{ animationDelay: '4s' }} />
      </section>

      {/* How It Works Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-display font-bold text-brand-charcoal mb-4">
              How It Works
            </h2>
            <p className="text-xl text-neutral-600 max-w-2xl mx-auto font-body">
              Transform your space in three simple steps
            </p>
          </motion.div>

          {/* Steps */}
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            {[
              {
                title: "Upload Room",
                description: "Capture 4 directional images of your space",
                icon: "📸",
              },
              {
                title: "Customize Style",
                description: "Choose your preferred design aesthetic",
                icon: "🎨",
              },
              {
                title: "Get Designs",
                description: "Receive AI-generated furnished interiors",
                icon: "✨",
              },
            ].map((step, index) => (
              <motion.div
                key={step.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2, duration: 0.6 }}
                className={cn(
                  "bg-white rounded-2xl p-8 shadow-soft",
                  "hover:shadow-luxury transition-all duration-300"
                )}
              >
                <div className="text-4xl mb-4">{step.icon}</div>
                <h3 className="text-xl font-semibold text-brand-charcoal mb-3">
                  {step.title}
                </h3>
                <p className="text-neutral-600 font-body">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Showcase Carousel */}
      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-warm-50">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-display font-bold text-brand-charcoal mb-4">
              Before → After Transformations
            </h2>
            <p className="text-xl text-neutral-600 max-w-2xl mx-auto mb-12 font-body">
              See the magic of AI-powered interior design
            </p>
          </motion.div>

          {/* Before/After Slider */}
          <div className="relative bg-white rounded-2xl shadow-luxury overflow-hidden">
            <div className="grid md:grid-cols-2">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-brand-charcoal/80 to-brand-charcoal/60 z-10 flex items-center justify-center">
                  <span className="text-white font-semibold text-lg">Before</span>
                </div>
                <img
                  src="/showcase-before.jpg"
                  alt="Empty room before design"
                  className="w-full h-64 object-cover"
                />
              </div>
              
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-brand-gold/80 to-brand-gold/60 z-10 flex items-center justify-center">
                  <span className="text-white font-semibold text-lg">After</span>
                </div>
                <img
                  src="/showcase-after.jpg"
                  alt="Designed room after AI transformation"
                  className="w-full h-64 object-cover"
                />
              </div>
            </div>
            
            {/* Slider controls */}
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2">
              <button className="w-3 h-3 bg-brand-gold rounded-full shadow-soft" />
              <button className="w-3 h-3 bg-neutral-300 rounded-full" />
              <button className="w-3 h-3 bg-neutral-300 rounded-full" />
            </div>
          </div>
        </div>
      </section>

      {/* For Agencies Section */}
      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <div className="inline-flex items-center px-6 py-3 mb-8 text-sm font-medium text-brand-charcoal bg-brand-gold/10 rounded-full">
              <SparklesIcon className="w-4 h-4 mr-2 text-brand-gold" />
              For Agencies & Designers
            </div>
            <h2 className="text-4xl font-display font-bold text-brand-charcoal mb-4">
              Enterprise-Grade Interior Design
            </h2>
            <p className="text-xl text-neutral-600 max-w-3xl mx-auto mb-12 font-body">
              Scale your design business with our AI-powered platform. 
              Collaborate, deliver stunning results, and grow your client base.
            </p>
          </motion.div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            {[
              {
                title: "Bulk Processing",
                description: "Handle multiple client projects simultaneously",
                icon: "⚡",
              },
              {
                title: "White Label",
                description: "Brand the platform as your own",
                icon: "🏷️",
              },
              {
                title: "API Access",
                description: "Integrate with your existing tools",
                icon: "🔌",
              },
            ].map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.2, duration: 0.6 }}
                className={cn(
                  "bg-white rounded-2xl p-8 shadow-soft",
                  "hover:shadow-luxury transition-all duration-300"
                )}
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-brand-charcoal mb-3">
                  {feature.title}
                </h3>
                <p className="text-neutral-600 font-body">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-brand-charcoal text-brand-white py-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <span className="text-2xl font-display font-bold text-brand-gold">
                AntarAalay.ai
              </span>
            </div>
            <p className="text-neutral-400 font-body">
              © 2024 AntarAalay.ai. Transforming spaces with AI-powered interior design.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
