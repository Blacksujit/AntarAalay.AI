import { motion } from 'framer-motion'
import { Mail, Phone, MapPin } from 'lucide-react'

const Footer = () => {
  const services = [
    'AI Room Scan',
    '3D Visualization',
    'Vastu Analysis',
    'Pandit Consultation',
  ]

  const styles = [
    'Modern Minimalist',
    'Traditional Indian',
    'Luxury Contemporary',
    'Custom Designs',
  ]

  const contact = [
    { icon: Mail, text: 'support@aiinterior.com' },
    { icon: Phone, text: '+91 98765 43210' },
    { icon: MapPin, text: 'Mumbai, India' },
  ]

  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h3 className="text-2xl font-bold mb-4 gradient-text">AI Interior</h3>
            <p className="text-gray-400">
              Transform your space with AI-powered interior design and ancient Vastu wisdom.
            </p>
          </motion.div>

          {/* Services */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            <h4 className="font-bold mb-4">Services</h4>
            <ul className="space-y-2">
              {services.map((service, index) => (
                <li key={index} className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                  {service}
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Design Styles */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >
            <h4 className="font-bold mb-4">Design Styles</h4>
            <ul className="space-y-2">
              {styles.map((style, index) => (
                <li key={index} className="text-gray-400 hover:text-white transition-colors cursor-pointer">
                  {style}
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Contact */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <h4 className="font-bold mb-4">Contact</h4>
            <ul className="space-y-3">
              {contact.map((item, index) => {
                const Icon = item.icon
                return (
                  <li key={index} className="flex items-center space-x-2 text-gray-400">
                    <Icon className="w-4 h-4" />
                    <span>{item.text}</span>
                  </li>
                )
              })}
            </ul>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="border-t border-gray-800 pt-8 text-center text-gray-400"
        >
          <p>© 2024 AI Interior. All rights reserved.</p>
          <p className="mt-2 text-sm">Built with v0</p>
        </motion.div>
      </div>
    </footer>
  )
}

export default Footer

