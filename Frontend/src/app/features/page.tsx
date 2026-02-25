import Link from 'next/link';
import { CompassIcon, ArrowLeftIcon } from 'lucide-react';

export default function FeaturesPage() {
  const features = [
    {
      title: 'AI-Powered Design',
      description: 'Generate interior designs using advanced AI that understands spatial harmony.',
      icon: '🎨'
    },
    {
      title: 'Vastu Analysis',
      description: 'Get directional recommendations based on ancient Vastu principles.',
      icon: '🧭'
    },
    {
      title: 'Room Upload',
      description: 'Upload photos of your space and get instant design suggestions.',
      icon: '📸'
    },
    {
      title: '3D Visualization',
      description: 'See your designs in immersive 3D before making changes.',
      icon: '👁️'
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
          <h1 className="text-4xl font-bold text-[#1F1F1F] mb-4">Features</h1>
          <p className="text-xl text-gray-600">Discover what makes AntarAalay.ai unique</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <div key={index} className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all">
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-[#1F1F1F] mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
