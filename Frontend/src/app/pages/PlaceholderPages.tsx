/**
 * Placeholder pages for routes
 * Quick implementations to satisfy router requirements
 */

import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  PhotoIcon,
  UserIcon,
  ScaleIcon,
  BuildingLibraryIcon,
  ArrowLeftIcon
} from '@heroicons/react/24/outline';
import { Button } from '../../components/ui/Button';
import { Card } from '../../components/ui/Card';

const PlaceholderPage = ({ 
  title, 
  description, 
  icon: Icon 
}: { 
  title: string; 
  description: string;
  icon: React.ElementType;
}) => {
  const navigate = useNavigate();
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-2xl mx-auto py-20 text-center"
    >
      <Card className="py-16 px-8">
        <div className="w-20 h-20 mx-auto mb-6 bg-brand-gold/10 rounded-full flex items-center justify-center">
          <Icon className="w-10 h-10 text-brand-gold" />
        </div>
        <h1 className="text-3xl font-display font-bold text-brand-charcoal mb-4">
          {title}
        </h1>
        <p className="text-neutral-600 mb-8 max-w-md mx-auto">
          {description}
        </p>
        <Button
          onClick={() => navigate('/dashboard')}
          leftIcon={<ArrowLeftIcon className="w-5 h-5" />}
        >
          Back to Dashboard
        </Button>
      </Card>
    </motion.div>
  );
};

export const DesignView = () => (
  <PlaceholderPage
    title="Design Details"
    description="View your generated design in full detail with cost breakdown and Vastu analysis."
    icon={PhotoIcon}
  />
);

export const History = () => (
  <PlaceholderPage
    title="Design History"
    description="Browse all your past interior designs and regenerate them with new customizations."
    icon={PhotoIcon}
  />
);

export const Profile = () => (
  <PlaceholderPage
    title="Your Profile"
    description="Manage your account settings, usage statistics, and subscription details."
    icon={UserIcon}
  />
);

export const Compare = () => (
  <PlaceholderPage
    title="Compare Designs"
    description="Side-by-side comparison of different interior design variations."
    icon={ScaleIcon}
  />
);

export const Vastu = () => (
  <PlaceholderPage
    title="Vastu Analysis"
    description="Learn about Vastu Shastra principles and get personalized recommendations."
    icon={BuildingLibraryIcon}
  />
);

export const NotFound = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="max-w-2xl mx-auto py-20 text-center"
  >
    <Card className="py-16 px-8">
      <div className="text-6xl font-display font-bold text-brand-gold mb-4">
        404
      </div>
      <h1 className="text-3xl font-display font-bold text-brand-charcoal mb-4">
        Page Not Found
      </h1>
      <p className="text-neutral-600 mb-8">
        The page you're looking for doesn't exist or has been moved.
      </p>
      <Button onClick={() => window.location.href = '/dashboard'}>
        Go to Dashboard
      </Button>
    </Card>
  </motion.div>
);

export default DesignView;
