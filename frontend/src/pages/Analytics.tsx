import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserSearches, getUserActivity, checkUserExists, createOrUpdateUserProfile } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ThemeToggle } from '@/components/ThemeToggle';
import { UserProfileDropdown } from '@/components/UserProfileDropdown';
import {
  BarChart3,
  TrendingUp,
  Search,
  MousePointer,
  ExternalLink,
  Eye,
  ArrowLeft,
  Calendar,
  ShoppingBag,
  Activity as ActivityIcon,
} from 'lucide-react';

interface SearchHistory {
  id: string;
  query: string;
  results_count: number;
  created_at: string;
}

interface ActivityEvent {
  id: string;
  event: string;
  payload: Record<string, any>;
  created_at: string;
}

const Analytics = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { toast } = useToast();
  const [searches, setSearches] = useState<SearchHistory[]>([]);
  const [activities, setActivities] = useState<ActivityEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    const fetchData = async () => {
      try {
        // Ensure user profile exists first (handles both new and existing users)
        try {
          await createOrUpdateUserProfile({
            auth_provider: user.providerData?.[0]?.providerId === 'google.com' ? 'google' : 'email',
          });
          console.log('✅ User profile ensured in MongoDB');
        } catch (profileError) {
          console.error('⚠️ Failed to ensure user profile:', profileError);
          // Non-critical, continue
        }

        const [searchData, activityData] = await Promise.all([
          getUserSearches(50),
          getUserActivity(100),
        ]);

        setSearches(searchData || []);
        setActivities(activityData || []);
      } catch (error) {
        console.error('Failed to fetch analytics data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, navigate, logout, toast]);

  // Calculate statistics
  const getActivityStats = () => {
    const productClicks = activities.filter(a => a.event === 'clicked_product').length;
    const retailerClicks = activities.filter(a => a.event === 'clicked_retailer_link').length;
    const viewMoreExpansions = activities.filter(a => a.event === 'expanded_view_more').length;
    
    const totalResults = searches.reduce((sum, s) => sum + s.results_count, 0);
    const avgResults = searches.length > 0 ? Math.round(totalResults / searches.length) : 0;

    return {
      productClicks,
      retailerClicks,
      viewMoreExpansions,
      totalResults,
      avgResults,
    };
  };

  const stats = getActivityStats();

  // Get most clicked retailers
  const getTopRetailers = () => {
    const retailerCounts: Record<string, number> = {};
    
    activities
      .filter(a => a.event === 'clicked_retailer_link' || a.event === 'clicked_product')
      .forEach(activity => {
        const retailer = activity.payload.retailer;
        if (retailer) {
          retailerCounts[retailer] = (retailerCounts[retailer] || 0) + 1;
        }
      });

    return Object.entries(retailerCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([retailer, count]) => ({ retailer, count }));
  };

  // Get most searched terms
  const getTopSearches = () => {
    const searchCounts: Record<string, number> = {};
    
    searches.forEach(search => {
      const query = search.query.toLowerCase();
      searchCounts[query] = (searchCounts[query] || 0) + 1;
    });

    return Object.entries(searchCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([query, count]) => ({ query, count }));
  };

  const topRetailers = getTopRetailers();
  const topSearches = getTopSearches();

  const formatDate = (dateString: string) => {
    // Parse the date string (which is in UTC or ISO format from backend)
    const date = new Date(dateString);
    
    // Convert to IST (Indian Standard Time - UTC+5:30)
    // Use toLocaleString with Asia/Kolkata timezone
    return date.toLocaleString('en-IN', {
      timeZone: 'Asia/Kolkata',
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true, // Use 12-hour format with AM/PM
    });
  };

  const getEventIcon = (event: string) => {
    switch (event) {
      case 'clicked_product':
        return <MousePointer className="h-4 w-4" />;
      case 'clicked_retailer_link':
        return <ExternalLink className="h-4 w-4" />;
      case 'expanded_view_more':
        return <Eye className="h-4 w-4" />;
      default:
        return <ActivityIcon className="h-4 w-4" />;
    }
  };

  const getEventColor = (event: string) => {
    switch (event) {
      case 'clicked_product':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'clicked_retailer_link':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'expanded_view_more':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-slate-900 dark:via-purple-900 dark:to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-t-4 border-purple-600 mx-auto mb-4"></div>
            <div className="absolute inset-0 animate-ping rounded-full h-16 w-16 border border-pink-400 opacity-20"></div>
          </div>
          <p className="text-lg font-medium bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
            Loading analytics...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-slate-900 dark:via-purple-900 dark:to-slate-900">
      {/* Header - Responsive */}
      <header className="glass-effect border-b border-purple-200/30 dark:border-purple-500/20 sticky top-0 z-50 backdrop-blur-xl bg-white/50 dark:bg-slate-900/50">
        <div className="container mx-auto px-3 sm:px-4 py-3 sm:py-4">
          <div className="flex items-center justify-between gap-2">
            {/* Left Section */}
            <div className="flex items-center gap-2 sm:gap-4 min-w-0 flex-1">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => navigate('/')}
                className="hover:bg-purple-100 dark:hover:bg-purple-900/30 transition-all duration-300 hover:scale-110 flex-shrink-0"
              >
                <ArrowLeft className="h-4 w-4 sm:h-5 sm:w-5 text-purple-600 dark:text-purple-400" />
              </Button>
              <div className="flex items-center gap-2 sm:gap-3 min-w-0">
                <div className="relative flex-shrink-0">
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 rounded-xl blur-lg opacity-50 animate-pulse"></div>
                  <div className="relative bg-gradient-to-r from-purple-500 via-pink-500 to-blue-500 p-1.5 sm:p-2.5 rounded-xl">
                    <BarChart3 className="h-4 w-4 sm:h-6 sm:w-6 text-white" />
                  </div>
                </div>
                <div className="min-w-0">
                  <h1 className="text-base sm:text-xl md:text-2xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent truncate">
                    Analytics Dashboard
                  </h1>
                  <p className="text-[10px] sm:text-xs text-muted-foreground hidden sm:block">Track your shopping insights</p>
                </div>
              </div>
            </div>
            {/* Right Section */}
            <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
              <ThemeToggle />
              <UserProfileDropdown />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content - Responsive */}
      <main className="container mx-auto px-3 sm:px-4 py-6 sm:py-8">
        {/* Overview Stats - Responsive Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6 mb-6 sm:mb-8">
          <Card className="glass-effect border-purple-200/30 dark:border-purple-500/20 hover:shadow-xl hover:shadow-purple-500/10 transition-all duration-300 hover:scale-105 group overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 via-pink-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Searches</CardTitle>
              <div className="p-2 bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900/30 dark:to-pink-900/30 rounded-lg">
                <Search className="h-4 w-4 text-purple-600 dark:text-purple-400" />
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                {searches.length}
              </div>
              <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                Avg {stats.avgResults} results per search
              </p>
            </CardContent>
          </Card>

          <Card className="glass-effect border-blue-200/30 dark:border-blue-500/20 hover:shadow-xl hover:shadow-blue-500/10 transition-all duration-300 hover:scale-105 group overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 via-cyan-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
              <CardTitle className="text-sm font-medium text-muted-foreground">Product Clicks</CardTitle>
              <div className="p-2 bg-gradient-to-br from-blue-100 to-cyan-100 dark:from-blue-900/30 dark:to-cyan-900/30 rounded-lg">
                <MousePointer className="h-4 w-4 text-blue-600 dark:text-blue-400" />
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">
                {stats.productClicks}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Products you explored
              </p>
            </CardContent>
          </Card>

          <Card className="glass-effect border-green-200/30 dark:border-green-500/20 hover:shadow-xl hover:shadow-green-500/10 transition-all duration-300 hover:scale-105 group overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-green-500/5 via-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
              <CardTitle className="text-sm font-medium text-muted-foreground">Retailer Visits</CardTitle>
              <div className="p-2 bg-gradient-to-br from-green-100 to-emerald-100 dark:from-green-900/30 dark:to-emerald-900/30 rounded-lg">
                <ExternalLink className="h-4 w-4 text-green-600 dark:text-green-400" />
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-3xl font-bold text-green-600 dark:text-green-400">
                {stats.retailerClicks}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Links you followed
              </p>
            </CardContent>
          </Card>

          <Card className="glass-effect border-pink-200/30 dark:border-pink-500/20 hover:shadow-xl hover:shadow-pink-500/10 transition-all duration-300 hover:scale-105 group overflow-hidden relative">
            <div className="absolute inset-0 bg-gradient-to-br from-pink-500/5 via-rose-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
              <CardTitle className="text-sm font-medium text-muted-foreground">View More</CardTitle>
              <div className="p-2 bg-gradient-to-br from-pink-100 to-rose-100 dark:from-pink-900/30 dark:to-rose-900/30 rounded-lg">
                <Eye className="h-4 w-4 text-pink-600 dark:text-pink-400" />
              </div>
            </CardHeader>
            <CardContent className="relative z-10">
              <div className="text-3xl font-bold text-pink-600 dark:text-pink-400">
                {stats.viewMoreExpansions}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Times expanded results
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Tabs for detailed views */}
        <Tabs defaultValue="searches" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 glass-effect border border-purple-200/30 dark:border-purple-500/20 p-1 bg-white/50 dark:bg-slate-900/50">
            <TabsTrigger 
              value="searches"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-500 data-[state=active]:via-pink-500 data-[state=active]:to-blue-500 data-[state=active]:text-white transition-all duration-300"
            >
              Search History
            </TabsTrigger>
            <TabsTrigger 
              value="activity"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-500 data-[state=active]:via-pink-500 data-[state=active]:to-blue-500 data-[state=active]:text-white transition-all duration-300"
            >
              Activity Log
            </TabsTrigger>
            <TabsTrigger 
              value="insights"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-purple-500 data-[state=active]:via-pink-500 data-[state=active]:to-blue-500 data-[state=active]:text-white transition-all duration-300"
            >
              Insights
            </TabsTrigger>
          </TabsList>

          {/* Search History Tab */}
          <TabsContent value="searches" className="space-y-4">
            <Card className="glass-effect border-purple-200/30 dark:border-purple-500/20 hover:shadow-xl transition-all duration-300">
              <CardHeader className="border-b border-purple-100 dark:border-purple-900/30 bg-gradient-to-r from-purple-50/50 via-pink-50/50 to-blue-50/50 dark:from-purple-900/10 dark:via-pink-900/10 dark:to-blue-900/10">
                <CardTitle className="flex items-center gap-2">
                  <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg">
                    <Search className="h-5 w-5 text-white" />
                  </div>
                  <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                    Recent Searches
                  </span>
                </CardTitle>
                <CardDescription>
                  Your search history and results
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <div className="space-y-3">
                  {searches.length === 0 ? (
                    <div className="text-center py-12">
                      <div className="inline-flex p-4 bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900/30 dark:to-pink-900/30 rounded-full mb-4">
                        <Search className="h-8 w-8 text-purple-500" />
                      </div>
                      <p className="text-muted-foreground">
                        No search history yet. Start searching to see your activity here!
                      </p>
                    </div>
                  ) : (
                    searches.slice(0, 20).map((search) => (
                      <div
                        key={search.id}
                        className="flex items-center justify-between p-4 rounded-xl bg-gradient-to-r from-purple-50/50 via-pink-50/50 to-blue-50/50 dark:from-purple-900/10 dark:via-pink-900/10 dark:to-blue-900/10 hover:from-purple-100/50 hover:via-pink-100/50 hover:to-blue-100/50 dark:hover:from-purple-900/20 dark:hover:via-pink-900/20 dark:hover:to-blue-900/20 transition-all duration-300 border border-purple-100/50 dark:border-purple-800/30 hover:scale-102"
                      >
                        <div className="flex-1">
                          <p className="font-medium text-foreground">{search.query}</p>
                          <p className="text-sm text-muted-foreground flex items-center gap-2">
                            <span className="inline-flex items-center gap-1">
                              <ShoppingBag className="h-3 w-3" />
                              {search.results_count} results
                            </span>
                            <span>•</span>
                            <span className="inline-flex items-center gap-1">
                              <Calendar className="h-3 w-3" />
                              {formatDate(search.created_at)}
                            </span>
                          </p>
                        </div>
                        <Badge 
                          variant="outline" 
                          className="bg-gradient-to-r from-purple-500 to-pink-500 text-white border-0"
                        >
                          {search.results_count}
                        </Badge>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Activity Log Tab */}
          <TabsContent value="activity" className="space-y-4">
            <Card className="glass-effect border-blue-200/30 dark:border-blue-500/20 hover:shadow-xl transition-all duration-300">
              <CardHeader className="border-b border-blue-100 dark:border-blue-900/30 bg-gradient-to-r from-blue-50/50 via-cyan-50/50 to-purple-50/50 dark:from-blue-900/10 dark:via-cyan-900/10 dark:to-purple-900/10">
                <CardTitle className="flex items-center gap-2">
                  <div className="p-2 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg">
                    <ActivityIcon className="h-5 w-5 text-white" />
                  </div>
                  <span className="bg-gradient-to-r from-blue-600 via-cyan-600 to-purple-600 bg-clip-text text-transparent">
                    Activity Timeline
                  </span>
                </CardTitle>
                <CardDescription>
                  All your interactions and events
                </CardDescription>
              </CardHeader>
              <CardContent className="pt-6">
                <div className="space-y-3">
                  {activities.length === 0 ? (
                    <div className="text-center py-12">
                      <div className="inline-flex p-4 bg-gradient-to-br from-blue-100 to-cyan-100 dark:from-blue-900/30 dark:to-cyan-900/30 rounded-full mb-4">
                        <ActivityIcon className="h-8 w-8 text-blue-500" />
                      </div>
                      <p className="text-muted-foreground">
                        No activity recorded yet. Interact with products to see your activity here!
                      </p>
                    </div>
                  ) : (
                    activities.slice(0, 50).map((activity) => (
                      <div
                        key={activity.id}
                        className="flex items-start gap-4 p-4 rounded-xl bg-gradient-to-r from-blue-50/30 via-cyan-50/30 to-purple-50/30 dark:from-blue-900/10 dark:via-cyan-900/10 dark:to-purple-900/10 hover:from-blue-100/50 hover:via-cyan-100/50 hover:to-purple-100/50 dark:hover:from-blue-900/20 dark:hover:via-cyan-900/20 dark:hover:to-purple-900/20 transition-all duration-300 border border-blue-100/50 dark:border-blue-800/30"
                      >
                        <div className={`p-2.5 rounded-full ${getEventColor(activity.event)} shadow-lg`}>
                          {getEventIcon(activity.event)}
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2 flex-wrap">
                            <Badge className={`${getEventColor(activity.event)} border-0 shadow-sm`}>
                              {activity.event.replace(/_/g, ' ')}
                            </Badge>
                            <span className="text-xs text-muted-foreground flex items-center gap-1">
                              <Calendar className="h-3 w-3" />
                              {formatDate(activity.created_at)}
                            </span>
                          </div>
                          {activity.payload.product_name && (
                            <p className="text-sm font-medium text-foreground mb-1">
                              {activity.payload.product_name}
                            </p>
                          )}
                          {activity.payload.retailer && (
                            <p className="text-xs text-muted-foreground flex items-center gap-2">
                              <span className="capitalize">{activity.payload.retailer}</span>
                              {activity.payload.price && (
                                <>
                                  <span>•</span>
                                  <span className="font-semibold">₹{activity.payload.price.toLocaleString()}</span>
                                </>
                              )}
                            </p>
                          )}
                          {activity.payload.platform && (
                            <p className="text-xs text-muted-foreground mt-1">
                              Platform: {activity.payload.platform}
                            </p>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Insights Tab */}
          <TabsContent value="insights" className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Top Searches */}
              <Card className="glass-effect border-pink-200/30 dark:border-pink-500/20 hover:shadow-xl transition-all duration-300">
                <CardHeader className="border-b border-pink-100 dark:border-pink-900/30 bg-gradient-to-r from-pink-50/50 via-rose-50/50 to-purple-50/50 dark:from-pink-900/10 dark:via-rose-900/10 dark:to-purple-900/10">
                  <CardTitle className="flex items-center gap-2">
                    <div className="p-2 bg-gradient-to-br from-pink-500 to-rose-500 rounded-lg">
                      <TrendingUp className="h-5 w-5 text-white" />
                    </div>
                    <span className="bg-gradient-to-r from-pink-600 via-rose-600 to-purple-600 bg-clip-text text-transparent">
                      Top Search Terms
                    </span>
                  </CardTitle>
                  <CardDescription>
                    Your most frequent searches
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="space-y-3">
                    {topSearches.length === 0 ? (
                      <div className="text-center py-8">
                        <div className="inline-flex p-4 bg-gradient-to-br from-pink-100 to-rose-100 dark:from-pink-900/30 dark:to-rose-900/30 rounded-full mb-4">
                          <TrendingUp className="h-8 w-8 text-pink-500" />
                        </div>
                        <p className="text-muted-foreground">
                          No search data yet
                        </p>
                      </div>
                    ) : (
                      topSearches.map((item, index) => (
                        <div
                          key={item.query}
                          className="flex items-center justify-between p-4 rounded-xl bg-gradient-to-r from-pink-50/50 via-rose-50/50 to-purple-50/50 dark:from-pink-900/10 dark:via-rose-900/10 dark:to-purple-900/10 hover:shadow-md transition-all duration-300 border border-pink-100/50 dark:border-pink-800/30"
                        >
                          <div className="flex items-center gap-3">
                            <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-pink-500 to-rose-500 text-white font-bold text-lg shadow-lg">
                              {index + 1}
                            </div>
                            <span className="font-medium text-foreground">{item.query}</span>
                          </div>
                          <Badge className="bg-gradient-to-r from-pink-500 to-rose-500 text-white border-0">
                            {item.count}x
                          </Badge>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Top Retailers */}
              <Card className="glass-effect border-green-200/30 dark:border-green-500/20 hover:shadow-xl transition-all duration-300">
                <CardHeader className="border-b border-green-100 dark:border-green-900/30 bg-gradient-to-r from-green-50/50 via-emerald-50/50 to-teal-50/50 dark:from-green-900/10 dark:via-emerald-900/10 dark:to-teal-900/10">
                  <CardTitle className="flex items-center gap-2">
                    <div className="p-2 bg-gradient-to-br from-green-500 to-emerald-500 rounded-lg">
                      <ShoppingBag className="h-5 w-5 text-white" />
                    </div>
                    <span className="bg-gradient-to-r from-green-600 via-emerald-600 to-teal-600 bg-clip-text text-transparent">
                      Favorite Retailers
                    </span>
                  </CardTitle>
                  <CardDescription>
                    Retailers you interact with most
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="space-y-3">
                    {topRetailers.length === 0 ? (
                      <div className="text-center py-8">
                        <div className="inline-flex p-4 bg-gradient-to-br from-green-100 to-emerald-100 dark:from-green-900/30 dark:to-emerald-900/30 rounded-full mb-4">
                          <ShoppingBag className="h-8 w-8 text-green-500" />
                        </div>
                        <p className="text-muted-foreground">
                          No retailer data yet
                        </p>
                      </div>
                    ) : (
                      topRetailers.map((item, index) => (
                        <div
                          key={item.retailer}
                          className="flex items-center justify-between p-4 rounded-xl bg-gradient-to-r from-green-50/50 via-emerald-50/50 to-teal-50/50 dark:from-green-900/10 dark:via-emerald-900/10 dark:to-teal-900/10 hover:shadow-md transition-all duration-300 border border-green-100/50 dark:border-green-800/30"
                        >
                          <div className="flex items-center gap-3">
                            <div className="flex items-center justify-center w-10 h-10 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 text-white font-bold text-lg shadow-lg">
                              {index + 1}
                            </div>
                            <span className="font-medium capitalize text-foreground">{item.retailer}</span>
                          </div>
                          <Badge className="bg-gradient-to-r from-green-500 to-emerald-500 text-white border-0">
                            {item.count} clicks
                          </Badge>
                        </div>
                      ))
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default Analytics;
