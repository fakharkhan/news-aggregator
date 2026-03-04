# Google OAuth Setup Guide

## Issue Resolution

The error `TypeError: undefined is not an object (evaluating 'o.window.location')` occurs because the Google OAuth environment variables are not configured. This causes the `route('auth.google')` function to return `undefined`.

## Required Environment Variables

Add the following variables to your `.env` file:

```env
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

## Google Cloud Console Setup

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API (or Google Identity API)

### 2. Create OAuth 2.0 Credentials
1. Navigate to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Choose "Web application" as the application type
4. Add authorized redirect URIs:
   - `http://localhost:8000/auth/google/callback` (for development)
   - `https://yourdomain.com/auth/google/callback` (for production)

### 3. Get Your Credentials
1. After creating the OAuth client, you'll get:
   - **Client ID**: Copy this to `GOOGLE_CLIENT_ID`
   - **Client Secret**: Copy this to `GOOGLE_CLIENT_SECRET`

## Configuration Steps

### 1. Update .env File
```env
# Add these lines to your .env file
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnop.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

### 2. Clear Configuration Cache
```bash
php artisan config:cache
```

### 3. Regenerate Ziggy Routes
```bash
php artisan ziggy:generate
```

### 4. Rebuild Frontend Assets
```bash
npm run build
```

## Testing the Fix

After setting up the environment variables:

1. Clear your browser cache
2. Refresh the login page
3. Click "Continue with Google"
4. You should be redirected to Google's OAuth consent screen

## Troubleshooting

### If you still get the error:
1. Check that all environment variables are set correctly
2. Verify the redirect URI matches exactly in Google Console
3. Ensure the Google+ API is enabled
4. Check browser console for any additional errors

### Common Issues:
- **"Invalid redirect URI"**: Make sure the redirect URI in Google Console matches exactly
- **"Client ID not found"**: Verify the client ID is correct and the API is enabled
- **"OAuth error"**: Check that the client secret is correct

## Security Notes

- Never commit your `.env` file to version control
- Use different OAuth credentials for development and production
- Regularly rotate your client secrets
- Monitor OAuth usage in Google Cloud Console

## Production Setup

For production, update the redirect URI:
```env
GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/google/callback
```

Make sure to add the production domain to your Google OAuth credentials' authorized domains.
