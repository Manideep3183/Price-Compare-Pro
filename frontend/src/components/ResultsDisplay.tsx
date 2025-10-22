import React, { useState, useEffect } from 'react';
import { Product } from '@/types/product';
import { Star, Percent, TrendingUp, TrendingDown } from 'lucide-react';
import { AIRecommendation } from './AIRecommendation';
import { ProductCard } from './ProductCard';
import { ProductSkeleton } from './ProductSkeleton';
import { ShoppingBag } from 'lucide-react';
import { ViewMoreButton } from './ViewMoreButton';

export interface ResultsDisplayProps {
  products: { [platform: string]: Product[] };
  isLoading: boolean;
  priceStats?: { low?: number; avg?: number; high?: number };
  aiRecommendation?: string | null;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ products, isLoading, priceStats, aiRecommendation }) => {
  const [expanded, setExpanded] = useState(false);
  const initialCount = 4; // Initial number of products to show

  // Convert products object to array and sort by platform
  const allProducts = Object.values(products).flat().filter(Boolean);
  const platformNames = Object.keys(products).filter(key => products[key]?.length > 0);
  const totalProducts = allProducts.length;
  
  // Reset expanded state whenever products change (new search)
  useEffect(() => {
    setExpanded(false);
  }, [totalProducts]);
  
  const displayedProducts = expanded 
    ? allProducts  // Show all products when expanded
    : allProducts.slice(0, initialCount);  // Show first 4 initially

  const displayedTotal = displayedProducts.length;
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            style={{ animationDelay: `${i * 0.1}s` }}
            className="animate-fade-in"
          >
            <ProductSkeleton />
          </div>
        ))}
      </div>
    );
  }

  if (totalProducts === 0) {
    return (
      <div className="text-center py-12 sm:py-16 px-4 animate-fade-in">
        <div className="animate-float mb-4">
          <ShoppingBag className="h-16 w-16 sm:h-20 sm:w-20 md:h-24 md:w-24 mx-auto text-muted-foreground/30" />
        </div>
        <h3 className="text-xl sm:text-2xl font-semibold mb-2">No Results Yet</h3>
        <p className="text-sm sm:text-base text-muted-foreground max-w-md mx-auto">
          Start by searching for a product above. We'll compare prices across multiple retailers
          and show you the best deals with AI-powered recommendations.
        </p>
      </div>
    );
  }

  // Find best deal across ALL products (not just displayed ones)
  // The best deal is the product with the highest final_score
  // Score is calculated based on: 70% price (lower is better) + 30% rating (higher is better)
  let bestDeal = allProducts[0];
  let maxScore = allProducts[0]?.final_score ?? 0;
  
  allProducts.forEach((p) => {
    const currentScore = p.final_score ?? 0;
    if (currentScore > maxScore) {
      maxScore = currentScore;
      bestDeal = p;
    }
  });

  // Log for debugging
  if (process.env.NODE_ENV === 'development') {
    console.log(`Best Deal: "${bestDeal?.product_name}" with score ${maxScore} from ${allProducts.length} total products`);
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* AI Recommendation at the top */}
      <AIRecommendation products={allProducts} />

      {/* Price Stats Card - Responsive */}
      {(priceStats?.low !== undefined || priceStats?.avg !== undefined || priceStats?.high !== undefined) && (
        <div className="mb-4 sm:mb-6 rounded-xl sm:rounded-2xl glass-effect border-2 border-gradient-to-r from-yellow-400 via-pink-400 to-purple-400 shadow-lg shadow-yellow-200/30 bg-gradient-to-br from-yellow-50 via-pink-50 to-purple-50 px-4 sm:px-6 py-4 sm:py-5 flex flex-col sm:flex-row gap-3 sm:gap-6 items-start sm:items-center animate-fade-in">
          <div className="flex items-center gap-2 sm:gap-3 w-full sm:w-auto">
            <TrendingDown className="h-5 w-5 sm:h-6 sm:w-6 text-green-500 flex-shrink-0" />
            <span className="font-semibold text-sm sm:text-base">Lowest Price:</span>
            <span className="font-bold text-green-500 text-base sm:text-lg ml-auto sm:ml-0">₹{priceStats?.low ?? '-'}</span>
          </div>
          <div className="flex items-center gap-2 sm:gap-3 w-full sm:w-auto">
            <Star className="h-5 w-5 sm:h-6 sm:w-6 text-yellow-500 flex-shrink-0" />
            <span className="font-semibold text-sm sm:text-base">Average Price:</span>
            <span className="font-bold text-yellow-500 text-base sm:text-lg ml-auto sm:ml-0">₹{priceStats?.avg ?? '-'}</span>
          </div>
          <div className="flex items-center gap-2 sm:gap-3 w-full sm:w-auto">
            <TrendingUp className="h-5 w-5 sm:h-6 sm:w-6 text-red-500 flex-shrink-0" />
            <span className="font-semibold text-sm sm:text-base">Highest Price:</span>
            <span className="font-bold text-red-500 text-base sm:text-lg ml-auto sm:ml-0">₹{priceStats?.high ?? '-'}</span>
          </div>
        </div>
      )}

      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 sm:gap-4 px-2">
        <h2 className="text-xl sm:text-2xl md:text-3xl font-bold animate-fade-in-up bg-gradient-primary bg-clip-text text-transparent">
          Showing {displayedTotal} of {totalProducts} {totalProducts === 1 ? 'Product' : 'Products'}
        </h2>
        <p className="text-xs sm:text-sm md:text-base text-muted-foreground">
          From {platformNames.join(', ')} • Sorted by best value
        </p>
      </div>

      <div className="space-y-6 sm:space-y-8">
        {/* Products grid - Responsive */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 sm:gap-6">
          {displayedProducts.map((product, index) => (
            <div
              key={`product-${index}`}
              style={{ animationDelay: `${index * 0.1}s` }}
              className="animate-scale-in"
            >
              <ProductCard 
                product={product} 
                highlighted={product.final_score === maxScore}
              />
            </div>
          ))}
        </div>

        {/* View More Button */}
        {totalProducts > initialCount && (
          <ViewMoreButton
            expanded={expanded}
            onClick={() => setExpanded(!expanded)}
            totalItems={totalProducts}
            currentlyShowing={displayedTotal}
            platform={platformNames.join(', ')}
          />
        )}
      </div>
    </div>
  );
};
