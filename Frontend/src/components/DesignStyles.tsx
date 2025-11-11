import { motion } from 'framer-motion'
import { ArrowRight } from 'lucide-react'

const DesignStyles = () => {
  const styles = [
    {
      name: 'Modern Minimalist',
      description: 'Clean lines, neutral colors, and functional beauty',
      gradient: 'from-gray-100 to-gray-200',
      hoverGradient: 'from-gray-200 to-gray-300',
      image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800',
    },
    {
      name: 'Traditional Indian',
      description: 'Rich textures, warm colors, and cultural heritage',
      gradient: 'from-amber-100 to-orange-200',
      hoverGradient: 'from-amber-200 to-orange-300',
      image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800',
    },
    {
      name: 'Luxury Contemporary',
      description: 'Sophisticated elegance with premium finishes',
      gradient: 'from-indigo-100 to-purple-200',
      hoverGradient: 'from-indigo-200 to-purple-300',
      image: 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800',
    },
  ]

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4 text-gray-900">
            Choose Your Design Style
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Explore different aesthetics that match your vision
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {styles.map((style, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -10, scale: 1.02 }}
              className="group relative bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all cursor-pointer"
            >
              <div className={`h-64 bg-gradient-to-br ${style.gradient} group-hover:${style.hoverGradient} transition-all relative overflow-hidden`}>
                <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-all" />
                <div className="absolute bottom-4 left-4 right-4">
                  <h3 className="text-2xl font-bold text-white mb-2">{style.name}</h3>
                </div>
              </div>
              <div className="p-6">
                <p className="text-gray-600 mb-4">{style.description}</p>
                <motion.button
                  whileHover={{ x: 5 }}
                  className="flex items-center space-x-2 text-blue-600 font-medium group-hover:text-blue-700"
                >
                  <span>View Suggestions</span>
                  <ArrowRight className="w-4 h-4" />
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default DesignStyles

