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
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
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
      <div className="text-center py-16 animate-fade-in">
        <div className="animate-float mb-4">
          <ShoppingBag className="h-24 w-24 mx-auto text-muted-foreground/30" />
        </div>
        <h3 className="text-2xl font-semibold mb-2">No Results Yet</h3>
        <p className="text-muted-foreground max-w-md mx-auto">
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
    <div className="space-y-10 animate-fade-in">
      {/* AI Recommendation at the top */}
      <AIRecommendation products={allProducts} />

      {/* Price Stats Card */}
      {(priceStats?.low !== undefined || priceStats?.avg !== undefined || priceStats?.high !== undefined) && (
        <div className="rounded-3xl backdrop-blur-xl bg-gradient-to-br from-card/80 via-card/60 to-card/80 border border-border/50 shadow-2xl px-8 py-6 animate-fade-in">
          <div className="flex flex-col md:flex-row gap-6 items-center justify-around">
            <div className="flex flex-col items-center gap-2 group cursor-default">
              <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-green-500/20 to-emerald-500/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                <TrendingDown className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <span className="text-sm font-medium text-muted-foreground">Lowest Price</span>
              <span className="font-extrabold text-2xl bg-gradient-to-br from-green-600 to-emerald-600 dark:from-green-400 dark:to-emerald-400 bg-clip-text text-transparent">
                ₹{priceStats?.low?.toLocaleString() ?? '-'}
              </span>
            </div>
            <div className="h-12 w-px bg-border/50 hidden md:block"></div>
            <div className="flex flex-col items-center gap-2 group cursor-default">
              <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-amber-500/20 to-yellow-500/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                <Star className="h-6 w-6 text-amber-600 dark:text-amber-400 fill-amber-600 dark:fill-amber-400" />
              </div>
              <span className="text-sm font-medium text-muted-foreground">Average Price</span>
              <span className="font-extrabold text-2xl bg-gradient-to-br from-amber-600 to-yellow-600 dark:from-amber-400 dark:to-yellow-400 bg-clip-text text-transparent">
                ₹{priceStats?.avg?.toLocaleString() ?? '-'}
              </span>
            </div>
            <div className="h-12 w-px bg-border/50 hidden md:block"></div>
            <div className="flex flex-col items-center gap-2 group cursor-default">
              <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-red-500/20 to-rose-500/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                <TrendingUp className="h-6 w-6 text-red-600 dark:text-red-400" />
              </div>
              <span className="text-sm font-medium text-muted-foreground">Highest Price</span>
              <span className="font-extrabold text-2xl bg-gradient-to-br from-red-600 to-rose-600 dark:from-red-400 dark:to-rose-400 bg-clip-text text-transparent">
                ₹{priceStats?.high?.toLocaleString() ?? '-'}
              </span>
            </div>
          </div>
        </div>
      )}

      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 px-2">
        <div>
          <h2 className="text-4xl font-extrabold animate-fade-in-up bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
            {displayedTotal} {totalProducts === 1 ? 'Product' : 'Products'}
          </h2>
          <p className="text-sm text-muted-foreground mt-1">
            {displayedTotal < totalProducts ? `Showing ${displayedTotal} of ${totalProducts}` : 'All results displayed'}
          </p>
        </div>
        <div className="px-4 py-2 rounded-xl bg-muted/50 backdrop-blur-sm border border-border/50">
          <p className="text-sm text-muted-foreground font-medium">
            {platformNames.length} retailers • Sorted by best value
          </p>
        </div>
      </div>

      <div className="space-y-8">
        {/* Products grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {displayedProducts.map((product, index) => (
            <div
              key={`product-${index}`}
              style={{ animationDelay: `${index * 0.05}s` }}
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
          />
        )}
      </div>
    </div>
  );
};
