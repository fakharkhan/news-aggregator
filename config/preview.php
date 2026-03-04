<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Preview Renderer Configuration
    |--------------------------------------------------------------------------
    |
    | This configuration controls the preview generation system for design
    | revisions. The renderer can be set to 'imagick' for high-quality
    | processing or 'gd' for basic image manipulation.
    |
    */

    'renderer' => env('PREVIEW_RENDERER', 'imagick'),

    /*
    |--------------------------------------------------------------------------
    | Default Preview Quality
    |--------------------------------------------------------------------------
    |
    | The default quality level for generated previews:
    | - draft: Low resolution for quick feedback
    | - standard: Standard quality for customer previews
    | - high: High quality for final review and marketing
    |
    */

    'default_quality' => env('PREVIEW_DEFAULT_QUALITY', 'standard'),

    /*
    |--------------------------------------------------------------------------
    | Image Processing Settings
    |--------------------------------------------------------------------------
    |
    | Configuration for image processing and normalization.
    |
    */

    'max_width' => env('PREVIEW_MAX_WIDTH', 2048),
    'max_height' => env('PREVIEW_MAX_HEIGHT', 2048),
    'thumbnail_size' => env('PREVIEW_THUMBNAIL_SIZE', 512),
    'dpi' => env('PREVIEW_DPI', 300),

    /*
    |--------------------------------------------------------------------------
    | Storage Settings
    |--------------------------------------------------------------------------
    |
    | Configuration for storing generated preview files.
    |
    */

    'storage_path' => env('PREVIEW_STORAGE_PATH', 'designs'),
    'temp_path' => env('PREVIEW_TEMP_PATH', 'temp/preview'),

    /*
    |--------------------------------------------------------------------------
    | Queue Settings
    |--------------------------------------------------------------------------
    |
    | Configuration for background processing of preview generation.
    |
    */

    'queue' => env('PREVIEW_QUEUE', 'default'),
    'timeout' => env('PREVIEW_TIMEOUT', 300), // 5 minutes
];
