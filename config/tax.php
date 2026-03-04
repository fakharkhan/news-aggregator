<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Tax Configuration
    |--------------------------------------------------------------------------
    |
    | Configuration for tax calculations including VAT rates,
    | company information, and tax-related settings.
    |
    */

    'default_vat_rate' => env('VAT_RATE', 0.00), // e.g. 0.20 = 20%
    'vat_number' => env('COMPANY_VAT_NUMBER', null),
    'legal_entity' => env('COMPANY_NAME', 'SOFT PYRAMID LLC'),
    'address' => env('COMPANY_ADDRESS', ''),
];
