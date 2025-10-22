import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { SearchForm } from '@/components/SearchForm';
import { ResultsDisplay } from '@/components/ResultsDisplay';
import { ThemeToggle } from '@/components/ThemeToggle';
import { FeaturedCarousel } from '@/components/FeaturedCarousel';
import { FloatingParticles } from '@/components/FloatingParticles';
import { UserProfileDropdown } from '@/components/UserProfileDropdown';
import { Product } from '@/types/product';
import { useToast } from '@/hooks/use-toast';
import { useAuth } from '@/contexts/AuthContext';
import { TrendingUp, Zap, Shield } from 'lucide-react';
import { Mail, Linkedin } from 'lucide-react';
import { saveSearch, checkUserExists, createOrUpdateUserProfile } from '@/lib/api';


const Index = () => {
  const [products, setProducts] = useState<{ amazon?: Product[]; flipkart?: Product[] }>(() => {
    // Load from sessionStorage on mount
    const saved = sessionStorage.getItem('searchResults_products');
    return saved ? JSON.parse(saved) : { amazon: [], flipkart: [] };
  });
  const [isLoading, setIsLoading] = useState(false);
  const [priceStats, setPriceStats] = useState<{low?: number, avg?: number, high?: number}>(() => {
    // Load from sessionStorage on mount
    const saved = sessionStorage.getItem('searchResults_priceStats');
    return saved ? JSON.parse(saved) : {};
  });
  const [aiRecommendation, setAiRecommendation] = useState<string | null>(() => {
    // Load from sessionStorage on mount
    const saved = sessionStorage.getItem('searchResults_aiRecommendation');
    return saved || null;
  });
  const { toast } = useToast();
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  // Persist search results to sessionStorage
  useEffect(() => {
    sessionStorage.setItem('searchResults_products', JSON.stringify(products));
  }, [products]);

  useEffect(() => {
    sessionStorage.setItem('searchResults_priceStats', JSON.stringify(priceStats));
  }, [priceStats]);

  useEffect(() => {
    if (aiRecommendation) {
      sessionStorage.setItem('searchResults_aiRecommendation', aiRecommendation);
    }
  }, [aiRecommendation]);

  // Ensure user profile exists in MongoDB (safety check for all auth users)
  useEffect(() => {
    const ensureUserProfile = async () => {
      if (user) {
        try {
          // Always create/update profile first - this is idempotent
          await createOrUpdateUserProfile({
            auth_provider: user.providerData?.[0]?.providerId === 'google.com' ? 'google' : 'email',
          });
          console.log('✅ User profile ensured in MongoDB');
        } catch (error) {
          console.error('⚠️ Failed to ensure user profile:', error);
          // Non-critical error, don't block the user
        }
      }
    };

    ensureUserProfile();
  }, [user]);

  const handleSearch = async (query: string) => {
  setIsLoading(true);
  setProducts({ amazon: [], flipkart: [] });
  setPriceStats({});
  setAiRecommendation(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || 'https://price-compare-pro-1.onrender.com';
      const response = await axios.post(`${apiUrl}/api/v1/search`, {
        query,
        location: "India",
        limit: 12  // Get top 12 products
      });

      // Update to handle the new platform-based structure
      const platformProducts: { [key: string]: Product[] } = {};
      response.data.platforms?.forEach((platform: any) => {
        platformProducts[platform.platform.toLowerCase()] = platform.products || [];
      });

      setProducts(platformProducts);

      setPriceStats({
        low: response.data.price_low,
        avg: response.data.price_avg,
        high: response.data.price_high,
      });
      setAiRecommendation(response.data.ai_recommendation || null);

      const totalCount = response.data.platforms?.reduce((acc: number, platform: any) => 
        acc + (platform.products?.length || 0), 0) || 0;
      
      // Save search to backend
      try {
        console.log('Attempting to save search:', query, totalCount);
        await saveSearch(query, totalCount);
        console.log('Search saved successfully!');
      } catch (searchError) {
        console.error('Failed to save search:', searchError);
        // Show more details about the error
        if (axios.isAxiosError(searchError)) {
          console.error('Error details:', {
            status: searchError.response?.status,
            data: searchError.response?.data,
            message: searchError.message
          });
        }
      }
      
      toast({
        title: 'Search Complete!',
        description: `Found ${totalCount} products across multiple platforms in India with INR pricing.`,
      });
    } catch (error) {
      console.error('Error searching products:', error);
      toast({
        title: 'Search Failed',
        description: axios.isAxiosError(error)
          ? error.response?.data?.detail || 'Unable to connect to the backend. Please check your internet connection and try again.'
          : 'An unexpected error occurred. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen transition-colors duration-300 relative overflow-hidden">
      {/* Floating Particles Background */}
      <FloatingParticles />

      {/* Header - Non-fixed, scrolls with page */}
      <header className="border-b glass-effect sticky top-0 z-40 shadow-glow transition-all duration-300 animate-slide-in-right">
        <div className="container mx-auto px-3 sm:px-4 py-3 sm:py-4">
          <div className="flex items-center justify-between gap-2 sm:gap-4">
            {/* Logo Section - Responsive */}
            <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
              <div className="h-10 w-10 sm:h-12 sm:w-12 rounded-lg bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 flex items-center justify-center transition-all duration-300 hover:scale-110 hover:rotate-12 animate-pulse-glow shadow-glow">
                <TrendingUp className="h-5 w-5 sm:h-7 sm:w-7 text-white" />
              </div>
              <div className="hidden xs:block">
                <h1 className="text-lg sm:text-2xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent glow-text">
                  SmartCart
                </h1>
                <p className="text-[10px] sm:text-xs text-muted-foreground hidden sm:block">AI-Powered Price Comparison</p>
              </div>
            </div>

            {/* Right Section - Theme Toggle + Profile */}
            <div className="flex items-center gap-2 sm:gap-3 animate-fade-in">
              <ThemeToggle />
              <UserProfileDropdown />
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section - Responsive */}
      <section className="py-8 sm:py-12 px-3 sm:px-4 animate-fade-in relative z-10">
        <div className="container mx-auto max-w-4xl text-center space-y-4 sm:space-y-6">
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold animate-fade-in-up px-2">
            Find the <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent glow-text animate-gradient-shift bg-[length:200%_200%]">Best Deals</span> in Seconds
          </h2>
          <p className="text-sm sm:text-base md:text-lg text-muted-foreground max-w-2xl mx-auto animate-fade-in-up px-4" style={{ animationDelay: '0.1s' }}>
            <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent font-semibold">Compare prices</span> across Amazon, Flipkart, Croma and more in India. 
            Get the best deals with accurate INR pricing from trusted retailers.
          </p>

          <div className="flex flex-wrap justify-center gap-3 sm:gap-6 pt-2 sm:pt-4 animate-fade-in-up px-2" style={{ animationDelay: '0.2s' }}>
            <div className="flex items-center gap-1.5 sm:gap-2 transition-all duration-300 hover:scale-110 hover:shadow-glow px-3 sm:px-4 py-1.5 sm:py-2 rounded-full glass-effect">
              <Zap className="h-4 w-4 sm:h-5 sm:w-5 text-purple-600 dark:text-purple-400 animate-pulse-glow" />
              <span className="text-xs sm:text-sm font-medium bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">Real-time Prices</span>
            </div>
            <div className="flex items-center gap-1.5 sm:gap-2 transition-all duration-300 hover:scale-110 hover:shadow-glow px-3 sm:px-4 py-1.5 sm:py-2 rounded-full glass-effect">
              <Shield className="h-4 w-4 sm:h-5 sm:w-5 text-pink-600 dark:text-pink-400 animate-pulse-glow" />
              <span className="text-xs sm:text-sm font-medium bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">AI Recommendations</span>
            </div>
            <div className="flex items-center gap-1.5 sm:gap-2 transition-all duration-300 hover:scale-110 hover:shadow-glow px-3 sm:px-4 py-1.5 sm:py-2 rounded-full glass-effect">
              <TrendingUp className="h-4 w-4 sm:h-5 sm:w-5 text-blue-600 dark:text-blue-400 animate-pulse-glow" />
              <span className="text-xs sm:text-sm font-medium bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">Best Value Score</span>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Carousel Section - Responsive */}
      <section className="px-3 sm:px-4 pb-8 sm:pb-12 relative z-10">
        <div className="container mx-auto">
          <h3 className="text-xl sm:text-2xl font-bold text-center mb-4 sm:mb-6 animate-fade-in-up px-2">
            <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">Key Features</span>
          </h3>
          <FeaturedCarousel />
        </div>
      </section>

      {/* Search Section - Responsive */}
      <section className="px-3 sm:px-4 pb-6 sm:pb-8 relative z-10">
        <div className="container mx-auto">
          <SearchForm onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </section>


      {/* Results Section - Responsive */}
      <section className="px-3 sm:px-4 pb-12 sm:pb-16 relative z-10">
        <div className="container mx-auto">
          <ResultsDisplay 
            products={products} 
            isLoading={isLoading}
            priceStats={priceStats}
            aiRecommendation={aiRecommendation}
          />
        </div>
      </section>

      {/* Footer - Responsive */}
      <footer className="border-t glass-effect py-6 sm:py-10 mt-auto relative z-10 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md">
        <div className="container mx-auto px-3 sm:px-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8 text-sm text-neutral-700 dark:text-neutral-300 animate-fade-in-up">
          {/* SmartCart - Column 1 */}
          <div className="text-left">
            <h4 className="font-bold text-base mb-2 text-neutral-900 dark:text-neutral-100">SmartCart</h4>
            <p className="text-neutral-800 dark:text-neutral-100 font-medium text-sm mb-2">A modern price comparison application for everyone.</p>
            <p className="text-neutral-600 dark:text-neutral-300 text-xs sm:text-sm">© 2025 SmartCart. All rights reserved.</p>
          </div>

          {/* Developers - Column 2 */}
          <div className="text-left">
            <h4 className="font-bold text-base mb-2 text-neutral-900 dark:text-neutral-100">Developers</h4>
            <ul className="space-y-2 sm:space-y-3">
              <li className="flex items-center gap-2">
                <span className="inline-flex items-center justify-center h-7 w-7 sm:h-8 sm:w-8 rounded-full bg-gradient-to-br from-green-500 to-blue-500 text-white font-bold text-base sm:text-lg shadow-glow">R</span>
                <span className="font-medium text-neutral-900 dark:text-neutral-100 text-xs sm:text-sm">Rohan Pagadala</span>
                <a href="https://in.linkedin.com/in/rohan-pagadala" target="_blank" rel="noopener noreferrer" className="ml-1 text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 transition-colors" title="LinkedIn">
                  <Linkedin className="h-4 w-4 sm:h-5 sm:w-5" />
                </a>
              </li>
              <li className="flex items-center gap-2">
                <span className="inline-flex items-center justify-center h-7 w-7 sm:h-8 sm:w-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 text-white font-bold text-base sm:text-lg shadow-glow">M</span>
                <span className="font-medium text-neutral-900 dark:text-neutral-100 text-xs sm:text-sm">Manideep Reddy P</span>
                <a href="https://www.linkedin.com/in/patlolla-manideep-reddy-31870827a/?originalSubdomain=in" target="_blank" rel="noopener noreferrer" className="ml-1 text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 transition-colors" title="LinkedIn">
                  <Linkedin className="h-4 w-4 sm:h-5 sm:w-5" />
                </a>
              </li>
              <li className="flex items-center gap-2">
                <span className="inline-flex items-center justify-center h-7 w-7 sm:h-8 sm:w-8 rounded-full bg-gradient-to-br from-yellow-500 to-orange-500 text-white font-bold text-base sm:text-lg shadow-glow">V</span>
                <span className="font-medium text-neutral-900 dark:text-neutral-100 text-xs sm:text-sm">Vineeth V</span>
                <a href="https://www.linkedin.com/in/vineeth-vuppala-331b4935a/?originalSubdomain=in" target="_blank" rel="noopener noreferrer" className="ml-1 text-blue-500 dark:text-blue-400 hover:text-blue-400 dark:hover:text-blue-300 transition-colors" title="LinkedIn">
                  <Linkedin className="h-4 w-4 sm:h-5 sm:w-5" />
                </a>
              </li>
            </ul>
          </div>

          {/* Connect with Us - Column 3 */}
          <div className="text-left">
            <h4 className="font-bold text-base mb-2 text-neutral-900 dark:text-neutral-100">Connect with Us</h4>
            <div className="flex flex-col gap-2 sm:gap-3">
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4 sm:h-5 sm:w-5 text-purple-500 dark:text-purple-400" />
                <span className="font-medium text-neutral-900 dark:text-neutral-100 text-xs sm:text-sm">Email Support</span>
              </div>
              <a href="mailto:miniprojectpricecomparepro@gmail.com" className="text-pink-600 dark:text-pink-400 hover:text-pink-400 dark:hover:text-pink-300 transition-colors font-medium break-all text-xs sm:text-sm" title="Email Support">
                miniprojectpricecomparepro@gmail.com
              </a>
              <p className="text-neutral-600 dark:text-neutral-300 text-xs">Have feedback or need help? We'd love to hear from you!</p>
            </div>
          </div>

          {/* Legal - Column 4 */}
          <div className="text-left">
            <h4 className="font-bold text-base mb-2 text-neutral-900 dark:text-neutral-100">Legal</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors flex items-center gap-2 text-xs sm:text-sm">
                  <span>Terms and Conditions</span>
                </a>
              </li>
              <li>
                <a href="#" className="text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors flex items-center gap-2 text-xs sm:text-sm">
                  <span>Privacy Policy</span>
                </a>
              </li>
              <li>
                <a href="#" className="text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors flex items-center gap-2 text-xs sm:text-sm">
                  <span>Cookie Policy</span>
                </a>
              </li>
              <li>
                <a href="#" className="text-neutral-600 dark:text-neutral-300 hover:text-neutral-900 dark:hover:text-neutral-100 transition-colors flex items-center gap-2 text-xs sm:text-sm">
                  <span>Disclaimer</span>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </footer>
  </div>
  );
};

export default Index;
