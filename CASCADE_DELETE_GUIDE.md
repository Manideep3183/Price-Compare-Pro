# 🗑️ Cascade Delete Implementation Guide

## Overview
SmartCart implements **automatic cascade deletion** when a user account is deleted. This ensures data integrity by removing all user-related data from the database.

## 🔄 How Cascade Delete Works

### When You Delete a User Through the Application:

1. **User clicks "Delete Account"** in the profile dropdown
2. **Confirmation dialog** appears with warning
3. **Frontend calls** `DELETE /api/v1/users/me` endpoint
4. **Backend automatically deletes:**
   - ✅ User profile from `users` collection
   - ✅ All searches from `searches` collection (where uid matches)
   - ✅ All activity logs from `activity` collection (where uid matches)
5. **User is logged out** and redirected to login page

### Backend Implementation (activity.py)

```python
@router.delete("/users/me", response_model=Dict[str, Any])
async def delete_user_account(user: CurrentUser = Depends(get_current_user)):
    """
    Delete user account and all associated data (cascade delete).
    """
    db = get_database()
    
    # Delete user's searches
    searches_result = await db.searches.delete_many({"uid": user.uid})
    
    # Delete user's activity logs
    activity_result = await db.activity.delete_many({"uid": user.uid})
    
    # Delete user profile
    user_result = await db.users.delete_one({"uid": user.uid})
    
    return {
        "success": True,
        "deleted": {
            "user": user_result.deleted_count,
            "searches": searches_result.deleted_count,
            "activity": activity_result.deleted_count
        }
    }
```

## ⚠️ Important Notes

### Cascade Delete ONLY Works When:
- ✅ Deleting through the **application UI** (profile dropdown → Delete Account)
- ✅ Calling the **DELETE /api/v1/users/me** API endpoint

### Cascade Delete DOES NOT Work When:
- ❌ Manually deleting from **MongoDB Compass**
- ❌ Manually deleting from **MongoDB Atlas UI**
- ❌ Using MongoDB shell commands directly
- ❌ Deleting through any other database management tool

**Why?** Because manual deletion bypasses the application logic. The cascade delete logic only runs when you call the API endpoint.

## 🔐 User Verification Feature

### Additional Protection:
The application also checks if a user still exists in the database:

1. **On page load** (Index page)
2. **When accessing Analytics** dashboard

If a user is found to be deleted (manually from DB), the app will:
- Show a toast notification: "Account Deleted"
- Log the user out
- Redirect to login page

### Backend Implementation:
```python
@router.get("/users/check-exists", response_model=Dict[str, bool])
async def check_user_exists(user: CurrentUser = Depends(get_current_user)):
    """Check if user still exists in database"""
    db = get_database()
    user_doc = await db.users.find_one({"uid": user.uid})
    return {"exists": user_doc is not None}
```

## 📝 How to Properly Delete a User Account

### Method 1: Through UI (Recommended)
1. Log in to the application
2. Click on your profile avatar (top right)
3. Select **"Delete Account"**
4. Confirm deletion in the dialog
5. ✅ All data is automatically deleted (cascade)

### Method 2: Through API
```bash
# Using authenticated request
curl -X DELETE http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN"
```

### ❌ Method 3: Manual Deletion (NOT RECOMMENDED)
If you manually delete a user from MongoDB:
1. Delete from `users` collection
2. **MANUALLY** delete all documents from `searches` collection where `uid` matches
3. **MANUALLY** delete all documents from `activity` collection where `uid` matches

**This is error-prone and NOT recommended!**

## 🧪 Testing Cascade Delete

### Test Steps:
1. Create a test account and log in
2. Perform some searches (creates search history)
3. Navigate around (creates activity logs)
4. Go to Analytics to see your data
5. Delete account through profile dropdown
6. Check MongoDB - all related data should be gone

### Verify in MongoDB:
```javascript
// Check if user exists
db.users.find({email: "test@example.com"})

// Check if user's searches exist (should be empty after cascade delete)
db.searches.find({uid: "USER_UID"})

// Check if user's activities exist (should be empty after cascade delete)
db.activity.find({uid: "USER_UID"})
```

## 📊 Deletion Statistics

The delete endpoint returns statistics:
```json
{
  "success": true,
  "deleted": {
    "user": 1,
    "searches": 15,
    "activity": 47,
    "total": 63
  }
}
```

## 🔒 Security Considerations

1. **Authentication Required**: Can only delete your own account (authenticated endpoint)
2. **No Admin Override**: No way to delete other users' accounts
3. **Irreversible**: Once deleted, data cannot be recovered
4. **Confirmation Required**: UI requires explicit confirmation

## 🚀 Summary

- ✅ **Cascade delete is AUTOMATIC** when using the API endpoint
- ✅ **All related data is removed** (user + searches + activity)
- ✅ **Safe and secure** (authentication required)
- ✅ **User verification** protects against orphaned sessions
- ❌ **Manual deletion** does NOT trigger cascade delete
- ❌ **Always use the application** to delete accounts properly

---

**Last Updated**: October 21, 2025
**Version**: 1.0.0
