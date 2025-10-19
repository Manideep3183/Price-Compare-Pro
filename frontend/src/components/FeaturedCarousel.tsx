import { useState, useEffect, useCallback } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import Autoplay from 'embla-carousel-autoplay';
import { ChevronLeft, ChevronRight, Zap, Shield, TrendingUp, Brain, Search, Database } from 'lucide-react';
import { Button } from '@/components/ui/button';

const projectFeatures = [
  {
    title: 'AI-Powered Recommendations',
    description: '70/30 weighted algorithm for best value',
    Icon: Brain,
    gradient: 'from-purple-500 via-purple-600 to-pink-500',
    iconColor: 'text-purple-300',
  },
  {
    title: 'Real-Time Price Scraping',
    description: 'Live data from Amazon & Flipkart',
    Icon: Search,
    gradient: 'from-blue-600 via-blue-700 to-purple-500',
    iconColor: 'text-blue-300',
  },
  {
    title: 'Smart Scoring System',
    description: 'Price & rating analysis combined',
    Icon: TrendingUp,
    gradient: 'from-pink-500 via-pink-600 to-purple-600',
    iconColor: 'text-pink-300',
  },
  {
    title: 'Multi-Platform Search',
    description: 'Compare across multiple retailers',
    Icon: Database,
    gradient: 'from-indigo-500 via-indigo-600 to-purple-500',
    iconColor: 'text-indigo-300',
  },
  {
    title: 'Lightning Fast Results',
    description: 'Concurrent scraping for speed',
    Icon: Zap,
    gradient: 'from-yellow-500 via-orange-500 to-pink-600',
    iconColor: 'text-yellow-300',
  },
  {
    title: 'Secure & Reliable',
    description: 'Built with modern tech stack',
    Icon: Shield,
    gradient: 'from-green-500 via-emerald-600 to-teal-500',
    iconColor: 'text-green-300',
  },
];

export const FeaturedCarousel = () => {
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [emblaRef, emblaApi] = useEmblaCarousel(
    { 
      loop: true,
      align: 'center',
      skipSnaps: false,
      slidesToScroll: 1,
      containScroll: 'trimSnaps',
    },
    [Autoplay({ delay: 5000, stopOnInteraction: false })]
  );

  const scrollPrev = useCallback(() => emblaApi?.scrollPrev(), [emblaApi]);
  const scrollNext = useCallback(() => emblaApi?.scrollNext(), [emblaApi]);

  const onSelect = useCallback(() => {
    if (!emblaApi) return;
    setSelectedIndex(emblaApi.selectedScrollSnap());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    onSelect();
    emblaApi.on('select', onSelect);
    return () => {
      emblaApi.off('select', onSelect);
    };
  }, [emblaApi, onSelect]);

  return (
    <div className="relative w-full max-w-7xl mx-auto animate-fade-in px-4 py-8">
      {/* Progress Dots */}
      <div className="flex justify-center gap-2 mb-6">
        {projectFeatures.map((_, index) => (
          <button
            key={index}
            onClick={() => emblaApi?.scrollTo(index)}
            className={`h-2 rounded-full transition-all duration-300 ${
              index === selectedIndex 
                ? 'w-8 bg-gradient-to-r from-purple-500 to-pink-500' 
                : 'w-2 bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500'
            }`}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>

      <div className="overflow-hidden" ref={emblaRef}>
        <div className="flex">
          {projectFeatures.map((feature, index) => {
            const IconComponent = feature.Icon;
            const isActive = index === selectedIndex;
            
            return (
              <div
                key={index}
                className="flex-[0_0_100%] min-w-0 sm:flex-[0_0_50%] lg:flex-[0_0_33.333%] px-3"
              >
                <div 
                  className={`
                    relative overflow-hidden rounded-2xl p-8 h-64
                    bg-gradient-to-br ${feature.gradient}
                    shadow-2xl
                    transition-all duration-700 ease-out
                    ${isActive 
                      ? 'scale-105 shadow-3xl opacity-100' 
                      : 'scale-95 opacity-75 hover:scale-100 hover:opacity-90'
                    }
                    group cursor-pointer
                    backdrop-blur-xl
                  `}
                  style={{
                    transform: isActive ? 'perspective(1000px) rotateY(0deg)' : 'perspective(1000px) rotateY(-5deg)',
                  }}
                >
                  {/* Animated Background Mesh */}
                  <div className="absolute inset-0 opacity-30">
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(255,255,255,0.1),transparent)]" />
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_20%,rgba(255,255,255,0.15),transparent)]" />
                  </div>

                  {/* Floating Orbs */}
                  <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full blur-3xl animate-pulse" 
                       style={{ animationDuration: '3s' }} />
                  <div className="absolute bottom-0 left-0 w-40 h-40 bg-white/5 rounded-full blur-2xl animate-pulse" 
                       style={{ animationDuration: '4s', animationDelay: '1s' }} />
                  
                  {/* Content Container */}
                  <div className="relative z-10 h-full flex flex-col justify-between">
                    {/* Icon Section */}
                    <div className="flex items-start justify-between mb-4">
                      <div className={`
                        relative bg-white/20 backdrop-blur-md rounded-2xl p-4 
                        group-hover:bg-white/30 group-hover:scale-110 
                        transition-all duration-500 shadow-xl
                        ${isActive ? 'animate-bounce-slow' : ''}
                      `}>
                        <IconComponent className={`h-10 w-10 ${feature.iconColor} drop-shadow-lg`} />
                        {/* Glow effect behind icon */}
                        <div className="absolute inset-0 bg-white/30 rounded-2xl blur-xl -z-10 group-hover:bg-white/50 transition-all duration-500" />
                      </div>
                      
                      {/* Corner Accent */}
                      <div className="flex flex-col gap-1">
                        <div className="w-8 h-1 bg-white/40 rounded-full" />
                        <div className="w-6 h-1 bg-white/30 rounded-full ml-auto" />
                        <div className="w-4 h-1 bg-white/20 rounded-full ml-auto" />
                      </div>
                    </div>
                    
                    {/* Text Content */}
                    <div className="space-y-3">
                      <h3 className={`
                        text-white font-bold text-xl leading-tight 
                        drop-shadow-lg
                        transition-all duration-300
                        ${isActive ? 'translate-x-0' : 'translate-x-1'}
                      `}>
                        {feature.title}
                      </h3>
                      <div className="flex items-center gap-2">
                        <div className="h-0.5 w-12 bg-white/50 rounded-full" />
                      </div>
                      <p className={`
                        text-white/90 text-sm leading-relaxed 
                        drop-shadow-md
                        transition-all duration-300
                        ${isActive ? 'translate-x-0' : 'translate-x-1'}
                      `}>
                        {feature.description}
                      </p>
                    </div>
                  </div>
                  
                  {/* Shimmer Effect on Hover */}
                  <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
                  </div>

                  {/* Border Glow */}
                  <div className={`
                    absolute inset-0 rounded-2xl 
                    transition-opacity duration-500
                    ${isActive ? 'opacity-100' : 'opacity-0'}
                  `}
                       style={{
                         boxShadow: '0 0 30px rgba(255, 255, 255, 0.3) inset',
                       }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Modern Navigation Buttons */}
      <Button
        variant="ghost"
        size="icon"
        className="absolute left-0 top-1/2 -translate-y-1/2 z-20 h-14 w-14 rounded-full bg-white/95 dark:bg-neutral-900/95 backdrop-blur-xl border-2 border-purple-200/50 dark:border-purple-700/50 hover:bg-gradient-to-r hover:from-purple-500 hover:to-pink-500 hover:text-white hover:border-transparent transition-all duration-300 hover:scale-110 shadow-2xl hover:shadow-purple-500/50 group"
        onClick={scrollPrev}
      >
        <ChevronLeft className="h-6 w-6 group-hover:animate-pulse" />
      </Button>
      <Button
        variant="ghost"
        size="icon"
        className="absolute right-0 top-1/2 -translate-y-1/2 z-20 h-14 w-14 rounded-full bg-white/95 dark:bg-neutral-900/95 backdrop-blur-xl border-2 border-purple-200/50 dark:border-purple-700/50 hover:bg-gradient-to-r hover:from-pink-500 hover:to-purple-500 hover:text-white hover:border-transparent transition-all duration-300 hover:scale-110 shadow-2xl hover:shadow-pink-500/50 group"
        onClick={scrollNext}
      >
        <ChevronRight className="h-6 w-6 group-hover:animate-pulse" />
      </Button>
    </div>
  );
};
