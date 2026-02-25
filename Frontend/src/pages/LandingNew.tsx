/**
 * Enterprise Landing Page
 * Luxury interior design platform landing
 */

import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  SparklesIcon,
  ArrowRightIcon,
  PhotoIcon,
  HeartIcon,
  ClockIcon
} from '@heroicons/react/24/outline';
import { Button } from '../components/ui/Button';
import { Card } from '../components/ui/Card';

export const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-beige via-brand-cream to-brand-white">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
        className="min-h-screen flex items-center justify-center px-4"
      >
        <div className="max-w-6xl mx-auto text-center">
          {/* Logo */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, duration: 0.5 }}
            className="w-20 h-20 mx-auto mb-8 bg-brand-gold rounded-3xl flex items-center justify-center shadow-glow"
          >
            <SparklesIcon className="w-10 h-10 text-brand-charcoal" />
          </motion.div>

          {/* Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="text-5xl md:text-7xl font-display font-bold text-brand-charcoal mb-6"
          >
            Transform Your
            <span className="block text-brand-gold">Living Space</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="text-xl md:text-2xl text-neutral-600 max-w-3xl mx-auto mb-12"
          >
            Experience the future of interior design with AI-powered transformations 
            that respect Vastu principles and your unique style.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.8 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <Button
              size="lg"
              onClick={() => navigate('/login')}
              className="px-8 py-4 text-lg shadow-luxury"
            >
              Start Designing
              <ArrowRightIcon className="w-5 h-5 ml-2" />
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() => navigate('/dashboard')}
              className="px-8 py-4 text-lg"
            >
              View Demo
            </Button>
          </motion.div>
        </div>
      </motion.section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl font-display font-bold text-brand-charcoal text-center mb-16"
          >
            Why Choose AntarAalay?
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: PhotoIcon,
                title: 'AI-Powered Design',
                description: 'Generate stunning interior designs in seconds with advanced AI technology.',
              },
              {
                icon: HeartIcon,
                title: 'Vastu Compliant',
                description: 'All designs follow Vastu Shastra principles for harmony and prosperity.',
              },
              {
                icon: ClockIcon,
                title: 'Quick Results',
                description: 'Get 3 design variations in under 60 seconds with cost estimation.',
              },
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
              >
                <Card className="h-full text-center p-8 shadow-soft hover:shadow-luxury transition-shadow duration-300">
                  <div className="w-16 h-16 mx-auto mb-6 bg-brand-gold/10 rounded-2xl flex items-center justify-center">
                    <feature.icon className="w-8 h-8 text-brand-gold" />
                  </div>
                  <h3 className="text-xl font-semibold text-brand-charcoal mb-4">
                    {feature.title}
                  </h3>
                  <p className="text-neutral-600">
                    {feature.description}
                  </p>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-brand-gold/10 to-brand-gold/5">
        <div className="max-w-4xl mx-auto text-center">
          <motion.h2
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-4xl font-display font-bold text-brand-charcoal mb-6"
          >
            Ready to Transform Your Space?
          </motion.h2>
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-xl text-neutral-600 mb-8"
          >
            Join thousands of homeowners who've redesigned their spaces with AntarAalay.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.4 }}
          >
            <Button
              size="lg"
              onClick={() => navigate('/login')}
              className="px-8 py-4 text-lg shadow-luxury"
            >
              Get Started Now
              <ArrowRightIcon className="w-5 h-5 ml-2" />
            </Button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export async function getServerSideProps() {
  return { props: {} };
}

export default Landing;
