import { Product } from '@/types/product';

// Base URLs for Amazon and Flipkart
export const AMAZON_BASE_URL = "https://www.amazon.in/";
export const FLIPKART_BASE_URL = "https://www.flipkart.com/";
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Star, ExternalLink } from 'lucide-react';

interface ProductCardProps {
  product: Product;
  highlighted?: boolean;
  hideRecommendationBadge?: boolean;  // New prop to hide the recommendation badge
}

const getRecommendationVariant = (recommendation: string): 'default' | 'secondary' | 'outline' => {
  if (recommendation.includes('Excellent')) return 'default';
  if (recommendation.includes('Good')) return 'secondary';
  return 'outline';
};

const getRecommendationColor = (recommendation: string): string => {
  if (recommendation.includes('Excellent')) return 'bg-accent text-accent-foreground';
  if (recommendation.includes('Good')) return 'bg-primary text-primary-foreground';
  return 'bg-warning text-warning-foreground';
};

export const ProductCard = ({ product, highlighted, hideRecommendationBadge = false }: ProductCardProps) => {
  return (
    <Card className={`overflow-hidden transition-all duration-500 hover:shadow-glow group animate-scale-in relative ${
      highlighted
        ? 'border-4 border-fuchsia-400 shadow-2xl shadow-fuchsia-400/50 scale-105 ring-4 ring-pink-300/30 bg-gradient-to-br from-fuchsia-50 via-pink-50 to-rose-50 dark:from-fuchsia-950/30 dark:via-pink-950/30 dark:to-rose-950/30'
        : 'glass-effect border-primary/20'
    }`} style={{ maxWidth: '300px', minWidth: '260px' }}>
      
      {/* Floating BEST DEAL Badge - Enhanced with Fuchsia/Pink theme */}
      {highlighted && (
        <>
          {/* Animated Glow Effect */}
          <div className="absolute -inset-1 bg-gradient-to-r from-fuchsia-400 via-pink-400 to-rose-500 rounded-lg blur-md opacity-60 animate-pulse z-0"></div>
          
          {/* Main Badge */}
          <div className="absolute -top-3 -left-3 z-30 transform rotate-[-12deg] animate-bounce-slow">
            <div className="relative">
              {/* Badge Glow */}
              <div className="absolute inset-0 bg-gradient-to-r from-fuchsia-400 via-pink-400 to-rose-500 rounded-full blur-lg opacity-75 scale-110"></div>
              
              {/* Badge Content */}
              <div className="relative bg-gradient-to-r from-fuchsia-500 via-pink-500 to-rose-600 text-white px-4 py-2 rounded-full shadow-2xl border-2 border-white/50 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white animate-spin-slow" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                <span className="font-black text-sm tracking-wide uppercase">Best Deal</span>
              </div>
            </div>
          </div>
        </>
      )}

      <CardHeader className="p-0 relative z-10">
        <div className="relative aspect-[4/5] overflow-hidden bg-gradient-card" style={{ height: '180px' }}>
          <div className="absolute inset-0 bg-gradient-primary opacity-0 group-hover:opacity-20 transition-opacity duration-500" />
          <img
            src={product.image_url || '/placeholder.svg'}
            alt={product.product_name}
            className="object-cover w-full h-full transition-all duration-700 group-hover:scale-105 group-hover:rotate-1"
            style={{ objectFit: 'cover', width: '100%', height: '100%' }}
          />
          {!hideRecommendationBadge && (
            <Badge 
              className={`absolute top-2 right-2 ${getRecommendationColor(product.recommendation)} font-semibold shadow-md text-xs px-2 py-1 ${highlighted ? 'ring-2 ring-white' : ''}`}
            >
              {product.recommendation}
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="p-2 relative z-10">
        <div className="space-y-3">
          <h3 className={`font-semibold text-lg line-clamp-2 min-h-[3rem] ${highlighted ? 'text-pink-900 dark:text-pink-100 font-bold' : ''}`}>
            {product.product_name}
          </h3>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className={`text-sm px-2.5 py-0.5 ${highlighted ? 'border-cyan-500 bg-cyan-50 dark:bg-cyan-900/30 font-semibold text-cyan-700 dark:text-cyan-300' : ''}`}>
              {product.retailer}
            </Badge>
            <div className="flex items-center gap-1.5">
              <Star className={`h-4 w-4 fill-yellow-500 text-yellow-500`} />
              <span className={`text-sm font-medium ${highlighted ? 'font-bold text-amber-600 dark:text-amber-400' : ''}`}>
                {product.rating?.toFixed(1)}
              </span>
            </div>
          </div>
          <div className="flex items-baseline gap-2">
            <span className={`text-2xl font-bold ${highlighted ? 'text-pink-900 dark:text-pink-100 text-3xl' : 'text-primary'}`}>
              ₹{product.price.toLocaleString()}
            </span>
          </div>
        </div>
      </CardContent>
      <CardFooter className="p-4 pt-0 relative z-10">
        <Button 
          asChild 
          className={`w-full transition-all duration-300 hover:scale-105 text-sm py-2 ${
            highlighted 
              ? 'bg-gradient-to-r from-fuchsia-500 via-pink-500 to-rose-600 hover:from-fuchsia-600 hover:via-pink-600 hover:to-rose-700 text-white font-bold shadow-lg shadow-fuchsia-500/50' 
              : 'bg-gradient-primary hover:opacity-90'
          }`}
        >
          <a 
            href={product.product_url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2"
          >
            View on {product.retailer}
            <ExternalLink className="h-4 w-4" />
          </a>
        </Button>
      </CardFooter>
    </Card>
  );
};
