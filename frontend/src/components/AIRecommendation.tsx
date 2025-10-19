import { Sparkles, TrendingDown, Clock, CheckCircle, Zap, Star, Award, Brain } from 'lucide-react';
import { Product } from '@/types/product';
import { ProductCard } from './ProductCard';

interface AIRecommendationProps {
  products: Product[];
}

export const AIRecommendation = ({ products }: AIRecommendationProps) => {
  if (products.length === 0) return null;

  // Find best deal (highest final_score)
  const bestDeal = products.reduce((best, current) => 
    current.final_score > best.final_score ? current : best
  , products[0]);

  const prices = products.map(p => p.price);
  const lowestPrice = Math.min(...prices);
  const averagePrice = prices.reduce((sum, price) => sum + price, 0) / prices.length;
  const priceVariance = ((Math.max(...prices) - lowestPrice) / lowestPrice) * 100;

  // Determine buy or wait recommendation
  const shouldBuy = bestDeal.price <= averagePrice * 1.05;
  const priceDifference = bestDeal.price - lowestPrice;
  
  // Generate price drop suggestion
  const estimatedDropMonths = priceVariance > 30 ? 2 : priceVariance > 15 ? 3 : null;

  return (
    <div className="mb-8 relative animate-fade-in">
      {/* Glowing Background Effect */}
      <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-600 rounded-2xl blur-xl opacity-40 animate-pulse-glow"></div>
      
      <div className="relative glass-effect rounded-2xl border-2 border-indigo-500/30 dark:border-indigo-400/30 p-8 shadow-2xl bg-gradient-to-br from-indigo-50/50 via-purple-50/50 to-pink-50/50 dark:from-indigo-950/30 dark:via-purple-950/30 dark:to-pink-950/30">
        {/* Header with AI Badge */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-600 rounded-xl blur-md opacity-75 animate-pulse"></div>
              <div className="relative p-3 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-600 shadow-lg">
                <Brain className="h-8 w-8 text-white animate-pulse" />
              </div>
            </div>
            <div>
              <h3 className="text-2xl font-extrabold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-700 dark:from-indigo-400 dark:via-purple-400 dark:to-pink-500 bg-clip-text text-transparent flex items-center gap-2">
                AI Smart Recommendation
                <Sparkles className="h-6 w-6 text-yellow-500 animate-bounce" />
              </h3>
              <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                <Zap className="h-3 w-3 text-indigo-600 dark:text-indigo-400" />
                Powered by Advanced Price Analysis
              </p>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-indigo-500/20 to-purple-500/20 border border-indigo-500/30">
            <Award className="h-4 w-4 text-indigo-600 dark:text-indigo-400" />
            <span className="text-xs font-semibold text-indigo-700 dark:text-indigo-300">Best Value</span>
          </div>
        </div>

        <div className="space-y-6">
          {/* Best Deal Card - Enhanced */}
          <div className="relative group">
            <div className="absolute -inset-2 bg-gradient-to-r from-indigo-400 via-purple-500 to-pink-600 rounded-3xl opacity-30 blur-xl group-hover:opacity-50 transition-all duration-500"></div>
            
            <div className="relative p-6 rounded-2xl bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 dark:from-indigo-950/40 dark:via-purple-950/40 dark:to-pink-950/40 border-2 border-indigo-400/50 dark:border-indigo-500/50 shadow-2xl shadow-indigo-500/20">
              
              <div className="flex flex-col md:flex-row gap-6 items-start md:items-center">
                {/* Product Card Preview */}
                <div className="w-full md:w-72 transform transition-all duration-300 hover:scale-105">
                  <ProductCard product={bestDeal} highlighted={true} hideRecommendationBadge={true} />
                </div>

                {/* Deal Insights */}
                <div className="flex-1 space-y-4">
                  <div className="flex items-start gap-3 p-4 rounded-xl bg-white/60 dark:bg-black/30 border border-indigo-300/50 dark:border-indigo-600/50 backdrop-blur-sm">
                    <div className="p-2 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600">
                      <CheckCircle className="h-5 w-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <p className="font-bold text-indigo-700 dark:text-indigo-400 mb-1">Perfect Match Score</p>
                      <p className="text-sm text-muted-foreground">
                        This product scored{' '}
                        <span className="font-bold text-indigo-600 dark:text-indigo-400">
                          {((bestDeal.final_score || 0) * 100).toFixed(1)}%
                        </span>
                        {' '}on our AI evaluation combining price and quality metrics.
                      </p>
                    </div>
                  </div>

                  {priceDifference === 0 && (
                    <div className="flex items-start gap-3 p-4 rounded-xl bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/30">
                      <TrendingDown className="h-5 w-5 text-indigo-600 dark:text-indigo-400 mt-0.5" />
                      <div>
                        <p className="font-bold text-indigo-700 dark:text-indigo-400 text-sm mb-1">
                          🎯 Lowest Price Guaranteed!
                        </p>
                        <p className="text-sm text-muted-foreground">
                          This is the absolute lowest price across all retailers. Act now!
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Buy or Wait Recommendation */}
          <div className={`relative overflow-hidden rounded-2xl border-2 transition-all duration-300 hover:scale-[1.02] ${
            shouldBuy 
              ? 'bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 border-green-500/40 shadow-lg shadow-green-500/20' 
              : 'bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-950/30 dark:to-orange-950/30 border-amber-500/40 shadow-lg shadow-amber-500/20'
          }`}>
            <div className="absolute top-0 right-0 w-32 h-32 opacity-10">
              {shouldBuy ? (
                <CheckCircle className="w-full h-full text-green-500" />
              ) : (
                <Clock className="w-full h-full text-amber-500" />
              )}
            </div>
            
            <div className="relative flex items-start gap-4 p-6">
              <div className={`p-3 rounded-xl shadow-lg ${
                shouldBuy 
                  ? 'bg-gradient-to-br from-green-500 to-emerald-600' 
                  : 'bg-gradient-to-br from-amber-500 to-orange-600'
              }`}>
                {shouldBuy ? (
                  <CheckCircle className="h-6 w-6 text-white" />
                ) : (
                  <Clock className="h-6 w-6 text-white" />
                )}
              </div>
              <div className="flex-1">
                <p className={`font-bold text-lg mb-2 ${
                  shouldBuy ? 'text-green-700 dark:text-green-400' : 'text-amber-700 dark:text-amber-400'
                }`}>
                  {shouldBuy ? '✅ Buy Now - Excellent Deal!' : '⏳ Consider Waiting'}
                </p>
                <p className="text-sm leading-relaxed">
                  {shouldBuy ? (
                    <>
                      This is an <span className="font-bold">excellent time to buy</span>! The recommended product is priced{' '}
                      <span className="font-bold text-green-600 dark:text-green-400">
                        at or below market average
                      </span>
                      {priceDifference === 0 && (
                        <span className="font-bold text-green-600 dark:text-green-400">
                          {' '}and matches the lowest price available
                        </span>
                      )}.
                    </>
                  ) : (
                    <>
                      The current best deal is{' '}
                      <span className="font-bold text-amber-600 dark:text-amber-400">
                        ₹{priceDifference.toLocaleString()}
                      </span>
                      {' '}above the lowest price. Consider waiting for a better deal or setting a price alert.
                    </>
                  )}
                </p>
              </div>
            </div>
          </div>

          {/* Price Drop Forecast */}
          {estimatedDropMonths && !shouldBuy && (
            <div className="relative overflow-hidden rounded-2xl border-2 border-blue-500/40 bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-950/30 dark:to-cyan-950/30 shadow-lg shadow-blue-500/20 transition-all duration-300 hover:scale-[1.02]">
              <div className="absolute top-0 right-0 w-32 h-32 opacity-10">
                <TrendingDown className="w-full h-full text-blue-500" />
              </div>
              
              <div className="relative flex items-start gap-4 p-6">
                <div className="p-3 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 shadow-lg">
                  <TrendingDown className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <p className="font-bold text-lg text-blue-700 dark:text-blue-400 mb-2">
                    📊 Price Drop Forecast
                  </p>
                  <p className="text-sm leading-relaxed mb-3">
                    Based on{' '}
                    <span className="font-bold text-blue-600 dark:text-blue-400">
                      {priceVariance.toFixed(0)}% price variance
                    </span>
                    {' '}across retailers, an estimated price drop of{' '}
                    <span className="font-bold text-blue-600 dark:text-blue-400">10-15%</span>
                    {' '}may occur within the next{' '}
                    <span className="font-bold text-lg text-blue-700 dark:text-blue-400">
                      {estimatedDropMonths} months
                    </span>.
                  </p>
                  <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-100 dark:bg-blue-900/50 border border-blue-300 dark:border-blue-700">
                    <Sparkles className="h-3 w-3 text-blue-600" />
                    <span className="text-xs font-semibold text-blue-700 dark:text-blue-300">
                      Consider setting a price alert or checking back later
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
