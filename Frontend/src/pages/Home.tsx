import { useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { Sparkles, Compass, Palette, Shield } from 'lucide-react';

export default function Home() {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  useEffect(() => {
    if (user) {
      navigate('/dashboard');
    }
  }, [user, navigate]);

  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered Design',
      description: 'Generate stunning interior designs in seconds using advanced AI technology.'
    },
    {
      icon: Compass,
      title: 'Vastu Integration',
      description: 'Every design is analyzed for Vastu compliance with actionable suggestions.'
    },
    {
      icon: Palette,
      title: 'Budget Planning',
      description: 'Get accurate cost estimates and budget breakdowns for your dream space.'
    },
    {
      icon: Shield,
      title: 'Ancient Wisdom',
      description: 'Combine modern aesthetics with 5000-year-old Vastu Shastra principles.'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-rose-50">
      {/* Header */}
      <header className="w-full px-6 py-4 flex items-center justify-between bg-white/50 backdrop-blur-sm border-b border-amber-100">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 bg-amber-600 rounded-xl flex items-center justify-center">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-amber-900">AntarAalay.ai</h1>
        </div>
        <nav className="flex items-center gap-4">
          <Link to="/login" className="text-amber-800 hover:text-amber-900 font-medium">
            Sign In
          </Link>
          <Link 
            to="/login" 
            className="px-6 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-xl font-medium transition-all"
          >
            Get Started
          </Link>
        </nav>
      </header>

      {/* Hero */}
      <section className="px-6 py-20 max-w-7xl mx-auto text-center">
        <h2 className="text-5xl md:text-6xl font-bold text-amber-950 mb-6">
          Transform Your Space with
          <span className="block text-amber-600">AI & Ancient Wisdom</span>
        </h2>
        <p className="text-xl text-amber-800 max-w-2xl mx-auto mb-10">
          Upload your room photo and get AI-generated interior designs that align with Vastu principles. 
          Perfect harmony between modern aesthetics and ancient science.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link 
            to="/login"
            className="px-8 py-4 bg-amber-600 hover:bg-amber-700 text-white rounded-xl font-semibold text-lg transition-all shadow-lg shadow-amber-600/25"
          >
            Start Designing
          </Link>
          <button className="px-8 py-4 bg-white hover:bg-amber-50 text-amber-900 border-2 border-amber-200 rounded-xl font-semibold text-lg transition-all">
            Learn More
          </button>
        </div>
      </section>

      {/* Features */}
      <section className="px-6 py-20 bg-white/50">
        <div className="max-w-7xl mx-auto">
          <h3 className="text-3xl font-bold text-center text-amber-950 mb-12">
            Why Choose AntarAalay?
          </h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div 
                key={index} 
                className="p-6 bg-white/80 backdrop-blur-sm rounded-2xl border border-amber-100 shadow-sm hover:shadow-md transition-all"
              >
                <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-amber-600" />
                </div>
                <h4 className="text-lg font-semibold text-amber-950 mb-2">{feature.title}</h4>
                <p className="text-amber-700">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 py-20">
        <div className="max-w-4xl mx-auto bg-gradient-to-r from-amber-600 to-orange-600 rounded-3xl p-12 text-center text-white">
          <h3 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Transform Your Home?
          </h3>
          <p className="text-lg text-amber-100 mb-8">
            Join thousands of homeowners who have discovered their perfect space with AntarAalay.
          </p>
          <Link 
            to="/login"
            className="inline-block px-8 py-4 bg-white text-amber-600 rounded-xl font-semibold text-lg hover:bg-amber-50 transition-all"
          >
            Get Started Free
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-8 border-t border-amber-100">
        <div className="max-w-7xl mx-auto text-center text-amber-700">
          <p>© 2025 AntarAalay.ai. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
