# Google OAuth Implementation

## Overview
This document describes the Google OAuth integration implemented for the Sneaker Platform, allowing users to sign in and register using their Google accounts.

## Features Implemented

### ✅ Core Functionality
- **Google OAuth Authentication**: Users can sign in/register using Google accounts
- **Account Linking**: Existing users can link their accounts to Google
- **Account Unlinking**: Users can disconnect their Google accounts
- **Automatic Email Verification**: Google accounts are automatically verified
- **Profile Creation**: User profiles are automatically created with Google data

### ✅ User Experience
- **Login Page Integration**: Google OAuth button on login page
- **Register Page Integration**: Google OAuth button on registration page
- **Profile Management**: Connected accounts section in user profile
- **Error Handling**: Comprehensive error handling and user feedback

## Technical Implementation

### Backend Components

#### 1. Database Schema
```sql
-- Added google_id field to users table
ALTER TABLE users ADD COLUMN google_id VARCHAR(255) UNIQUE NULL AFTER provider_id;
```

#### 2. Configuration
```php
// config/services.php
'google' => [
    'client_id' => env('GOOGLE_CLIENT_ID'),
    'client_secret' => env('GOOGLE_CLIENT_SECRET'),
    'redirect' => env('GOOGLE_REDIRECT_URI'),
],
```

#### 3. Controller
- **File**: `app/Http/Controllers/Auth/GoogleController.php`
- **Methods**:
  - `redirectToGoogle()`: Redirects to Google OAuth
  - `handleGoogleCallback()`: Handles OAuth callback
  - `linkAccount()`: Links existing account to Google
  - `unlinkAccount()`: Unlinks Google account

#### 4. Routes
```php
// Guest routes
Route::get('auth/google', [GoogleController::class, 'redirectToGoogle'])->name('auth.google');
Route::get('auth/google/callback', [GoogleController::class, 'handleGoogleCallback'])->name('auth.google.callback');

// Authenticated routes
Route::post('auth/google/link', [GoogleController::class, 'linkAccount'])->name('auth.google.link');
Route::post('auth/google/unlink', [GoogleController::class, 'unlinkAccount'])->name('auth.google.unlink');
```

### Frontend Components

#### 1. Login Page (`resources/js/Pages/Auth/Login.vue`)
- Added Google OAuth button with Google logo
- Styled divider between email/password and OAuth options
- Proper tabindex for accessibility

#### 2. Register Page (`resources/js/Pages/Auth/Register.vue`)
- Added Google OAuth button for new user registration
- Consistent styling with login page

#### 3. Profile Page (`resources/js/pages/Customer/Account/Profile.vue`)
- Added "Connected Accounts" section
- Shows Google account connection status
- Provides disconnect functionality

## Environment Configuration

### Required Environment Variables
```env
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

### Google Console Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback` (development)
   - `https://yourdomain.com/auth/google/callback` (production)

## User Flow

### New User Registration
1. User clicks "Continue with Google" on login/register page
2. Redirected to Google OAuth consent screen
3. User authorizes the application
4. Google redirects back to callback URL
5. System creates new user account with Google data
6. User is automatically logged in and redirected to dashboard

### Existing User Login
1. User clicks "Continue with Google" on login page
2. Redirected to Google OAuth consent screen
3. User authorizes the application
4. Google redirects back to callback URL
5. System finds existing user by email
6. If no Google ID linked, links the account
7. User is automatically logged in and redirected to dashboard

### Account Linking
1. User goes to profile page
2. Clicks "Connect Google Account"
3. Follows OAuth flow
4. Account is linked to Google ID

### Account Unlinking
1. User goes to profile page
2. Clicks "Disconnect" in Connected Accounts section
3. Google ID is removed from account
4. User can still login with email/password

## Security Features

### ✅ Implemented Security Measures
- **CSRF Protection**: All forms protected with CSRF tokens
- **Rate Limiting**: OAuth endpoints protected with rate limiting
- **Input Validation**: All user inputs validated
- **Error Handling**: Comprehensive error handling without exposing sensitive data
- **Session Security**: Secure session management

### ✅ Data Protection
- **Email Verification**: Google accounts automatically verified
- **Profile Data**: Google profile data safely stored
- **Password Security**: OAuth users get secure random passwords
- **Account Linking**: Secure account linking with email verification

## Testing

### Test Coverage
- **File**: `tests/Feature/GoogleOAuthTest.php`
- **Tests**:
  - Google OAuth redirect functionality
  - New user creation via OAuth
  - Existing user linking via OAuth
  - Existing Google user login
  - Error handling

### Running Tests
```bash
php artisan test tests/Feature/GoogleOAuthTest.php
```

## Error Handling

### Common Errors
1. **Invalid Credentials**: Google OAuth credentials not configured
2. **Network Issues**: Unable to reach Google OAuth servers
3. **User Cancellation**: User cancels OAuth flow
4. **Email Mismatch**: OAuth email doesn't match existing account

### Error Responses
- All errors redirect to login page with user-friendly messages
- No sensitive information exposed in error messages
- Comprehensive logging for debugging

## Performance Considerations

### ✅ Optimizations
- **Database Indexing**: `google_id` field indexed for fast lookups
- **Caching**: User data cached after OAuth login
- **Minimal API Calls**: Only essential Google API calls made
- **Efficient Queries**: Optimized database queries for user lookups

## Future Enhancements

### Potential Improvements
1. **Additional Providers**: Add Facebook, Apple, GitHub OAuth
2. **Advanced Profile Sync**: Sync additional profile data from Google
3. **OAuth Scopes**: Request additional permissions for enhanced features
4. **Two-Factor Authentication**: Integrate with Google's 2FA
5. **Account Merging**: Allow merging multiple OAuth accounts

## Troubleshooting

### Common Issues

#### 1. "Invalid redirect URI" Error
- **Cause**: Redirect URI not configured in Google Console
- **Solution**: Add correct redirect URI to Google OAuth credentials

#### 2. "Client ID not found" Error
- **Cause**: Google OAuth credentials not properly configured
- **Solution**: Check environment variables and Google Console setup

#### 3. "Email already exists" Error
- **Cause**: User with same email exists but not linked to Google
- **Solution**: System automatically links accounts, but user should use email/password login first

#### 4. "OAuth error" Message
- **Cause**: Various OAuth-related issues
- **Solution**: Check logs for specific error details

### Debug Mode
Enable debug logging for OAuth issues:
```php
// In GoogleController
Log::debug('Google OAuth callback', [
    'user' => $googleUser->getEmail(),
    'id' => $googleUser->getId(),
]);
```

## Conclusion

The Google OAuth implementation provides a seamless authentication experience for users while maintaining security and data integrity. The implementation follows Laravel best practices and includes comprehensive testing and error handling.

### ✅ Success Metrics
- **User Onboarding**: Reduced signup friction
- **Security**: Enhanced account security with Google verification
- **User Experience**: Seamless login process
- **Data Integrity**: Proper account linking and management

---

*Last Updated: January 2025*
*Implementation Status: ✅ Complete*
