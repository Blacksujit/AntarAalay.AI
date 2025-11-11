import { motion } from 'framer-motion'
import { Scan, Box, Layout, Compass, User, Package } from 'lucide-react'

const Services = () => {
  const services = [
    {
      icon: Scan,
      title: 'AI Room Scan',
      description: 'Advanced computer vision analyzes your space dimensions and features',
    },
    {
      icon: Box,
      title: '3D Visualization',
      description: 'Photorealistic 3D renders of your redesigned space before implementation',
    },
    {
      icon: Layout,
      title: 'Furniture Placement Plan',
      description: 'Optimal furniture arrangement for maximum functionality and flow',
    },
    {
      icon: Compass,
      title: 'Vastu Direction Analysis',
      description: 'Comprehensive directional analysis based on Vastu Shastra principles',
    },
    {
      icon: User,
      title: 'Connect with Pandit',
      description: 'One-on-one consultations with certified Vastu experts and pandits',
    },
    {
      icon: Package,
      title: 'Complete Design Package',
      description: 'All services combined for a comprehensive interior transformation',
      featured: true,
    },
  ]

  return (
    <section id="services" className="py-20 bg-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <div className="inline-block mb-4">
            <span className="px-4 py-2 bg-blue-100 text-blue-600 rounded-full text-sm font-semibold">
              AI POWERED
            </span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900">
            Our AI Services
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Comprehensive interior design solutions powered by artificial intelligence
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service, index) => {
            const Icon = service.icon
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ y: -5, scale: 1.02 }}
                className={`relative bg-white rounded-2xl p-6 shadow-lg border-2 transition-all ${
                  service.featured
                    ? 'border-blue-500 bg-gradient-to-br from-blue-50 to-purple-50'
                    : 'border-gray-100 hover:border-blue-300'
                }`}
              >
                {service.featured && (
                  <div className="absolute top-4 right-4">
                    <span className="px-3 py-1 bg-blue-600 text-white text-xs font-bold rounded-full">
                      POPULAR
                    </span>
                  </div>
                )}
                <div className={`w-14 h-14 rounded-xl ${
                  service.featured
                    ? 'bg-gradient-to-br from-blue-600 to-purple-600'
                    : 'bg-blue-100'
                } flex items-center justify-center mb-4`}>
                  <Icon className={`w-7 h-7 ${service.featured ? 'text-white' : 'text-blue-600'}`} />
                </div>
                <h3 className="text-xl font-bold mb-2 text-gray-900">{service.title}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{service.description}</p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

export default Services

