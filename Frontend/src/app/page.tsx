/**
 * AntarAalay.ai Landing Page
 * Vastu × AI Spatial Intelligence Platform
 */

'use client';

import { motion } from 'framer-motion';
import { 
  ArrowRightIcon, 
  CompassIcon, 
  HomeIcon, 
  SparklesIcon,
  UserIcon,
  MenuIcon,
  XIcon
} from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';

export default function LandingPage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#F4EFE6]">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-[#F4EFE6]/80 backdrop-blur-md border-b border-[#C6A75E]/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <Link href="/" className="flex items-center space-x-2">
              <CompassIcon className="w-8 h-8 text-[#C6A75E]" />
              <span className="text-xl font-bold text-[#1F1F1F]">AntarAalay.ai</span>
            </Link>

            <div className="hidden md:flex items-center space-x-4">
              <Link href="/login" className="px-6 py-2 bg-[#C6A75E] text-white rounded-xl font-medium hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl">
                Get Started
              </Link>
            </div>

            <button className="md:hidden p-2 text-[#1F1F1F]" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              {mobileMenuOpen ? <XIcon className="w-6 h-6" /> : <MenuIcon className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {mobileMenuOpen && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="md:hidden bg-[#F4EFE6] border-t border-[#C6A75E]/20">
            <div className="px-4 py-4">
              <Link href="/login" className="block py-2 px-4 bg-[#C6A75E] text-white rounded-xl text-center">Get Started</Link>
            </div>
          </motion.div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 pt-16">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-1/4 right-1/4 w-64 h-64 bg-[#C6A75E]/5 rounded-full blur-3xl" />
          <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-[#C6A75E]/5 rounded-full blur-3xl" />
        </div>

        <div className="relative z-10 max-w-6xl mx-auto text-center">
          <motion.div animate={{ rotate: 360 }} transition={{ duration: 20, repeat: Infinity, ease: 'linear' }} className="absolute -top-10 right-10 w-24 h-24 opacity-10 hidden lg:block">
            <CompassIcon className="w-full h-full text-[#C6A75E]" />
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="inline-flex items-center px-4 py-2 bg-[#C6A75E]/10 rounded-full mb-8">
            <SparklesIcon className="w-4 h-4 text-[#C6A75E] mr-2" />
            <span className="text-sm text-[#C6A75E] font-medium">AI-Powered Vastu Design</span>
          </motion.div>

          <motion.h1 initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.1 }} className="text-5xl md:text-7xl font-bold text-[#1F1F1F] leading-tight mb-6">
            Design in<span className="text-[#C6A75E] block"> Harmony.</span>
            <span className="text-3xl md:text-5xl font-normal text-[#1F1F1F]/80 block mt-4">Powered by Intelligence.</span>
          </motion.h1>

          <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.2 }} className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed mb-10">
            AntarAalay blends ancient Vastu principles with modern AI to transform empty spaces into balanced, fully designed interiors.
          </motion.p>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.3 }} className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/login" className="px-8 py-4 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl flex items-center">
              Design My Space<ArrowRightIcon className="ml-2 w-5 h-5" />
            </Link>
            <Link href="/login" className="px-8 py-4 border-2 border-[#C6A75E] text-[#C6A75E] rounded-xl font-semibold hover:bg-[#C6A75E] hover:text-white transition-all flex items-center">
              <UserIcon className="mr-2 w-5 h-5" />Sign In
            </Link>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.4 }} className="mt-16 flex flex-wrap items-center justify-center gap-8 text-gray-500">
            <div className="flex items-center space-x-2"><HomeIcon className="w-5 h-5" /><span>10,000+ Spaces Transformed</span></div>
            <div className="flex items-center space-x-2"><SparklesIcon className="w-5 h-5" /><span>AI-Powered Precision</span></div>
            <div className="flex items-center space-x-2"><CompassIcon className="w-5 h-5" /><span>Vastu Certified</span></div>
          </motion.div>
        </div>
      </section>

      {/* Directional Design Section */}
      <section className="py-24 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-[#1F1F1F] mb-6">The Science of Directional Design</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">Every direction influences energy. Our AI understands spatial geometry. Together, they create harmony.</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[{ direction: 'North', element: 'Water', quality: 'Prosperity', color: '#3B82F6', icon: '↑' },{ direction: 'South', element: 'Fire', quality: 'Reputation', color: '#EF4444', icon: '↓' },{ direction: 'East', element: 'Air', quality: 'Health', color: '#10B981', icon: '→' },{ direction: 'West', element: 'Earth', quality: 'Family', color: '#F59E0B', icon: '←' }].map((item, index) => (
              <motion.div key={item.direction} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: index * 0.1 }} className="bg-white rounded-2xl p-8 text-center shadow-lg hover:shadow-xl transition-all border border-gray-100">
                <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 text-2xl font-bold text-white" style={{ backgroundColor: item.color }}>{item.icon}</div>
                <h3 className="text-xl font-bold text-[#1F1F1F] mb-1">{item.direction}</h3>
                <p className="text-[#C6A75E] font-medium mb-1">{item.element}</p>
                <p className="text-gray-500 text-sm">{item.quality}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4 bg-[#F4EFE6]">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
            <h2 className="text-4xl md:text-5xl font-bold text-[#1F1F1F] mb-6">Ready to Transform Your Space?</h2>
            <p className="text-xl text-gray-600 mb-10">Join thousands who have discovered the power of directional design. Begin your journey to a more harmonious home.</p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link href="/login" className="px-8 py-4 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl flex items-center">
                Start Your Design Journey<ArrowRightIcon className="ml-2 w-5 h-5" />
              </Link>
              <Link href="/login" className="px-8 py-4 border-2 border-[#C6A75E] text-[#C6A75E] rounded-xl font-semibold hover:bg-[#C6A75E] hover:text-white transition-all">Sign In to Your Account</Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 bg-[#1F1F1F] text-white">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <CompassIcon className="w-6 h-6 text-[#C6A75E]" />
              <span className="text-lg font-bold">AntarAalay.ai</span>
            </div>
            <div className="flex items-center space-x-6 text-gray-400">
              <Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link>
              <Link href="/terms" className="hover:text-white transition-colors">Terms</Link>
              <Link href="/contact" className="hover:text-white transition-colors">Contact</Link>
            </div>
          </div>
          <p className="mt-8 text-center text-gray-500 text-sm">© 2026 AntarAalay.ai. Ancient wisdom meets modern intelligence.</p>
        </div>
      </footer>
    </div>
  );
}
