import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { RetailerLinks } from '@/components/RetailerLinks';
import { Search, MapPin } from 'lucide-react';

interface SearchFormProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
}

export const SearchForm = ({ onSearch, isLoading }: SearchFormProps) => {
  const [query, setQuery] = useState('');
  const [lastSearchedQuery, setLastSearchedQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
      setLastSearchedQuery(query.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-4xl mx-auto animate-fade-in-up">
      <div className="flex flex-col gap-6">
        {/* Glowing Background Effect for Search Container */}
        <div className="relative">
          <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 rounded-2xl blur-xl opacity-20 dark:opacity-30 animate-pulse-glow pointer-events-none"></div>
          
          <div className="relative glass-effect rounded-2xl p-6 border-2 border-purple-500/20 dark:border-purple-500/30 shadow-2xl bg-gradient-to-br from-purple-50/30 via-pink-50/30 to-blue-50/30 dark:from-purple-950/20 dark:via-pink-950/20 dark:to-blue-950/20">
            {/* Location Info */}
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="p-1.5 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500">
                <MapPin className="h-3.5 w-3.5 text-white" />
              </div>
              <span className="text-sm font-semibold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                Searching in India (INR Prices)
              </span>
            </div>

            {/* Search Input */}
            <div className="flex gap-3">
              <div className="relative flex-1 group">
                {/* Input Glow Effect */}
                <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 rounded-xl opacity-0 group-focus-within:opacity-30 blur transition-opacity duration-300"></div>
                
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground transition-all duration-300 group-focus-within:text-purple-600 dark:group-focus-within:text-purple-400 group-focus-within:scale-110" />
                  <Input
                    type="text"
                    placeholder="Search for products (e.g., laptop, headphones, camera)..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    className="pl-12 h-14 text-base shadow-lg transition-all duration-300 focus:shadow-2xl focus:scale-[1.01] border-2 border-purple-200/50 dark:border-purple-700/50 focus:border-purple-500 dark:focus:border-purple-400 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-xl font-medium"
                    disabled={isLoading}
                  />
                </div>
              </div>
              <Button
                type="submit"
                disabled={isLoading || !query.trim()}
                className="h-14 px-8 bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 hover:from-purple-700 hover:via-pink-700 hover:to-blue-700 transition-all duration-300 shadow-lg hover:shadow-2xl hover:shadow-purple-500/50 hover:scale-105 disabled:hover:scale-100 disabled:opacity-50 text-white font-bold rounded-xl"
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    Searching...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <Search className="h-5 w-5" />
                    Compare Prices
                  </span>
                )}
              </Button>
            </div>
          </div>
        </div>
        
        {/* Retailer Links - Show after search */}
        {lastSearchedQuery && (
          <RetailerLinks searchQuery={lastSearchedQuery} />
        )}
      </div>
    </form>
  );
};
