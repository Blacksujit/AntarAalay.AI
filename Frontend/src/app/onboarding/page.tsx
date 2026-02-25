'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CompassIcon, 
  ArrowRightIcon, 
  ArrowLeftIcon,
  HomeIcon,
  UserIcon,
  BuildingIcon,
  PaletteIcon,
  CheckCircleIcon
} from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

const steps = [
  { id: 'welcome', title: 'Welcome' },
  { id: 'user-type', title: 'User Type' },
  { id: 'preferences', title: 'Preferences' },
  { id: 'complete', title: 'Complete' }
];

export default function OnboardingPage() {
  const [currentStep, setCurrentStep] = useState(0);
  const [userType, setUserType] = useState<string | null>(null);
  const [preferences, setPreferences] = useState<string[]>([]);
  const router = useRouter();

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      router.push('/dashboard');
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const togglePreference = (pref: string) => {
    setPreferences(prev => 
      prev.includes(pref) 
        ? prev.filter(p => p !== pref)
        : [...prev, pref]
    );
  };

  return (
    <div className="min-h-screen bg-[#F4EFE6] flex flex-col">
      {/* Progress Bar */}
      <div className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-[#C6A75E]/20">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-4">
            <Link href="/" className="flex items-center space-x-2">
              <CompassIcon className="w-6 h-6 text-[#C6A75E]" />
              <span className="font-bold text-[#1F1F1F]">AntarAalay.ai</span>
            </Link>
            <span className="text-sm text-gray-600">
              Step {currentStep + 1} of {steps.length}
            </span>
          </div>
          <div className="flex space-x-2">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`flex-1 h-2 rounded-full transition-colors ${
                  index <= currentStep ? 'bg-[#C6A75E]' : 'bg-gray-200'
                }`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Content */}
      <main className="flex-1 flex items-center justify-center pt-24 pb-12 px-4">
        <div className="w-full max-w-2xl">
          <AnimatePresence mode="wait">
            {currentStep === 0 && (
              <motion.div
                key="welcome"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="text-center"
              >
                <div className="w-24 h-24 bg-[#C6A75E]/10 rounded-full flex items-center justify-center mx-auto mb-8">
                  <CompassIcon className="w-12 h-12 text-[#C6A75E]" />
                </div>
                <h1 className="text-4xl md:text-5xl font-bold text-[#1F1F1F] mb-6">
                  Begin Your Journey
                </h1>
                <p className="text-xl text-gray-600 mb-8 max-w-lg mx-auto">
                  Discover how ancient Vastu wisdom and modern AI can transform your living spaces into harmonious sanctuaries.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <button
                    onClick={nextStep}
                    className="px-8 py-4 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl flex items-center justify-center"
                  >
                    Get Started
                    <ArrowRightIcon className="ml-2 w-5 h-5" />
                  </button>
                </div>
              </motion.div>
            )}

            {currentStep === 1 && (
              <motion.div
                key="user-type"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <h2 className="text-3xl font-bold text-[#1F1F1F] mb-4 text-center">
                  Which describes you best?
                </h2>
                <p className="text-gray-600 mb-8 text-center">
                  This helps us personalize your Vastu design experience
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
                  {[
                    { id: 'homeowner', icon: HomeIcon, label: 'Homeowner', desc: 'Designing my own space' },
                    { id: 'interior_designer', icon: PaletteIcon, label: 'Interior Designer', desc: 'Professional designer' },
                    { id: 'architect', icon: BuildingIcon, label: 'Architect', desc: 'Building professional' },
                    { id: 'student', icon: UserIcon, label: 'Student', desc: 'Learning about Vastu' }
                  ].map((type) => (
                    <button
                      key={type.id}
                      onClick={() => setUserType(type.id)}
                      className={`p-6 rounded-2xl border-2 text-left transition-all ${
                        userType === type.id
                          ? 'border-[#C6A75E] bg-[#C6A75E]/5'
                          : 'border-gray-200 hover:border-[#C6A75E]/50'
                      }`}
                    >
                      <type.icon className={`w-8 h-8 mb-3 ${userType === type.id ? 'text-[#C6A75E]' : 'text-gray-400'}`} />
                      <h3 className="font-semibold text-[#1F1F1F]">{type.label}</h3>
                      <p className="text-sm text-gray-500">{type.desc}</p>
                    </button>
                  ))}
                </div>

                <div className="flex justify-between">
                  <button
                    onClick={prevStep}
                    className="px-6 py-3 text-gray-600 hover:text-[#1F1F1F] transition-colors flex items-center"
                  >
                    <ArrowLeftIcon className="mr-2 w-5 h-5" />
                    Back
                  </button>
                  <button
                    onClick={nextStep}
                    disabled={!userType}
                    className="px-8 py-3 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                  >
                    Continue
                    <ArrowRightIcon className="ml-2 w-5 h-5" />
                  </button>
                </div>
              </motion.div>
            )}

            {currentStep === 2 && (
              <motion.div
                key="preferences"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <h2 className="text-3xl font-bold text-[#1F1F1F] mb-4 text-center">
                  What are you interested in?
                </h2>
                <p className="text-gray-600 mb-8 text-center">
                  Select all that apply to personalize your experience
                </p>

                <div className="grid grid-cols-2 gap-4 mb-8">
                  {[
                    { id: 'living_room', label: 'Living Room' },
                    { id: 'bedroom', label: 'Bedroom' },
                    { id: 'kitchen', label: 'Kitchen' },
                    { id: 'office', label: 'Home Office' },
                    { id: 'bathroom', label: 'Bathroom' },
                    { id: 'outdoor', label: 'Outdoor Space' }
                  ].map((pref) => (
                    <button
                      key={pref.id}
                      onClick={() => togglePreference(pref.id)}
                      className={`p-4 rounded-xl border-2 transition-all ${
                        preferences.includes(pref.id)
                          ? 'border-[#C6A75E] bg-[#C6A75E]/5'
                          : 'border-gray-200 hover:border-[#C6A75E]/50'
                      }`}
                    >
                      <span className={`font-medium ${preferences.includes(pref.id) ? 'text-[#C6A75E]' : 'text-[#1F1F1F]'}`}>
                        {pref.label}
                      </span>
                    </button>
                  ))}
                </div>

                <div className="flex justify-between">
                  <button
                    onClick={prevStep}
                    className="px-6 py-3 text-gray-600 hover:text-[#1F1F1F] transition-colors flex items-center"
                  >
                    <ArrowLeftIcon className="mr-2 w-5 h-5" />
                    Back
                  </button>
                  <button
                    onClick={nextStep}
                    className="px-8 py-3 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all flex items-center"
                  >
                    Continue
                    <ArrowRightIcon className="ml-2 w-5 h-5" />
                  </button>
                </div>
              </motion.div>
            )}

            {currentStep === 3 && (
              <motion.div
                key="complete"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center"
              >
                <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-8">
                  <CheckCircleIcon className="w-12 h-12 text-green-600" />
                </div>
                <h2 className="text-3xl font-bold text-[#1F1F1F] mb-4">
                  You&apos;re All Set!
                </h2>
                <p className="text-xl text-gray-600 mb-8">
                  Your Vastu design journey begins now. Let&apos;s create harmonious spaces together.
                </p>
                <button
                  onClick={() => router.push('/dashboard')}
                  className="px-8 py-4 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl flex items-center justify-center mx-auto"
                >
                  Go to Dashboard
                  <ArrowRightIcon className="ml-2 w-5 h-5" />
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
