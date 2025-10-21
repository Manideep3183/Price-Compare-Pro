# Google Re-Signup Flow After Account Deletion

## Problem Statement
When a user signs up with Google and then deletes their account, trying to sign in again with Google would show an error "account is deleted" even though Firebase still has the authentication record. The issue is that the user profile was deleted from MongoDB but Firebase authentication remained.

## Solution Overview
Implemented a two-step re-signup process for Google authentication after account deletion:
1. **First click**: Show error message asking user to click again
2. **Second click**: Automatically re-create the account

## Implementation Details

### 1. Login Page (`frontend/src/pages/Login.tsx`)

#### Email/Password Login
```typescript
const handleEmailLogin = async (e: React.FormEvent) => {
  // After successful Firebase authentication
  await login(email, password);
  
  // Check if user exists in MongoDB
  const userExists = await checkUserExists();
  
  if (!userExists) {
    // User deleted - show error and sign out
    setError('Your account was deleted. Please sign up again to continue.');
    await auth.signOut();
    return;
  }
  
  navigate('/');
};
```

**Flow:**
- User logs in with email/password
- System checks if user exists in MongoDB
- If deleted → Show error, sign out
- If exists → Navigate to home

#### Google Login
```typescript
const handleGoogleLogin = async () => {
  // After successful Google authentication
  await loginWithGoogle();
  
  // Check if user exists in MongoDB
  const userExists = await checkUserExists();
  
  if (!userExists) {
    // Check if this is a re-signup attempt
    const isResignupAttempt = localStorage.getItem('google_resignup_attempt');
    
    if (!isResignupAttempt) {
      // FIRST ATTEMPT: Set flag and show error
      localStorage.setItem('google_resignup_attempt', 'true');
      setError('Your account was deleted. Please click "Continue with Google" again to re-create your account.');
      await auth.signOut();
      return;
    } else {
      // SECOND ATTEMPT: Create the account
      localStorage.removeItem('google_resignup_attempt');
      console.log('🔄 Re-creating Google account after deletion...');
    }
  }
  
  // Create/update user profile in MongoDB
  await createOrUpdateUserProfile({ auth_provider: 'google' });
  navigate('/');
};
```

**Flow:**
1. **User clicks "Continue with Google"**
   - Firebase authenticates successfully
   - Check MongoDB: User doesn't exist (was deleted)
   - First attempt: Show error + set localStorage flag
   - Sign out user
   
2. **User clicks "Continue with Google" again**
   - Firebase authenticates successfully
   - Check MongoDB: User still doesn't exist
   - Second attempt detected (localStorage flag exists)
   - Clear the flag
   - Create user profile in MongoDB
   - Navigate to home

### 2. Sign Up Page (`frontend/src/pages/SignUp.tsx`)

Same logic implemented for the Sign Up page's Google authentication option.

### 3. Backend API (`app/api/activity.py`)

#### Check User Exists Endpoint
```python
@router.get("/users/check-exists", response_model=Dict[str, bool])
async def check_user_exists(user: CurrentUser = Depends(get_current_user)):
    """
    Check if user exists in MongoDB database.
    Returns {"exists": true/false}
    Used to verify user hasn't been deleted.
    """
    db = get_database()
    user_doc = await db.users.find_one({"uid": user.uid})
    return {"exists": user_doc is not None}
```

#### Create/Update User Profile Endpoint
```python
@router.post("/users/create-or-update", response_model=Dict[str, bool])
async def create_or_update_user(
    user_data: UserProfileRequest,
    user: CurrentUser = Depends(get_current_user)
):
    """
    Create or update user profile in MongoDB.
    Called after sign up or login.
    """
    # Check if user exists
    existing_user = await db.users.find_one({"uid": user.uid})
    
    if existing_user:
        # Update existing user
        await db.users.update_one({"uid": user.uid}, {"$set": user_doc})
    else:
        # Create new user
        await db.users.insert_one(user_doc)
    
    return {"success": True}
```

## User Experience Flow

### Scenario 1: Email/Password User (Deleted Account)
1. User tries to login with email/password
2. Firebase authenticates successfully
3. System checks MongoDB → User doesn't exist
4. Shows error: "Your account was deleted. Please sign up again to continue."
5. User is signed out
6. User must go to Sign Up page and create a new account

### Scenario 2: Google User (Deleted Account)
1. **First Attempt:**
   - User clicks "Continue with Google"
   - Google authenticates successfully
   - System checks MongoDB → User doesn't exist
   - Shows error: "Your account was deleted. Please click 'Continue with Google' again to re-create your account."
   - User is signed out
   - Flag set in localStorage

2. **Second Attempt:**
   - User clicks "Continue with Google" again
   - Google authenticates successfully
   - System detects re-signup attempt (localStorage flag)
   - Automatically creates user profile in MongoDB
   - Clears localStorage flag
   - User is logged in and navigated to home

### Scenario 3: Existing User (Not Deleted)
1. User logs in (email or Google)
2. Firebase authenticates
3. System checks MongoDB → User exists
4. Creates/updates user profile (updates timestamp)
5. User navigated to home

## Technical Details

### localStorage Flag
- **Key:** `google_resignup_attempt`
- **Value:** `'true'`
- **Purpose:** Track if this is the second attempt to sign in with Google after deletion
- **Lifecycle:** 
  - Set on first attempt after detecting deleted account
  - Cleared on second attempt after re-creating account

### API Endpoints Used
1. **GET `/api/v1/users/check-exists`**
   - Checks if user exists in MongoDB
   - Returns `{exists: boolean}`

2. **POST `/api/v1/users/create-or-update`**
   - Creates or updates user profile
   - Payload: `{auth_provider: 'google' | 'email', display_name?, phone_number?}`
   - Returns `{success: boolean}`

## Benefits

### For Users
- Clear feedback when account is deleted
- Simple re-signup process for Google users (just click twice)
- Consistent behavior across email and Google authentication

### For System
- Prevents ghost accounts (Firebase auth without MongoDB profile)
- Maintains data integrity
- Proper separation between Firebase authentication and MongoDB user data

## Error Handling

1. **Network Errors:** If API calls fail, user is signed out and error is shown
2. **MongoDB Down:** Error message displayed, navigation prevented
3. **Race Conditions:** localStorage flag ensures proper state tracking

## Security Considerations

1. User must authenticate with Firebase before any checks
2. MongoDB queries use authenticated user's UID from Firebase token
3. No user data is exposed in error messages
4. Sign-out happens on any error to prevent unauthorized access

## Testing Checklist

- [ ] Email/Password: Login after account deletion
- [ ] Google: First click after account deletion (shows error)
- [ ] Google: Second click after account deletion (creates account)
- [ ] Google: Login with existing account (normal flow)
- [ ] Email: Sign up after account deletion
- [ ] Error handling: Network failures
- [ ] Error handling: MongoDB unavailable
- [ ] localStorage flag is cleared properly

## Future Enhancements

1. Add expiration to localStorage flag (e.g., 24 hours)
2. Send email notification when account is re-created
3. Add analytics tracking for re-signup events
4. Allow users to recover deleted accounts within grace period
