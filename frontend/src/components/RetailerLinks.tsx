import { ExternalLink } from 'lucide-react';

interface RetailerLinksProps {
  searchQuery: string;
}

interface Retailer {
  name: string;
  logo: string;
  searchUrl: string;
  primaryColor: string;
}

const retailers: Retailer[] = [
  {
    name: 'Amazon',
    logo: 'https://cdn.worldvectorlogo.com/logos/amazon-icon-1.svg',
    searchUrl: 'https://www.amazon.in/s?k=',
    primaryColor: 'from-orange-500 to-yellow-500'
  },
  {
    name: 'Flipkart',
    logo: 'https://static-assets-web.flixcart.com/batman-returns/batman-returns/p/images/fkheaderlogo_exploreplus-44005d.svg',
    searchUrl: 'https://www.flipkart.com/search?q=',
    primaryColor: 'from-blue-500 to-indigo-500'
  },
  {
    name: 'Croma',
    logo: 'https://www.croma.com/assets/logo/logo.svg',
    searchUrl: 'https://www.croma.com/searchB?q=',
    primaryColor: 'from-green-500 to-emerald-500'
  },
  {
    name: 'JioMart',
    logo: 'https://www.jiomart.com/images/jiomart-logo.svg',
    searchUrl: 'https://www.jiomart.com/search/',
    primaryColor: 'from-blue-600 to-purple-600'
  },
  {
    name: 'Tata CLiQ',
    logo: 'https://www.tatacliq.com/src/general/components/img/logo.svg',
    searchUrl: 'https://www.tatacliq.com/search/?searchCategory=all&text=',
    primaryColor: 'from-indigo-500 to-blue-500'
  },
  {
    name: 'Reliance Digital',
    logo: 'https://www.reliancedigital.in/build/client/images/loaders/rd_logo.svg',
    searchUrl: 'https://www.reliancedigital.in/products?q=',
    primaryColor: 'from-purple-500 to-pink-500'
  },
  {
    name: 'Myntra',
    logo: 'https://constant.myntassets.com/web/assets/img/icon.e8734479.png',
    searchUrl: 'https://www.myntra.com/search/',
    primaryColor: 'from-pink-500 to-red-500'
  },
  {
    name: 'Nykaa',
    logo: 'https://www.nykaa.com/assets/desktop/images/nykaa-logo.svg',
    searchUrl: 'https://www.nykaa.com/search/result/?q=',
    primaryColor: 'from-pink-400 to-rose-400'
  }
];

export const RetailerLinks = ({ searchQuery }: RetailerLinksProps) => {
  if (!searchQuery.trim()) {
    return null;
  }

  const encodedQuery = encodeURIComponent(searchQuery.trim());

  // Special URL construction for Croma
  const getRetailerUrl = (retailer: Retailer) => {
    if (retailer.name === 'Croma') {
      // Croma requires: q=query:relevance&text=query
      return `${retailer.searchUrl}${encodedQuery}%3Arelevance&text=${encodedQuery}`;
    }
    return `${retailer.searchUrl}${encodedQuery}`;
  };

  return (
    <div className="w-full max-w-4xl mx-auto mt-6 animate-fade-in-up">
      <div className="text-center mb-4">
        <h3 className="text-lg font-semibold text-foreground/80 mb-2">
          Search directly on your favorite retailers:
        </h3>
        <p className="text-sm text-muted-foreground">
          Compare prices across multiple platforms for "{searchQuery}"
        </p>
      </div>
      
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-3">
        {retailers.map((retailer) => (
          <a
            key={retailer.name}
            href={getRetailerUrl(retailer)}
            target="_blank"
            rel="noopener noreferrer"
            className={`
              group relative overflow-hidden rounded-xl p-4 
              bg-gradient-to-br ${retailer.primaryColor} 
              hover:scale-105 transform transition-all duration-300 
              shadow-md hover:shadow-xl active:scale-95
              text-white font-medium text-center
              focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary
            `}
          >
            {/* Background pattern */}
            <div className="absolute inset-0 bg-white/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            
            {/* Content */}
            <div className="relative z-10 flex flex-col items-center gap-2">
              <div className="w-12 h-12 flex items-center justify-center bg-white rounded-lg p-1.5 shadow-md">
                <img 
                  src={retailer.logo} 
                  alt={`${retailer.name} logo`}
                  className="w-full h-full object-contain"
                  onError={(e) => {
                    // Fallback to text if image fails to load
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    target.parentElement!.innerHTML = `<span class="text-2xl font-bold text-gray-700">${retailer.name.charAt(0)}</span>`;
                  }}
                />
              </div>
              <div className="text-sm font-semibold truncate w-full">
                {retailer.name}
              </div>
              <ExternalLink className="h-3 w-3 opacity-70 group-hover:opacity-100 transition-opacity" />
            </div>
            
            {/* Hover effect overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          </a>
        ))}
      </div>
      
      <div className="text-center mt-4">
        <p className="text-xs text-muted-foreground">
          💡 Tip: Click any retailer above to search for "{searchQuery}" directly on their website
        </p>
      </div>
    </div>
  );
};
