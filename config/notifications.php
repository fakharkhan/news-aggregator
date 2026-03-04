<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Notification Settings
    |--------------------------------------------------------------------------
    |
    | Configure notification preferences, templates, and branding for the
    | sneaker platform.
    |
    */

    'branding' => [
        'sender_name' => env('MAIL_FROM_NAME', 'Sneaker Platform'),
        'logo_url' => env('APP_URL') . '/placeholder-sneaker.svg',
        'support_email' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    ],

    /*
    |--------------------------------------------------------------------------
    | Event Notifications
    |--------------------------------------------------------------------------
    |
    | Toggle switches for different notification types. Set to false to
    | disable specific notification types globally.
    |
    */

    'events' => [
        'order_placed' => true,
        'order_milestone' => true,
        'manufacturer_assigned' => true,
        'manufacturer_decision' => true,
        'issue_opened' => true,
        'artwork_scanned' => false, // Disabled for MVP
    ],

    /*
    |--------------------------------------------------------------------------
    | Email Templates
    |--------------------------------------------------------------------------
    |
    | Default templates and styling for email notifications.
    |
    */

    'templates' => [
        'layout' => 'emails.layouts.app',
        'styles' => [
            'primary_color' => '#3B82F6',
            'secondary_color' => '#6B7280',
            'background_color' => '#F9FAFB',
        ],
    ],

    /*
    |--------------------------------------------------------------------------
    | Recipient Rules
    |--------------------------------------------------------------------------
    |
    | Define who receives notifications for different events.
    |
    */

    'recipients' => [
        'order_placed' => ['customer'],
        'order_milestone' => ['customer'],
        'manufacturer_assigned' => ['manufacturer'],
        'manufacturer_decision' => ['admin'],
        'issue_opened' => ['admin'],
        'artwork_scanned' => ['creator'],
    ],
];
