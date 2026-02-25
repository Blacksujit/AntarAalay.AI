import Link from 'next/link';
import { CompassIcon, ArrowLeftIcon, CheckIcon } from 'lucide-react';

export default function PricingPage() {
  const plans = [
    {
      name: 'Free',
      price: '$0',
      period: 'forever',
      description: 'Perfect for getting started',
      features: ['3 AI designs per month', 'Basic Vastu analysis', 'Room upload (1 photo)', 'Email support'],
      cta: 'Get Started',
      href: '/onboarding',
      popular: false
    },
    {
      name: 'Pro',
      price: '$19',
      period: 'per month',
      description: 'For serious home designers',
      features: ['Unlimited AI designs', 'Advanced Vastu analysis', 'Multiple room uploads', 'Priority support', '3D visualization', 'Design history'],
      cta: 'Start Pro Trial',
      href: '/onboarding',
      popular: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: 'pricing',
      description: 'For architects & designers',
      features: ['Everything in Pro', 'White-label solutions', 'API access', 'Dedicated support', 'Custom training', 'Team collaboration'],
      cta: 'Contact Sales',
      href: '/contact',
      popular: false
    }
  ];

  return (
    <div className="min-h-screen bg-[#F4EFE6] py-16 px-4">
      <div className="max-w-6xl mx-auto">
        <Link href="/" className="inline-flex items-center text-[#1F1F1F] hover:text-[#C6A75E] mb-8 transition-colors">
          <ArrowLeftIcon className="w-5 h-5 mr-2" />
          Back to Home
        </Link>

        <div className="text-center mb-12">
          <div className="w-16 h-16 bg-[#C6A75E]/10 rounded-full flex items-center justify-center mx-auto mb-6">
            <CompassIcon className="w-8 h-8 text-[#C6A75E]" />
          </div>
          <h1 className="text-4xl font-bold text-[#1F1F1F] mb-4">Simple Pricing</h1>
          <p className="text-xl text-gray-600">Choose the plan that fits your needs</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan) => (
            <div key={plan.name} className={`bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all ${plan.popular ? 'border-2 border-[#C6A75E] relative' : ''}`}>
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-[#C6A75E] text-white px-4 py-1 rounded-full text-sm font-medium">
                  Most Popular
                </div>
              )}
              <h3 className="text-2xl font-bold text-[#1F1F1F] mb-2">{plan.name}</h3>
              <div className="mb-4">
                <span className="text-4xl font-bold text-[#1F1F1F]">{plan.price}</span>
                <span className="text-gray-500">/{plan.period}</span>
              </div>
              <p className="text-gray-600 mb-6">{plan.description}</p>
              
              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-center text-gray-700">
                    <CheckIcon className="w-5 h-5 text-[#C6A75E] mr-3 flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>

              <Link href={plan.href} className={`block w-full py-3 rounded-xl font-semibold text-center transition-all ${
                plan.popular 
                  ? 'bg-[#C6A75E] text-white hover:bg-[#B89A4F] shadow-lg hover:shadow-xl' 
                  : 'border-2 border-[#C6A75E] text-[#C6A75E] hover:bg-[#C6A75E] hover:text-white'
              }`}>
                {plan.cta}
              </Link>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
