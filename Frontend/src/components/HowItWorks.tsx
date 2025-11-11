import { motion } from 'framer-motion'
import { Upload, Sparkles, Compass, User, Download } from 'lucide-react'

const HowItWorks = () => {
  const steps = [
    {
      number: 1,
      icon: Upload,
      title: 'Upload Room Video',
      description: 'Upload your room video or 360° scan',
    },
    {
      number: 2,
      icon: Sparkles,
      title: 'AI Suggests Design',
      description: 'Our AI analyzes and suggests optimal designs',
    },
    {
      number: 3,
      icon: Compass,
      title: 'Check Vastu',
      description: 'Get Vastu-compliant recommendations',
    },
    {
      number: 4,
      icon: User,
      title: 'Consult Pandit',
      description: 'Connect with certified Vastu experts',
    },
    {
      number: 5,
      icon: Download,
      title: 'Download Plan',
      description: 'Get your complete design package',
    },
  ]

  return (
    <section id="how-it-works" className="py-20 bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900">
            How It Works
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Simple steps to transform your space
          </p>
        </motion.div>

        <div className="relative">
          {/* Connection Line */}
          <div className="hidden lg:block absolute top-24 left-0 right-0 h-1 bg-gradient-to-r from-blue-200 via-purple-200 to-blue-200" />

          <div className="grid grid-cols-1 md:grid-cols-5 gap-8 relative">
            {steps.map((step, index) => {
              const Icon = step.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  whileHover={{ scale: 1.05 }}
                  className="relative"
                >
                  <div className="bg-white rounded-2xl p-6 shadow-lg border-2 border-gray-100 hover:border-blue-500 transition-all text-center">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-600 to-purple-600 flex items-center justify-center text-white font-bold text-xl">
                      {step.number}
                    </div>
                    <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-blue-100 flex items-center justify-center">
                      <Icon className="w-6 h-6 text-blue-600" />
                    </div>
                    <h3 className="text-lg font-bold mb-2 text-gray-900">{step.title}</h3>
                    <p className="text-sm text-gray-600">{step.description}</p>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.6 }}
          className="text-center mt-12"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-bold text-lg shadow-lg hover:shadow-xl transition-all"
          >
            Try Now — It's Free!
          </motion.button>
        </motion.div>
      </div>
    </section>
  )
}

export default HowItWorks

