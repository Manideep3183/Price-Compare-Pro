# 🔄 Google Sign-Up After Account Deletion - Testing Guide

## Overview
This guide explains how the system handles Google users who delete their account and then sign up again with the same Google account.

## 🎯 How It Works

### 1. **First Sign-Up with Google**
When a user first signs up with Google:
- Firebase creates user authentication
- Application calls `createOrUpdateUserProfile()` with `auth_provider: 'google'`
- Backend creates new user in MongoDB `users` collection with IST timestamp
- User can search products, view analytics, etc.

### 2. **Account Deletion**
When user deletes their account through the app:
- User clicks profile dropdown → "Delete Account"
- Confirmation dialog appears
- Backend DELETE `/api/v1/users/me` is called
- **CASCADE DELETE** happens automatically:
  - ✅ User profile deleted from `users` collection
  - ✅ All searches deleted from `searches` collection
  - ✅ All activity deleted from `activity` collection
- User is logged out from Firebase
- Redirected to login page

### 3. **Re-Sign-Up with Same Google Account**
When the same user signs up again with Google:
- Firebase re-authenticates the user (same UID)
- Login/SignUp page calls `createOrUpdateUserProfile()`
- Backend checks if user exists in MongoDB (by UID)
- **Since user was deleted, `existing_user` is null**
- Backend creates a **NEW user profile** with:
  - Same UID (from Firebase)
  - Same email
  - Fresh `created_at` timestamp (IST)
  - Auth provider: 'google'
- User starts with empty search history and activity
- ✅ **User can use the app normally again!**

## 🔒 Safety Mechanisms

### Multiple Profile Creation Checks:
1. **Login Page** - Calls `createOrUpdateUserProfile()` after Google login
2. **SignUp Page** - Calls `createOrUpdateUserProfile()` after Google signup
3. **Index Page** - Safety check on page load to ensure profile exists
4. **Analytics Page** - Safety check before fetching data

### Why Multiple Checks?
- Handles edge cases where user navigates directly to a page
- Ensures profile is recreated if user was deleted
- Idempotent operation (safe to call multiple times)

## 🧪 Testing Procedure

### **Test Case 1: Normal Google Sign-Up and Deletion**

1. **Sign Up with Google**
   ```
   ✅ Navigate to /signup
   ✅ Click "Continue with Google"
   ✅ Select your Google account
   ✅ Should redirect to home page (/)
   ✅ Check MongoDB: User should exist in `users` collection
   ```

2. **Use the Application**
   ```
   ✅ Search for "laptop"
   ✅ Navigate to Analytics
   ✅ Check MongoDB: Search should exist in `searches` collection
   ✅ Check MongoDB: Activities should exist in `activity` collection
   ```

3. **Delete Account**
   ```
   ✅ Click profile avatar (top right)
   ✅ Click "Delete Account"
   ✅ Confirm deletion
   ✅ Should show success toast
   ✅ Should log out and redirect to /login
   ✅ Check MongoDB: User should be GONE from `users` collection
   ✅ Check MongoDB: Searches should be GONE from `searches` collection
   ✅ Check MongoDB: Activities should be GONE from `activity` collection
   ```

### **Test Case 2: Re-Sign-Up After Deletion**

1. **Sign Up Again with Same Google Account**
   ```
   ✅ Navigate to /signup
   ✅ Click "Continue with Google"
   ✅ Select the SAME Google account you just deleted
   ✅ Should redirect to home page (/)
   ✅ Check MongoDB: User should be RE-CREATED in `users` collection
   ✅ Check created_at: Should have NEW timestamp (current time in IST)
   ```

2. **Verify Fresh Start**
   ```
   ✅ Navigate to Analytics
   ✅ Should show NO search history (empty)
   ✅ Should show NO activity logs (empty)
   ✅ User profile should exist with same email
   ```

3. **Use Application Normally**
   ```
   ✅ Search for "phone"
   ✅ Navigate to Analytics
   ✅ Check MongoDB: NEW search should exist in `searches` collection
   ✅ Search history should show only the new search
   ```

### **Test Case 3: Direct Navigation After Re-Login**

1. **Delete account and re-login with Google**
2. **Navigate directly to Analytics**
   ```
   ✅ Should not crash
   ✅ Profile should be auto-created if missing
   ✅ Analytics should show empty data (no searches/activities)
   ```

## 📊 MongoDB Verification Queries

### Check User Exists:
```javascript
db.users.find({email: "your-google-email@gmail.com"})
```

### Check User's Searches:
```javascript
db.searches.find({uid: "FIREBASE_USER_UID"})
```

### Check User's Activities:
```javascript
db.activity.find({uid: "FIREBASE_USER_UID"})
```

### Check Timestamps are IST:
```javascript
db.users.find({email: "your-google-email@gmail.com"}, {created_at: 1})
// Should show: created_at: ISODate("2025-10-21T14:30:00.000+05:30")
// Notice the +05:30 timezone offset
```

## 🔑 Key Points

### ✅ What Works:
- Google users can delete their account
- Same Google account can sign up again
- Profile is recreated with fresh data
- No data persists from previous account
- All timestamps use IST timezone
- Cascade delete works perfectly through UI

### ⚠️ Important Notes:
- **Same Google account** will have **same Firebase UID**
- After deletion and re-signup, it's treated as a **NEW user**
- **Search history is EMPTY** after re-signup
- **Activity logs are EMPTY** after re-signup
- `created_at` timestamp will be **NEW** (current time in IST)

### ❌ What Doesn't Work:
- Manual deletion from MongoDB doesn't trigger cascade delete
- You must use the application to delete accounts properly

## 🔄 Backend Logic (Reference)

```python
# In create_or_update_user endpoint:
existing_user = await db.users.find_one({"uid": user.uid})

if existing_user:
    # Update existing user
    await db.users.update_one({"uid": user.uid}, {"$set": user_doc})
else:
    # Create NEW user (this happens after deletion)
    user_doc["created_at"] = datetime.now(IST)
    await db.users.insert_one(user_doc)
```

## 🎯 Expected Behavior Summary

| Scenario | Expected Result |
|----------|----------------|
| First Google Sign-Up | ✅ New user created in MongoDB |
| Delete Account | ✅ User + Searches + Activity all deleted |
| Re-Sign-Up (Same Google) | ✅ New user created with same UID/email |
| Search History After Re-Signup | ✅ Empty (fresh start) |
| Activity After Re-Signup | ✅ Empty (fresh start) |
| Can Search Products | ✅ Works normally |
| Can View Analytics | ✅ Shows empty data initially |
| Multiple Re-Signups | ✅ Works every time |

## 🚀 Conclusion

The system is **fully functional** for Google users who:
- Delete their account
- Sign up again with the same Google account
- Start fresh with no historical data
- Use the application normally

**Everything works as expected!** ✅

---

**Last Updated**: October 21, 2025  
**Version**: 1.0.0
