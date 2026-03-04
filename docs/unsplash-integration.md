# Unsplash Integration for Sample Image Placeholders

## Overview

This document describes the integration of Unsplash public domain images as sample placeholders for the sneaker platform. The integration provides high-quality, free-to-use images when original images are unavailable or fail to load.

## Features

- **Automatic Fallback**: When original images fail to load, automatically fetch relevant Unsplash images
- **Caching**: Images are cached for 1 hour to minimize API calls and improve performance
- **Multiple Categories**: Support for sneaker-specific, lifestyle, and custom category images
- **Error Handling**: Graceful fallback to local SVG placeholders if Unsplash is unavailable
- **Responsive**: Images are automatically resized to requested dimensions

## Configuration

### Environment Variables

Add these to your `.env` file:

```env
# Unsplash API Configuration
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here
UNSPLASH_SECRET_KEY=your_unsplash_secret_key_here
```

### Getting Unsplash API Keys

1. Visit [Unsplash Developers](https://unsplash.com/developers)
2. Sign up/Login to your Unsplash account
3. Create a new application
4. Copy your Access Key and Secret Key

## API Endpoints

### Public Endpoints (No Authentication Required)

- `GET /api/unsplash/sneaker` - Get a random sneaker-related image
- `GET /api/unsplash/lifestyle` - Get a random lifestyle/fashion image
- `GET /api/unsplash/category/{category}` - Get a random image by category

### Query Parameters

- `width` (optional): Image width in pixels (default: 800)
- `height` (optional): Image height in pixels (default: 600)

### Admin Endpoints (Admin Only)

- `POST /api/v1/admin/unsplash/cache/clear` - Clear all cached Unsplash images

## Frontend Usage

### Vue Component

Use the `UnsplashImage` component for automatic fallback:

```vue
<template>
  <UnsplashImage
    :src="originalImageUrl"
    alt="Product image"
    fallback-type="sneaker"
    :width="400"
    :height="400"
  />
</template>

<script setup>
import UnsplashImage from '@/components/UnsplashImage.vue'
</script>
```

### Props

- `src` (optional): Original image URL
- `alt` (required): Alt text for accessibility
- `fallbackType` (optional): Type of fallback image ('sneaker', 'lifestyle', 'category')
- `category` (optional): Category for custom fallback images
- `width` (optional): Image width (default: 800)
- `height` (optional): Image height (default: 600)
- `imageClass` (optional): CSS classes for the image element
- `loading` (optional): Loading attribute ('lazy' or 'eager', default: 'lazy')

### Vue Composable

Use the `useUnsplashImages` composable for programmatic access:

```vue
<script setup>
import { useUnsplashImages } from '@/composables/useUnsplashImages'

const { getSneakerPlaceholder, loading, error } = useUnsplashImages()

const loadImage = async () => {
  const imageUrl = await getSneakerPlaceholder(400, 400)
  if (imageUrl) {
    // Use the image URL
  }
}
</script>
```

## Implementation Details

### Backend Services

- `UnsplashImageService`: Handles API calls to Unsplash with caching
- `UnsplashController`: Provides REST API endpoints

### Frontend Components

- `UnsplashImage.vue`: Vue component with automatic fallback
- `useUnsplashImages.ts`: Vue composable for programmatic access

### Caching Strategy

- Images are cached for 1 hour using Laravel's cache system
- Cache keys include dimensions for different sizes
- Admin can clear cache via API endpoint

## Error Handling

1. **Original Image Fails**: Try to load Unsplash image
2. **Unsplash Fails**: Use local SVG placeholder
3. **Network Issues**: Graceful degradation with loading states

## Rate Limits

- Unsplash free tier: 5,000 requests per hour
- Caching reduces actual API calls significantly
- Monitor usage in Unsplash developer dashboard

## Best Practices

1. **Always provide alt text** for accessibility
2. **Use appropriate fallback types** (sneaker for products, lifestyle for general)
3. **Cache images** to minimize API calls
4. **Handle loading states** for better UX
5. **Monitor API usage** to stay within limits

## Troubleshooting

### Common Issues

1. **404 Errors**: Check if Unsplash API key is configured correctly
2. **Rate Limit Exceeded**: Implement more aggressive caching
3. **Images Not Loading**: Check network connectivity and API status

### Debug Mode

Enable debug logging by checking Laravel logs for Unsplash-related warnings and errors.

## Future Enhancements

- [ ] Image optimization and compression
- [ ] Multiple image sources (Unsplash + other providers)
- [ ] Advanced caching strategies
- [ ] Image analytics and usage tracking
