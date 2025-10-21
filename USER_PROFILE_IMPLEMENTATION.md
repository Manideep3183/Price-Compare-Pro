# User Profile Storage Implementation

## Overview
Successfully implemented user profile storage in MongoDB with differentiated data for Google OAuth vs Email signup users.

## Database Structure

### Users Collection
The `users` collection stores user profile information with the following schema:

```json
{
  "_id": "ObjectId",
  "uid": "string (Firebase UID)",
  "email": "string",
  "email_verified": "boolean",
  "display_name": "string (optional)",
  "phone_number": "string (optional)",
  "picture": "string (optional, Google OAuth)",
  "auth_provider": "string ('email' or 'google')",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## Backend Changes

### New Endpoints in `app/api/activity.py`

#### 1. POST `/api/v1/users/create-or-update`
**Purpose**: Create or update user profile in MongoDB  
**Authentication**: Required (Firebase JWT token)  
**Request Body**:
```json
{
  "display_name": "string (optional)",
  "phone_number": "string (optional)",
  "auth_provider": "email" | "google"
}
```
**Response**:
```json
{
  "success": true
}
```

**Features**:
- Automatic upsert logic (creates new or updates existing user)
- Adds Firebase user data (uid, email, email_verified, picture)
- Sets timestamps (created_at for new users, updated_at for all)
- Logs all operations with emojis for easy debugging

#### 2. GET `/api/v1/users/me`
**Purpose**: Get current user's profile from MongoDB  
**Authentication**: Required (Firebase JWT token)  
**Response**:
```json
{
  "uid": "string",
  "email": "string",
  "display_name": "string",
  "email_verified": "boolean",
  "picture": "string",
  "auth_provider": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Features**:
- Returns MongoDB user document
- Falls back to Firebase data if user not in MongoDB yet
- Converts MongoDB ObjectId to string for JSON serialization

### New Pydantic Model
```python
class UserProfileRequest(BaseModel):
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    auth_provider: str = "email"
```

## Frontend Changes

### API Client (`frontend/src/lib/api.ts`)

Added two new functions:

```typescript
// Create or update user profile in MongoDB
export const createOrUpdateUserProfile = async (data: {
  display_name?: string;
  phone_number?: string;
  auth_provider: 'email' | 'google';
}) => {
  const response = await apiClient.post('/api/v1/users/create-or-update', data);
  return response.data;
};

// Get current user's profile from MongoDB
export const getUserProfileFromDB = async () => {
  const response = await apiClient.get('/api/v1/users/me');
  return response.data;
};
```

### SignUp Page (`frontend/src/pages/SignUp.tsx`)

#### Email Signup Flow
After successful Firebase signup:
1. Calls `createOrUpdateUserProfile` with:
   - `display_name`: User's entered name
   - `auth_provider`: "email"
2. Logs success/failure (doesn't block navigation)
3. Redirects to home page

#### Google Signup Flow
After successful Google authentication:
1. Calls `createOrUpdateUserProfile` with:
   - `auth_provider`: "google"
   - Firebase automatically provides name and picture
2. Logs success/failure (doesn't block navigation)
3. Redirects to home page

### Login Page (`frontend/src/pages/Login.tsx`)

#### Google Login Flow
After successful Google authentication:
1. Calls `createOrUpdateUserProfile` with:
   - `auth_provider`: "google"
2. Updates existing user or creates new profile
3. Logs success/failure (doesn't block navigation)
4. Redirects to home page

## Data Flow

### Email Signup User
```
User submits form → Firebase creates account → Frontend calls API
                                              ↓
                                    Backend saves to MongoDB:
                                    - uid (from Firebase)
                                    - email (from Firebase)
                                    - display_name (from form)
                                    - email_verified (from Firebase)
                                    - auth_provider: "email"
                                    - created_at: now()
```

### Google OAuth User
```
User clicks Google button → Firebase authenticates → Frontend calls API
                                                     ↓
                                           Backend saves to MongoDB:
                                           - uid (from Firebase)
                                           - email (from Firebase)
                                           - display_name (from Google)
                                           - picture (from Google)
                                           - email_verified (from Firebase)
                                           - auth_provider: "google"
                                           - created_at: now()
```

## Testing

### Manual Testing Steps

1. **Start Backend** (already running):
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend** (if not running):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test Email Signup**:
   - Navigate to http://localhost:8081/signup
   - Fill in name, email, and password
   - Click "Create Account"
   - Check MongoDB users collection for new document
   - Verify `auth_provider` is "email"
   - Verify `display_name` matches entered name

4. **Test Google Signup**:
   - Navigate to http://localhost:8081/signup
   - Click "Continue with Google"
   - Complete Google authentication
   - Check MongoDB users collection for new document
   - Verify `auth_provider` is "google"
   - Verify `picture` URL is present

5. **Test Google Login** (existing user):
   - Navigate to http://localhost:8081/login
   - Click "Continue with Google"
   - Check MongoDB - should update `updated_at` timestamp

### API Testing

Use `test_user_profile.py` for direct API testing:

```bash
python test_user_profile.py
```

**Note**: Update `TEST_TOKEN` variable with actual Firebase ID token from browser console.

## MongoDB Verification

### Check Users Collection
```javascript
// In MongoDB Atlas or Compass
use SmartCart

// Count documents
db.users.countDocuments()

// View all users
db.users.find().pretty()

// View email signup users
db.users.find({ auth_provider: "email" }).pretty()

// View Google OAuth users
db.users.find({ auth_provider: "google" }).pretty()
```

### Expected Document Examples

**Email Signup User**:
```json
{
  "_id": ObjectId("..."),
  "uid": "abc123...",
  "email": "user@example.com",
  "email_verified": false,
  "display_name": "John Doe",
  "auth_provider": "email",
  "created_at": ISODate("2025-01-15T10:30:00Z"),
  "updated_at": ISODate("2025-01-15T10:30:00Z")
}
```

**Google OAuth User**:
```json
{
  "_id": ObjectId("..."),
  "uid": "xyz789...",
  "email": "user@gmail.com",
  "email_verified": true,
  "display_name": "Jane Smith",
  "picture": "https://lh3.googleusercontent.com/...",
  "auth_provider": "google",
  "created_at": ISODate("2025-01-15T11:00:00Z"),
  "updated_at": ISODate("2025-01-15T11:00:00Z")
}
```

## Error Handling

All operations include comprehensive error handling:

1. **Backend**:
   - Database unavailable → 503 Service Unavailable
   - Authentication failure → 401 Unauthorized
   - Database operation failure → 500 Internal Server Error
   - All errors logged with ❌ emoji

2. **Frontend**:
   - Profile save failure doesn't block user navigation
   - Errors logged to console for debugging
   - User experience not disrupted if MongoDB is temporarily unavailable

## Console Logging

The implementation includes helpful console logs:

**Backend**:
- 📝 Creating/updating user profile for: {email}
- ✏️ Updating existing user: {email}
- ➕ Creating new user: {email}
- ✅ User profile saved successfully: {email}
- ❌ Failed to save user profile: {error}

**Frontend**:
- ✅ User profile saved to MongoDB
- ✅ Google user profile saved to MongoDB
- ⚠️ Failed to save profile, but signup succeeded

## Future Enhancements

Potential improvements:
1. Add phone_number field to signup form
2. Create user profile edit page
3. Add avatar upload for email users
4. Add more profile fields (bio, preferences, etc.)
5. Create admin dashboard to view all users
6. Add user deletion endpoint (GDPR compliance)
7. Add email verification reminder for unverified users

## Security Considerations

✅ **Implemented**:
- All endpoints require Firebase authentication
- MongoDB stores sanitized data only
- No sensitive data (passwords) stored in MongoDB
- User can only access their own profile

⚠️ **Future Considerations**:
- Add rate limiting to prevent abuse
- Implement data encryption at rest
- Add audit logging for profile changes
- Implement GDPR data export/deletion

## Troubleshooting

### Issue: Users not appearing in MongoDB
**Solution**: Check browser console for errors. Verify:
- Backend is running on port 8000
- MongoDB connection is active
- Firebase authentication is working
- Auth token is being sent in requests

### Issue: "Database not available" error
**Solution**: 
- Verify MongoDB connection string in backend
- Check network connectivity
- Ensure MongoDB Atlas whitelist includes your IP

### Issue: Auth token errors
**Solution**:
- Clear browser cache and cookies
- Sign out and sign back in
- Check Firebase configuration in frontend

## Status
✅ **COMPLETE** - User profile storage is now fully implemented and ready for testing!

## Next Steps
1. Test email signup → Check MongoDB for new user
2. Test Google signup → Check MongoDB for new user
3. Test Google login (existing user) → Verify updated_at changes
4. Verify Analytics dashboard can now show real user data
