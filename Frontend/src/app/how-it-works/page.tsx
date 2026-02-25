import Link from 'next/link';
import { CompassIcon, ArrowLeftIcon, ArrowRightIcon } from 'lucide-react';

export default function HowItWorksPage() {
  const steps = [
    {
      step: 1,
      title: 'Upload Your Space',
      description: 'Take a photo of your room and upload it to our platform.',
      icon: '📸'
    },
    {
      step: 2,
      title: 'AI Analyzes Direction',
      description: 'Our AI determines the cardinal directions and Vastu alignment.',
      icon: '🧭'
    },
    {
      step: 3,
      title: 'Generate Designs',
      description: 'Get multiple AI-generated design options based on Vastu principles.',
      icon: '✨'
    },
    {
      step: 4,
      title: 'Transform Your Space',
      description: 'Apply the designs and create a harmonious living environment.',
      icon: '🏠'
    }
  ];

  return (
    <div className="min-h-screen bg-[#F4EFE6] py-16 px-4">
      <div className="max-w-4xl mx-auto">
        <Link href="/" className="inline-flex items-center text-[#1F1F1F] hover:text-[#C6A75E] mb-8 transition-colors">
          <ArrowLeftIcon className="w-5 h-5 mr-2" />
          Back to Home
        </Link>

        <div className="text-center mb-12">
          <div className="w-16 h-16 bg-[#C6A75E]/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <CompassIcon className="w-8 h-8 text-[#C6A75E]" />
          </div>
          <h1 className="text-4xl font-bold text-[#1F1F1F] mb-4">How It Works</h1>
          <p className="text-xl text-gray-600">Four simple steps to transform your space</p>
        </div>

        <div className="space-y-6">
          {steps.map((item) => (
            <div key={item.step} className="bg-white rounded-2xl p-8 shadow-lg flex items-start space-x-6">
              <div className="w-12 h-12 bg-[#C6A75E] rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">
                {item.step}
              </div>
              <div className="flex-1">
                <div className="text-3xl mb-2">{item.icon}</div>
                <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">{item.title}</h3>
                <p className="text-gray-600">{item.description}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-12 text-center">
          <Link href="/onboarding" className="inline-flex items-center px-8 py-4 bg-[#C6A75E] text-white rounded-xl font-semibold hover:bg-[#B89A4F] transition-all shadow-lg hover:shadow-xl">
            Start Your Journey
            <ArrowRightIcon className="ml-2 w-5 h-5" />
          </Link>
        </div>
      </div>
    </div>
  );
}
