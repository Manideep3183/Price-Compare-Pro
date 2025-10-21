import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getUserProfile, checkUserExists, createOrUpdateUserProfile, deleteUserAccount } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import { ThemeToggle } from '@/components/ThemeToggle';
import { UserProfileDropdown } from '@/components/UserProfileDropdown';
import {
  User,
  Mail,
  Calendar,
  Shield,
  ArrowLeft,
  Trash2,
  CheckCircle2,
} from 'lucide-react';

interface UserProfile {
  uid: string;
  email: string;
  name?: string;
  picture?: string;
  email_verified: boolean;
  stats: {
    total_searches: number;
    recent_searches: string[];
  };
}

const Account = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const { toast } = useToast();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    const fetchData = async () => {
      try {
        // Check if user still exists in database
        const exists = await checkUserExists();
        if (!exists) {
          console.log('⚠️ User no longer exists in database, logging out...');
          toast({
            title: "Account Deleted",
            description: "Your account has been deleted. Please sign up again.",
            variant: "destructive",
          });
          await logout();
          navigate('/login');
          return;
        }

        // Ensure user profile exists (safety check for re-signup after deletion)
        try {
          await createOrUpdateUserProfile({
            auth_provider: user.providerData?.[0]?.providerId === 'google.com' ? 'google' : 'email',
          });
          console.log('✅ User profile ensured in MongoDB');
        } catch (profileError) {
          console.error('⚠️ Failed to ensure user profile:', profileError);
          // Non-critical, continue
        }

        const profileData = await getUserProfile();
        setProfile(profileData);
      } catch (error) {
        console.error('Failed to fetch profile data:', error);
        toast({
          title: "Error",
          description: "Failed to load your profile. Please try again.",
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user, navigate, logout, toast]);

  const handleDeleteAccount = async () => {
    setIsDeleting(true);
    try {
      console.log('🗑️ Deleting user account...');
      await deleteUserAccount();
      
      toast({
        title: "Account Deleted",
        description: "Your account and all associated data have been permanently deleted.",
      });
      
      // Logout and redirect to login
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Delete account error:', error);
      toast({
        title: "Deletion Failed",
        description: "Failed to delete your account. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsDeleting(false);
      setShowDeleteDialog(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-purple-900/20 dark:to-blue-900/20">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mb-4"></div>
          <p className="text-muted-foreground">Loading your profile...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-purple-900/20 dark:to-blue-900/20">
      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/')}
              className="gap-2 hover:bg-purple-100 dark:hover:bg-purple-900/20"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Home
            </Button>
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500 via-pink-500 to-blue-500 rounded-lg flex items-center justify-center">
                <User className="h-4 w-4 text-white" />
              </div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                Account Settings
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />
            <UserProfileDropdown />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="space-y-6">
          {/* Profile Information Card */}
          <Card className="glass-effect border-purple-200/30 dark:border-purple-500/20 hover:shadow-xl transition-all duration-300">
            <CardHeader className="border-b border-purple-100 dark:border-purple-900/30 bg-gradient-to-r from-purple-50/50 via-pink-50/50 to-blue-50/50 dark:from-purple-900/10 dark:via-pink-900/10 dark:to-blue-900/10">
              <CardTitle className="flex items-center gap-2">
                <div className="p-2 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg">
                  <User className="h-5 w-5 text-white" />
                </div>
                <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                  Profile Information
                </span>
              </CardTitle>
              <CardDescription>
                Your account details and verification status
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-6 space-y-6">
              {/* Profile Header */}
              <div className="flex items-center gap-4">
                {profile?.picture ? (
                  <img
                    src={profile.picture}
                    alt={profile.name || 'User'}
                    className="w-20 h-20 rounded-full border-4 border-purple-200 dark:border-purple-800 shadow-lg"
                  />
                ) : (
                  <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                    {profile?.name?.[0]?.toUpperCase() || profile?.email?.[0]?.toUpperCase() || 'U'}
                  </div>
                )}
                <div>
                  <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                    {profile?.name || 'User'}
                  </h3>
                  <p className="text-muted-foreground flex items-center gap-2">
                    <Mail className="h-4 w-4" />
                    {profile?.email}
                  </p>
                  {profile?.email_verified && (
                    <Badge className="mt-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white border-0">
                      <CheckCircle2 className="h-3 w-3 mr-1" />
                      Verified
                    </Badge>
                  )}
                </div>
              </div>

              {/* Account Stats */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-gradient-to-r from-purple-100/50 via-pink-100/50 to-blue-100/50 dark:from-purple-900/20 dark:via-pink-900/20 dark:to-blue-900/20 border border-purple-200/30 dark:border-purple-800/30">
                  <p className="text-sm text-muted-foreground mb-1 flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Total Searches
                  </p>
                  <p className="text-3xl font-bold bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                    {profile?.stats.total_searches || 0}
                  </p>
                </div>
                <div className="p-4 rounded-xl bg-gradient-to-r from-blue-100/50 via-cyan-100/50 to-purple-100/50 dark:from-blue-900/20 dark:via-cyan-900/20 dark:to-purple-900/20 border border-blue-200/30 dark:border-blue-800/30">
                  <p className="text-sm text-muted-foreground mb-1 flex items-center gap-2">
                    <Shield className="h-4 w-4" />
                    Account Status
                  </p>
                  <p className="text-lg font-semibold text-green-600 dark:text-green-400">
                    Active
                  </p>
                </div>
              </div>

              {/* Recent Searches */}
              <div>
                <h4 className="font-semibold mb-3 flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Recent Search Terms
                </h4>
                <div className="flex flex-wrap gap-2">
                  {profile?.stats.recent_searches.length === 0 ? (
                    <p className="text-muted-foreground text-sm">No recent searches</p>
                  ) : (
                    profile?.stats.recent_searches.map((term, index) => (
                      <Badge 
                        key={index} 
                        variant="outline" 
                        className="px-3 py-1 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/30 dark:to-pink-900/30 border-purple-200 dark:border-purple-800"
                      >
                        {term}
                      </Badge>
                    ))
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Danger Zone Card */}
          <Card className="glass-effect border-red-200/30 dark:border-red-500/20">
            <CardHeader className="border-b border-red-100 dark:border-red-900/30 bg-gradient-to-r from-red-50/50 via-orange-50/50 to-pink-50/50 dark:from-red-900/10 dark:via-orange-900/10 dark:to-pink-900/10">
              <CardTitle className="flex items-center gap-2 text-red-600 dark:text-red-400">
                <div className="p-2 bg-gradient-to-br from-red-500 to-orange-500 rounded-lg">
                  <Trash2 className="h-5 w-5 text-white" />
                </div>
                Danger Zone
              </CardTitle>
              <CardDescription>
                Irreversible and destructive actions
              </CardDescription>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="p-4 rounded-xl border-2 border-red-200 dark:border-red-800 bg-red-50/50 dark:bg-red-900/10">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h4 className="font-semibold text-red-900 dark:text-red-300 mb-2">
                      Delete Account
                    </h4>
                    <p className="text-sm text-red-700 dark:text-red-400 mb-4">
                      Once you delete your account, there is no going back. This will permanently delete:
                    </p>
                    <ul className="text-sm text-red-700 dark:text-red-400 space-y-1 mb-4">
                      <li className="flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                        Your profile information
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                        All search history ({profile?.stats.total_searches || 0} searches)
                      </li>
                      <li className="flex items-center gap-2">
                        <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                        All activity logs
                      </li>
                    </ul>
                  </div>
                  <Button
                    variant="destructive"
                    onClick={() => setShowDeleteDialog(true)}
                    className="bg-red-600 hover:bg-red-700 text-white shrink-0"
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete Account
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent className="glass-effect border-red-500/20">
          <AlertDialogHeader>
            <AlertDialogTitle className="text-red-600 dark:text-red-400 flex items-center gap-2">
              <Trash2 className="h-5 w-5" />
              Delete Account Permanently?
            </AlertDialogTitle>
            <AlertDialogDescription className="space-y-3">
              <p className="font-semibold text-foreground">
                This action cannot be undone. This will permanently delete your account and remove all your data including:
              </p>
              <ul className="list-disc list-inside space-y-1 text-muted-foreground">
                <li>Your profile information for <strong>{profile?.email}</strong></li>
                <li>All search history ({profile?.stats.total_searches || 0} searches)</li>
                <li>All activity logs</li>
              </ul>
              <p className="text-red-600 dark:text-red-400 font-semibold">
                You will be logged out immediately and cannot recover this data.
              </p>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel disabled={isDeleting}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleDeleteAccount}
              disabled={isDeleting}
              className="bg-red-600 hover:bg-red-700 text-white"
            >
              {isDeleting ? (
                <>
                  <div className="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                  Deleting...
                </>
              ) : (
                <>
                  <Trash2 className="h-4 w-4 mr-2" />
                  Yes, Delete My Account
                </>
              )}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default Account;
