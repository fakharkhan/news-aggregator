<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Pricing Configuration
    |--------------------------------------------------------------------------
    |
    | Configuration for pricing calculations including platform fees,
    | taxes, shipping zones, and default currency settings.
    |
    */

    'platform_fee_percentage' => env('PLATFORM_FEE_PCT', 0.12),
    'default_tax_percentage' => env('DEFAULT_TAX_PCT', 0.00),
    'default_currency' => env('DEFAULT_CURRENCY', 'USD'),

    'shipping_zones' => [
        'US' => env('SHIPPING_US_CENTS', 1500),    // $15.00
        'EU' => env('SHIPPING_EU_CENTS', 1800),    // $18.00
        'APAC' => env('SHIPPING_APAC_CENTS', 2000), // $20.00
        'OTHER' => env('SHIPPING_OTHER_CENTS', 2500), // $25.00
    ],

    // ISO 3166-1 alpha-2 → zone mapping
    'country_zone_map' => [
        'US' => 'US', 'CA' => 'US',
        'GB' => 'EU', 'DE' => 'EU', 'FR' => 'EU', 'ES' => 'EU', 'IT' => 'EU', 'NL' => 'EU',
        'CN' => 'APAC', 'JP' => 'APAC', 'KR' => 'APAC', 'SG' => 'APAC', 'AU' => 'APAC', 'NZ' => 'APAC',
    ],

    'default_zone' => env('DEFAULT_SHIPPING_ZONE', 'OTHER'),

    // Fallback base costs per silhouette type (in cents)
    'fallback_base_costs' => [
        'sneaker' => 2500, // $25.00
        'boot' => 3000,    // $30.00
        'sandal' => 2000,  // $20.00
        'default' => 2500, // $25.00
    ],
];
